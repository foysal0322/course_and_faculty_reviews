import json

posts = json.load(open("raw/q_cse299.json", encoding="utf-8"))
norm = lambda s: s.strip().replace("\n", " / ")
texts = []
for p in posts:
    texts.append(p["text"])
    texts.extend(c["text"] for c in p["comments"])

# (faculty, opening words of the post/comment, rating)
PICKS = [
    # AFE
    ("afe", "AFE unpredictable se ki cay se nijeo jane na", "harsh"),
    ("afe", "AFE best", "great"),
    ("afe", "Afe sir valo / Easy going ache / Project regular basis e update nei , seta time to time update dite parle valo grade pawa possible", "great"),

    # ITN
    ("itn", "ITN nen sir, just course na ekta professional level er kivabe kaj korte hoy everything sir korabe how to submit weekly report jeta life and other course marked e help korbe", "Outstanding"),
    ("itn", "Msk1 ba itn", "great"),
    ("itn", "MD Redwan Islam jodi pai tahole nibo, Itn sir paile itn sir nibo na auq sir nibo bujhtesinah...", "great"),

    # MLE
    ("mle", "He used to give rag based Chatbot for the whole class. If he still does that then easyyyy", "great"),
    ("mle", "In cse445 he curved almost 15marks in last semester", "great"),
    ("mle", "He did the same in 445.", "great"),
    ("mle", "he teaches from the absolute beginning, answers every question. whoever said that doesn't know how to take things from him", "Outstanding"),

    # MSRB
    ("msrb", "Msrb good, just be regular and on time", "great"),
    ("msrb", "440 is a very basic course and MSRB is a very good teacher, he will help you in every way but regularity is a must.", "Outstanding"),

    # MUO
    ("muo", "To get an A from MUO sir, you must make sure to show the weekly updates properly. / I missed getting a good grade because I missed showing progress for 2 weeks. / Highly recommended faculty. Just do your work properly.", "great"),
    ("muo", "Sumit Bosu Raj easy going..weekly report gula thik moto diben..Ekta final presentation hobe", "Outstanding"),
    ("muo", "Muo sir bhalo", "great"),

    # NLH
    ("nlh", "Nlh sir and Sva mam best for 299.", "great"),

    # OISD
    ("oisd", "Sti or oisd k worst aitar competition hbe.", "avoid"),

    # SFR1
    ("sfr1", "SfR1 best for learning & grading", "Outstanding"),
    ("sfr1", "Sfr1 is best", "great"),
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

json.dump({"cse299": out}, open("cse299_detailed_reviews.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("Missing items count:", len(missing))
if missing:
    print("Missing details:", [m[1][:30] for m in missing])
print("Faculties saved:", {k: len(v) for k, v in out.items()})
