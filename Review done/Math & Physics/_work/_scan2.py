import re

f = r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\Math & Physics\_work\mat361_x1.txt"
lines = open(f, encoding="utf-8").read().split("\n")

posts = []
cur = None
for ln in lines:
    if ln.startswith("==X"):
        m = re.match(r"==X(\d+)==", ln)
        cur = {"i": int(m.group(1)), "head": ln, "comments": []}
        posts.append(cur)
    elif ln.startswith("[x") and cur is not None:
        cur["comments"].append(ln)

out = []
for p in posts:
    if "361" in p["head"]:
        out.append(p["head"])
        out.extend(p["comments"])
        out.append("-" * 50)

open(r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\Math & Physics\_work\_relevant_dump.txt", "w", encoding="utf-8").write("\n".join(out))
print("posts:", len(posts))
print("relevant lines:", len(out))
print("bytes:", len("\n".join(out).encode("utf-8")))
# print which post indices have 361
print("361 posts:", [p["i"] for p in posts if "361" in p["head"]])
print("non361 posts:", [p["i"] for p in posts if "361" not in p["head"]])
