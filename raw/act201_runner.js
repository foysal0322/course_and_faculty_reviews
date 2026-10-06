(function(arguments) {
// Sent through Selenium execute_script on the Facebook group search page. args: [outputName, maxPosts]
// Progress lives on disk through the localhost sink tab because Facebook clears localStorage on reload.
const NAME = arguments[0], MAX = arguments[1] || 60;
if (window.__fb && window.__fb.running) return 'already running';
const S = window.__fb = {posts: [], running: true, done: false, log: [], stop: false, name: NAME, saves: 0};
const sleep = ms => new Promise(r => setTimeout(r, ms));
const rnd = (a, b) => a + Math.random() * (b - a);
// Re-acquire the sink tab on every use: the window reference silently goes stale after reloads.
const getSink = () => {
  const w = window.open('', 'fbsink');
  try { if (w.location.href === 'about:blank') w.location = 'http://127.0.0.1:8765/'; } catch (e) {}
  window.focus();
  return w;
};
getSink();
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
  if (!text) text = [...k.querySelectorAll('div[dir=auto]')].map(e => e.innerText.trim()).filter(Boolean).slice(0, 3).join('\n');
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
  // The comment count lives on the "Leave a comment" button; it exists even when a post has no reactions.
  const cb = [...k.querySelectorAll('[role=button][aria-label="Leave a comment"]')].find(b => /^\d+$/.test(b.innerText.trim()));
  if (!cb) return {comments: [], permalink: ''};
  cb.click();
  await sleep(rnd(2500, 4000));
  const d = [...document.querySelectorAll('[role=dialog]')].pop();
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
  const x = d.querySelector('[aria-label=Close]');
  if (x) x.click();
  await sleep(rnd(1800, 2800));
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
    const feed = document.querySelector('[role=feed]');
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
      // Only mark a post as seen once its message has rendered; half-loaded posts are retried later.
      const info = postInfo(k);
      if (!info.text && !info.image_alt.length) continue;
      seen.add(k);
      const key = info.text.slice(0, 150);
      if (seenText.has(key)) continue;
      seenText.add(key);
      got++;
      k.scrollIntoView({block: 'center'});
      await sleep(rnd(1000, 2000));
      persist(info);
      await sleep(500);
      const courseMatch = NAME.match(/[a-z]{3}\d+[a-z]*/i);
      const coursePat = courseMatch ? new RegExp('\\b' + courseMatch[0].slice(0, 3) + '[-_\\s]?' + courseMatch[0].slice(3) + '\\b', 'i') : null;
      const fullPostHeader = info.text + ' ' + info.image_alt.join(' ');
      const hasCourse = !coursePat || coursePat.test(fullPostHeader);

      let c = {comments: [], permalink: ''};
      if (hasCourse) {
        try { c = await readComments(k); } catch (e) { S.log.push('err ' + e.message); }
      }
      S.posts.push({...info, ...c});
      save();
      persist();
      if (blocked()) { S.log.push('BLOCK WARNING'); S.stop = true; break; }
      window.scrollBy(0, rnd(250, 450));
      await sleep(c.comments.length ? rnd(5000, 7000) : rnd(2500, 3500));
    }
    if (got === 0 && ended()) { S.log.push('End of results reached'); break; }
    if (got === 0) { idle++; if (idle > 8) { S.log.push('no more posts'); break; } } else idle = 0;
    if (got === 0) window.scrollTo(0, document.body.scrollHeight); else window.scrollBy(0, rnd(600, 900));
    await sleep(rnd(4000, 6000));
  }
  save();
  post(NAME + '.done', {log: S.log, n: S.posts.length});
  S.running = false;
  S.done = true;
})();
return 'started ' + NAME;

})(["accounting/q_act201.json", 60]);