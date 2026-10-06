import json
import re
import os

raw_path = "raw/q_cse413.json"
posts = json.load(open(raw_path, encoding='utf-8'))

# List of known/discovered faculty initials for CSE413 and general NSU CSE faculty
# (including IQR, MUA3, RMZ1, MDRK, PBH, RJP, RRN, RSY, RKZ, AUZ, etc.)

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
        if len(t) < 80:
            return True

    inquiry_phrases = [
        "honest faculty review please", "detailed review please", "detailed review needed",
        "need review", "review please", "review lgbe", "details bolen", "bhai kew advice den",
        "ki type project korle", "how much does sir curve", "how was", "question pattern ki",
        "slidebased koren naki", "please give suggestions", "if anyone has taken",
        "looking for a cse", "project mate", "same section", "which section"
    ]
    if any(p in t_lower for p in inquiry_phrases):
        return True

    return False

def is_noise_or_non_review(text, fac_code):
    t = text.strip()
    t_lower = t.lower()
    
    if len(t) == 0:
        return True
        
    if t in ['.', 'F', 'f', 'up', 'bump', 'BUMP', 'cfbr', 'thanks', 'thank you', '#followers', 'Interested']:
        return True
        
    chatter = [
        "pabi na", "secret agent", "hat-trick", "mara khaboo", "double dekhi", "doomed",
        "exchange", "routine", "lab conflict", "partner", "looking for a"
    ]
    if any(c in t_lower for c in chatter):
        return True

    cleaned = re.sub(r'@[A-Za-z0-9._\s]+', '', t).strip()
    words = [w for w in re.split(r'\s+', cleaned.lower()) if w]
    if len(words) == 0:
        return True
    if all(w in [fac_code.lower(), 'sir', 'maam', 'mam', 'vaia', 'bhaiya', 'bhai', 'bro', 'mama', 'vai'] for w in words):
        return True

    return False

def classify_rating(text):
    t_lower = text.lower()
    
    if any(k in t_lower for k in ["nah. onek kharap", "rege jay", "grade ashce c", "decurve", "save your money", "worst", "be ready for insult", "bekar"]):
        return "avoid"
    if "drop" in t_lower and not any(p in t_lower for p in ["no drop", "don't drop", "dont drop", "never drop"]):
        return "avoid"
        
    if any(k in t_lower for k in ["slide reading", "unorganized", "strict", "unpredictable", "tough", "hard", "pera", "stressful", "insult", "pressure"]):
        return "harsh"
        
    if any(k in t_lower for k in ["goat", "goated", "11/10", "10/10", "best best", "a+ e dibe", "highly recommended", "must to do", "100 100", "top tier"]):
        return "Outstanding"
    if "best for learning" in t_lower and "grading" in t_lower:
        return "Outstanding"
        
    if any(k in t_lower for k in ["best", "valo", "bhalo", "good", "easy going", "friendly", "helpful", "curved", "go for", "recommended"]):
        return "great"
        
    return "normal"

# Candidate faculty codes to look for in CSE413 data
POTENTIAL_FACS = ["iqr", "mua3", "rmz1", "mdrk", "pbh", "rjp", "rrn", "rsy", "rkz", "auz", "itn", "mle", "nlh", "sfr1"]

fac_reviews = {}
seen_texts = {}

for p in posts:
    ptext = p.get('text', '').strip()
    p_facs = [f for f in POTENTIAL_FACS if re.search(r'\b' + re.escape(f) + r'\b', ptext, re.I)]

    for c in p.get('comments', []):
        ctext = c.get('text', '').strip()
        if not ctext:
            continue

        c_facs = [f for f in POTENTIAL_FACS if re.search(r'\b' + re.escape(f) + r'\b', ctext, re.I)]
        target_facs = list(set(c_facs if c_facs else p_facs))

        if not target_facs:
            continue

        for fac in target_facs:
            if is_question_or_inquiry(ctext):
                continue
            if is_noise_or_non_review(ctext, fac):
                continue

            norm_txt = ctext.strip()
            fac_reviews.setdefault(fac, [])
            seen_texts.setdefault(fac, set())

            if norm_txt not in seen_texts[fac] and len(fac_reviews[fac]) < 20:
                seen_texts[fac].add(norm_txt)
                fac_reviews[fac].append({
                    "review": norm_txt,
                    "rating": classify_rating(norm_txt)
                })

final_output = {
    "cse413": {fac: revs for fac, revs in fac_reviews.items() if len(revs) > 0}
}

output_filename = "cse413_detailed_reviews.json"
with open(output_filename, "w", encoding="utf-8") as out_f:
    json.dump(final_output, out_f, ensure_ascii=False, indent=2)

print(f"Saved {output_filename}:")
for fac, revs in final_output["cse413"].items():
    print(f"  - {fac.upper()}: {len(revs)} reviews")
