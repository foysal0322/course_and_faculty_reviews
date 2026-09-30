"""Build a compact review-candidate list from raw scraped posts.

For each comment, resolve which faculty it is about:
  - initials written in the comment itself, or
  - the single faculty named in the post / parent comment it replies to.
Only posts whose text (or image alt) mentions CSE115, or whose comments do, are kept.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ref = json.load(open(os.path.join(HERE, "..", "course_faculty.json"), encoding="utf-8"))
COURSE_FAC, FAC_COURSE = {}, {}
for entry in ref:
    for course, facs in entry.items():
        c = course.upper()
        for f in dict.fromkeys(x.strip().upper() for x in facs.split(",") if x.strip()):
            COURSE_FAC.setdefault(c, []).append(f)
            FAC_COURSE.setdefault(f, []).append(c)

REF115 = [f for f in COURSE_FAC["CSE115"] if f != "TBA"]
ALL_FAC = set(FAC_COURSE) - {"TBA"}
COURSE_RE = re.compile(r"\bcse[\s\-_]*115\b|\b115\s*l?\b", re.I)
AGE_RE = re.compile(r"(\d+|a) (year|month|week|day|hour|minute)s? ago")
# Short common words that collide with faculty initials.
STOP = {"AND", "THE", "FOR", "NOT", "BUT", "YOU", "ARE", "ALL", "ONE", "HOW", "SIR", "LAB", "MAT", "ENG",
        "CSE", "PHY", "HIS", "POL", "ECO", "BUS", "ACT", "FIN", "MKT", "BEN", "EEE", "CHE", "BIO", "LOL", "OK",
        "ASK", "GET", "CAN", "HAS", "HAD", "HIM", "HER", "ITS", "WHO", "WHY", "ANY", "AMI", "KI", "NA", "EI",
        "OI", "AR", "TAI", "APU", "VAI", "BRO", "MAM", "YES", "NOW", "NEW", "OLD", "DAY", "MID", "TOO", "USE",
        "GPA", "CGPA", "SEE", "TRY", "WAY", "OFF", "OUT", "LET", "SET", "BAD", "BEST", "GOOD", "EASY", "HARD"}


def facs_in(text):
    toks = re.findall(r"[A-Za-z]+\d?", text or "")
    found = []
    for t in toks:
        u = t.upper()
        if u in STOP or len(u) < 2:
            continue
        if u in ALL_FAC and u not in found:
            if len(u) <= 3 and t.islower() and u not in REF115:
                continue
            found.append(u)
    return found


def years_ago(label):
    m = AGE_RE.search(label or "")
    if not m:
        return None
    n = 1 if m.group(1) == "a" else int(m.group(1))
    return n if m.group(2) == "year" else 0


def author_of(label):
    label = re.sub(r"^(Comment|Reply) by ", "", label or "")
    label = AGE_RE.sub("", label).strip()
    m = re.match(r"(.*?) to (.*?)'s (comment|reply)$", label)
    return (m.group(1), m.group(2)) if m else (label, None)


def main(out_path):
    posts, seen = [], set()
    for f in sorted(glob.glob(os.path.join(HERE, "q*.json"))):
        for p in json.load(open(f, encoding="utf-8")):
            key = p["text"][:150]
            if key in seen:
                continue
            seen.add(key)
            posts.append(p)

    lines, n_keep = [], 0
    for i, p in enumerate(posts):
        ptext = p["text"] + " " + " ".join(p.get("image_alt", []))
        post_115 = bool(COURSE_RE.search(ptext))
        post_facs = facs_in(ptext)
        ages = [years_ago(c["label"]) for c in p["comments"]]
        ages = [a for a in ages if a is not None]
        post_age = max(ages) if ages else None
        if post_age is not None and post_age >= 7:
            continue
        cands = []
        last_fac_by_author = {}
        for c in p["comments"]:
            txt = c["text"] + " " + " ".join(c.get("image_alt", []))
            who, to = author_of(c["label"])
            cf = facs_in(txt)
            ctx = cf or last_fac_by_author.get(to) or ([] if len(post_facs) != 1 else post_facs)
            if cf:
                last_fac_by_author[who] = cf
            if ctx and len(c["text"]) > 1:
                cands.append((ctx, who, c["text"].replace("\n", " / ")))
        if not (post_115 or any(COURSE_RE.search(c["text"]) for c in p["comments"])):
            continue
        if not cands:
            continue
        n_keep += 1
        lines.append(f"## P{i} age~{post_age}y link={p.get('permalink','')}")
        lines.append("POST: " + p["text"].replace("\n", " / ")[:400])
        for ctx, who, t in cands:
            lines.append(f"  [{','.join(ctx)}] {t[:600]}")
    open(out_path, "w", encoding="utf-8").write("\n".join(lines))
    print(len(posts), "posts,", n_keep, "with candidates ->", out_path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "candidates.txt"))
