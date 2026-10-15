import json
import re

def process_reviews(input_file, output_file1, output_file2):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Output structure
    output_data = {"fin254": {}}
    
    seen_reviews = set()
    
    def get_rating(text):
        t = text.lower()
        if any(w in t for w in ["worst", "avoid", "save money", "drop", "faltu", "bacho", "bad"]):
            return "avoid"
        if any(w in t for w in ["tough", "strict", "pera", "harsh", "slide reading", "strick", "bash", "pressure", "doesn't do fair", "doesnt do fair", "biased"]):
            return "harsh"
        if any(w in t for w in ["top tier", "goated", "11/10", "highly recommended", "best", "shera", "top-notch", "sweetheart"]):
            return "Outstanding"
        if any(w in t for w in ["friendly", "easy going", "good", "curved", "curve", "bonus", "helpful", "fair", "curves"]):
            return "great"
        return "normal"
        
    def is_question(text):
        t = text.lower()
        if "?" in t: return True
        if "how is" in t: return True
        if "how was" in t: return True
        if "review de" in t: return True
        if "review dao" in t: return True
        if "kmn chilo" in t: return True
        if "kemon chilo" in t: return True
        if "detail review" in t: return True
        if "could you share" in t: return True
        return False
        
    def is_junk(text):
        if len(text.strip().split()) <= 3 and not any(w in text.lower() for w in ["good", "bad", "best", "worst", "avoid", "drop", "pera", "goated", "shera"]):
            return True
        if len(text) < 10:
            return True
        return False
        
    for item in data:
        text = item.get("text", "").strip()
        faculties = item.get("faculties", [])
        
        if not text or not faculties:
            continue
            
        if is_question(text) or is_junk(text):
            continue
            
        if text in seen_reviews:
            continue
        seen_reviews.add(text)
        
        for fac in faculties:
            fac_lower = fac.lower()
            if fac_lower not in output_data["fin254"]:
                output_data["fin254"][fac_lower] = []
                
            relevant_text = text
            if len(output_data["fin254"][fac_lower]) < 20:
                output_data["fin254"][fac_lower].append({
                    "review": relevant_text,
                    "rating": get_rating(relevant_text)
                })
                
    counts = {}
    for fac, reviews in output_data["fin254"].items():
        counts[fac] = len(reviews)
        
    print(f"Processed {len(seen_reviews)} valid unique reviews.")
    print("Faculty counts:", counts)
    
    with open(output_file1, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    with open(output_file2, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
if __name__ == '__main__':
    input_file = r'c:\Users\Foysal\OneDrive\Desktop\course_and_faculty_reviews\finance\fin254_llm_candidates.json'
    out1 = r'c:\Users\Foysal\OneDrive\Desktop\course_and_faculty_reviews\finance\fin4254_detailed_reviews.json'
    out2 = r'c:\Users\Foysal\OneDrive\Desktop\course_and_faculty_reviews\finance\fin254_detailed_reviews.json'
    process_reviews(input_file, out1, out2)
