import re, json

f = r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\Math & Physics\_work\mat361_x1.txt"
lines = open(f, encoding="utf-8").read().split("\n")
posts = []
cur = None
for ln in lines:
    if ln.startswith("==X"):
        cur = {"i": int(re.match(r"==X(\d+)==", ln).group(1)), "head": ln, "comments": []}
        posts.append(cur)
    elif ln.startswith("[x") and cur is not None:
        cur["comments"].append(ln)

known = ["ads1", "hhs", "isr", "mdrk", "mlm", "smht", "mmrh", "maim", "st"]

tokens = set(known)
print("TOKENS:", sorted(tokens))

def has_token(s):
    ls = s.lower()
    for t in tokens:
        if re.search(r"(?<![a-z])" + re.escape(t) + r"(?![a-z])", ls):
            return True
    return False

out = []
for p in posts:
    if p["i"] in (9, 10):
        continue
    is361 = "361" in p["head"]
    head_short = p["head"].split("|")[-1]
    relevant_comments = [c for c in p["comments"] if has_token(c)]
    if is361 and p["i"] not in (8, 9, 10):
        out.append(p["head"])
        out.extend(p["comments"])
        out.append("-" * 40)
    elif p["i"] == 8:
        out.append(p["head"] + "   [DUPLICATED x9,x10 omitted]")
        for c in relevant_comments:
            out.append(c)
        out.append("-" * 40)
    else:
        if relevant_comments or has_token(p["head"]):
            out.append(p["head"])
            for c in relevant_comments:
                out.append(c)
            out.append("-" * 40)

txt = "\n".join(out)
open(r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\Math & Physics\_work\_dump_clean.txt", "w", encoding="utf-8").write(txt)
print("clean lines:", len(out), "bytes:", len(txt.encode("utf-8")))
