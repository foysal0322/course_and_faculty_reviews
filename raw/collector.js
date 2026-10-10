// Sent through Selenium execute_script on the Facebook group search page. args: [outputName, maxPosts]
// Progress lives on disk through the localhost sink tab because Facebook clears localStorage on reload.
const NAME = (typeof arguments !== 'undefined' && arguments[0]) || window.__fbTargetName || 'ECO/q_eco101.json';
const MAX = (typeof arguments !== 'undefined' && arguments[1]) || window.__fbTargetMax || 60;
const SEARCH_URL = location.href;
if (window.__fb && window.__fb.running) return 'already running';
const S = window.__fb = {posts: [], running: true, done: false, log: [], stop: false, name: NAME, saves: 0};
const sleep = ms => new Promise(r => setTimeout(r, ms));
const rnd = (a, b) => a + Math.random() * (b - a);

// Re-acquire the sink tab on every use: the window reference silently goes stale after reloads.
const getSink = () => {
  const w = window.open('', 'fbsink');
  try { if (w.location.href === 'about:blank') w.location = 'http://127.0.0.1:8085/'; } catch (e) {}
  window.focus();
  return w;
};
getSink();

// Permanently block any click on Like or React elements during scraping
document.addEventListener('click', e => {
  const el = e.target.closest('[role=button]');
  if (el) {
    const aria = el.getAttribute('aria-label') || '';
    if (/Like|React/i.test(aria) || aria === 'Remove Like') {
      e.stopImmediatePropagation();
      e.preventDefault();
    }
  }
}, true);

// Parse course code from output name, e.g. "ECO/q_eco101.json" -> "eco", "101"
const mCode = NAME.match(/q_([a-z]+)(\d+)/i);
let courseRegex = null;
if (mCode) {
  const dept = mCode[1];
  const num = mCode[2];
  courseRegex = new RegExp('\\b' + dept + '[\\s-_]*' + num + '\\b', 'i');
}

function hasCourseCode(k, info) {
  if (!courseRegex) return true;
  if (courseRegex.test(info.text)) return true;
  if (courseRegex.test(k.innerText || '')) return true;
  if (info.image_alt && info.image_alt.some(a => courseRegex.test(a))) return true;
  return false;
}

const want = {};
addEventListener('message', e => {
  const m = e.data;
  if (m && m.saved) S.saves++;
  if (m && m.file && want[m.file]) { want[m.file](m.ok ? m.body : null); delete want[m.file]; }
});
const get = f => new Promise(res => { want[f] = res; getSink().postMessage({get: f}, '*'); setTimeout(() => res(null), 8000); });
const post = (name, obj) => { try { getSink().postMessage({name, body: JSON.stringify(obj)}, '*'); } catch (e) { S.log.push('save err ' + e.message); } };
const persist = cur => post(NAME + '.cur', cur || {});
const save = () => post(NAME, S.posts);
const seen = new WeakSet(), seenText = new Set();
const blocked = () => /Temporarily Blocked|You.re going too fast|slow down|misusing this feature/i.test(document.body.innerText.slice(0, 20000));
const ended = () => /End of results/i.test(document.body.innerText);

function postInfo(k) {
  const msgEls = [...k.querySelectorAll('[data-ad-rendering-role=story_message],[data-ad-comet-preview=message]')];
  let text = msgEls.map(e => e.innerText.trim()).filter(Boolean)[0] || '';
  if (!text) text = [...k.querySelectorAll('div[dir=auto]')].map(e => e.innerText.trim()).filter(Boolean).slice(0, 5).join('\n');
  if (!text) text = k.innerText.trim();
  const imgs = [...k.querySelectorAll('img')].map(i => i.alt || '').filter(a => a.length > 15);
  return {text, image_alt: imgs};
}

async function expandPostSeeMore(k) {
  const candidates = [...k.querySelectorAll('[role=button], span, div')].filter(el => {
    if (el.children.length > 0) return false;
    if (el.closest('a[href]')) return false;
    const txt = el.innerText.trim();
    return /^(See more|\.\.\.\s*See more)$/i.test(txt);
  });
  for (const c of candidates) {
    const btn = c.closest('[role=button]') || c;
    const aria = btn.getAttribute('aria-label') || '';
    if (/Like|React/i.test(aria) || aria === 'Remove Like') continue;
    try {
      btn.scrollIntoView({block: 'nearest'});
      await sleep(300);
      btn.click();
      await sleep(rnd(1200, 2000));
    } catch (e) {}
  }
}

function scroller(d) {
  return [...d.querySelectorAll('div')].filter(e => {
    const s = getComputedStyle(e);
    return /(auto|scroll)/.test(s.overflowY) && e.scrollHeight > e.clientHeight + 50;
  }).sort((a, b) => b.scrollHeight - a.scrollHeight)[0];
}

async function readComments(k) {
  const btns = [...k.querySelectorAll('[role=button]')].filter(b => !b.closest('a') && !b.querySelector('a'));
  const cb = btns.find(b => {
    const aria = b.getAttribute('aria-label') || '';
    if (/Like|React/i.test(aria)) return false;
    if (aria === 'Leave a comment') return true;
    const t = b.innerText.trim();
    return /^\d+\s+comments?$/i.test(t);
  });
  if (!cb) return {comments: [], permalink: ''};
  cb.click();
  await sleep(rnd(2500, 4000));
  const d = [...document.querySelectorAll('[role=dialog]')].filter(d => !/Notifications|Chat|Messenger/i.test(d.getAttribute('aria-label') || '')).pop();
  if (!d) return {comments: [], permalink: ''};
  const permalink = location.href;
  const filt = [...d.querySelectorAll('[role=button]')].find(b => /^(Most relevant|Newest|All comments)$/.test(b.innerText.trim()));
  if (filt && filt.innerText.trim() !== 'All comments') {
    filt.click();
    await sleep(rnd(1200, 2000));
    const mi = [...document.querySelectorAll('[role=menuitem]')].find(m => /All comments/.test(m.innerText));
    if (mi) { mi.click(); await sleep(rnd(2500, 3500)); }
  }
  let stable = 0, last = -1;
  for (let i = 0; i < 60 && stable < 3; i++) {
    const more = [...d.querySelectorAll('[role=button]')].filter(b => b.innerText.length < 60 && !b.closest('a[href]') &&
      /^(View (more|previous|all|\d+)|See more|\d+ repl|View \d+ repl|View all \d+ repl)/i.test(b.innerText.trim()));
    for (const b of more) { b.click(); await sleep(rnd(900, 1800)); }
    const sc = scroller(d);
    if (sc) sc.scrollTop = sc.scrollHeight;
    await sleep(rnd(1500, 2800));
    const n = d.querySelectorAll('[role=article]').length;
    if (n === last && more.length === 0) stable++; else stable = 0;
    last = n;
  }
  const comments = [...d.querySelectorAll('[role=article]')].map(a => ({
    label: a.getAttribute('aria-label') || '',
    text: [...a.querySelectorAll('div[dir=auto]')].map(e => e.innerText.trim()).filter(Boolean).join('\n'),
    image_alt: [...a.querySelectorAll('img')].map(i => i.alt || '').filter(x => x.length > 15),
  })).filter(c => c.text || c.image_alt.length);
  const closeBtn = d.querySelector('[aria-label="Close"]') || d.querySelector('[aria-label=Close]');
  if (closeBtn && !closeBtn.closest('a[href]') && closeBtn.tagName !== 'A') {
    closeBtn.click();
    await sleep(rnd(1500, 2500));
  } else {
    document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', code: 'Escape', keyCode: 27, which: 27, bubbles: true}));
    await sleep(rnd(1500, 2500));
  }
  const still = [...document.querySelectorAll('[role=dialog]')].pop();
  if (still) {
    const x = still.querySelector('[aria-label="Close"]') || still.querySelector('[aria-label=Close]');
    if (x && !x.closest('a[href]') && x.tagName !== 'A') { x.click(); await sleep(1500); }
    else { document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', code: 'Escape', keyCode: 27, bubbles: true})); await sleep(1500); }
  }
  if (!location.href.includes('search/?q=') && document.querySelector('[role=feed]')) {
    try { history.replaceState(null, '', SEARCH_URL); } catch (e) {}
  }
  return {comments, permalink};
}

(async () => {
  await sleep(3000);
  S.posts = JSON.parse(await get(NAME) || '[]');
  const cur = JSON.parse(await get(NAME + '.cur') || 'null');
  if (cur && cur.text !== undefined && !S.posts.some(p => p.text.slice(0, 150) === cur.text.slice(0, 150)))
    S.posts.push({...cur, comments: [], permalink: '', note: 'page reloaded while reading comments'});
  S.posts.forEach(p => seenText.add(p.text.slice(0, 150)));
  S.log.push('resumed with ' + S.posts.length);
  let idle = 0;
  while (!S.stop && S.posts.length < MAX) {
    if (blocked()) { S.log.push('BLOCK WARNING detected, stopping'); break; }
    const feed = document.querySelector('[role=feed]') || document.querySelector('[role=main]');
    if (!feed) { await sleep(3000); idle++; if (idle > 8) break; continue; }
    const kids = [...feed.children].filter(k => !seen.has(k));
    let got = 0;
    for (const k of kids) {
      if (S.stop || S.posts.length >= MAX) break;
      if (!k.innerText.trim()) {
        k.scrollIntoView({block: 'center'});
        await sleep(rnd(1500, 2500));
        if (!k.innerText.trim()) continue;
      }

      // Expand "See more" in post body if present before checking course code
      await expandPostSeeMore(k);

      const info = postInfo(k);
      if (!info.text && !info.image_alt.length) continue;
      seen.add(k);
      const key = info.text.slice(0, 150);
      if (seenText.has(key)) continue;
      seenText.add(key);

      // Verify course code presence: both department and code must be present together
      if (!hasCourseCode(k, info)) {
        S.log.push('skipped post without ' + (mCode ? mCode[0] : 'course code'));
        continue;
      }

      got++;
      k.scrollIntoView({block: 'center'});
      await sleep(rnd(1000, 2000));
      persist(info);
      await sleep(500);
      let c = {comments: [], permalink: ''};
      try { c = await readComments(k); } catch (e) { S.log.push('err ' + e.message); }
      S.posts.push({...info, ...c});
      save();
      persist();
      if (blocked()) { S.log.push('BLOCK WARNING'); S.stop = true; break; }
      window.scrollBy(0, rnd(250, 450));
      await sleep(c.comments.length ? rnd(5000, 7000) : rnd(2500, 3500));
    }
    if (got === 0 && ended()) { S.log.push('End of results reached'); break; }
    if (kids.length === 0) {
      idle++;
      if (idle > 8) { S.log.push('no more posts'); break; }
    } else {
      idle = 0;
    }
    window.scrollBy(0, rnd(600, 900));
    await sleep(rnd(4000, 6000));
  }
  save();
  post(NAME + '.done', {log: S.log, n: S.posts.length});
  S.running = false;
  S.done = true;
})();
return 'started ' + NAME;
