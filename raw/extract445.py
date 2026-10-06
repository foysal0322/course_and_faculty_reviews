import json, re

FAC = ["jsa", "maqm", "msrb", "rtk", "sfm1", "sfr1"]
pat = re.compile(r"\b(" + "|".join(FAC) + r")\b", re.I)
c_pat = re.compile(r"\bcse[-_\s]?445\b", re.I)

posts = json.load(open("raw/q_cse445.json", encoding="utf-8"))

out = []
for i, p in enumerate(posts):
    ptext = p.get("text", "").strip()
    comments = p.get("comments", [])
    ctexts = [c.get("text", "").strip() for c in comments if c.get("text", "").strip()]
    full_thread = ptext + " " + " ".join(ctexts)

    if not c_pat.search(full_thread) and not pat.search(full_thread):
        continue

    out.append(f"=== #{i} POST ({len(comments)} comments) ===")
    out.append(ptext.replace("\n", " / "))
    for c in comments:
        t = c.get("text", "").strip()
        if t:
            out.append("   - " + t.replace("\n", " / "))
    out.append("")

open("raw/candidates445.txt", "w", encoding="utf-8").write("\n".join(out))
print(f"Wrote {len(out)} lines from {len(posts)} posts to raw/candidates445.txt")
