import json
import re
import os

# Load valid faculty codes
with open('valid_faculties.json', encoding='utf-8') as f:
    ALL_VALID = set(json.load(f))

# General words / pronouns / common terms to EXCLUDE as faculty codes
EXCLUDE_FACS = {
    'for', 'cse', 'not', 'you', 'him', 'her', 'his', 'and', 'are', 'can', 'get', 'has', 'how', 'new', 
    'now', 'old', 'one', 'out', 'see', 'the', 'too', 'two', 'was', 'who', 'our', 'way', 'all', 'any', 
    'ask', 'boy', 'bad', 'big', 'buy', 'day', 'did', 'dry', 'due', 'end', 'far', 'fly', 'fun', 'god', 
    'got', 'guy', 'hit', 'hot', 'job', 'key', 'kid', 'let', 'low', 'man', 'max', 'may', 'mid', 'mix', 
    'net', 'off', 'pay', 'per', 'put', 'red', 'run', 'say', 'set', 'sir', 'sit', 'top', 'try', 'use', 
    'win', 'yes', 'yet', 'bhai', 'bro', 'vai', 'mam', 'maam', 'more', 'open', 'side', 'form', 'past', 
    'your', 'able', 'ache', 'add', 'also', 'am', 'an', 'apu', 'as', 'at', 'be', 'been', 'by', 'dept', 
    'do', 'er', 'hope', 'both', 'cgpa', 'core', 'dm', 'ece', 'file', 'case', 'blue', 'alam', 'antu', 
    'bash', 'bcoz', 'dia', 'dibe', 'ar', 'adib', 'afia', 'agar', 'age', 'ai', 'aibr', 'akhn', 'aktu', 
    'al', 'ain', 'azk', 'aage', 'abar', 'abir', 'abr', 'abt', 'abu', 'ace', 'acha', 'aht', 'ads', 
    'akib', 'ami', 'apni', 'auq', 'pick', 'list', 'two', 'meet', 'them', 'seen', 'join', 'last', 'one', 
    'good', 'well', 'best', 'hard', 'take', 'took', 'give', 'from', 'with', 'that', 'this', 'have', 
    'what', 'some', 'they', 'time', 'like', 'just', 'only', 'very', 'even', 'much', 'know', 'make', 
    'will', 'would', 'could', 'should', 'here', 'there', 'what', 'when', 'where', 'why', 'which', 
    'than', 'then', 'them', 'these', 'those', 'also', 'over', 'into', 'such', 'some', 'same', 'help', 
    'need', 'want', 'please', 'thanks', 'thank', 'group', 'post', 'sell', 'buy', 'tutor', 'lab', 'class',
    'section', 'exchange', 'swap', 'trail', 'track', 'routine', 'credit', 'sem', 'semester', 'grade'
}

VALID_FACULTY_CODES = ALL_VALID - EXCLUDE_FACS

def is_non_review_or_question(text):
    t_lower = text.lower().strip()
    
    # 1. Section Exchange / Seat Swap / Partner / Tutor / Sell / Buy posts
    exchange_keywords = [
        "section exchange", "exchange section", "swap section", "section swap", "you get", "you will get",
        "looking for group", "project mate", "group mate", "need tutor", "tutor needed", "sell post", 
        "buy post", "seat available", "lab conflict", "routine conflict", "seat exchange"
    ]
    if any(k in t_lower for k in exchange_keywords):
        return True

    # 2. Questions / Inquiries asking for reviews or advice
    if '?' in text:
        q_triggers = [
            "kemon", "bhalo", "valo", "kivabe", "kmne", "naki", "kon", "ke", "koto",
            "can anyone", "anyone", "details", "which", "how is", "how was", "is he", "is she", "who", "please",
            "suggest", "option", "bhai", "vai", "section", "ki ", "ki?", "kore?", "review?", "faculty?",
            "how to do well", "any idea", "opinion", "thought", "kaene", "kader section"
        ]
        if any(w in t_lower for w in q_triggers):
            return True
        if len(t_lower) < 100 and any(w in t_lower for w in ["how", "is", "suggest", "review", "details"]):
            return True

    inquiry_phrases = [
        "honest faculty review please", "detailed review please", "detailed review needed",
        "need review", "review please", "review lgbe", "details bolen", "bhai kew advice den",
        "ki type project korle", "how much does sir curve", "how was", "question pattern ki",
        "slidebased koren naki", "please give suggestions", "if anyone has taken",
        "looking for a cse", "which section", "recommendation please"
    ]
    if any(p in t_lower for p in inquiry_phrases):
        return True

    # 3. Noise / Bumps / Tag-only
    if len(t_lower) < 15:
        return True
    if t_lower in ['.', 'f', 'up', 'bump', 'cfbr', 'thanks', 'thank you', '#followers', 'interested', 'following']:
        return True

    return False

def evaluate_sentiment(text, fac_code):
    """
    Holistic sentiment determination for faculty review:
    - 'Outstanding': Top tier praise, glowing reviews, goated teacher, highly recommended.
    - 'great': Positive recommendation, good teaching, fair/generous curves or grading, student advice on succeeding under a solid faculty.
    - 'normal': Neutral, balanced, factual description of course structure, exams, slides, or attendance.
    - 'harsh': Extremely strict, unaccommodating, heavy pressure with poor teaching support, or frustrating course atmosphere.
    - 'avoid': Student strongly warns others against taking the faculty, expresses deep dissatisfaction, or experienced unfair outcomes.
    """
    t_lower = text.lower()
    
    # Avoid signals
    avoid_terms = [
        "avoid", "don't take", "dont take", "never take", "worst", "bekar", "rege jay", 
        "insult", "save your money", "save your cgpa", "ruined my grade", "dropped", 
        "drop krsi", "drop korsilam", "failing", "unfriendly", "bad experience", "terrible", "horrible",
        "f pabi", "f dibe", "f marbe"
    ]
    # Outstanding signals
    outstanding_terms = [
        "goat", "goated", "10/10", "11/10", "100/100", "top tier", "best teacher", 
        "best faculty", "gem of nsu", "highly recommended", "must take", "a+ guaranteed", 
        "awesome teacher", "legend", "one of the best", "best best", "10 out of 10"
    ]
    # Harsh signals
    harsh_terms = [
        "strict", "hard grader", "harsh grading", "heavy pressure", "pera", "stressful", 
        "unaccommodating", "no curve", "decurve", "tough exam", "tough question", 
        "slide reader", "slide reading", "unpredictable", "strict attendance", "marattok pera"
    ]
    # Great signals
    great_terms = [
        "good", "great", "friendly", "helpful", "generous", "curved", "good curve", 
        "recommended", "easy going", "explains well", "fair grader", "nice faculty", 
        "take him", "take her", "good teaching", "helpful advice", "chilled", "a+ paba",
        "easy a", "fair examiner", "cooperative"
    ]
    
    cnt_avoid = sum(1 for w in avoid_terms if w in t_lower)
    cnt_outstanding = sum(1 for w in outstanding_terms if w in t_lower)
    cnt_harsh = sum(1 for w in harsh_terms if w in t_lower)
    cnt_great = sum(1 for w in great_terms if w in t_lower)
    
    if cnt_avoid > 0 and cnt_avoid >= cnt_great and cnt_avoid >= cnt_outstanding:
        return "avoid"
    if cnt_outstanding > 0 and cnt_outstanding >= cnt_harsh:
        return "Outstanding"
    if cnt_harsh > 0 and cnt_harsh > cnt_great:
        return "harsh"
    if cnt_great > 0 or ("good" in t_lower or "recommended" in t_lower or "helpful" in t_lower or "take" in t_lower):
        return "great"
    if cnt_harsh > 0:
        return "harsh"
        
    return "normal"

def extract_valid_faculties(text, cand_facs):
    facs = set()
    for f in cand_facs:
        fl = f.lower().strip()
        if fl in VALID_FACULTY_CODES:
            facs.add(fl)
            
    # Search text for 3-4 uppercase/lowercase standalone code patterns
    words = re.findall(r'\b[a-zA-Z0-9]{3,4}\b', text)
    for w in words:
        wl = w.lower()
        if wl in VALID_FACULTY_CODES:
            facs.add(wl)
            
    return sorted(list(facs))

def process_all_courses():
    courses = [
        'cse417', 'cse401', 'cse418', 'cse426', 'cse473', 'cse422', 
        'cse485', 'cse486', 'cse433', 'cse414', 'cse419', 'cse467', 
        'cse468', 'cse470', 'cse446', 'cse447', 'cse448', 'cse449'
    ]
    
    total_summary = {}

    for c in courses:
        cand_path = f"cse/{c}_llm_candidates.json"
        if not os.path.exists(cand_path):
            continue

        with open(cand_path, encoding='utf-8') as f:
            candidates = json.load(f)

        fac_reviews = {}
        seen_texts = {}

        for cand in candidates:
            text = cand.get('text', '').strip()
            if not text:
                continue

            if is_non_review_or_question(text):
                continue

            target_facs = extract_valid_faculties(text, cand.get('faculties', []))
            if not target_facs:
                continue

            for fac in target_facs:
                rating = evaluate_sentiment(text, fac)

                if fac not in fac_reviews:
                    fac_reviews[fac] = []
                    seen_texts[fac] = set()

                if text not in seen_texts[fac] and len(fac_reviews[fac]) < 20:
                    seen_texts[fac].add(text)
                    fac_reviews[fac].append({
                        "review": text,
                        "rating": rating
                    })

        output_file = f"cse/{c}_llm_review.json"
        res_data = {c: fac_reviews}
        
        with open(output_file, "w", encoding="utf-8") as out_f:
            json.dump(res_data, out_f, ensure_ascii=False, indent=2)

        # Store stats
        stat_entry = {}
        for fac, revs in fac_reviews.items():
            dist = {}
            for r in revs:
                dist[r['rating']] = dist.get(r['rating'], 0) + 1
            stat_entry[fac] = {
                "total_reviews": len(revs),
                "rating_distribution": dist
            }
        total_summary[c] = stat_entry

    # Print final overview
    print("\n=======================================================")
    print("      HOLISTIC REVIEW EVALUATION SUMMARY FOR 18 CSE COURSES")
    print("=======================================================\n")
    for c, fac_map in total_summary.items():
        print(f"Course {c.upper()}: {len(fac_map)} faculties with valid reviews")
        for fac, info in fac_map.items():
            print(f"  - Faculty [{fac.upper()}]: {info['total_reviews']} reviews | Ratings: {info['rating_distribution']}")
        print()

if __name__ == '__main__':
    process_all_courses()
