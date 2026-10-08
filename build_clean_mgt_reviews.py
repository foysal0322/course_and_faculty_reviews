import glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REF_PATH = os.path.join(HERE, "course_faculty.json")
ref_data = json.load(open(REF_PATH, encoding="utf-8")) if os.path.exists(REF_PATH) else []

COURSE_REF_FACS = {}
ALL_KNOWN_FACS = set()

for entry in ref_data:
    for course, facs in entry.items():
        c = course.lower().replace("**", "")
        flist = [x.strip().lower() for x in facs.split(",") if x.strip()]
        COURSE_REF_FACS[c] = flist
        for f in flist:
            ALL_KNOWN_FACS.add(f)

# Expanded list of non-faculty words/pronouns to ignore
EXCLUDE_WORDS = {
    "and", "the", "for", "not", "but", "you", "are", "all", "one", "how", "sir", "lab", "mat", "eng",
    "cse", "phy", "his", "pol", "eco", "bus", "act", "fin", "mkt", "ben", "eee", "che", "bio", "law",
    "lol", "ok", "ask", "get", "can", "has", "had", "him", "her", "its", "who", "why", "any", "ami", "ki",
    "na", "ei", "oi", "ar", "tai", "apu", "vai", "bro", "mam", "yes", "now", "new", "old", "day", "mid",
    "too", "use", "gpa", "cgpa", "see", "try", "way", "off", "out", "let", "set", "bad", "best", "good",
    "easy", "hard", "f", "up", "bump", "cfbr", "tba", "tmi", "sei", "tae", "abt", "tmr", "kse", "cpa",
    "free", "test", "have", "take", "from", "some", "them", "each", "more", "done", "with", "open", "left",
    "want", "know", "do", "guys", "hey", "post", "mgt", "nsu", "book", "sale", "dept", "sale", "link",
    "page", "card", "luck", "sure", "need", "this", "that", "very", "last", "work", "only", "week", "year",
    "call", "many", "our", "fact", "asap", "days", "much", "isn", "down", "took", "ever", "mind", "just",
    "make", "late", "drop", "she", "pera", "also", "what", "does", "must", "did", "jodi", "uni", "amr",
    "unir", "moto", "shob", "your", "help", "meye", "pls", "buy", "sell", "taka", "bba", "hrm", "sec",
    "phi", "psy", "soc", "inb", "nibo", "dao", "den", "kore", "kora", "pore", "dibe", "dewa", "hobe",
    "bhai", "vaia", "kazi", "saba", "khan", "raj", "saha", "alam", "epic", "aman", "baki", "aage",
    "som", "red", "hand", "boss", "news", "idea", "form", "case", "over", "yet", "nice", "ends", "back",
    "huge", "pora", "amar", "khub", "baje", "ager", "din", "pura", "unar", "ekta", "ache", "tula", "aktu",
    "mind", "fit", "left", "kind", "rlly", "rare", "fond", "real", "asad", "kase", "krle", "chai", "amtr",
    "amio", "next", "peye", "neii", "both", "big", "ture", "bt", "ques", "ed", "eo", "pry", "most",
    "hie", "lmk", "plz", "dao", "iam", "ase", "red", "even", "then", "saw", "got", "due", "imo", "high",
    "pawa", "tho", "by", "mark", "newa", "math", "ment", "ent", "daw", "ageh", "kon", "chas", "two", "ba",
    "ek", "mids", "jay", "mcqs", "gets", "nai", "idk", "yeah", "ones", "jnno", "eto", "nh", "thik", "kono",
    "tell", "fair", "tbh", "know", "king", "give", "shit", "care", "plus", "boli", "omg", "dena", "paba",
    "rus", "khu", "tnk", "kar", "hdo", "maf", "nnm", "aba", "klm", "baki", "por", "cfb", "bum", "mof",
    "big", "sou", "shby", "dhur", "beta", "valo", "hoye", "jao", "anu", "pabo", "diye", "dei", "onk",
    "mki", "tas", "rzz", "jah", "kmn", "save", "hate", "dleo", "de", "frnd", "roja", "ged", "lage", "age",
    "sob", "bole", "seat", "quiz", "was", "jeta", "ta", "holo", "amr", "end", "hoi", "khp", "mone", "etto",
    "seta", "row", "te", "amr1", "hme", "he", "onek", "did", "amr"
}

QUESTION_RE = re.compile(
    r"^\s*(honest\s+)?(faculty\s+)?review\s+please|\b(review\s+please|honest\s+review|advice\s+please|how\s+is|how\s+was|details\s+review|which\s+section|same\s+section)\b|\?",
    re.I
)

RATING_RULES = [
    ("Outstanding", re.compile(r"\b(goat|goated|best best|11/10|10/10|top tier|unmatched|shaccess|shaccessful)\b", re.I)),
    ("avoid", re.compile(r"\b(avoid|drop|worst|kharaap|kharap|save money|save yourself|bachai de|dure thako|do not take)\b", re.I)),
    ("harsh", re.compile(r"\b(tough|strict|hard|pera|pressure|angry|insult|no curve|strict grading)\b", re.I)),
    ("great", re.compile(r"\b(good|valo|bhalo|shera|joss|recommended|fair|curve|helpful|matir manush|great)\b", re.I)),
]

def get_rating(text):
    for rlabel, pat in RATING_RULES:
        if pat.search(text):
            return rlabel
    return "normal"

def is_valid_comment(text):
    if not text or len(text.strip()) < 2:
        return False
    if QUESTION_RE.search(text) and not re.search(r"\b(good|bad|best|avoid|drop|valo|bhalo|strict|tough|pera|helpful|great|shera|joss|goat)\b", text, re.I):
        return False
    if re.match(r"^(@\w+\s*)+$", text.strip()) or text.strip().upper() in {"F", "UP", "BUMP", "CFBR", "."}:
        return False
    return True

def extract_faculties_from_text(text, course_code):
    ref_facs = COURSE_REF_FACS.get(course_code.lower(), [])
    found = set()
    tokens = re.findall(r"\b[A-Za-z0-9]{2,5}\b", text)
    for tok in tokens:
        u = tok.lower()
        # Rule 1: Belongs to reference faculty list for this course
        if u in ref_facs:
            found.add(u)
        # Rule 2: Belongs to known NSU faculty codes and not in EXCLUDE_WORDS
        elif u in ALL_KNOWN_FACS and u not in EXCLUDE_WORDS and len(u) >= 3:
            found.add(u)
        # Rule 3: Formatted as explicit 3-4 letter uppercase/titlecase initial not in EXCLUDE_WORDS
        elif len(u) in (3, 4) and u not in EXCLUDE_WORDS and not u.isdigit():
            if tok.isupper() or (tok.istitle() and len(u) >= 3):
                found.add(u)
    return list(found)

target_courses = ['mgt210', 'mgt212', 'mgt314', 'mgt321', 'mgt330', 'mgt351', 'mgt360', 'mgt368', 'mgt410', 'mgt460', 'mgt470', 'mgt489', 'mgt490']

all_course_results = {}
per_faculty_summary = {}

for course in target_courses:
    files = glob.glob(f"raw/q_{course}.json") + glob.glob(f"q_{course}.json")
    posts = []
    for f in files:
        if os.path.exists(f):
            try:
                posts.extend(json.load(open(f, encoding="utf-8")))
            except Exception:
                pass
    
    fac_reviews = {}
    
    for p in posts:
        ptext = p.get("text", "")
        pfacs = extract_faculties_from_text(ptext, course)
        
        if is_valid_comment(ptext) and pfacs:
            r = get_rating(ptext)
            for f in pfacs:
                fac_reviews.setdefault(f, []).append({"review": ptext.strip(), "rating": r})
        
        for c in p.get("comments", []):
            ctxt = c.get("text", "")
            if not is_valid_comment(ctxt):
                continue
            cfacs = extract_faculties_from_text(ctxt, course) or pfacs
            if not cfacs:
                continue
            r = get_rating(ctxt)
            for f in cfacs:
                existing = [x["review"] for x in fac_reviews.get(f, [])]
                if ctxt.strip() not in existing:
                    fac_reviews.setdefault(f, []).append({"review": ctxt.strip(), "rating": r})
    
    final_map = {}
    for f, revs in fac_reviews.items():
        if revs:
            final_map[f] = revs[:20]
    
    output_filename = f"{course}_detailed_reviews.json"
    output_content = {course: final_map}
    
    with open(output_filename, "w", encoding="utf-8") as out_f:
        json.dump(output_content, out_f, indent=2, ensure_ascii=False)
    
    all_course_results[course] = final_map

print("BUILD_CLEAN_COMPLETE")
for c, fmap in all_course_results.items():
    print(f"\n================ {c.upper()} ================")
    if not fmap:
        print("  No kept reviews.")
    for f, revs in fmap.items():
        counts = {}
        for r in revs:
            counts[r["rating"]] = counts.get(r["rating"], 0) + 1
        print(f"  Faculty {f.upper()}: Total {len(revs)} reviews -> {counts}")
