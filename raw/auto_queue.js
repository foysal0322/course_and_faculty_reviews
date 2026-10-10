// Auto-Runner: Automatically runs through all Marketing courses in sequence!
(async () => {
  const COURSES = [
    "mkt202", "mkt330", "mkt337", "mkt344", "mkt355", "mkt382",
    "mkt412", "mkt417", "mkt450", "mkt460", "mkt465", "mkt470", "mkt475"
  ];
  const GROUP_ID = "241165482653333";
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  // Determine current course from URL or start with first
  const match = location.href.match(/[?&]q=([^&#]+)/i);
  const currentQuery = match ? decodeURIComponent(match[1]).toLowerCase() : "";
  let idx = COURSES.indexOf(currentQuery);
  if (idx === -1) idx = 0;

  const course = COURSES[idx];
  const outName = `marketing/q_${course}.json`;
  console.log(`[AutoScraper] === Starting course ${idx + 1}/${COURSES.length}: ${course.toUpperCase()} (${outName}) ===`);

  window.__fbTargetName = outName;
  window.__fbTargetMax = 60;

  // Load collector library
  const scriptText = await fetch("http://127.0.0.1:8085/lib/collector.js").then(r => r.text());
  new Function(scriptText)();
  window.__fbCollector();

  // Monitor until current course collector finishes
  while (window.__fb && window.__fb.running && !window.__fb.done) {
    await sleep(5000);
  }

  console.log(`[AutoScraper] === Completed ${course.toUpperCase()}! Posts gathered: ${window.__fb ? window.__fb.posts.length : 0} ===`);

  // Navigate to the next course if available
  const nextIdx = idx + 1;
  if (nextIdx < COURSES.length) {
    const nextCourse = COURSES[nextIdx];
    const nextUrl = `https://www.facebook.com/groups/${GROUP_ID}/search/?q=${nextCourse}`;
    console.log(`[AutoScraper] Waiting 90 seconds before next course (${nextCourse.toUpperCase()}) to prevent rate limits...`);
    await sleep(90000);
    console.log(`[AutoScraper] Navigating to next course: ${nextUrl}`);
    location.href = nextUrl;
  } else {
    console.log("[AutoScraper] All 13 Marketing courses completed successfully!");
    alert("All 13 Marketing courses scraped successfully!");
  }
})();
