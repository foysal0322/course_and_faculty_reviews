import glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REF_PATH = os.path.join(HERE, "course_faculty.json")
ref_data = json.load(open(REF_PATH, encoding="utf-8")) if os.path.exists(REF_PATH) else []

# Load reference faculty initials if present
COURSE_FAC = {}
for entry in ref_data:
    for course, facs in entry.items():
        c = course.upper()
        for f in [x.strip().lower() for x in facs.split(",") if x.strip()]:
            COURSE_FAC.setdefault(c, set()).add(f)

# Common non-faculty initials / stop words to ignore
STOP_INITIALS = {
    "tmi", "sei", "tae", "has", "abt", "him", "tmr", "kse", "cpa", "gpa", "cgpa",
    "mid", "nsu", "cse", "mgt", "eco", "fin", "bus", "act", "mat", "eng", "phy",
    "che", "bio", "pol", "his", "law", "psy", "soc", "phi", "lab", "sir", "mam",
    "apu", "vai", "bro", "you", "are", "and", "the", "for", "not", "but", "all",
    "one", "how", "lol", "ok", "ask", "get", "can", "had", "her", "its", "who",
    "why", "any", "ami", "ki", "na", "ei", "oi", "ar", "tai", "yes", "now", "new",
    "old", "day", "see", "try", "way", "off", "out", "let", "set", "bad", "best",
    "good", "easy", "hard", "f", "up", "bump", "cfbr", "tba"
}

QUESTION_PAT = re.compile(
    r"\b(review|honest|advice|pattern|pattern ki|suggest|how is|how was|keval|kivabe|details review|which section|same section|kew|den|bhai|bro|please|plz)\b|\?",
    re.I
)

RATING_PATTERNS = [
    ("Outstanding", re.compile(r"\b(goat|goated|best best|11/10|10/10|top tier|unmatched|shaccess|shaccessful)\b", re.I)),
    ("avoid", re.compile(r"\b(avoid|drop|worst|kharaap|kharap|save money|save yourself|bachai de|dure thako|do not take)\b", re.I)),
    ("harsh", re.compile(r"\b(tough|strict|hard|pera|pressure|angry|insult|no curve|strict grading)\b", re.I)),
    ("great", re.compile(r"\b(good|valo|bhalo|shera|joss|recommended|fair|curve|helpful|matir manush|great)\b", re.I)),
]

def classify_sentiment(text):
    for rlabel, pat in RATING_PATTERNS:
        if pat.search(text):
            return rlabel
    return "normal"

def is_valid_review(text):
    if not text or len(text.strip()) < 3:
        return False
    # Drop question-type comments if they only ask without asserting an opinion
    if QUESTION_PAT.search(text) and not re.search(r"\b(good|bad|best|avoid|drop|valo|bhalo|strict|tough|pera|helpful|great|shera|joss|goat)\b", text, re.I):
        return False
    # Drop tag only / pure noise
    if re.match(r"^(@\w+\s*)+$", text.strip()) or text.strip().upper() in {"F", "UP", "BUMP", "CFBR", "."}:
        return False
    return True

def extract_faculty_codes(text):
    # Extract 2 to 4 letter uppercase or titlecase initials (e.g. MHIS, QTI, ASZ, SSA, etc.)
    tokens = re.findall(r"\b[A-Za-z]{2,4}\d?\b", text)
    found = []
    for t in tokens:
        u = t.lower()
        if u not in STOP_INITIALS and len(u) >= 2:
            if u not in found:
                found.append(u)
    return found

courses = ['mgt210', 'mgt212', 'mgt314', 'mgt321', 'mgt330', 'mgt351', 'mgt360', 'mgt368', 'mgt410', 'mgt460', 'mgt470', 'mgt489', 'mgt490']

summary_report = {}

for c_code in courses:
    files = glob.glob(f'raw/q_{c_code}.json') + glob.glob(f'q_{c_code}.json')
    posts = []
    for f in files:
        if os.path.exists(f):
            try:
                posts.extend(json.load(open(f, encoding='utf-8')))
            except Exception:
                pass
    
    course_reviews = {}
    
    for p in posts:
        post_txt = p.get("text", "")
        post_facs = extract_faculty_codes(post_txt)
        
        # Process post text itself if it contains a detailed review
        if is_valid_review(post_txt) and post_facs:
            for fac in post_facs:
                rating = classify_sentiment(post_txt)
                course_reviews.setdefault(fac, []).append({"review": post_txt.strip(), "rating": rating})
        
        # Process comments
        for comm in p.get("comments", []):
            ctxt = comm.get("text", "")
            if not is_valid_review(ctxt):
                continue
            cfacs = extract_faculty_codes(ctxt) or post_facs
            if not cfacs:
                continue
            
            rating = classify_sentiment(ctxt)
            for fac in cfacs:
                # Deduplicate identical review text per faculty
                existing = [x["review"] for x in course_reviews.get(fac, [])]
                if ctxt.strip() not in existing:
                    course_reviews.setdefault(fac, []).append({"review": ctxt.strip(), "rating": rating})
    
    # Cap reviews at 20 max per faculty
    final_fac_map = {}
    for fac, revs in course_reviews.items():
        if revs:
            final_fac_map[fac] = revs[:20]
    
    output_filename = f"{c_code}_detailed_reviews.json"
    result_structure = {c_code: final_fac_map}
    
    with open(output_filename, "w", encoding="utf-8") as f_out:
        json.dump(result_structure, f_out, indent=2, ensure_ascii=False)
    
    summary_report[c_code] = {fac: len(revs) for fac, revs in final_fac_map.items()}

print("PROCESSING_COMPLETE")
print(json.dumps(summary_report, indent=2))
