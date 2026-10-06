import json, re

posts = json.load(open("raw/q_cse311.json", encoding="utf-8"))
FAC = ["fth", "nlh", "rih", "tns1"]

OTHER_FACS = ["rhu", "fkh", "saife", "haque", "shams", "kmm", "smah", "stq", "aud", "maqm", "png", "mft", "mth", "ara2", "sfm1", "afn1", "mas", "ait", "isr"]

data = json.load(open("cse311_detailed_reviews.json", encoding="utf-8"))
cse311_data = data["cse311"]

cleaned_cse311 = {}
for fac, revs in cse311_data.items():
    cleaned_revs = []
    for r in revs:
        txt = r["review"].strip()
        t = txt.lower()
        # Ensure length is substantial (>= 5 words)
        if len(txt.split()) < 5:
            continue
        # Ensure not reviewing other non-reference faculty
        if any(re.search(r"\b" + of + r"\b", t) for of in OTHER_FACS) and not any(re.search(r"\b" + ref + r"\b", t) for ref in [fac]):
            continue
        cleaned_revs.append(r)
    if cleaned_revs:
        cleaned_cse311[fac] = cleaned_revs

json.dump({"cse311": cleaned_cse311}, open("cse311_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("Filtered long, high-confidence reviews successfully!")
print("Final review counts per faculty:")
for f, lst in cleaned_cse311.items():
    print(f"  - {f.upper()}: {len(lst)} detailed reviews")
