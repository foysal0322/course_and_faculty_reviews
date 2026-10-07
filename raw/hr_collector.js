// HR Collector JS script
const NAME = arguments[0], MAX = arguments[1] || 200;
delete window.__fb;
const S = window.__fb = {
  posts: [],
  running: true,
  done: false,
  log: [],
  stop: false,
  name: NAME,
  saves: 0
};

const sleep = ms => new Promise(r => setTimeout(r, ms));
const rnd = (a, b) => a + Math.random() * (b - a);

const seenText = new Set();
const blocked = () => /Temporarily Blocked|You're going too fast|slow down|misusing this feature/i.test(document.body.innerText.slice(0, 20000));
const hasEndText = () => /End of results/i.test(document.body.innerText);

function postInfo(k) {
  const msgEls = [...k.querySelectorAll('[data-ad-rendering-role=story_message],[data-ad-comet-preview=message]')];
  let text = msgEls.map(e => e.innerText.trim()).filter(Boolean)[0] || '';
  if (!text) text = [...k.querySelectorAll('div[dir=auto]')].map(e => e.innerText.trim()).filter(Boolean).slice(0, 5).join('\n');
  const imgs = [...k.querySelectorAll('img')].map(i => i.alt || '').filter(a => a.length > 15);
  return {text, image_alt: imgs};
}

function scroller(d) {
  return [...d.querySelectorAll('div')].filter(e => {
    const s = getComputedStyle(e);
    return /(auto|scroll)/.test(s.overflowY) && e.scrollHeight > e.clientHeight + 50;
  }).sort((a, b) => b.scrollHeight - a.scrollHeight)[0];
}

async function readComments(k) {
  const cb = [...k.querySelectorAll('[role=button][aria-label="Leave a comment"]')].find(b => /^\d+$/.test(b.innerText.trim()));
  if (!cb || cb.closest('a[href]')) return {comments: [], permalink: ''};
  try {
    cb.click();
    await sleep(rnd(2000, 3500));
    const d = [...document.querySelectorAll('[role=dialog]')].pop();
    if (!d) return {comments: [], permalink: ''};
    const permalink = location.href;
    const filt = [...d.querySelectorAll('[role=button]')].find(b => /^(Most relevant|Newest|All comments)$/.test(b.innerText.trim()));
    if (filt && filt.innerText.trim() !== 'All comments') {
      filt.click();
      await sleep(rnd(1000, 1800));
      const mi = [...document.querySelectorAll('[role=menuitem]')].find(m => /All comments/.test(m.innerText));
      if (mi) { mi.click(); await sleep(rnd(2000, 3000)); }
    }
    let stable = 0, last = -1;
    for (let i = 0; i < 30 && stable < 3; i++) {
      const more = [...d.querySelectorAll('[role=button]')].filter(b => b.innerText.length < 60 && !b.closest('a[href]') &&
        /^(View (more|previous|all|\d+)|See more|\d+ repl|View \d+ repl|View all \d+ repl)/i.test(b.innerText.trim()));
      for (const b of more) { b.click(); await sleep(rnd(800, 1500)); }
      const sc = scroller(d);
      if (sc) sc.scrollTop = sc.scrollHeight;
      await sleep(rnd(1200, 2200));
      const n = d.querySelectorAll('[role=article]').length;
      if (n === last && more.length === 0) stable++; else stable = 0;
      last = n;
    }
    const comments = [...d.querySelectorAll('[role=article]')].map(a => ({
      label: a.getAttribute('aria-label') || '',
      text: [...a.querySelectorAll('div[dir=auto]')].map(e => e.innerText.trim()).filter(Boolean).join('\n'),
      image_alt: [...a.querySelectorAll('img')].map(i => i.alt || '').filter(x => x.length > 15),
    })).filter(c => c.text || c.image_alt.length);
    const x = d.querySelector('[aria-label=Close]');
    if (x) x.click();
    await sleep(rnd(1500, 2500));
    return {comments, permalink};
  } catch(e) {
    return {comments: [], permalink: ''};
  }
}

(async () => {
  S.log.push('started scraping ' + NAME);
  let noNewCount = 0;
  
  while (!S.stop && S.posts.length < MAX) {
    if (blocked()) {
      S.log.push('BLOCK WARNING detected, stopping');
      break;
    }
    
    // Find all post elements in feed
    const feed = document.querySelector('[role=feed]') || document.body;
    const cards = [...feed.querySelectorAll('div[role="feed"] > div, div[data-ad-preview="message"], div[role="article"]')];
    let addedInThisLoop = 0;

    for (const k of cards) {
      if (S.stop || S.posts.length >= MAX) break;
      const textVal = k.innerText ? k.innerText.trim() : '';
      if (!textVal || textVal.length < 20) continue;
      
      const info = postInfo(k);
      if (!info.text && !info.image_alt.length) continue;
      
      const key = info.text.slice(0, 150);
      if (seenText.has(key)) continue;
      seenText.add(key);
      addedInThisLoop++;

      try {
        k.scrollIntoView({block: 'center'});
        await sleep(rnd(800, 1500));
      } catch(e) {}

      let c = {comments: [], permalink: ''};
      try {
        c = await readComments(k);
      } catch(e) {
        S.log.push('comment read err: ' + e.message);
      }

      S.posts.push({
        raw: info.text,
        text: info.text,
        image_alt: info.image_alt,
        comments: c.comments,
        permalink: c.permalink,
        scrapedAt: new Date().toISOString()
      });
      S.saves++;

      if (blocked()) {
        S.log.push('BLOCK WARNING');
        S.stop = true;
        break;
      }
      
      window.scrollBy(0, rnd(200, 400));
      await sleep(c.comments.length ? rnd(2500, 4000) : rnd(1200, 2000));
    }

    if (addedInThisLoop === 0) {
      noNewCount++;
      // Even if 'End of results' appears, continue searching and scrolling up to 8 extra cycles
      // to ensure all posts beside 'End of results' are completely extracted.
      if (hasEndText()) {
        S.log.push('End of results visible, checking remaining posts (retry ' + noNewCount + '/8)...');
      }
      if (noNewCount >= 8) {
        S.log.push('No new posts found after 8 full scroll retries. Finished.');
        break;
      }
    } else {
      noNewCount = 0;
    }

    window.scrollBy(0, rnd(700, 1100));
    await sleep(rnd(2500, 4000));
  }

  S.done = true;
  S.running = false;
  S.log.push('completed with ' + S.posts.length + ' posts');
})();
return 'collector launched for ' + NAME;
