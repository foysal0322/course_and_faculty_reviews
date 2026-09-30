import json

posts = json.load(open("raw/q_cse215.json", encoding="utf-8"))
norm = lambda s: s.strip().replace("\n", " / ")
texts = []
for p in posts:
    texts.append(p["text"])
    texts.extend(c["text"] for c in p["comments"])

# (faculty, opening words of the post/comment, rating)
PICKS = [
    ("rjp", "Kosto hoileo rjp er kase kor.", "great"),
    ("rjp", "Muhammad Zakey Tricky question kore.", "normal"),
    ("rjp", "Rjp sir best", "great"),
    ("rjp", "Muhammad Zakey Sir class e ekdom details e poray", "great"),
    ("rjp", "Muhammad Zakey trust me. RjP onk joss", "Outstanding"),
    ("rjp", "of course RJP", "great"),
    ("rjp", "215 - RjP, MUO", "great"),
    ("rjp", "CSE215 - CFA/RjP", "great"),
    ("rjp", "Eee141 kmm / Mat125 Umm / Phy 107 hrr / Cse215 Rjp", "great"),
    ("rjp", "215 rjp sir jodi ney thn rjp", "great"),
    ("rjp", "RJP best in every aspect and in any course he takes.", "Outstanding"),
    ("rjp", "Musia Islam Jerin Yes Sir Curve koren.", "Outstanding"),
    ("rjp", "Rjp sir onek shera in terms of learning", "great"),
    ("rjp", "Rjp? he the boss", "great"),

    ("muo", "Kosto hoileo rjp er kase kor.", "normal"),
    ("muo", "MUO - Shafayat Osman Sir", "Outstanding"),
    ("muo", "Muo sir", "great"),
    ("muo", "MUO sir uni jei marking kore curve lage na.", "Outstanding"),
    ("muo", "Muo best ! Er por RIH", "great"),
    ("muo", "Muo", "great"),
    ("muo", "MUO, RIH", "great"),
    ("muo", "Muo, RIH or SVA", "great"),
    ("muo", "215 - RjP, MUO", "great"),
    ("muo", "215 rrn muo", "great"),
    ("muo", "Cse215,225- Muo", "great"),
    ("muo", "Cse 215, 225- MUO", "great"),
    ("muo", "Cse215 muo", "great"),
    ("muo", "MUO king", "great"),
    ("muo", "Without a doubt one of the best faculties of NSU.", "Outstanding"),
    ("muo", "Try to answer questions like you", "normal"),
    ("muo", "Muo sir bhalo", "great"),
    ("muo", "MUO is one of the most thorough teachers", "great"),
    ("muo", "Muo sei sure A", "Outstanding"),
    ("muo", "Muo sir best...", "great"),
    ("muo", "MUO King", "great"),
    ("muo", "MUO Best", "great"),
    ("muo", "Muhammad Aminul Islam Labib Nah sir 6-7 jon ke A dise", "great"),

    ("rrn", "215 rrn sir learning er jonno best", "great"),
    ("rrn", "AVOIDDD RRN", "avoid"),
    ("rrn", "RRn excellent for teaching and very student friendly.", "great"),
    ("rrn", "Manush rrn er bepare onek baje review dibe", "great"),
    ("rrn", "Sbw Joss / Sorry to say Rrn er kase", "harsh"),
    ("rrn", "215 rrn muo", "great"),

    ("rih", "RIH", "great"),
    ("rih", "Muo best ! Er por RIH", "great"),
    ("rih", "MUO, RIH", "great"),
    ("rih", "Muo, RIH or SVA", "great"),

    ("sfr1", "Flex?!! sob A.", "great"),
    ("sfr1", "SfR1 best for learning & grading", "great"),
    ("sfr1", "Sfr1 best for learning and grading", "great"),
    ("sfr1", "Both Sfr1 and Apv are great.", "great"),
    ("sfr1", "sfr1 and apv both are good", "great"),
    ("sfr1", "Sfr1 best", "great"),
    ("sfr1", "Sfr1 and APV", "great"),
    ("sfr1", "Apv mam bst / SfR1 bst", "great"),
    ("sfr1", "Sfr1 is good.", "great"),
    ("sfr1", "SFR1 Best!", "great"),
    ("sfr1", "Both sfr1 and Apv are good. Worth it", "great"),
    ("sfr1", "SFR1 sir is one of the best faculty", "Outstanding"),
    ("sfr1", "Sfr1 is best", "great"),
    ("sfr1", "You should feel lucky that you got the chance to do CSE215 under SFR1.", "Outstanding"),
    ("sfr1", "Arnob Ahmed grade dekhe to mone hoy nai vai", "normal"),
    ("sfr1", "Sfr1 joss crv kore", "great"),

    ("mft", "Drop Mft", "avoid"),
    ("mft", "Mft drop kore sam3 ne", "avoid"),

    ("hsm", "Rest in peace", "harsh"),

    ("sva", "SvA", "great"),
    ("sva", "Muo, RIH or SVA", "great"),
    ("sva", "আবিদ আহসান good", "great"),
    ("sva", "Faculty Review: SVA (Silvia Ahmed Ma", "Outstanding"),
    ("sva", "Ma'am 100 100", "Outstanding"),
    ("sva", "ARA2 (cse115):", "great"),
    ("sva", "Drop", "avoid"),
    ("sva", "If you want to do a tour like cox's bazar", "harsh"),
    ("sva", "Trust me, she is one of the best faculties of NSU.", "Outstanding"),
    ("sva", "utube e video dekhte blbe unar channel theke.", "normal"),
    ("sva", "Good one. Valo shikhabe but grade valo tula ektu tough", "harsh"),
    ("sva", "Good for learning but fair grading", "normal"),
    ("sva", "drop/change the section if you are not an extraordinary student.", "harsh"),
    ("sva", "Keep believe in Sva", "great"),
    ("sva", "Drop and save your money", "avoid"),
    ("sva", "If you want to learn, definitely Sva mam is one of the best", "great"),
    ("sva", "Tàsñîm Müsfîkå ho", "avoid"),
    ("sva", "She is the best in terms of learning.", "great"),
    ("sva", "Bayezid Prince ভাই উনি চমৎকার একজন টিচার।", "great"),
    ("sva", "তিমির বিহারী Hae bhai. I love Java because of her", "great"),
    ("sva", "Tbh oto khrp na jotota manush bole", "normal"),
    ("sva", "Sva ma’am you tube er channel er link", "normal"),
    ("sva", "Best for learning.copy na korle curve o kore", "great"),
    ("sva", "Khub valo bujhay. Copy niye pera dibe. Curve kore", "great"),
    ("sva", "Ekta course a ektu koshto koren", "great"),
    ("sva", "If you want the honest review / I will say drop.", "avoid"),
    ("sva", "Sadik Ittesaf Abir Bhai / Well She used to teach us", "normal"),
    ("sva", "Drop..", "avoid"),
    ("sva", "Drop asap", "avoid"),
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

json.dump({"cse215": out}, open("cse215_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("missing:", missing)
