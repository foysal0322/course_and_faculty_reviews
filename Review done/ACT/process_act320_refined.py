import json, re

with open("course_faculty.json", encoding="utf-8") as f:
    cf_data = json.load(f)

ALL_NSU_FACULTIES = set()
for item in cf_data:
    for c, fac_str in item.items():
        for code in fac_str.split(","):
            c_clean = code.strip().lower()
            if c_clean and c_clean != "tba":
                ALL_NSU_FACULTIES.add(c_clean)

posts = json.load(open("accounting/q_act320.json", encoding="utf-8"))
c_pat = re.compile(r"\bact[-_\s]?320\b", re.I)

def is_question_or_inquiry(text):
    t = text.strip()
    t_lower = t.lower()
    if '?' in t:
        q_triggers = [
            "review", "kemon", "bhalo", "valo", "kivabe", "kmne", "naki", "kon", "ke", "koto",
            "can anyone", "anyone", "details", "which", "how", "is ", "are ", "who", "please",
            "suggest", "option", "bhai", "vai", "section", "ki ", "ki?", "kore?"
        ]
        if any(w in t_lower for w in q_triggers):
            return True
        if len(t) < 50:
            return True

    inquiry_phrases = [
        "honest faculty review please", "detailed review please", "detailed review needed",
        "need review", "review please", "review lgbe", "details bolen", "bhai kew advice den",
        "ki type project korle", "how much does sir curve", "how was", "question pattern ki",
        "slidebased koren naki", "please give suggestions", "if anyone has taken",
        "looking for a cse", "project mate", "same section", "which section", "seat pabona",
        "sorry", "post o tui disos", "eyy sem e kortesi", "nite parini"
    ]
    if any(p in t_lower for p in inquiry_phrases):
        return True
    return False

def is_noise_or_non_review(text, fac_code):
    t = text.strip()
    t_lower = t.lower()

    if len(t) == 0:
        return True

    if t in ['.', 'F', 'f', 'up', 'bump', 'BUMP', 'cfbr', 'thanks', 'thank you', '#followers', 'Interested', 'yes', 'no']:
        return True

    chatter = [
        "pabi na", "secret agent", "hat-trick", "mara khaboo", "double dekhi", "doomed",
        "exchange", "routine", "lab conflict", "partner", "looking for a", "seat pabona",
        "tui disos", "kortesi", "nite parini", "bondhu", "milad dibo"
    ]
    if any(c in t_lower for c in chatter):
        return True

    cleaned = re.sub(r'@[A-Za-z0-9._\s]+', '', t).strip()
    words = [w for w in re.split(r'\s+', cleaned.lower()) if w]
    if len(words) < 3 and not any(w in ['best', 'goat', 'good', 'valo', 'bhalo', 'drop', 'avoid', 'pera', 'strict', 'curved', 'shera', 'cutie'] for w in words):
        return True
    if all(w in [fac_code.lower(), 'sir', 'maam', 'mam', 'vaia', 'bhaiya', 'bhai', 'bro', 'mama', 'vai'] for w in words):
        return True

    return False

def classify_rating(text):
    t_lower = text.lower()
    if any(k in t_lower for k in ["nah. onek kharap", "rege jay", "save your money", "worst", "be ready for insult", "bekar"]):
        return "avoid"
    if "drop" in t_lower and not any(p in t_lower for p in ["no drop", "don't drop", "dont drop", "never drop"]):
        return "avoid"
    if any(k in t_lower for k in ["slide reading", "unorganized", "strict", "tough", "hard", "pera", "stressful", "insult", "pressure"]):
        return "harsh"
    if any(k in t_lower for k in ["goat", "goated", "11/10", "10/10", "best best", "a+ e dibe", "highly recommended", "top tier"]):
        return "Outstanding"
    if any(k in t_lower for k in ["best", "valo", "bhalo", "good", "easy going", "friendly", "helpful", "curved", "go for", "recommended", "shera", "cutie"]):
        return "great"
    return "normal"

act320_facs = set()
for p in posts:
    ptext = p.get("text", "")
    ctexts = [c.get("text", "") for c in p.get("comments", [])]
    full_thread = ptext + " " + " ".join(ctexts)
    if c_pat.search(full_thread):
        for m in re.findall(r'\b[A-Za-z0-9]{3,4}\b', full_thread):
            code = m.lower()
            if code in ALL_NSU_FACULTIES:
                act320_facs.add(code)

TARGET_FACS = sorted(list(act320_facs))
fac_reviews = {f: [] for f in TARGET_FACS}
seen_texts = {f: set() for f in TARGET_FACS}

for p in posts:
    ptext = p.get("text", "").strip()
    comments = p.get("comments", [])
    ctexts = [c.get("text", "").strip() for c in comments]
    full_thread = ptext + " " + " ".join(ctexts)

    if not c_pat.search(full_thread):
        continue

    for c in comments:
        ctext = c.get("text", "").strip()
        if not ctext or is_question_or_inquiry(ctext):
            continue

        c_facs = [f for f in TARGET_FACS if re.search(r'\b' + re.escape(f) + r'\b', ctext, re.I)]

        for fac in c_facs:
            if is_noise_or_non_review(ctext, fac):
                continue
            norm_txt = ctext.strip()
            if norm_txt not in seen_texts[fac] and len(fac_reviews[fac]) < 20:
                seen_texts[fac].add(norm_txt)
                fac_reviews[fac].append({
                    "review": norm_txt,
                    "rating": classify_rating(norm_txt)
                })

final_output = {
    "act320": {fac: revs for fac, revs in fac_reviews.items() if len(revs) > 0}
}

with open("accounting/act320_detailed_reviews.json", "w", encoding="utf-8") as out_f:
    json.dump(final_output, out_f, ensure_ascii=False, indent=2)

print("--- ACT320 Final Output ---")
for fac, revs in final_output["act320"].items():
    ratings = [r['rating'] for r in revs]
    rating_counts = dict((r, ratings.count(r)) for r in set(ratings))
    print(f"{fac.upper()}: {len(revs)} reviews -> {rating_counts}")
