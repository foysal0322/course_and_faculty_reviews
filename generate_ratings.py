import json
import re
from collections import Counter

with open('final_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ratings keywords
keywords = {
    "Outstanding": ["outstanding", "excellent", "best", "goat", "amazing", "10/10", "brilliant", "perfect", "highly recommend", "sheraaaa", "shera"],
    "great": ["great", "good", "nice", "friendly", "helpful", "chill", "easy", "cool", "better", "awesome", "lenient", "vlo", "valo", "bhalo"],
    "normal": ["normal", "average", "okay", "fine", "moderate", "fair", "not bad", "decent", "thik", "motamuti"],
    "harsh": ["strict", "hard", "harsh", "tough", "bad", "terrible", "worst", "rude", "low grade", "para", "pain", "hard marker", "fokkinni", "faltu"],
    "avoid": ["avoid", "drop", "don't take", "run", "never", "skip", "do not take", "bdc"]
}

def analyze_sentiment(text):
    text_lower = text.lower()
    scores = {k: 0 for k in keywords}
    
    # Check for direct grades (like "- A", "- A-", "-> A")
    if re.search(r'[-=:]\s*A\b', text, re.IGNORECASE) or re.search(r'[-=:]\s*A-', text, re.IGNORECASE):
        return "Outstanding"
    if re.search(r'[-=:]\s*B\b', text, re.IGNORECASE) or re.search(r'[-=:]\s*B-', text, re.IGNORECASE):
        return "great"
    if re.search(r'[-=:]\s*C\b', text, re.IGNORECASE) or re.search(r'[-=:]\s*D\b', text, re.IGNORECASE) or re.search(r'[-=:]\s*F\b', text, re.IGNORECASE):
        return "harsh"

    for rating, words in keywords.items():
        for w in words:
            if re.search(r'\b' + re.escape(w) + r'\b', text_lower):
                scores[rating] += 1
                
    if scores["avoid"] > 0: return "avoid"
    if scores["Outstanding"] > 0 and scores["harsh"] == 0: return "Outstanding"
    if scores["harsh"] > scores["great"]: return "harsh"
    if scores["great"] > 0: return "great"
    
    return "normal"

def is_question_or_noise(text):
    t = text.lower()
    if '?' in t:
        return True
    if re.search(r'\b(how was|how is|how abt|how about|review plz|need review|can you share|can you give|give me review|anyone)\b', t):
        return True
    if len(t.split()) < 2:
        return True
    return False

faculty_data = {}

for post in data:
    text = post.get('extracted_text', '')
    if not text: continue
    
    matched = post.get('matched_cse115_faculties', [])
    # We only process MATCHED faculties now
    all_faculties = list(set(matched))
    
    lines = text.split('\n')
    
    for fac in all_faculties:
        fac_upper = fac.upper()
        if fac_upper not in faculty_data:
            faculty_data[fac_upper] = []
            
        for i, line in enumerate(lines):
            if re.search(rf'\b{fac_upper}\b', line, re.IGNORECASE):
                review_context = line
                if i + 1 < len(lines) and len(lines[i+1].split()) > 3:
                    review_context += " " + lines[i+1]
                
                review_context = review_context.strip()
                if not is_question_or_noise(review_context):
                    faculty_data[fac_upper].append(review_context)

final_output = {"cse115": {}}

for fac, reviews in faculty_data.items():
    if not reviews: continue
    
    unique_reviews = list(set(reviews))
    
    # Analyze each comment to find the overall rating
    ratings_tally = []
    judged_reviews = []
    
    for r in unique_reviews:
        sentiment = analyze_sentiment(r)
        ratings_tally.append(sentiment)
        judged_reviews.append(f"{r}")
        
    if not ratings_tally:
        continue
        
    # Get the most common sentiment
    counter = Counter(ratings_tally)
    final_rating = counter.most_common(1)[0][0]
    
    final_output["cse115"][fac.lower()] = {
        "rating": final_rating,
        "reviews": judged_reviews
    }

with open('cse115_ratings.json', 'w', encoding='utf-8') as f:
    json.dump(final_output, f, indent=4, ensure_ascii=False)

print("Generated cse115_ratings.json successfully with strict criteria!")
