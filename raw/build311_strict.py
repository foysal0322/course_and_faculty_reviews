import json, re

posts = json.load(open("raw/q_cse311.json", encoding="utf-8"))
FAC = ["fth", "nlh", "rih", "tns1"]

def judge_rating(text):
    t = text.lower()
    if any(k in t for k in ["goat", "11/10", "best best", "a+ e dibe", "highly recommended", "must to do", "100 100", "top tier"]):
        return "Outstanding"
    elif any(k in t for k in ["avoid", "drop", "worst"]):
        return "avoid"
    elif any(k in t for k in ["strict", "unpredictable", "tough", "insult", "mood bujha", "hard", "pera"]):
        return "harsh"
    elif any(k in t for k in ["normal", "average", "regular update", "deadline", "fair"]):
        return "normal"
    elif any(k in t for k in ["best", "valo", "bhalo", "good", "easy going", "friendly", "helpful", "curved", "go for"]):
        return "great"
    return "great"

def is_strict_review(text, post_text):
    t = text.strip()
    # Drop short non-verdict strings & name tags
    words = t.split()
    if len(words) < 3 and not re.search(r"\b(best|good|valo|bhalo|drop|avoid|worst|goat|pera|curve|king)\b", t, re.I):
        return False
    # Drop pure questions or requests
    if t.endswith("?") or re.search(r"\b(how to|how is|can you|give suggestions|review please|anyone\?|which one|kemon|kivabe|how do you|how was|drop some tips)\b", t, re.I):
        return False
    # Drop thank-yous
    if re.search(r"\b(thanks|thank you|dhonnobad|thx|tks)\b", t, re.I):
        return False
    # Drop section, logistics, and credit talk
    if re.search(r"\b(same section|credits|credit|sec\s*\d+|section|timing|exchange|normally i did)\b", t, re.I):
        return False
    # Drop bumps / tags
    if re.match(r"^(bump|cfbr|\.|up|interested|f|#followers|boink)$", t, re.I):
        return False
    
    # Must express a judgment, opinion, or recommendation on teaching/grading/faculty behavior
    if not re.search(r"\b(best|good|valo|bhalo|drop|avoid|worst|goat|pera|curve|king|easy|hard|strict|friendly|helpful|learning|grading|marks|mark|slide|lecture|exam|quiz|mid|final|pass|fail|a\+|a-|take|recommend|recommended)\b", t, re.I):
        return False

    return True

out = {}

for p in posts:
    ptxt = p["text"].strip()
    p_facs = [f for f in FAC if re.search(r"\b" + f + r"\b", ptxt, re.I)]
    
    for c in p["comments"]:
        ctxt = c["text"].strip()
        if not is_strict_review(ctxt, ptxt): continue
        c_facs = [f for f in FAC if re.search(r"\b" + f + r"\b", ctxt, re.I)]
        
        target_facs = c_facs if c_facs else p_facs
        for f in target_facs:
            lst = out.setdefault(f, [])
            if not any(r["review"] == ctxt for r in lst):
                rating = judge_rating(ctxt)
                lst.append({"review": ctxt, "rating": rating})

final_out = {}
for f, lst in out.items():
    if lst:
        final_out[f] = lst[:20]

json.dump({"cse311": final_out}, open("cse311_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("Regenerated cse311_detailed_reviews.json strictly!")
print("Review counts per faculty:")
for f, lst in final_out.items():
    print(f"  - {f}: {len(lst)} reviews")
