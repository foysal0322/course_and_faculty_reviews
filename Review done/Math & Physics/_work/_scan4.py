import re

f = r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\Math & Physics\_work\mat361_x1.txt"
raw = open(f, encoding="utf-8").read().split("\n")

posts = []
cur_post = None
cur_comment = None
for ln in raw:
    if ln.startswith("==X"):
        cur_post = {"i": int(re.match(r"==X(\d+)==", ln).group(1)), "head": ln, "comments": []}
        posts.append(cur_post)
        cur_comment = None
    elif ln.startswith("[x") and cur_post is not None:
        cur_comment = ln
        cur_post["comments"].append(ln)
    else:
        if cur_comment is not None and ln.strip() != "":
            cur_post["comments"][-1] = cur_post["comments"][-1] + "\n" + ln

known = ["ads1", "hhs", "isr", "mdrk", "mlm", "smht", "mmrh", "maim", "maln", "st", "anhs", "hmn", "ajm", "ppd"]

def has_token(s):
    ls = s.lower()
    for t in known:
        if re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", ls):
            return True
    return False

out = []
seen_comment_text = set()
for p in posts:
    if p["i"] in (9, 10):
        continue
    is361 = "361" in p["head"]
    if p["i"] == 8:
        out.append(p["head"] + "   [DUP x9,x10 omitted]")
        for c in p["comments"]:
            if has_token(c):
                out.append(c)
                out.append("   >>>")
        out.append("-" * 40)
    elif is361:
        out.append(p["head"])
        out.extend(p["comments"])
        out.append("-" * 40)
    else:
        rc = [c for c in p["comments"] if has_token(c)]
        if rc:
            out.append(p["head"])
            out.extend(rc)
            out.append("-" * 40)

txt = "\n\n".join(out)
open(r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\Math & Physics\_work\_dump_clean.txt", "w", encoding="utf-8").write(txt)
print("units:", len(out), "bytes:", len(txt.encode("utf-8")))
