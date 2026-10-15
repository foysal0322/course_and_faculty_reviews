import json, io, os, re, sys

BASE = r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews"
RAW = os.path.join(BASE, "raw")

def load(name):
    return json.load(io.open(os.path.join(RAW, name), encoding="utf-8"))

def strip_mention(text, label):
    """Strip a leading replied-to @mention name if the comment is a reply to that person."""
    m = re.match(r"Reply by .*? to (.*?)'s (?:comment|reply)", label or "")
    if not m:
        return text
    target = m.group(1).strip()
    if target and text.startswith(target):
        rest = text[len(target):]
        if rest[:1] in (" ", "\n", "\t"):
            return rest.lstrip()
    return text

def build_corpus(files):
    corpus = []  # (text, label, post_text, source)
    for name in files:
        for i, p in enumerate(load(name)):
            ptxt = (p.get("text") or "").strip()
            for c in (p.get("comments") or []):
                raw = (c.get("text") or "").strip()
                if not raw:
                    continue
                lab = c.get("label") or ""
                corpus.append((strip_mention(raw, lab), lab, ptxt, "%s#%d" % (name, i)))
            if ptxt:
                corpus.append((ptxt, "", ptxt, "%s#%d(post)" % (name, i)))
    return corpus

def select(corpus, spec):
    """spec: (key, mode, value, rating); mode 'exact' or 'snip'. Returns list of (key, text, rating)."""
    key, mode, val, rating = spec
    hits = []
    for text, lab, ptxt, src in corpus:
        if mode == "exact" and text == val:
            cand = text
        elif mode == "snip" and val in text:
            cand = text
        elif mode == "suffix" and text.endswith(val):
            cand = val  # drops a leading replied-to @mention that is not parseable
        elif mode == "from" and val in text:
            cand = text[text.index(val):]  # drops a leading @mention not parseable from the label
        else:
            continue
        if cand not in hits:
            hits.append(cand)
    if not hits:
        print("!! NO MATCH:", key, mode, repr(val)[:80])
        return []
    if len(hits) > 1:
        print("?? AMBIGUOUS (%d):" % len(hits), key, repr(val)[:70])
        for h in hits:
            print("      ->", repr(h)[:110])
    return [(key, hits[0], rating)]

CSE215 = [
    # ---- rrn ----
    ("rrn", "snip", "215 rrn sir learning er jonno best", "outstanding"),
    ("rrn", "exact", "AVOIDDD RRN", "avoid"),
    ("rrn", "snip", "RRn excellent for teaching and very student friendly", "moderate"),
    ("rrn", "snip", "Faculty review :RRN", "outstanding"),
    ("rrn", "snip", "Manush rrn er bepare onek baje review dibe", "great"),
    ("rrn", "snip", "Sorry to say Rrn er kase apnar onek survive korte hobe", "harsh"),
    ("rrn", "snip", "Avoid rrn for 215 and auz for 107", "avoid"),
    ("rrn", "exact", "one of the hardest questions", "harsh"),
    ("rrn", "exact", "one of the hardest questions (2)", "harsh"),
    ("rrn", "snip", "lengthy, and ekta question dsa theke chilo", "harsh"),
    ("rrn", "snip", "Code likhte hbe onek. Fill in the blanks type o thskte pare", "great"),
    ("rrn", "snip", "one of the easiest questions just bujhe jaiyo", "great"),
    ("rrn", "snip", "Mid temon hard chilo na, but final", "great"),
    ("rrn", "snip", "class e jeshob code dekhaise ogula theke disilo", "great"),
    ("rrn", "snip", "abstraction theke just quiz e ekta simple question disilo", "great"),
    ("rrn", "snip", "sir class e jegula dise ogula thekei quiz dey normally", "great"),
    ("rrn", "snip", "final e ekta restaurant er jonno billing type banate bolsilo", "great"),
    # ---- muo ----
    ("muo", "snip", "MUO - Shafayat Osman Sir", "outstanding"),
    ("muo", "snip", "MUO sir uni jei marking kore curve lage na", "outstanding"),
    ("muo", "snip", "Without a doubt one of the best faculties of NSU", "outstanding"),
    ("muo", "snip", "Try to answer questions like you", "great"),
    ("muo", "snip", "MUO is one of the most thorough teachers for CSE in NSU", "outstanding"),
    ("muo", "snip", "Muo sir best...", "outstanding"),
    ("muo", "exact", "MUO King", "great"),
    ("muo", "exact", "MUO Best", "great"),
    ("muo", "exact", "Muo sei sure A", "great"),
    ("muo", "snip", "Muo best ! Er por RIH sir er kache jaite paro", "great"),
    ("muo", "exact", "Muo sir bhalo", "great"),
    ("muo", "snip", "Nah sir 6-7 jon ke A dise last semester e", "great"),
    ("muo", "snip", "215,225-MUO", "outstanding"),
    # ---- rjp ----
    ("rjp", "snip", "Kosto hoileo rjp er kase kor", "great"),
    ("rjp", "exact", "Rjp sir best", "great"),
    ("rjp", "snip", "Sir class e ekdom details e poray, question standard koren", "great"),
    ("rjp", "snip", "Tricky question kore. Concept clear thakle prosno dhora sohoj hoy.", "great"),
    ("rjp", "snip", "trust me. RjP onk joss", "outstanding"),
    ("rjp", "exact", "RJP best in every aspect and in any course he takes.", "outstanding"),
    ("rjp", "from", "Yes Sir Curve koren.", "outstanding"),
    ("rjp", "snip", "Rjp sir onek shera in terms of learning", "outstanding"),
    ("rjp", "exact", "Rjp? he the boss", "great"),
    ("rjp", "snip", "He fits exactly what you want. easy going, curve kore.", "great"),
    ("rjp", "snip", "Sir onk bhalo poray qsth easy hoy onno faculty theke i guess", "great"),
    # ---- rih ----
    ("rih", "snip", "Best for learning & grading.", "outstanding"),
    ("rih", "snip", "Overall, he is not a bad faculty member.", "great"),
    # ---- sva ----
    ("sva", "snip", "Very good for learning and curve oooh kore", "outstanding"),
    ("sva", "from", "People have different opinions", "great"),
    ("sva", "exact", "good", "great"),
    ("sva", "snip", "Trust me, she is one of the best faculties of NSU.", "outstanding"),
    ("sva", "snip", "utube e video dekhte blbe unar channel theke", "moderate"),
    ("sva", "snip", "Good one. Valo shikhabe but grade valo tula ektu tough", "moderate"),
    ("sva", "exact", "Good for learning but fair grading", "great"),
    ("sva", "snip", "drop/change the section if you are not an extraordinary student.", "harsh"),
    ("sva", "exact", "If you want to learn, definitely Sva mam is one of the best faculties of NSU.", "outstanding"),
    ("sva", "snip", "kicu korar nai sva er kase manei taka mair", "avoid"),
    ("sva", "snip", "She is the best in terms of learning.", "outstanding"),
    ("sva", "exact", "Tbh oto khrp na jotota manush bole", "moderate"),
    ("sva", "snip", "Sva ma’am you tube er channel er link diye dibe", "moderate"),
    ("sva", "exact", "Best for learning.copy na korle curve o kore", "great"),
    ("sva", "exact", "Khub valo bujhay. Copy niye pera dibe. Curve kore", "great"),
    ("sva", "snip", "Ekta course a ektu koshto koren", "moderate"),
    ("sva", "exact", "Drop and save your money \n and time", "avoid"),
    ("sva", "exact", "Drop", "avoid"),
    ("sva", "snip", "Faculty Review: SVA", "great"),
    ("sva", "snip", "ARA2 (cse115):", "great"),
    # ---- may ----
    ("may", "snip", "May sir bhalo try to seat in the first row", "great"),
    ("may", "exact", "MAY best", "great"),
    ("may", "exact", "Purai scam.", "avoid"),
    ("may", "exact", "May best", "great"),
    ("may", "exact", "May best\njust class valo moto follow krte hobe", "great"),
    ("may", "exact", "May Sir best", "great"),
    ("may", "snip", "May sir 215 er one of the best faculty.", "outstanding"),
    # ---- sfr1 ----
    ("sfr1", "exact", "Sfr1 best for learning and grading", "outstanding"),
    ("sfr1", "exact", "SfR1 best for learning & grading", "outstanding"),
    ("sfr1", "exact", "Sfr1 best", "great"),
    ("sfr1", "exact", "Sfr1 is good.", "great"),
    ("sfr1", "exact", "SFR1 Best!", "great"),
    ("sfr1", "snip", "SFR1 sir is one of the best faculty", "outstanding"),
    ("sfr1", "exact", "Sfr1 is best", "great"),
    ("sfr1", "exact", "Sfr1 joss crv kore", "great"),
    ("sfr1", "snip", "You should feel lucky that you got the chance to do CSE215 under SFR1.", "outstanding"),
    ("sfr1", "exact", "grade dekhe to mone hoy nai vai..", "harsh"),
    ("sfr1", "exact", "Both Sfr1 and Apv are great.", "great"),
    ("sfr1", "snip", "Both sfr1 and Apv are good. Worth it", "great"),
    # ---- hsm ----
    ("hsm", "snip", "HSM will be medium hard.", "moderate"),
    ("hsm", "exact", "CSE173 and CSE215 together doable but not under MsK1 and HSM, too much pressure", "moderate"),
    ("hsm", "exact", "Yes doable but hsm is not worth it", "harsh"),
    # ---- msrb ----
    ("msrb", "snip", "Sir onek bonus marks dei r quiz mid final eo onek partial marks dei.", "great"),
    ("msrb", "exact", "amr 92.25 chilo(without bonus marks) then curve kore A dise", "great"),
    # ---- mslk ----
    ("mslk", "exact", "class er shobar marks messed up kore dise bhai...still cant say anything for sure", "harsh"),
    # ---- sam3 ----
    ("sam3", "exact", "Sam3 worst", "avoid"),
    ("sam3", "exact", "Avoid SAM3", "avoid"),
    # ---- mft ----
    ("mft", "snip", "MFT sir barely teaches anything in class", "harsh"),
    ("mft", "snip", "Drop mft last semester e ami korsilam", "avoid"),
    ("mft", "exact", "avoid", "avoid"),
    ("mft", "snip", "it’s better to avoid him...", "avoid"),
    ("mft", "exact", "Drop Mft", "avoid"),
    ("mft", "exact", "Mft drop kore sam3 ne", "avoid"),
    # ---- trr ----
    ("trr", "snip", "TRR পড়ায় ভাল কিন্তু grade এ বাশ", "harsh"),
    ("trr", "snip", "No. He gives very good grades but you have to work for it.", "moderate"),
    ("trr", "snip", "ভাই আমি যতেষ্ট খাটছিলাম", "moderate"),
    ("trr", "snip", "Sir oneker marks deduct kore code copy paste", "moderate"),
    ("trr", "snip", "vai trr jdi grade na dey taile k dey?", "harsh"),
    ("trr", "snip", "Bro i did 215 with TRR.", "great"),
    # ---- cfa ----
    ("cfa", "exact", "CFA curves though not good for learning", "moderate"),
    ("cfa", "exact", "slides poraye shathe book o porte bole", "moderate"),
    ("cfa", "exact", "question average kore", "moderate"),
    ("cfa", "exact", "basic clear thakle possible", "great"),
    # ---- maqm ----
    ("maqm", "snip", "He is easy going", "great"),
]

CSE419 = [
    ("rrn", "suffix", "sir valo kintu question onek lengthy kore", "moderate"),
    ("rrn", "snip", "Sir paper chara kisu bujena", "harsh"),
]

def make(specs, corpus, course):
    out = {}
    for s in specs:
        for key, text, rating in select(corpus, s):
            out.setdefault(key, [])
            if not any(r["review"] == text for r in out[key]):
                out[key].append({"review": text, "rating": rating})
    return {course: out}

c215 = build_corpus(["q_cse215.json", "q_cse215b.json"])
c419 = build_corpus(["q_cse419.json"])

res215 = make(CSE215, c215, "cse215")
res419 = make(CSE419, c419, "cse419")

for course, data, fn in [("cse215", res215, "cse215_llm_review_v2.json"),
                         ("cse419", res419, "cse419_llm_review_v2.json")]:
    path = os.path.join(BASE, "CSE", fn)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    d = data[course]
    print("%s -> %s : %d keys, %d reviews" % (course, fn, len(d), sum(len(v) for v in d.values())))
    for k in sorted(d):
        print("   %-6s %d" % (k, len(d[k])))
