import json, re

posts = json.load(open("raw/q_cse311.json", encoding="utf-8"))
FAC = ["fth", "nlh", "rih", "tns1"]

# Non-reference faculty codes to filter out
OTHER_FACS = ["aud", "mle", "msrb", "muo", "afe", "oisd", "smsl", "sva", "maqm"]

data = json.load(open("cse311_detailed_reviews.json", encoding="utf-8"))
cse311_data = data["cse311"]

cleaned_cse311 = {}
for fac, revs in cse311_data.items():
    cleaned_revs = []
    for r in revs:
        txt = r["review"].strip()
        t = txt.lower()
        # Drop if comment specifically reviews another non-reference faculty
        if any(re.search(r"\b" + of + r"\b", t) for of in OTHER_FACS) and not any(re.search(r"\b" + ref + r"\b", t) for ref in [fac]):
            continue
        cleaned_revs.append(r)
    if cleaned_revs:
        cleaned_cse311[fac] = cleaned_revs

json.dump({"cse311": cleaned_cse311}, open("cse311_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("Cleaned non-reference faculty mentions!")
print("Final review counts:")
for f, lst in cleaned_cse311.items():
    print(f"  - {f.upper()}: {len(lst)} reviews")
