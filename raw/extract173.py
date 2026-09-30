import json, re

FAC = ["itn", "mle", "msk1", "msrb", "sle", "ssi", "sva", "tnf"]
pat = re.compile(r"\b(" + "|".join(FAC) + r")\b", re.I)
posts = json.load(open("raw/q_cse173.json", encoding="utf-8"))

out = []
for i, p in enumerate(posts):
    ptext = p["text"].replace("\n", " / ")
    post_hit = bool(pat.search(p["text"]))
    lines = []
    for c in p["comments"]:
        t = c["text"].strip()
        if not t:
            continue
        if pat.search(t) or post_hit:
            lines.append("   - " + t.replace("\n", " / ")[:400])
    if lines:
        out.append(f"#{i} POST: {ptext[:300]}")
        out.extend(lines)

open("raw/candidates173.txt", "w", encoding="utf-8").write("\n".join(out))
print(len(out))
