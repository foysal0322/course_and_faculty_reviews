"""Validate Math & Physics review files."""
import glob
import json
import os
import re

ALLOWED = {"Outstanding", "great", "Moderate", "Harsh", "Avoid"}
bad, grand = [], 0
for path in sorted(glob.glob(os.path.join("Math & Physics", "*_llm_review.json"))):
    code = os.path.basename(path).replace("_llm_review.json", "")
    d = json.load(open(path, encoding="utf-8"))
    if list(d.keys()) != [code]:
        bad.append((code, "KEY", list(d.keys())))
    counts = {}
    for fac, revs in d[code].items():
        if not re.fullmatch(r"[a-z0-9]{2,6}", fac):
            bad.append((code, "FAC", fac))
        if len(revs) > 20:
            bad.append((code, "CAP", f"{fac}={len(revs)}"))
        for r in revs:
            if not isinstance(r, dict) or "review" not in r or "rating" not in r:
                bad.append((code, "SHAPE", fac))
                continue
            if r["rating"] not in ALLOWED:
                bad.append((code, "RATING", f"{fac}:{r['rating']}"))
            if not isinstance(r["review"], str) or not r["review"].strip():
                bad.append((code, "EMPTY", fac))
            counts[r["rating"]] = counts.get(r["rating"], 0) + 1
            grand += 1
    print(f"{code}: faculties={len(d[code]):2d} reviews={sum(counts.values()):3d} {counts}")
print(f"\nTOTAL reviews: {grand}")
print("ISSUES:", bad if bad else "none")
