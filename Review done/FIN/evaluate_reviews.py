import json
import re

def is_non_review(text):
    text_lower = text.lower().strip()
    words = text_lower.split()
    if len(words) <= 3 and not any(w in text_lower for w in ['best', 'good', 'bad', 'worst', 'avoid', 'drop', 'gem', 'joss', 'valo', 'bhalo']):
        return True
    if '?' in text or 'how was' in text_lower or 'kemon' in text_lower or 'kmn' in text_lower:
        if 'but' not in text_lower and 'however' not in text_lower: # basic check for just question
            return True
    if 'review chai' in text_lower or 'review lage' in text_lower or 'share your experience' in text_lower:
        return True
    if text_lower in ['mzf', 'tnk', 'tnk sir', 'mzf ne', 'mbsr', 'srs2', 'rar', 'ayn']:
        return True
    if 'anyone better than' in text_lower:
        return True
    return False

def evaluate_sentiment(text, faculty):
    text_lower = text.lower()
    
    # Specific edge cases
    if 'avoid' in text_lower and faculty.lower() in text_lower:
        return 'avoid'
    if 'drop' in text_lower and faculty.lower() in text_lower:
        return 'avoid'
        
    outstanding_words = ['outstanding', 'best', 'gem', 'joss', 'goat', 'boss', 'queen', 'highest regards', 'remarkable']
    great_words = ['great', 'good', 'sweet', 'helpful', 'friendly', 'fair', 'cool']
    harsh_words = ['harsh', 'worst', 'bad', 'baje', 'foul', 'dumb', 'biased', 'waste', 'regret', 'trauma', 'unprofessional', 'arrogant', 'rude']
    avoid_words = ['avoid', 'drop', 'hate', 'sh*it', 'shit', 'fokir']

    out_score = sum(1 for w in outstanding_words if w in text_lower)
    great_score = sum(1 for w in great_words if w in text_lower)
    harsh_score = sum(1 for w in harsh_words if w in text_lower)
    avoid_score = sum(1 for w in avoid_words if w in text_lower)
    
    if 'not good' in text_lower or 'bhalo na' in text_lower or 'valo na' in text_lower:
        harsh_score += 2
        great_score = 0
    if 'avg' in text_lower or 'average' in text_lower:
        return 'normal'
        
    if avoid_score > 0 or 'waste of energy' in text_lower:
        return 'avoid'
    if harsh_score > 0:
        return 'harsh'
    if out_score > 0:
        return 'Outstanding'
    if great_score > 0:
        return 'great'
        
    return 'normal'


def main():
    input_file = r"c:\Users\Foysal\OneDrive\Desktop\course_and_faculty_reviews\finance\fin444_llm_candidates.json"
    output_file = r"c:\Users\Foysal\OneDrive\Desktop\course_and_faculty_reviews\finance\fin444_detailed_reviews.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    result = {"fin444": {}}
    
    for item in data:
        text = item.get('text', '')
        faculties = item.get('faculties', [])
        
        if is_non_review(text):
            continue
            
        for faculty in faculties:
            fac_lower = faculty.lower()
            if fac_lower not in result["fin444"]:
                result["fin444"][fac_lower] = []
                
            # deduplicate
            is_dup = False
            for existing in result["fin444"][fac_lower]:
                if existing['review'] == text:
                    is_dup = True
                    break
            
            if is_dup:
                continue
                
            if len(result["fin444"][fac_lower]) >= 20:
                continue
                
            rating = evaluate_sentiment(text, faculty)
            
            # hardcode some manual overrides for holistic semantic meaning
            if "The audacity he have for nothing" in text: rating = 'avoid'
            if "You can do well if you listen to and record his lectures" in text: rating = 'great'
            if "MZF doesn't teach a single math in FIN444" in text: rating = 'harsh'
            if "doesn’t mean you’ll get one too. It totally depends on your luck. Btw Mzf is good" in text: rating = 'great'
            if "Attend all his classes and take notes" in text: rating = 'great'
            if "SAI2 onk easygoing but jodi apnar target" in text: rating = 'normal'
            if "Unar course e A,A- pawa shobche easy" in text: rating = 'Outstanding'
            if "Srs2 is quite strict, rude and will give some unnecessary para" in text: rating = 'harsh'
            if "Srs2 onk khatabe. Traumar moddhe rakhbe but at the end of the day onkkk curve korbe" in text: rating = 'normal'
            if "Cls nibe only 20-30min..7-8 ta cls cancel korbe" in text: rating = 'avoid'
            if "bhai onek baje . Try to avoid" in text: rating = 'avoid'
            if "SRS2 will humiliate you" in text: rating = 'harsh'
            if "Hhq1 is good for learning but grade unexpected diye dey" in text: rating = 'normal'
            if "Srs2 bhalo korte chaile u just have to get questions from other sections" in text: rating = 'normal'
            if "Mbsr er course e you will hardly get a B+" in text: rating = 'harsh'
            if "Rar and srs2 combo ate up my cg" in text: rating = 'harsh'
            if "He makes the course unnecessarily harder" in text: rating = 'harsh'
            if "Zkh1 onk easy going sobay average b b+ pabei" in text: rating = 'great'
            if "Zkh1 best and SQT fair grading good teacher" in text: rating = 'Outstanding'
            
            result["fin444"][fac_lower].append({
                "review": text,
                "rating": rating
            })
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
