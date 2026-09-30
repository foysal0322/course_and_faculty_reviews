import json, re

FAC = ["hsm","mft","mhis","muo","rih","rrn","rjp","sfr1","sva"]
pat = re.compile(r"\b(" + "|".join(FAC) + r")\b", re.I)
posts = json.load(open("raw/q_cse215.json", encoding="utf-8"))

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

open("raw/candidates215.txt", "w", encoding="utf-8").write("\n".join(out))
print(len(out))
