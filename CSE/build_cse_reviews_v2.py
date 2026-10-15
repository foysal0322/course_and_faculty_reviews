import json
import re
import os

SRC = r"C:\Users\SMFoysalAhmed\.copilot\session-state\6cf53329-40e4-4979-8ddc-b03df459755e\files"
OUT = r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\CSE"

COURSES = ["cse413", "cse495a", "cse435", "cse418", "cse414", "cse495b", "cse427", "cse485"]

HEADER = re.compile(r"^--- \[(\d+)\.(\d+)\] (Comment by|Reply by) (.*)$")
REPLY = re.compile(r"^(.+?) to (.+?)'s (?:comment|reply) (?:\d+|a) (?:week|month|year|day)s? ago$")


def parse(path):
    """Return {block_id: {'content': str, 'reply_to': str|None, 'author': str}}."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    blocks = {}
    cur_id = None
    cur_lines = []
    for line in lines:
        m = HEADER.match(line)
        if m:
            if cur_id is not None:
                blocks[cur_id] = (cur_lines, None)
            cur_id = m.group(1) + "." + m.group(2)
            rest = m.group(4)
            rm = REPLY.match(rest) if m.group(3) == "Reply by" else None
            blocks_meta_reply = rm.group(2) if rm else None
            blocks.setdefault("__meta__", {})[cur_id] = blocks_meta_reply
            cur_lines = []
            continue
        if line.startswith("#####") or line.startswith("====="):
            if cur_id is not None:
                blocks[cur_id] = (cur_lines, None)
                cur_id = None
                cur_lines = []
            continue
        if cur_id is not None:
            cur_lines.append(line)
    if cur_id is not None:
        blocks[cur_id] = (cur_lines, None)

    meta = blocks.pop("__meta__", {})
    out = {}
    for bid, (content_lines, _) in blocks.items():
        # drop trailing blank lines
        while content_lines and content_lines[-1].strip() == "":
            content_lines.pop()
        out[bid] = {"lines": content_lines, "reply_to": meta.get(bid)}
    return out


def text_of(block, strip_names=(), strip_reply_to=True):
    lines = list(block["lines"])
    if not lines:
        return ""
    first = lines[0]
    if strip_reply_to and block["reply_to"] and first.startswith(block["reply_to"]):
        first = first[len(block["reply_to"]):]
        first = first.lstrip(" ")
    for nm in strip_names:
        if first.startswith(nm):
            first = first[len(nm):].lstrip(" ")
    lines[0] = first
    return "\n".join(lines)


# spec: course -> {faculty: [ (block_id, rating, override_text_or_None, strip_names) ] }
SPEC = {
    "cse413": {
        "iqr": [
            ("0.1", "great", "iqr A", ()),
            ("0.3", "great", None, ()),
            ("0.18", "outstanding", None, ()),
            ("0.20", "outstanding", "IQR SES", ()),
            ("19.3", "outstanding", None, ()),
            ("28.10", "moderate", None, ()),
            ("28.11", "moderate", None, ()),
            ("28.13", "moderate", None, ()),
            ("36.2", "great", None, ()),
            ("36.4", "great", None, ()),
            ("36.7", "moderate", None, ()),
        ]
    },
    "cse495a": {
        "sns1": [
            ("15.13", "outstanding",
             "465A- SNS1 sir one of the best faculty. Introduction to robotics sir top notch poray. Open book exam. No quiz, 3/4 ta Assignment submit korte hy.",
             ()),
            ("18.15", "great", None, ("Faiyad Hossain",)),
            ("18.30", "great", None, ()),
        ]
    },
    "cse435": {
        "iqr": [
            ("19.1", "outstanding", None, ()),
            ("30.3", "outstanding", None, ()),
        ],
        "dmh": [
            ("19.6", "great", None, ()),
            ("19.8", "great", None, ()),
            ("29.0", "moderate", None, ()),
            ("29.2", "outstanding", None, ()),
            ("29.7", "great", None, ()),
        ],
    },
    "cse418": {},
    "cse414": {},
    "cse495b": {
        "azk": [
            ("11.0", "great", None, ()),
            ("11.1", "moderate", None, ()),
            ("20.0", "harsh", None, ()),
            ("20.1", "great", None, ()),
            ("20.3", "moderate", None, ()),
        ]
    },
    "cse427": {
        "iqn": [
            ("7.20", "avoid", None, ()),
        ],
        "mma1": [
            ("7.22", "outstanding",
             "shon, course offer korle mma1 nite pare. Tahole nish. Onno faculty der vorosha nai.", ()),
            ("7.24", "great", None, ()),
        ],
        "mdsh": [
            ("7.22", "great", "MDSH o not bad", ()),
        ],
    },
    "cse485": {
        "svs": [
            ("35.0", "outstanding", None, ()),
        ]
    },
}

for course in COURSES:
    blocks = parse(os.path.join(SRC, "craw_%s.txt" % course))
    result = {}
    for faculty, items in SPEC[course].items():
        reviews = []
        seen = set()
        for bid, rating, override, strip_names in items:
            if bid not in blocks:
                raise SystemExit("missing block %s in %s" % (bid, course))
            txt = override if override is not None else text_of(blocks[bid], strip_names)
            if not txt.strip():
                raise SystemExit("empty text for %s %s" % (course, bid))
            if txt in seen:
                continue
            seen.add(txt)
            reviews.append({"review": txt, "rating": rating})
        result[faculty] = reviews

    path = os.path.join(OUT, "%s_llm_review_v2.json" % course)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({course: result}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", path, "faculties:", list(result.keys()),
          "counts:", {k: len(v) for k, v in result.items()})
