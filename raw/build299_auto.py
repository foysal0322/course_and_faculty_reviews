import json, re

posts = json.load(open("raw/q_cse299.json", encoding="utf-8"))
FAC = ["afe", "itn", "mle", "msrb", "muo", "nlh", "oisd", "smsl", "sfr1", "tns1"]

# Automatic rule-based rating helper based on instruction guidelines
def judge_rating(text):
    t = text.lower()
    if any(k in t for k in ["goat", "11/10", "best best", "a+ e dibe", "highly recommended", "must to do", "100 100"]):
        return "Outstanding"
    elif any(k in t for k in ["avoid", "drop", "worst"]):
        return "avoid"
    elif any(k in t for k in ["strict", "unpredictable", "tough", "Insult", "mood bujha", "hard"]):
        return "harsh"
    elif any(k in t for k in ["normal", "average", "regular update", "deadline"]):
        return "normal"
    elif any(k in t for k in ["best", "valo", "bhalo", "good", "easy going", "friendly", "helpful", "curved", "go for"]):
        return "great"
    return "great"

def is_valid_review(text):
    t = text.strip()
    if len(t) < 4: return False
    if re.match(r"^(bump|cfbr|\.|up|interested|f|#followers|same section|boink)$", t, re.I): return False
    if t.lower().startswith("looking for") or t.lower().startswith("who is"): return False
    return True

out = {}

for p in posts:
    ptxt = p["text"].strip()
    p_facs = [f for f in FAC if re.search(r"\b" + f + r"\b", ptxt, re.I)]
    
    for c in p["comments"]:
        ctxt = c["text"].strip()
        if not is_valid_review(ctxt): continue
        c_facs = [f for f in FAC if re.search(r"\b" + f + r"\b", ctxt, re.I)]
        
        target_facs = c_facs if c_facs else p_facs
        for f in target_facs:
            lst = out.setdefault(f, [])
            if not any(r["review"] == ctxt for r in lst):
                rating = judge_rating(ctxt)
                lst.append({"review": ctxt, "rating": rating})

# Clean & cap per faculty
final_out = {}
for f, lst in out.items():
    if lst:
        final_out[f] = lst[:20]

json.dump({"cse299": final_out}, open("cse299_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("Generated cse299_detailed_reviews.json successfully!")
print("Review counts per faculty:")
for f, lst in final_out.items():
    print(f"  - {f}: {len(lst)} reviews")
