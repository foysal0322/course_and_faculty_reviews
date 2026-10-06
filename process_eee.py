"""Usage: python process_eee.py eee452 [eee498 ...]
Copies eee/q_<course>.json into raw/, builds <course>_detailed_reviews.json via
build_all_reviews.process_course, and mirrors the result into eee/."""
import json
import os
import shutil
import sys

import build_all_reviews

for course in sys.argv[1:]:
    course = course.lower()
    src = f"eee/q_{course}.json"
    if not os.path.exists(src):
        print(f"{course}: no raw file, writing empty review file")
        res = {course: {}}
        for path in (f"{course}_detailed_reviews.json", f"eee/{course}_detailed_reviews.json"):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(res, f, indent=2)
        continue
    with open(src, encoding="utf-8") as f:
        posts = json.load(f)
    print(f"{course}: {len(posts)} posts, {sum(len(p.get('comments', [])) for p in posts)} comments")
    shutil.copy(src, f"raw/q_{course}.json")
    build_all_reviews.process_course(course)
    with open(f"{course}_detailed_reviews.json", encoding="utf-8") as f:
        res = json.load(f)
    with open(f"eee/{course}_detailed_reviews.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
