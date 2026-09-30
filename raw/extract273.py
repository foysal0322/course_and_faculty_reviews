import json, re

FAC = ["ara2","mhis","mmk1","smsl"]
pat = re.compile(r"\b(" + "|".join(FAC) + r")\b", re.I)
posts = json.load(open("raw/q_cse273.json", encoding="utf-8"))

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

open("raw/candidates273.txt", "w", encoding="utf-8").write("\n".join(out))
print("Candidate lines extracted:", len(out))
