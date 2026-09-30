import json, re

posts = json.load(open("raw/q_cse173.json", encoding="utf-8"))
norm = lambda s: s.strip().replace("\n", " / ")
texts = []
for p in posts:
    texts.append(p["text"])
    texts.extend(c["text"] for c in p["comments"])

FAC = ["itn","mle","msk1","msrb","sle","ssi","sva","tnf"]
out = {f: [] for f in FAC}

def rate_comment(text):
    t = text.lower()
    if re.search(r'\b(worst|drop|avoid|retake|nightmare|money|astagfirullah|bhalo naa|baje)\b', t): return 'avoid'
    if re.search(r'\b(hard|stressful|strict|struggle|tough|pera)\b', t): return 'harsh'
    if re.search(r'\b(goat|outstanding|11/10|got a|sure a)\b', t): return 'Outstanding'
    if re.search(r'\b(best|valo|bhalo|great|good|joss|shera|recommend|easy|mashallah|boss)\b', t): return 'great'
    return 'normal'

def is_valid_review(t):
    t_lower = t.lower()
    
    # Explicitly drop Exchange posts, bare schedule posts/lists, and pure questions/requests
    if 'exchange post' in t_lower or 'you get:' in t_lower or 'kindly provide your valuable review' in t_lower or 'how to get a/a-' in t_lower:
        return False
    
    # Drop pure section/schedule lists without any opinion word
    if re.search(r'\bcse\d{3}\s*[-.]', t_lower) and not re.search(r'\b(good|best|valo|bhalo|drop|avoid|worst|joss|pera|hard|easy|great|review)\b', t_lower):
        return False
        
    words = t.split()
    if len(words) < 2: return False

    # Allow short verdict/reviews like "MHIS is good", "drop MHIS", "MSK1 best"
    if len(words) <= 4 and re.search(r'\b(good|best|valo|bhalo|drop|avoid|worst|joss|shera)\b', t_lower):
        return True

    # Drop non-opinion questions
    if ('?' in t or 'plz' in t_lower or 'please' in t_lower or 'kemon' in t_lower or 'kmn' in t_lower) and not re.search(r'\b(best|valo|good|drop|avoid|worst|joss|bhalo)\b', t_lower):
        return False

    if 'section' in t_lower and len(words) <= 5 and not re.search(r'\b(good|best|valo|bhalo|drop|avoid|worst|joss)\b', t_lower):
        return False

    return True

for fac in FAC:
    pat = re.compile(r"\b" + fac + r"\b", re.I)
    for t in texts:
        t_norm = norm(t)
        if pat.search(t_norm):
            if is_valid_review(t_norm):
                if all(r["review"] != t_norm.strip() for r in out[fac]):
                    out[fac].append({"review": t_norm.strip(), "rating": rate_comment(t_norm)})

# Max cap rule: max 20 per faculty; if 20+, keep longer/detailed ones
for fac, lst in out.items():
    if len(lst) > 20:
        lst.sort(key=lambda r: len(r["review"]), reverse=True)
        out[fac] = lst[:20]

out = {k: v for k, v in out.items() if v}

json.dump({"cse173": out}, open("cse173_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print({k: len(v) for k, v in out.items()})
