# NSU Faculty Review Scraper — Agent Instructions

Read this whole file before doing anything. It is self-contained: an agent with no prior
context should be able to scrape a new course and produce its review file by following it.

---

## 1. Goal

For one NSU course at a time (e.g. `CSE215`), collect student reviews of that course's
faculty from the Facebook group **NSU Faculty Course & Grade Analysis**, judge every
meaningful comment, rate it, and save a new JSON file for that course.

Status so far:

| Course | Raw data | Final file |
|---|---|---|
| CSE115 | `raw/q0_recent.json`, `raw/q1_cse115.json` | `cse115_individual_reviews.json` |
| CSE173 | `raw/q_cse173.json` | `cse173_detailed_reviews.json` |
| CSE215 | `raw/q_cse215b.json` (the complete re-run; supersedes `raw/q_cse215.json`) | `cse215_detailed_reviews.json` (built from the first run only; should be rebuilt from `q_cse215b.json`) |

Always create **new** output files. Never overwrite or edit existing result files unless
the user asks.

---

## 2. Project layout

```
course_and_faculty_reviews/
  course_faculty.json          reference COURSE → FACULTY data (authoritative)
  instruction.md               this file
  cseXXX_*_reviews.json        final outputs, one per course
  raw/
    sink.py                    local helper server that writes scraped data to disk
    collector.js               in-page scraper (sent through Selenium)
    q_<course>.json            raw scraped posts + comments
    q_<course>.json.cur        post being processed right now (crash recovery)
    q_<course>.json.done       written when a run ends (log + count)
    extract173.py / extract215.py   print candidate comments for manual judging
    build173.py / build215.py       turn judged picks into the final JSON
```

---

## 3. Reference dataset: `course_faculty.json`

- Format: a list of one-key objects with comma-separated lowercase initials, e.g.
  `[{"cse115": "fth,hsm,mhis,..."}, {"cse173": "itn,mle,msk1,..."}]`. May contain
  duplicates, so normalize case and dedupe.
- Read the list for a course in PowerShell:
  ```powershell
  $j = Get-Content course_faculty.json -Raw | ConvertFrom-Json; ($j | ? { $_.cse215 }).cse215
  ```
- The relationship is **many-to-many**. Build both lookups: COURSE → FACULTIES and
  FACULTY → COURSES. Never assume a faculty teaches only one course.
- `tba` = "to be announced"; ignore it.
- Suffixed initials (`tns1`, `msk1`, `sfr1`, `sha1`) are distinct people. Keep them exact.
  If a student writes a bare form such as "SHA" and it's ambiguous, mark it UNCERTAIN.
  Don't guess.

Faculty lists used so far:

- CSE115: fth, hsm, mhis, mle, msrb, nlh, nva, oisd, rsy, rjp, smsl, sus, shaifur, tnr, tns1
- CSE173: itn, mle, msk1, msrb, sle, ssi, sva, tnf
- CSE215: hsm, mft, mhis, muo, rih, rrn, rjp, sfr1, sva

---

## 4. Environment and tools

- **OS:** Windows, PowerShell. Python is available (`python`).
- **Browser:** Chrome, driven by the **`user-selenium` MCP** (`start_browser`, `navigate`,
  `execute_script`, `take_screenshot`, `window`). The user is already logged into
  Facebook in that Chrome session.
  - If no session exists: `start_browser` with `{"browser": "chrome"}`. Edge doesn't work
    (no driver installed).
  - Don't use the Cursor built-in browser for scraping.
- **Group search URL** (replace the query):
  `https://www.facebook.com/groups/1574365339447298/search/?q=cse215`
  Use the default "Top" sort. The "Most recent" toggle returns only ~5 results.

### Why a local helper server is needed
Facebook's page security policy blocks `fetch` to localhost, blocks `eval`/`new Function`,
blocks loading scripts from `http://127.0.0.1`, and **wipes `localStorage` on reload**.
Blob downloads didn't land on disk either. What works: the collector opens a second tab,
`http://127.0.0.1:8765/` (named `fbsink`), and sends data to it with `postMessage`. That
page POSTs it to `raw/sink.py`, which writes files into `raw/`. The sink also serves saved
files back (`GET /f/<name>`) so a restarted collector can resume.

The helper tab reappears if it's closed. That's expected; tell the user to leave it open.

---

## 5. Step-by-step workflow for a new course

### Step 1: Start the sink server (if it isn't running)
```powershell
try { (Invoke-WebRequest http://127.0.0.1:8765/ -UseBasicParsing -TimeoutSec 3).StatusCode } catch { "down" }
# if down:
Start-Process python -ArgumentList "raw\sink.py" -WindowStyle Hidden
```
If you edit `sink.py`, kill every old instance first (`Get-Process python | Stop-Process -Force`),
because a stale process keeps serving the old code.

### Step 2: Get the faculty list
From `course_faculty.json` (see section 3).

### Step 3: Open the search
`navigate` to the group search URL with `q=<course code>` (e.g. `cse215`).

### Step 4: Start the collector
Call `execute_script` with the **full contents of `raw/collector.js`** as `script` and
`args: ["q_<course>.json", 60]` (the output file name and the max post count). It returns
`started ...` immediately and keeps running inside the page.

For each post, the collector:
1. Clicks the post's **"Leave a comment"** button (the one showing the comment count).
2. Switches the comment filter to **All comments**.
3. Keeps clicking "View more comments" / "View N replies" / "See more" and scrolling the
   comment box until nothing new loads. Ensure all truncated comments with "See more" are clicked to expand the full text.
4. Reads every comment (`role=article`; its `aria-label` holds author + relative age).
5. Closes the dialog, saves to disk, scrolls the page a little, and **waits ~5–7 s**
   before the next post (~3 s for posts without comments).
6. When nothing new is loaded, scrolls to the bottom to trigger more results.

It stops when:
- **"End of results"** is on screen and no unprocessed posts remain,
- it reaches the max post count,
- it finds nothing new for ~9 rounds, or
- Facebook shows any block / "slow down" / "going too fast" warning.

### Step 5: Monitor
Poll every ~5 minutes (never in a tight loop):
```js
const S=window.__fb; return S?{n:S.posts.length, running:S.running, saves:S.saves, log:S.log}:'no state '+location.href
```
Also check that the file on disk is growing:
```powershell
python -c "import json;d=json.load(open('raw/q_cse215.json',encoding='utf-8'));print(len(d),sum(len(p['comments']) for p in d))"
```
- **If the in-page count grows but the file doesn't**, saves are failing. Push manually:
  ```js
  const w=window.open('','fbsink'); window.focus(); w.postMessage({name:window.__fb.name, body:JSON.stringify(window.__fb.posts)},'*'); return 'sent'
  ```
- **If the result is `no state`**, the page reloaded and killed the collector. `navigate`
  back to the search URL and run Step 4 again with the same file name. It resumes from
  disk, and the post that caused the reload is recorded without comments and skipped.
- **To stop** when the user asks: `window.__fb.stop = true`, then push a manual save.

### Step 6: Extract candidates
Copy `raw/extract215.py`, change the input file, output file and faculty list, and run it.
It writes `raw/candidates<course>.txt`: each post that mentions a listed faculty, followed
by its comments, plus comments elsewhere that name a listed faculty. Read that file fully.

Also check posts whose comments came back empty but whose text is a question about a
listed faculty. If there are many, the comment button wasn't found (see pitfalls).

### Step 7: Judge and rate (manual, semantic)
Read each candidate in its post's context and decide keep/drop plus a rating (sections 6–7).
Record your picks as `(faculty, opening words of the comment, rating)` in a copy of
`raw/build215.py`. The script finds the full original text by prefix (exact match first),
so the saved review is always the verbatim Facebook text. It dedupes and applies the
review count rule. Run it and confirm `missing: []`.

### Step 8: Report to the user
Give a per-faculty table of review counts by rating, name faculty with no reviews, and
flag the judgment calls (split opinions, sarcasm, skipped non-reference faculty).

---

## 6. Interpretation rules

### What counts as a review source
- Any post about the course, especially:
  - "Best faculty for CSE215?" / "Review please: CSE215 - RRN"
  - **"How is X for COURSE?" posts**, e.g. "How's RRn for cse215?", "How is Sva for
    CSE 215?", "Anyone did CSE215 under RRN?", "Is RIH better than MFT for CSE215?".
    Replies to such posts review that faculty for that course, **even if the reply doesn't
    repeat the initials** ("Drop", "best for learning, curves a lot"). If the post compares
    two faculty, give each reply to the faculty it's actually about.
- A post whose own text is a detailed review (e.g. "#FacultyReview #sva #cse173 …") is
  itself a review.

### Course/faculty validation
- When a post names both a course and a faculty, check the pair against the reference:
  `VALID`, `NOT_FOUND_IN_REFERENCE` (the student isn't necessarily wrong; the data may be
  outdated), or `UNCERTAIN`.
- **Only include faculty that are in the course's reference list.** Skip others, even in
  course context (e.g. AKR, SFT, MSRB for CSE215). Never fabricate a faculty-course link.
- Faculty-only mention ("MFS kemon?"): use the reverse lookup for the possible courses and
  use the surrounding context to pick one. If the context doesn't establish the course,
  don't include it.
- Course-only question ("Best faculty for CSE215?"): the reference says who teaches it,
  but a recommendation must come from actual comments.

### Text normalization
- Treat `CSE 215`, `CSE-215`, `cse215`, "CSE215 er jonno" as the same course.
- Don't infer a course from a bare number ("215 er jonno ke valo?") unless the post or
  thread makes it clear.
- Normalize faculty case: `TnS1` → `tns1`, `NvA` → `nva`, `MsK1` → `msk1`.

### Bangla / Banglish
Read for meaning, not keywords. Common phrases:
- valo / bhalo = good; shera / joss / goat / best = great
- drop / avoid / bachai de = avoid; pera = hard/stressful; curve kore = curves grades
- matir manush = down-to-earth, kind

### Context and comments
- The post supplies the context. Under "Best faculty for CSE115?", a reply of "Nva" is a
  recommendation. Under "Faculty NvA CSE115 review plz", a reply of "Drop" is a negative
  review of NVA.
- A reply tagging a name and then giving an opinion ("Tousif … A+ o paite paren") keeps
  its original text, name included. Judge the opinion.
- Watch for **sarcasm**, e.g. "khub valo ki r bolbo… eto valo je just valo bolleo kom hoye
  jabe", and "Koren vai Msk1.. be ready for insult" (means avoid). Rate the intent.
- Skip comments about a *different* faculty or course in the same thread, like a lab
  instructor, MAT120 faculty in a CSE215 post, or a CSE225 experience in a CSE215 thread.

### Images
If course/faculty info is only in an image, read it (the collector stores `img.alt`; use
visual reading if needed). Extract the course and faculty, validate them, and treat them
like text. Note `information_source = IMAGE` if relevant.

### Don't over-trust the reference
Use it to validate identities, never to invent content. Keep separate:
reference fact / student question / opinion / experience / recommendation / agent inference.
Don't present a student's opinion as fact. **Always preserve the raw Facebook text
verbatim.**

---

## 7. Keep/drop and rating rules

### Drop (not a review)
Name tags alone, `.`, `F`, `up`, `bump`, `cfbr`, thank-yous, "same section", section and
timing talk, section-exchange / course-exchange logistics (e.g., "Exchange post: / You get: / CSE273.01 (ARa2)"),
bare schedule lists (e.g., "Cse273 - SMSL / Mkn1 / Cse373 - Ara2"), pure questions/requests
(e.g., "Kindly provide your valuable review on those faculties", "How to get A/A- under these faculties"),
jokes with no judgment, and comments about a faculty not in the reference list.

### Keep
Anything that judges the faculty: teaching, grading, curving, question difficulty,
behavior, experience ("got A-"), recommendation ("go for X", "MHIS is good"), or warning ("drop X", "drop MHIS").
A bare short verdict or recommendation under a post (e.g., "MHIS is good", "drop MHIS") MUST be kept as a review.

### Review count rule
- **Target minimum:** Keep scraping until *each* faculty has at least 10 meaningful reviews. If you reach posts from 2020 (estimate post age via comment timestamps like "4 years ago" or "5 years ago") OR see "End of results" on screen before reaching 2020, stop there even if 10 reviews were not found for a faculty.
- **Quality over quantity:** If a faculty gets 20+ reviews, keep only comparatively long reviews with a proper statement, opinion, or suggestion.
- **Max cap:** A single faculty will have 20 reviews max in the final output.
- Omit faculty with zero kept reviews.

### Rating scale (one rating per review)
| Rating | Use when |
|---|---|
| `Outstanding` | Superlative praise: "best best best", "GOAT", "11/10", "got A even with a bad mid", "best for learning AND grading", detailed glowing experience |
| `great` | Clearly positive / recommendation: "X best", "go for X", "valo", bare initials under a "who's best" post, positive with minor caveats |
| `normal` | Mixed or neutral: "average learning, good grading", "fair grading, no curve", tips without a verdict, probable-sarcasm praise |
| `harsh` | Tough but not a flat "drop": hard questions, stressful, biased, strict, "not for freshers", "you'll struggle", heavy-pressure warnings |
| `avoid` | "Drop", "avoid", "worst", "save your money", clearly sarcastic praise that means avoid |

---

## 8. Output format

File name: `<course>_detailed_reviews.json` (e.g. `cse215_detailed_reviews.json`).
Every kept comment is its **own** review with its **own** rating:

```json
{
  "cse215": {
    "muo": [
      {"review": "<verbatim comment text>", "rating": "Outstanding"},
      {"review": "<verbatim comment text>", "rating": "great"}
    ],
    "sva": [
      {"review": "<verbatim comment text>", "rating": "harsh"}
    ]
  }
}
```

- Keys are lowercase course and faculty codes.
- Save as UTF-8 with `ensure_ascii=False` so Bangla text stays readable.
- Dedupe identical review strings per faculty.

---

## 9. Scraping safety (avoid Facebook restrictions)

- One post at a time, randomized human-like delays (1–4 s between clicks, ~5–7 s between
  posts). Never parallelize tabs or run two collectors.
- Stop immediately on any block / "slow down" / "going too fast" / "misusing this
  feature" message, and report it to the user.
- **Stop as soon as "End of results" is on screen** (after finishing posts already loaded).
  Don't keep scrolling.
- Cap each run based on the requirement to hit 10 meaningful reviews per faculty, or until reaching posts from 2020. You can run multiple batches if needed.
- Never read or save Messenger chat content. Only read the group feed (`[role=feed]`) and
  post dialogs. The page also has `role=article` elements from Messenger chats; ignore them.
- Do only what the user asked. If the user says stop, set `window.__fb.stop = true`,
  save, and don't restart.

---

## 10. Known pitfalls (already fixed in `collector.js`, but keep them in mind)

1. **Obfuscated text.** A post's `innerText` is padded with repeated "Facebook" filler.
   Read the message from `[data-ad-rendering-role=story_message]`, or fall back to
   `div[dir=auto]`.
2. **Hidden dates.** The search results don't expose post dates. Estimate age from comment
   labels ("… 2 years ago") if you need a cutoff.
3. **Virtualized feed.** Results render blank until scrolled into view, and more load only
   near the bottom. Scroll each blank item into view, and scroll to the bottom when nothing
   new is found.
4. **Half-rendered posts.** Only mark a post as processed after its message text exists;
   otherwise it gets skipped forever.
5. **Comment button.** Use `[aria-label="Leave a comment"]` with a numeric count. Posts with
   comments but no reactions have only this one numeric button. An older "two numeric
   buttons" rule skipped them, which lost all replies to "How is RRn for CSE215?" posts.
6. **Page reloads.** Sometimes opening a post forces a full reload. State is lost, but
   `.cur` + resume-from-disk handle it. Re-navigate and re-run.
7. **Stale sink reference.** Always re-acquire it with `window.open('', 'fbsink')` before
   `postMessage`. A saved reference silently stopped working once, and nothing was written
   until a manual push.
8. **Closing a post dialog** can navigate away (e.g. to the Facebook home page) if the
   dialog was the first history entry. Re-navigate to the search URL if that happens.
