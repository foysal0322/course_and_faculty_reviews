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

## 3. Dynamic Faculty Discovery Rule

- **Do NOT restrict faculty extraction to a static reference dataset or `course_faculty.json`.**
- For any target course, discover **ALL faculty members** mentioned, discussed, or reviewed in the scraped post headers and comment threads for that course.
- Automatically identify all 3-to-4 letter faculty initial codes (and variants) referenced by students for the target course code.

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

### Step 2: Open the search
`navigate` to the group search URL with `q=<course code>` (e.g. `cse215`).

### Step 3: Start the collector
Call `execute_script` with the **full contents of `raw/collector.js`** as `script` and
`args: ["q_<course>.json", 60]` (the output file name and the max post count). It returns
`started ...` immediately and keeps running inside the page.

For each post, the collector:
1. **Course Code Pre-Check:** Checks if the post text or image alt explicitly contains the target course code (e.g., `CSE445`, `CSE 445`, `CSE-445`). If the post does NOT contain the course code, **do NOT open the comment section**; record the post text and move immediately to the next post.
2. If it contains the course code, clicks the post's **"Leave a comment"** button (the one showing the comment count).
3. Switches the comment filter to **All comments**.
4. Keeps clicking "View more comments" / "View N replies" / "See more" and scrolling the
   comment box until nothing new loads. Ensure all truncated comments with "See more" are clicked to expand the full text.
5. Reads every comment (`role=article`; its `aria-label` holds author + relative age).
6. Closes the dialog, saves to disk, scrolls the page a little, and **waits ~5–7 s**
   before the next post (~3 s for posts without comments).
7. When nothing new is loaded, scrolls to the bottom to trigger more results.

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

### Step 5: Extract candidates for LLM evaluation
Run a candidate extraction script (e.g. `python -c ...` or an `extract_<course>.py` script).
It reads `q_<course>.json`, checks course code relevance, dynamically matches candidate comments against all discovered faculty initials for that course, and outputs two files:
- `candidates_<course>.txt` (Human-readable text thread file)
- `<course>_llm_candidates.json` (Structured candidate review objects)

### Step 6: Automated LLM Evaluation & Sentiment Processing (Gemini Flash Model)
Use an LLM subagent (preferably **Gemini Flash** / `flash` tier model for cost efficiency across all course batches):
1. **Full-Text Semantic Comprehension (No String-Keyword Reliance):**
   - Read every candidate comment end-to-end to understand genuine student sentiment, underlying tone, emotions, overall experience, and intent.
   - Do NOT rely on simple string or keyword matching (e.g., avoid misclassifying recommendations that quote "saying to avoid" or mention board practice/homework).
2. **Sentiment & Rating Assignment (5 Scale):**
   - `Outstanding`: Glowing praise, top-tier goated teachers, 11/10, student expresses extreme satisfaction.
   - `great`: Positive recommendation, good teaching, fair/generous curves or grading, student advice on succeeding under a solid faculty.
   - `normal`: Neutral, balanced, factual description of course structure, exams, slides, or attendance.
   - `harsh`: Extremely strict, unaccommodating, heavy pressure with poor teaching support, or frustrating course atmosphere.
   - `avoid`: Student strongly warns others against taking the faculty, expresses deep dissatisfaction, or experienced unfair outcomes.
3. **Filter Non-Reviews & False Positives:**
   - Filter out invalid faculty initials that are common words or pronouns (e.g. `TMI`, `SEI`, `TAE`, `HAS`, `ABT`, `HIM` when used as a pronoun, `TMR`, `KSE`).
   - Filter out student questions, seat requests, routine/partner queries, or tag-only chatter.
4. **Multi-Faculty Disambiguation & Deduplication:**
   - Extract independent feedback for each professor if a comment discusses multiple faculty members.
   - Deduplicate verbatim identical comments for the same professor.
   - Enforce a max cap of 20 detailed reviews per faculty member.
5. **Output Generation:**
   - Save directly to `<course>_detailed_reviews.json` (or inside subject folders like `accounting/` or `finance/`).

### Step 7: Report to the user
Give a per-faculty table of review counts by rating, name faculty with no reviews, and
flag the judgment calls (split opinions, sarcasm, skipped non-reference faculty).

---

## 6. Interpretation rules

### What counts as a review source
- A post whose own text is a detailed review (e.g. "#FacultyReview #sva #cse173 …") is itself a review.
- Replies under posts that offer a **CLEAR STATEMENT, VERDICT, OR EXPERIENCE** regarding a faculty.
- **CRITICAL RULE — QUESTION-TYPE COMMENTS MUST BE DROPPED:**
  - Ignore and drop ALL question-type comments and posts in both top-level comments and replies. Examples to DROP:
    - "Can anyone give a detailed review for MLE CSE299 please?"
    - "Honest Faculty review please"
    - "How was AUQ for 323?" / "How was auq?"
    - "Question pattern ki?" / "Qus ki slidebased koren naki lecture notes based?"
    - "how much does sir curve?" / "details review please.."
    - "Bhai kew advice den" / "which section" / "same section"
  - Replies that only ask a follow-up question or request details without providing a verdict are **NOT reviews** and MUST be dropped.

### Course/faculty validation
- **MANDATORY COURSE CODE INCLUSION RULE:** The post text (or its direct comment thread context) **MUST explicitly contain the target course code** (e.g., `CSE434`, `CSE 434`, `CSE-434`, `CSE_434`). If a post/thread does NOT explicitly mention the target course code, skip and drop it completely to prevent cross-course leakage.
- **ALL FACULTY INCLUSION RULE:** Include **ALL faculty members** related to, mentioned in, or reviewed for the target course code.
- Do not restrict extraction to static reference lists. Automatically discover and include all faculty members mentioned by students in posts/threads belonging to that course.
- Validate faculty codes against full NSU faculty databases when available, but preserve any newly discovered faculty who teach or are reviewed for that course.

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
- Read each comment as a human evaluator: evaluate the exact human intent.
- Under "Best faculty for CSE115?", a reply of "Nva" is a recommendation. Under "Faculty NvA CSE115 review plz", a reply of "Drop" is a negative review of NVA.
- A reply tagging a name and then giving an opinion ("Tousif … A+ o paite paren") keeps its original text, name included. Judge the opinion.
- Watch for **sarcasm and negative outcomes**, e.g. "khub valo ki r bolbo… eto valo je just valo bolleo kom hoye jabe", "Koren vai Msk1.. be ready for insult" (means avoid), or praising a project initially but ending up giving a C grade (means avoid).
- Skip comments about a *different* faculty or course in the same thread, like a lab instructor, MAT120 faculty in a CSE215 post, or a CSE225 experience in a CSE215 thread.

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
- **All Question-Type Comments:** Any comment or post asking for reviews, advice, questions about exam pattern, slide dependence, grading curve questions, or course inquiries.
- **Noise / Logistics:** Name tags alone, `.`, `F`, `up`, `bump`, `BUMP`, `cfbr`, thank-yous, `#followers`, "same section", section exchange, course exchange, partner search ("Looking for a CSE299 Project Mate!!", "Interested"), bare schedule lists, jokes, social chatter ("pabi na", "AIUB secret agent", "Hat-trick hoye gelo", "Double Dekhi", "Doomed", "why :')"), and comments reviewing a faculty not in the reference list.

### Keep
- **Clear Statements Only:** Keep ONLY comments that contain a clear statement, judgment, or experience regarding the faculty (teaching quality, slide quality, grading, curving, question difficulty, behavior, experience, recommendation, or warning).
- Short verdicts under a recommendation post (e.g., "MHIS is good", "drop MHIS") must be kept if they express a clear statement/recommendation.

### Review count rule
- **Target minimum:** Keep scraping until *each* faculty has at least 10 meaningful reviews. If you reach posts from 2020 (estimate post age via comment timestamps like "4 years ago" or "5 years ago") OR see "End of results" on screen before reaching 2020, stop there even if 10 reviews were not found for a faculty.
- **Quality over quantity:** If a faculty gets 20+ reviews, keep only comparatively long reviews with a proper statement, opinion, or suggestion.
- **Max cap:** A single faculty will have 20 reviews max in the final output.
- Omit faculty with zero kept reviews.

### Rating scale (one rating per review)
| Rating | Use when |
|---|---|
| `Outstanding` | Superlative glowing praise with detailed positive experience: "best best best", "GOAT", "11/10", "got A even with a bad mid", "best for learning AND grading". |
| `great` | Clearly positive recommendation: "X best", "go for X", "valo", "very good teacher, regular updates", positive with minor caveats. |
| `normal` | Mixed or neutral statement: "average learning, good grading", "fair grading, no curve", humble/helpful teacher with average grade, casual praise with course uncertainty ("goated, not sure about 299"). |
| `harsh` | Tough / strict / warning: slide reader, unorganized slides, gets angry when students struggle, hard questions, stressful, heavy-pressure warnings. |
| `avoid` | Explicit warning: "nah. onek kharap", gets angry when asked questions, praised project initially but gave C grade, "Drop", "avoid", "worst", "save your money", clearly sarcastic praise. |

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
