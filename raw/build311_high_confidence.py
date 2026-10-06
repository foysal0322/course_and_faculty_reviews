import json, re

posts = json.load(open("raw/q_cse311.json", encoding="utf-8"))
FAC = ["fth", "nlh", "rih", "tns1"]

# Non-reference faculties to filter out completely
OTHER_FACS = ["kmm", "smah", "stq", "aud", "maqm", "png", "mft", "mth", "ara2", "sfm1", "afn1", "mas", "ait", "isr"]

# High confidence curated reviews with detailed statements
PICKS = [
    # NLH (Niaz Murshed Chowdhury / Niaz L. Hamid)
    ("nlh", "NLH best for learning and grading", "great"),
    ("nlh", "TB Dipu Tushar bhaiya, best for learning, and generous grading.", "Outstanding"),
    ("nlh", "TB Dipu Tushar Bashak bhaiya is best for learning...", "great"),
    ("nlh", "TB Dipu Tushar vai thakle easy A kono pera nai. Pass na korleo vai pass koray dibe.", "harsh"),
    ("nlh", "NLH=> best / SFM=> best / ARa2=> best, but lectures are bit boring", "great"),
    ("nlh", "NLH sir best for CSE311.", "great"),
    ("nlh", "NLH sir is super helpful and friendly.", "Outstanding"),

    # FTH (Farzana Tasnim Himi)
    ("fth", "Drop fth wrost of all time", "avoid"),
    ("fth", "Bhai FTH / Just drop him!! He's such a weirdo! / Learning and grading both 0/100! Just believe me gurl! Not lenient at all.", "avoid"),
    ("fth", "He teaches well and gives easy questions mostly, but before finals you need to practice more as his lecture notes might not be enough.", "normal"),
    ("fth", "drop FTH", "avoid"),
    ("fth", "Abrar Ahmad friend bolse avoid korte", "avoid"),

    # RIH (Rashedur Rahman / Rashedul Islam)
    ("rih", "Best , I have just done in last semester", "great"),
    ("rih", "Cse311 Rih- pretty easy going, grades well and teaches decent as long as you dont cheat everything will be fine", "Outstanding"),
    ("rih", "RIH good but not good for grading", "harsh"),
    ("rih", "SFM sir onek bhalo but grade uthano ektu pera", "harsh"),
    ("rih", "sfm sir er porano best. dont worry about it. question o easy kore. class attentively korlei enough for quizes. and final, mid er jonno sample", "great"),
    ("rih", "Fahim Muntasir Soumyo Best", "great"),

    # TNS1 (Tanjila N. Saima)
    ("tns1", "TnS1 sir khub calm and student friendly.", "great"),
    ("tns1", "TnS1 sir er class regular presentation and report thik thakle mark bhalo ashe.", "great"),
    ("tns1", "Miss curve kore r eita 311 onr first semister", "great"),
    ("tns1", "TNS1 fine but strict with deadline", "normal"),
]

norm = lambda s: s.strip().replace("\n", " / ")
texts = []
for p in posts:
    texts.append(p["text"])
    texts.extend(c["text"] for c in p["comments"])

out = {}
for fac, prefix, rating in PICKS:
    exact = [t for t in texts if norm(t) == prefix]
    hit = exact[0] if exact else next((t for t in texts if norm(t).startswith(prefix)), None)
    if hit:
        lst = out.setdefault(fac, [])
        if all(r["review"] != hit.strip() for r in lst):
            lst.append({"review": hit.strip(), "rating": rating})

# Also dynamically pick high-confidence long detailed comments (word count >= 6)
for p in posts:
    ptxt = p["text"].strip()
    p_facs = [f for f in FAC if re.search(r"\b" + f + r"\b", ptxt, re.I)]
    
    for c in p["comments"]:
        ctxt = c["text"].strip()
        t = ctxt.lower()
        words = ctxt.split()
        
        # Must be at least 6 words long
        if len(words) < 6: continue
        # Must not be a question, thank-you, or section/credit talk
        if "?" in ctxt or "thanks" in t or "same section" in t or "credit" in t or "looking for" in t: continue
        # Must not review a non-reference faculty
        if any(re.search(r"\b" + of + r"\b", t) for of in OTHER_FACS): continue
        
        # Must express explicit faculty opinion / verdict / recommendation / experience
        if any(w in t for w in ["best", "good", "valo", "bhalo", "drop", "avoid", "worst", "wrost", "pera", "strict", "friendly", "helpful", "learning", "grading", "curve", "easy"]):
            c_facs = [f for f in FAC if re.search(r"\b" + f + r"\b", ctxt, re.I)]
            target_facs = c_facs if c_facs else p_facs
            
            for f in target_facs:
                lst = out.setdefault(f, [])
                if all(r["review"] != ctxt for r in lst):
                    if any(w in t for w in ["avoid", "drop", "worst", "wrost"]):
                        rate = "avoid"
                    elif any(w in t for w in ["strict", "pera", "tough", "hard"]):
                        rate = "harsh"
                    elif any(w in t for w in ["generous grading", "top tier", "super helpful", "best for learning and grading"]):
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

print("High-confidence long reviews build complete!")
print("Review counts per faculty:")
for f, lst in final_out.items():
    print(f"  - {f.upper()}: {len(lst)} long, high-confidence reviews")
