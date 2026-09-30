import json

posts = json.load(open("raw/q_cse173.json", encoding="utf-8"))
norm = lambda s: s.strip().replace("\n", " / ")
texts = []
for p in posts:
    texts.append(p["text"])
    texts.extend(c["text"] for c in p["comments"])

# (faculty, opening words of the post/comment, rating)
PICKS = [
    ("itn", "Msrb,itn", "great"),
    ("itn", "ITN Sir. / MSRb Sir o vlo.", "great"),
    ("itn", "Mat120 - mtm / akad / cnp / Cse173 - itn", "great"),
    ("itn", "cse173 itn,sva", "great"),
    ("itn", "ITN average for learning but good for grading.", "normal"),
    ("itn", "It will be easy going if you can concentrate", "great"),
    ("itn", "best vai best", "Outstanding"),
    ("itn", "learning+ grading both er jonno valo", "great"),
    ("itn", "His teaching skills are very good. Exams will be hard", "great"),
    ("itn", "Towhid Aslam bhai kemon hard question kore", "normal"),
    ("itn", "not best for learning", "normal"),
    ("itn", "Shera", "great"),
    ("itn", "Itn best", "great"),
    ("itn", "Itn shera", "great"),
    ("itn", "itn not best for learning", "normal"),
    ("itn", "ITN vlo", "great"),
    ("itn", "CSE173-ITN valo(Best for grading)", "great"),
    ("itn", "Itn goat", "Outstanding"),
    ("itn", "173 120 ITN MTM rip learning", "harsh"),
    ("itn", "CSE 173 avoid ITN", "avoid"),
    ("itn", "Cse173 / ITN best", "great"),
    ("itn", "Itn", "great"),
    ("itn", "ITN", "great"),
    ("itn", "Go for ITN sir.", "great"),
    ("itn", "Joss", "great"),
    ("itn", "best", "great"),
    ("itn", "ITN sir best for learning and grading", "Outstanding"),
    ("itn", "Itn best vai", "great"),
    ("itn", "ITN best", "great"),
    ("itn", "Stop making him best,attended every class", "harsh"),

    ("msrb", "MSRB", "great"),
    ("msrb", "Msrb,itn", "great"),
    ("msrb", "ITN Sir. / MSRb Sir o vlo.", "great"),

    ("tnf", "Tnf avoid.. Beshi beshi ekdom", "avoid"),

    ("sle", "Cse173 SLE", "great"),
    ("sle", "CSE-173 : SLE / Teaching: decent for learning", "normal"),
    ("sle", "SLE is biased", "harsh"),
    ("sle", "SLE sir er shathe ektu interact korte hobe", "normal"),
    ("sle", "Suhail Kabir Rafi learning er jonno bhalo / Curving & easy going erta mix review", "normal"),
    ("sle", "Sky Berry bhai ank mix review", "normal"),
    ("sle", "Ahmed Mushtasin Super biased", "harsh"),
    ("sle", "Bro drop sle", "avoid"),

    ("sva", "cse173 itn,sva", "great"),
    ("sva", "Cse 173 Msk1, Sva", "great"),
    ("sva", "sva, she's excellent in terms of teaching", "Outstanding"),
    ("sva", "sva, mmhn both good", "great"),
    ("sva", "SVA, NIA BESTTTT", "Outstanding"),
    ("sva", "SvA drop (amake diye den ami nibo", "great"),
    ("sva", "Abdur Rahman Yasin SvA er kache korar jonno", "great"),
    ("sva", "Sva Nia goated", "Outstanding"),
    ("sva", "#FacultyReview #sva #cse173", "Outstanding"),
    ("sva", "sva all the way then!", "great"),
    ("sva", "Accuracy / SVA ma'am is the best for CSE215 too.", "great"),
    ("sva", "sva best. ar kono kotha nai", "Outstanding"),
    ("sva", "maam onek kind", "great"),
    ("sva", "She is the best. Even getting a C grade worth it", "Outstanding"),
    ("sva", "Abrar Faiyaz true, ei ekmatro course jekhane kharap koreo", "great"),
    ("sva", "She is definitely one of the best faculty... but, msk1", "great"),

    ("msk1", "CSE173 and CSE215 together doable but not under MsK1", "harsh"),
    ("msk1", "Cse173 is too easy but msk1 sir er question is kinda hard", "normal"),
    ("msk1", "Salman Sabin i would suggest 6 days class", "avoid"),
    ("msk1", "Maba will be easy.", "harsh"),
    ("msk1", "Msk1 life ta sarabara kore dibe", "avoid"),
    ("msk1", "Drop MSK1", "avoid"),
    ("msk1", "Which one? These are respected faculties.", "great"),
    ("msk1", "hallaaalboi honestly speaking, if you don't want unnecessary mental pressure", "avoid"),
    ("msk1", "MSK1 is good", "great"),
    ("msk1", "Msk1", "great"),
    ("msk1", "MSK1 Sir is the best for learning.", "Outstanding"),
    ("msk1", "Taufiq Omar highest possible grade A-", "harsh"),
    ("msk1", "Msk1 for learning also for the curving", "great"),
    ("msk1", "Msk1 valona", "harsh"),
    ("msk1", "Avg grade c,d, je sobr che valo korbe", "harsh"),
    ("msk1", "MysticalKoala9336 unar sctione raw marke 95%", "harsh"),
    ("msk1", "Class e 60-70 percent paile a paoa jay", "normal"),
    ("msk1", "Niamul Islam Noman yes . final e 2/3 ta book theke", "normal"),
    ("msk1", "Highest to A dey e", "normal"),
    ("msk1", "d/d+ dhoraya dibe", "harsh"),
    ("msk1", "If you are worried about passing, he makes everyone pass", "harsh"),
    ("msk1", "Cse 173 Msk1, Sva", "great"),
    ("msk1", "anonymous110723 I did 173 under msk1", "great"),
    ("msk1", "173 -msk1/akr for teaching", "great"),
    ("msk1", "Drop msk1", "avoid"),
    ("msk1", "Tabita Islam msk1 sobi bole best but", "harsh"),
    ("msk1", "Drop Msk1", "avoid"),
    ("msk1", "Mai Rei HORRIBLE. He teaches really well", "harsh"),
    ("msk1", "NSUCSE261 Best for learning, but not easygoing.", "great"),
    ("msk1", "NSUCSE261 yes. Amader sec theke 5/6 jon A chilo.", "great"),
    ("msk1", "Cse173 Learning er jonno MSK1 best.", "great"),
    ("msk1", "Msk1 best", "great"),
    ("msk1", "MSK1 hoyto marks r grade dekhe moja lagte paree", "harsh"),
    ("msk1", "I did last semester under msk1", "great"),
    ("msk1", "Koren vai Msk1..", "avoid"),
    ("msk1", "Faculty review: MSK1 CSE173", "avoid"),
    ("msk1", "Bhai, sorry to say msk1 fakibuzz", "Outstanding"),
    ("msk1", "Bhai sorry, you must be someone from the braindead following", "avoid"),
    ("msk1", "Samir Ahmed Srz bhul direction koi mama.", "Outstanding"),
    ("msk1", "Sir is actually Good jodi apni ekdm 100 100 effort den.", "harsh"),
    ("msk1", "You lost me at study suggestions are useless.", "Outstanding"),
    ("msk1", "Sazid Ahmed Tomal And you lost me at", "harsh"),
    ("msk1", "Shahriar Rifat best faculty for abstention", "harsh"),
    ("msk1", "Murad Mustakim amader favourite Sir niye ki bole eishob.", "great"),
    ("msk1", "Msk1 sir best, / Life lesson 100/100", "great"),
    ("msk1", "Fahim F. Souwmik kire ami to sbair theke shuni", "harsh"),
    ("msk1", "Ashfak Best Faculty ever", "Outstanding"),
    ("msk1", "Did you ever go through the book he added", "great"),
    ("msk1", "Nahian Sarower Siam sir is one of the very few Good faculties", "great"),
    ("msk1", "I disagree with some of your points.", "great"),
    ("msk1", "Being demanding and pushing students", "great"),
    ("msk1", "I got D under him i didn", "great"),
    ("msk1", "I disagree on some points. I know MSK1", "Outstanding"),
    ("msk1", "MSK1 is scary for students who are not REGULAR", "great"),
    ("msk1", "Msk1 is one of the bestest faculty", "Outstanding"),
    ("msk1", "In undergraduate I don", "great"),
    ("msk1", "Teaching = 100", "avoid"),
    ("msk1", "Sir poran onk bhalo , learning er jonno best", "great"),
    ("msk1", "Msk1 onk valo vai ami course korar ageee", "Outstanding"),
    ("msk1", "If grade matters to you & you are not a hard worker", "harsh"),
    ("msk1", "Brother, just try to focus his classes.", "normal"),
    ("msk1", "msk1", "great"),
    ("msk1", "Msk1 sir best tai na Durjoy Ghosh", "great"),
    ("msk1", "Durjoy Ghosh Haa vai amr nsu life er favourite sir", "Outstanding"),
    ("msk1", "Mask1 pera + learning.", "normal"),
    ("msk1", "Trust me, you'll need to learn shit load", "great"),
    ("msk1", "msk1 good for learning + curving", "great"),
    ("msk1", "MsK1 “nightmare experience”", "harsh"),
    ("msk1", "Msk1 for learning / Sft for grading", "normal"),
    ("msk1", "Msk1 sir is really good for cse173.", "Outstanding"),
    ("msk1", "MSK1", "great"),
    ("msk1", "For learning msk1", "great"),
    ("msk1", "Msk1.", "great"),
    ("msk1", "Msk1 for learning best and also curves a lot", "great"),
    ("msk1", "Aditto Rahman Msk1 zindabaad", "great"),
    ("msk1", "Sft sir er pora bujha jay na, ask krle", "great"),
    ("msk1", "msk1 স্যার ভালো মানুষ", "great"),
    ("msk1", "Msk1 bestt", "great"),
    ("msk1", "- msk1 manush valo", "great"),
    ("msk1", "Avoid MSK1", "avoid"),
    ("msk1", "Msk1 avoid / Idk how he is now", "avoid"),
    ("msk1", "bhuleo dont take msk1 if youre a regular student", "harsh"),
    ("msk1", "She is definitely one of the best faculty... but, msk1", "great"),
    ("msk1", "Msk1 sir best", "great"),
    ("msk1", "MSK1 sir", "great"),
    ("msk1", "Msk1, will make you feel a bit stressed", "great"),
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

for fac, lst in out.items():
    if len(lst) > 10:
        out[fac] = [r for r in lst if len(r["review"].split()) > 3]

json.dump({"cse173": out}, open("cse173_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for f, v in out.items():
    print(f, len(v))
print("missing:", missing)
