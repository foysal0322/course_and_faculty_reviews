import json

posts = json.load(open("raw/q_cse311.json", encoding="utf-8"))
norm = lambda s: s.strip().replace("\n", " / ")
texts = []
for p in posts:
    texts.append(p["text"])
    texts.extend(c["text"] for c in p["comments"])

# Curated Picks based on human common sense, sentiment analysis, and context
PICKS = [
    # NLH
    ("nlh", "NLH best for learning and grading", "great"),
    ("nlh", "TB Dipu Tushar bhaiya, best for learning, and generous grading.", "Outstanding"),
    ("nlh", "Nlh sir beshi strict o na beshi chill o na.", "normal"),
    ("nlh", "TB Dipu Tushar Bashak bhaiya is best for learning", "great"),
    ("nlh", "NLH sir best for CSE311.", "great"),
    ("nlh", "NLH sir is super helpful and friendly.", "Outstanding"),
    ("nlh", "NLH sir top tier for learning web dev.", "Outstanding"),

    # FTH
    ("fth", "drop FTH", "avoid"),
    ("fth", "Abrar Ahmad friend bolse avoid korte", "avoid"),
    ("fth", "Drop fth wrost of all time", "avoid"),
    ("fth", "Bhai FTH / Just drop him!! He's such a weirdo! / Learning and grading both 0/100! Just believe me gurl!", "avoid"),
    ("fth", "FTH section drop deya e bhalo.", "avoid"),
    ("fth", "FTH grading is tough and no curve.", "harsh"),
    ("fth", "FTH is very strict in lab.", "harsh"),

    # RIH
    ("rih", "Best , I have just done in last semester", "great"),
    ("rih", "Best", "great"),
    ("rih", "Fahim Muntasir Soumyo Best", "great"),
    ("rih", "SFM sir onek bhalo but grade uthano ektu pera", "harsh"),
    ("rih", "RIH sir is good for learning.", "great"),
    ("rih", "Rih sir exam questions standard koren.", "normal"),
    ("rih", "RIH sir best", "great"),

    # TNS1
    ("tns1", "TnS1 sir khub calm and student friendly.", "great"),
    ("tns1", "TnS1 sir er class regular presentation and report thik thakle mark bhalo ashe.", "great"),
    ("tns1", "TNS1 fine but strict with deadline", "normal"),
    ("tns1", "TnS1 mam is good for 311", "great"),
    ("tns1", "Drop drop", "avoid"),
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

# Also perform automated sentiment filtering for remaining comments to reach comprehensive human-curated reviews
for p in posts:
    ptxt = p["text"].strip()
    p_facs = [f for f in ["fth", "nlh", "rih", "tns1"] if f in ptxt.lower()]
    for c in p["comments"]:
        ctxt = c["text"].strip()
        t = ctxt.lower()
        if len(t) < 5 or "?" in t or "thanks" in t or "same section" in t or "credits" in t: continue
        
        # Check explicit sentiment / review keywords
        if any(w in t for w in ["best", "good", "valo", "bhalo", "drop", "avoid", "worst", "pera", "strict", "friendly", "helpful", "learning"]):
            for f in ["fth", "nlh", "rih", "tns1"]:
                if f in t or (f in p_facs and len(t) > 10):
                    lst = out.setdefault(f, [])
                    if all(r["review"] != ctxt for r in lst):
                        if any(w in t for w in ["avoid", "drop", "worst", "wrost"]):
                            rate = "avoid"
                        elif any(w in t for w in ["strict", "pera", "tough", "hard"]):
                            rate = "harsh"
                        elif any(w in t for w in ["goat", "11/10", "best best", "super helpful"]):
                            rate = "Outstanding"
                        elif any(w in t for w in ["normal", "average", "fair"]):
                            rate = "normal"
                        else:
                            rate = "great"
                        lst.append({"review": ctxt, "rating": rate})

final_out = {}
for f, lst in out.items():
    if lst:
        final_out[f] = lst[:20]

json.dump({"cse311": final_out}, open("cse311_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("Human common sense & sentiment regenerated cse311_detailed_reviews.json successfully!")
print("Review counts per faculty:")
for f, lst in final_out.items():
    print(f"  - {f}: {len(lst)} reviews")
