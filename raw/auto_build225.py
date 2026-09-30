import json, re

posts = json.load(open("raw/q_cse225.json", encoding="utf-8"))
norm = lambda s: s.strip().replace("\n", " / ")
texts = []
for p in posts:
    texts.append(p["text"])
    texts.extend(c["text"] for c in p["comments"])

FAC = ["fth","iqn","mhis","muo","rih","rjp","shafiur"]
out = {f: [] for f in FAC}

def rate_comment(text):
    t = text.lower()
    if re.search(r'\b(worst|drop|avoid|retake|nightmare|money|astagfirullah|bhalo naa|baje)\b', t): return 'avoid'
    if re.search(r'\b(hard|stressful|strict|struggle|tough|pera)\b', t): return 'harsh'
    if re.search(r'\b(goat|outstanding|11/10|got a|sure a)\b', t): return 'Outstanding'
    if re.search(r'\b(best|valo|bhalo|great|good|joss|shera|recommend|easy|mashallah|boss)\b', t): return 'great'
    return 'normal'

def is_valid_review(t):
    words = t.split()
    if len(words) < 2: return False
    t_lower = t.lower()
    # skip questions
    if '?' in t or 'plz' in t_lower or 'please' in t_lower or 'kemon' in t_lower or 'kmn' in t_lower:
        if not re.search(r'\b(best|valo|good|drop|avoid|worst|joss)\b', t_lower):
            return False
    # skip single mentions
    if len(words) <= 3 and not any(re.search(r'\b(best|valo|good|drop|avoid|worst|joss)\b', t_lower) for _ in [1]):
        return False
    # skip typical not-review things
    if 'section' in t_lower and len(words) <= 5: return False
    return True

for fac in FAC:
    pat = re.compile(r"\b" + fac + r"\b", re.I)
    for t in texts:
        t_norm = norm(t)
        if pat.search(t_norm):
            if is_valid_review(t_norm):
                # Don't add duplicates
                if all(r["review"] != t_norm.strip() for r in out[fac]):
                    out[fac].append({"review": t_norm.strip(), "rating": rate_comment(t_norm)})

# Apply review count rule
for fac, lst in out.items():
    if len(lst) > 10:
        out[fac] = [r for r in lst if len(r["review"].split()) > 3]

# Remove empty faculties
out = {k: v for k, v in out.items() if v}

json.dump({"cse225": out}, open("cse225_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print({k: len(v) for k, v in out.items()})
