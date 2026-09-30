// Run on a post permalink page after a reload; appends the pending (.cur) post with its comments to NAME.
const NAME = arguments[0];
window.__pr = 'running';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const rnd = (a, b) => a + Math.random() * (b - a);
const sink = window.open('http://127.0.0.1:8765/', 'fbsink');
window.focus();
const want = {};
addEventListener('message', e => { const m = e.data; if (m && m.file && want[m.file]) { want[m.file](m.ok ? m.body : null); delete want[m.file]; } });
const get = f => new Promise(res => { want[f] = res; sink.postMessage({get: f}, '*'); setTimeout(() => res(null), 8000); });
const post = (name, obj) => sink.postMessage({name, body: JSON.stringify(obj)}, '*');
(async () => {
  await sleep(2500);
  const posts = JSON.parse(await get(NAME) || '[]');
  const cur = JSON.parse(await get(NAME + '.cur') || 'null');
  if (!cur || cur.text === undefined) { window.__pr = 'no pending post'; return; }
  const root = document.body;
  const filt = [...root.querySelectorAll('[role=button]')].find(b => /^(Most relevant|Newest|All comments)$/.test(b.innerText.trim()));
  if (filt && filt.innerText.trim() !== 'All comments') {
    filt.click(); await sleep(rnd(1200, 2000));
    const mi = [...document.querySelectorAll('[role=menuitem]')].find(m => /All comments/.test(m.innerText));
    if (mi) { mi.click(); await sleep(rnd(2500, 3500)); }
  }
  let stable = 0, last = -1;
  for (let i = 0; i < 60 && stable < 3; i++) {
    const more = [...root.querySelectorAll('[role=button]')].filter(b => b.innerText.length < 60 && !b.closest('a[href]') &&
      /^(View (more|previous|all|\d+)|See more|\d+ repl|View \d+ repl|View all \d+ repl)/i.test(b.innerText.trim()));
    for (const b of more.slice(0, 4)) { b.click(); await sleep(rnd(900, 1800)); }
    window.scrollTo(0, document.body.scrollHeight);
    await sleep(rnd(1500, 2800));
    const n = root.querySelectorAll('[role=article]').length;
    if (n === last && more.length === 0) stable++; else stable = 0;
    last = n;
  }
  const comments = [...root.querySelectorAll('[role=article]')].map(a => ({
    label: a.getAttribute('aria-label') || '',
    text: [...a.querySelectorAll('div[dir=auto]')].map(e => e.innerText.trim()).filter(Boolean).join('\n'),
    image_alt: [...a.querySelectorAll('img')].map(i => i.alt || '').filter(x => x.length > 15),
  })).filter(c => /^(Comment|Reply) by/.test(c.label) && (c.text || c.image_alt.length));
  posts.push({...cur, comments, permalink: location.href});
  post(NAME, posts);
  await sleep(1000);
  post(NAME + '.cur', {});
  window.__pr = 'saved ' + comments.length + ' comments, total posts ' + posts.length;
})();
return 'started';
