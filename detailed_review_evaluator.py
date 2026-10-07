import json
import re
import os

# Load valid faculties from valid_faculties.json
with open('valid_faculties.json', encoding='utf-8') as f:
    ALL_VALID_FACULTIES = set(json.load(f))

# Define common words / stop words to NEVER count as faculty initials
EXCLUDE_WORDS = {
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
    'need', 'want', 'please', 'thanks', 'thank', 'group', 'post', 'sell', 'buy', 'tutor', 'lab', 'class'
}

VALID_FACULTY_CODES = ALL_VALID_FACULTIES - EXCLUDE_WORDS

def is_question_or_inquiry(text):
    t_lower = text.lower().strip()
    
    # Check for direct question marks with question intent
    if '?' in text:
        q_triggers = [
            "kemon", "bhalo", "valo", "kivabe", "kmne", "naki", "kon", "ke", "koto",
            "can anyone", "anyone", "details", "which", "how is", "how was", "is ", "are ", "who", "please",
            "suggest", "option", "bhai", "vai", "section", "ki ", "ki?", "kore?", "review?", "faculty?",
            "how to do well", "any idea", "opinion", "thought", "kaene"
        ]
        if any(w in t_lower for w in q_triggers):
            return True
        if len(t_lower) < 90:
            return True

    # General inquiry patterns
    inquiry_phrases = [
        "honest faculty review please", "detailed review please", "detailed review needed",
        "need review", "review please", "review lgbe", "details bolen", "bhai kew advice den",
        "ki type project korle", "how much does sir curve", "how was", "question pattern ki",
        "slidebased koren naki", "please give suggestions", "if anyone has taken",
        "looking for a cse", "looking for group", "project mate", "same section", "which section",
        "need tutor", "tutor needed", "looking for group mate", "seat available", "lab conflict",
        "routine conflict", "exchange section", "swap section"
    ]
    if any(p in t_lower for p in inquiry_phrases):
        return True

    return False

def is_noise_or_non_review(text, fac_code):
    t = text.strip()
    t_lower = t.lower()
    
    if len(t) < 5:
        return True
        
    if t_lower in ['.', 'f', 'up', 'bump', 'cfbr', 'thanks', 'thank you', '#followers', 'interested', 'following']:
        return True
        
    chatter = [
        "pabi na", "secret agent", "hat-trick", "mara khaboo", "double dekhi", "doomed",
        "exchange", "routine", "lab conflict", "partner", "looking for a", "sell post", "buy post"
    ]
    if any(c in t_lower for c in chatter):
        return True

    # Check if text is just a tag/mention of faculty or name
    cleaned = re.sub(r'@[A-Za-z0-9._\s]+', '', t).strip()
    words = [w for w in re.split(r'\s+', cleaned.lower()) if w]
    if len(words) == 0:
        return True
    if all(w in [fac_code.lower(), 'sir', 'maam', 'mam', 'vaia', 'bhaiya', 'bhai', 'bro', 'mama', 'vai'] for w in words):
        return True

    return False

def classify_sentiment(text, fac_code):
    """
    Perform holistic semantic sentiment analysis for a specific faculty member mentioned in the review.
    5 categories:
    - 'Outstanding': Top tier praise, glowing reviews, goated teacher, highly recommended.
    - 'great': Positive recommendation, good teaching, fair/generous curves or grading, student advice on succeeding under a solid faculty.
    - 'normal': Neutral, balanced, factual description of course structure, exams, slides, or attendance.
    - 'harsh': Extremely strict, unaccommodating, heavy pressure with poor teaching support, or frustrating course atmosphere.
    - 'avoid': Student strongly warns others against taking the faculty, expresses deep dissatisfaction, or experienced unfair outcomes.
    """
    t_lower = text.lower()
    
    # Check for 'avoid' sentiment indicators
    avoid_indicators = [
        "avoid", "don't take", "dont take", "never take", "worst", "bekar", "rege jay", 
        "insulting", "save your money", "save your cgpa", "ruined my grade", "dropped", 
        "drop krsi", "drop korsilam", "failing", "unfriendly", "bad experience", "terrible", "horrible"
    ]
    # Check for 'Outstanding' indicators
    outstanding_indicators = [
        "goat", "goated", "10/10", "11/10", "100/100", "top tier", "best teacher", 
        "best faculty", "gem of nsu", "highly recommended", "must take", "a+ guaranteed", 
        "awesome teacher", "legend", "one of the best"
    ]
    # Check for 'harsh' indicators
    harsh_indicators = [
        "strict", "hard grader", "harsh grading", "heavy pressure", "pera", "stressful", 
        "unaccommodating", "no curve", "decurve", "tough exam", "tough question", 
        "slide reader", "slide reading", "unpredictable", "strict attendance"
    ]
    # Check for 'great' indicators
    great_indicators = [
        "good", "great", "friendly", "helpful", "generous", "curved", "good curve", 
        "recommended", "easy going", "explains well", "fair grader", "nice faculty", 
        "take him", "take her", "good teaching", "helpful advice", "chilled"
    ]
    
    # Semantic scoring logic
    score_avoid = sum(1 for w in avoid_indicators if w in t_lower)
    score_outstanding = sum(1 for w in outstanding_indicators if w in t_lower)
    score_harsh = sum(1 for w in harsh_indicators if w in t_lower)
    score_great = sum(1 for w in great_indicators if w in t_lower)
    
    if score_avoid > 0 and score_avoid >= score_great and score_avoid >= score_outstanding:
        return "avoid"
    if score_outstanding > 0 and score_outstanding >= score_harsh:
        return "Outstanding"
    if score_harsh > 0 and score_harsh > score_great and score_harsh > score_outstanding:
        return "harsh"
    if score_great > 0 or ("good" in t_lower or "recommended" in t_lower or "help" in t_lower):
        return "great"
    if score_harsh > 0:
        return "harsh"
        
    return "normal"

def extract_faculty_codes_from_text(text, cand_facs):
    facs = set()
    # Check candidate tags first
    for f in cand_facs:
        fl = f.lower().strip()
        if fl in VALID_FACULTY_CODES:
            facs.add(fl)
            
    # Check text for valid 3-4 letter faculty codes
    words = re.findall(r'\b[a-zA-Z0-9]{3,4}\b', text)
    for w in words:
        wl = w.lower()
        if wl in VALID_FACULTY_CODES:
            facs.add(wl)
            
    return list(facs)

def process_course_candidates(course_code):
    cand_path = f"cse/{course_code}_llm_candidates.json"
    if not os.path.exists(cand_path):
        print(f"Warning: {cand_path} not found.")
        return {}

    with open(cand_path, encoding='utf-8') as f:
        candidates = json.load(f)

    fac_reviews = {}
    seen_texts = {}

    for cand in candidates:
        text = cand.get('text', '').strip()
        if not text:
            continue

        cand_facs = cand.get('faculties', [])
        mentioned_facs = extract_faculty_codes_from_text(text, cand_facs)

        if not mentioned_facs:
            continue

        for fac in mentioned_facs:
            if is_question_or_inquiry(text):
                continue
            if is_noise_or_non_review(text, fac):
                continue

            rating = classify_sentiment(text, fac)

            if fac not in fac_reviews:
                fac_reviews[fac] = []
                seen_texts[fac] = set()

            # Deduplicate identical text
            if text not in seen_texts[fac] and len(fac_reviews[fac]) < 20:
                seen_texts[fac].add(text)
                fac_reviews[fac].append({
                    "review": text,
                    "rating": rating
                })

    output_data = {
        course_code: fac_reviews
    }
    
    out_path = f"cse/{course_code}_llm_review.json"
    with open(out_path, "w", encoding="utf-8") as out_f:
        json.dump(output_data, out_f, ensure_ascii=False, indent=2)
        
    return output_data

if __name__ == '__main__':
    courses = ['cse417', 'cse401', 'cse418', 'cse426', 'cse473', 'cse422', 'cse485', 'cse486', 'cse433', 'cse414', 'cse419', 'cse467', 'cse468', 'cse470', 'cse446', 'cse447', 'cse448', 'cse449']
    summary = {}
    for c in courses:
        res = process_course_candidates(c)
        c_data = res.get(c, {})
        summary[c] = {fac: len(revs) for fac, revs in c_data.items()}
        print(f"{c}: {len(c_data)} faculties processed")
        for fac, revs in c_data.items():
            ratings = [r['rating'] for r in revs]
            print(f"  - {fac.upper()}: {len(revs)} reviews ({ratings})")
