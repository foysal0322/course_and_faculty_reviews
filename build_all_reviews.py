import json
import re
import os

with open('course_faculty.json', encoding='utf-8') as f:
    cf_data = json.load(f)

# Build set of ALL known NSU faculty codes from full course_faculty.json dataset
ALL_NSU_FACULTIES = set()
for item in cf_data:
    for c, fac_str in item.items():
        for code in fac_str.split(','):
            c_clean = code.strip().lower()
            if c_clean and c_clean != 'tba':
                ALL_NSU_FACULTIES.add(c_clean)

def course_pattern(course_code):
    # Matches e.g. cse434, cse 434, cse-434, cse_434
    dept = course_code[:3]
    num = course_code[3:]
    return re.compile(r'\b' + re.escape(dept) + r'[-_\s]?' + re.escape(num) + r'\b', re.I)

def discover_course_faculties(posts, course_code, static_ref_list):
    fac_set = set(static_ref_list)
    pat = course_pattern(course_code)
    
    # Only discover from posts/threads that mention the specific course
    for p in posts:
        ptext = p.get('text', '')
        ctexts = [c.get('text', '') for c in p.get('comments', [])]
        full_text = ptext + ' ' + ' '.join(ctexts)
        
        if pat.search(full_text):
            for m in re.findall(r'\b[A-Za-z0-9]{3,4}\b', full_text):
                code = m.lower()
                if code in ALL_NSU_FACULTIES:
                    fac_set.add(code)
                    
    return sorted(list(fac_set))

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

def process_course(course):
    raw_path = f"raw/q_{course}.json"
    if not os.path.exists(raw_path):
        print(f"Note: {raw_path} not found")
        return

    with open(raw_path, encoding='utf-8') as f:
        posts = json.load(f)

    c_pat = course_pattern(course)

    static_facs = []
    for item in cf_data:
        if course in item:
            static_facs.extend([x.strip().lower() for x in item[course].split(',') if x.strip() and x.strip().lower() != 'tba'])

    target_faculties = discover_course_faculties(posts, course, static_facs)
    
    fac_reviews = {f: [] for f in target_faculties}
    seen_texts = {f: set() for f in target_faculties}

    for p in posts:
        ptext = p.get('text', '').strip()
        comments = p.get('comments', [])
        ctexts = [c.get('text', '') for c in comments]
        full_thread = ptext + ' ' + ' '.join(ctexts)

        # STRICT COURSE CONTEXT REQUIREMENT: Thread/post MUST contain the course code!
        if not c_pat.search(full_thread):
            continue

        p_facs = [f for f in target_faculties if re.search(r'\b' + re.escape(f) + r'\b', ptext, re.I)]

        if p_facs and ("#facultyreview" in ptext.lower() or "review" in ptext.lower() or len(ptext) > 120):
            if not is_question_or_inquiry(ptext):
                for fac in p_facs:
                    if not is_noise_or_non_review(ptext, fac):
                        norm_txt = ptext.strip()
                        if norm_txt not in seen_texts[fac] and len(fac_reviews[fac]) < 20:
                            seen_texts[fac].add(norm_txt)
                            fac_reviews[fac].append({
                                "review": norm_txt,
                                "rating": classify_rating(norm_txt)
                            })

        for c in comments:
            ctext = c.get('text', '').strip()
            if not ctext:
                continue

            c_facs = [f for f in target_faculties if re.search(r'\b' + re.escape(f) + r'\b', ctext, re.I)]
            target_facs = list(set(c_facs if c_facs else p_facs))

            if not target_facs:
                continue

            for fac in target_facs:
                if is_question_or_inquiry(ctext):
                    continue
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
        course: {fac: revs for fac, revs in fac_reviews.items() if len(revs) > 0}
    }

    output_filename = f"{course}_detailed_reviews.json"
    with open(output_filename, "w", encoding="utf-8") as out_f:
        json.dump(final_output, out_f, ensure_ascii=False, indent=2)

    print(f"Saved {output_filename}: {len(final_output[course])} faculties with reviews")
    for fac, revs in final_output[course].items():
        print(f"  - {fac.upper()}: {len(revs)} reviews")

if __name__ == '__main__':
    all_courses = ['cse115', 'cse173', 'cse215', 'cse225', 'cse231', 'cse273', 'cse299', 'cse311', 'cse323', 'cse327', 'cse331', 'cse332', 'cse338', 'cse411', 'cse413', 'cse425', 'cse434']
    for c in all_courses:
        process_course(c)
