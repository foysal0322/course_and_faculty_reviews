import json

posts = json.load(open("raw/q_cse225.json", encoding="utf-8"))
norm = lambda s: s.strip().replace("\n", " / ")
texts = []
for p in posts:
    texts.append(p["text"])
    texts.extend(c["text"] for c in p["comments"])

# (faculty, opening words of the post/comment, rating)
PICKS = [
    ("muo", "Muo sir best", "great"),
    ("muo", "Muo Easy going", "great"),
    ("muo", "Muo sir valo, slide gula valo vabe porle", "great"),
    ("muo", "225 - Muo(easygoing and curves", "Outstanding"),
    ("muo", "In terms of learning and fair grading: MUO", "Outstanding"),
    
    ("iqn", "IQN bhalo naa", "avoid"),
    ("iqn", "Don't take iqn if you don't wanna", "avoid"),
    ("iqn", "IQN er kache korar theke", "avoid"),
    ("iqn", "Worst ever. Drop den", "avoid"),
    ("iqn", "IQN bade shob valo", "avoid"),
    ("iqn", "Avoid iqn!", "avoid"),
    
    ("rih", "225 - RIH / 250", "great"),
    ("rih", "Sir theoretical qsthn korbe", "normal"),
    
    ("rjp", "225: RJP / 250: MLA", "great"),
    ("rjp", "RJP teaches well and grading is fair.", "Outstanding"),
    ("rjp", "RJP", "great"),
]

out, missing = {}, []
for fac, prefix, rating in PICKS:
    exact = [t for t in texts if norm(t) == prefix]
    hit = exact[0] if exact else next((t for t in texts if norm(t).startswith(prefix)), None)
    if hit is None:
        missing.append((fac, prefix))
        continue
    lst = out.setdefault(fac, [])
    if all(r["review"] != hit.strip() for r in lst):
        lst.append({"review": hit.strip(), "rating": rating})

for fac, lst in out.items():
    if len(lst) > 10:
        out[fac] = [r for r in lst if len(r["review"].split()) > 3]

json.dump({"cse225": out}, open("cse225_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("missing:", missing)
