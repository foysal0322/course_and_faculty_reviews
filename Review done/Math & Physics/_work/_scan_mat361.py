import re, sys

f = r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\Math & Physics\_work\mat361_x1.txt"
lines = open(f, encoding="utf-8").read().split("\n")

posts = []  # (idx, headerline, [comment lines])
cur = None
for ln in lines:
    if ln.startswith("==X"):
        m = re.match(r"==X(\d+)==", ln)
        cur = {"i": int(m.group(1)), "head": ln, "comments": []}
        posts.append(cur)
    elif ln.startswith("[x") and cur is not None:
        cur["comments"].append(ln)

def header_has_361(p):
    return "361" in p["head"]

print("TOTAL POSTS:", len(posts))
print("POSTS WITH 361:", sum(1 for p in posts if header_has_361(p)))
print("=" * 80)
for p in posts:
    if header_has_361(p):
        print(p["head"])
        for c in p["comments"]:
            print(c)
        print("-" * 60)
