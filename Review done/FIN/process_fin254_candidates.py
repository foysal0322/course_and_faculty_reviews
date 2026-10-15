import json
import re

def process_fin254():
    candidates = json.load(open('finance/fin254_llm_candidates.json', encoding='utf-8'))

    # Questions / Inquiries filter
    def is_question_or_inquiry(text):
        t = text.strip()
        t_lower = t.lower()
        if '?' in t:
            q_triggers = [
                "review", "kemon", "bhalo", "valo", "kivabe", "kmne", "naki", "kon", "ke", "koto",
                "can anyone", "anyone", "details", "which", "how", "is ", "are ", "who", "please",
                "suggest", "option", "bhai", "vai", "section", "ki ", "ki?", "kore?"
            ]
            if any(w in t_lower for w in q_triggers):
                return True
            if len(t) < 50:
                return True

        inquiry_phrases = [
            "honest faculty review please", "detailed review please", "detailed review needed",
            "need review", "review please", "review lgbe", "details bolen", "bhai kew advice den",
            "ki type project korle", "how much does sir curve", "how was", "question pattern ki",
            "slidebased koren naki", "please give suggestions", "if anyone has taken",
            "looking for a cse", "project mate", "same section", "which section", "seat pabona",
            "sorry", "post o tui disos", "eyy sem e kortesi", "nite parini", "kmn chilo", "kemon chilo",
            "could you share", "review de", "review dao"
        ]
        if any(p in t_lower for p in inquiry_phrases):
            return True
        return False

    # Noise / Junk / Bumps filter
    def is_junk_or_noise(text, fac):
        t = text.strip()
        t_lower = t.lower()

        if not t:
            return True

        if t in ['.', 'F', 'f', 'up', 'bump', 'BUMP', 'cfbr', 'thanks', 'thank you', '#followers', 'Interested', 'yes', 'no', 'msho', 'mdm', 'rby']:
            return True

        chatter = [
            "pabi na", "secret agent", "hat-trick", "mara khaboo", "double dekhi", "doomed",
            "exchange", "routine", "lab conflict", "partner", "looking for a", "seat pabona",
            "tui disos", "kortesi", "nite parini", "bondhu", "milad dibo"
        ]
        if any(c in t_lower for c in chatter):
            return True

        cleaned = re.sub(r'@[A-Za-z0-9._\s]+', '', t).strip()
        words = [w for w in re.split(r'\s+', cleaned.lower()) if w]
        if len(words) < 3 and not any(w in ['best', 'goat', 'goated', 'good', 'valo', 'bhalo', 'drop', 'avoid', 'pera', 'strict', 'curved', 'shera', 'cutie', 'better'] for w in words):
            return True
        if all(w in [fac.lower(), 'sir', 'maam', 'mam', 'vaia', 'bhaiya', 'bhai', 'bro', 'mama', 'vai'] for w in words):
            return True

        return False

    # Rating classification logic matching critical user rules
    def classify_rating(text):
        t_lower = text.lower()

        # Rule Check: Does the review praise teaching, curve, bonus, marking, or recommend taking / doing well?
        positive_recommendation = any(k in t_lower for k in [
            "curves", "curved", "curve", "bonus", "good marking", "haat khule", "good grade",
            "good choice", "onek valo poray", "basic shikhte", "easy going", "friendly",
            "helpful", "take him", "take her", "recommended", "go for", "shera", "cutie",
            "utmost to make sure", "easy for you to get a good grade", "always gives extra"
        ])

        top_tier = any(k in t_lower for k in [
            "goat", "goated", "11/10", "10/10", "best best", "a+ e dibe", "highly recommended", "top tier", "bestt", "best"
        ])

        if top_tier:
            return "Outstanding"

        if positive_recommendation:
            return "great"

        # Explicit avoid / warnings
        if any(k in t_lower for k in ["nah. onek kharap", "rege jay", "save your money", "worst", "be ready for insult", "bekar"]):
            return "avoid"

        if ("avoid" in t_lower or "drop" in t_lower) and not any(p in t_lower for p in ["no drop", "don't drop", "dont drop", "never drop", "saying to avoid"]):
            return "avoid"

        # Harsh / strict / tough
        if any(k in t_lower for k in ["slide reading", "unorganized", "strict", "tough", "hard", "pera", "stressful", "insult", "pressure", "doesnt do fair", "doesn't do fair"]):
            return "harsh"

        if any(k in t_lower for k in ["valo", "bhalo", "good"]):
            return "great"

        return "normal"

    output_data = {"fin254": {}}
    seen_per_fac = {}

    for c in candidates:
        text = c.get("text", "").strip()
        faculties = c.get("faculties", [])

        if not text or not faculties:
            continue

        if is_question_or_inquiry(text):
            continue

        for fac in faculties:
            fac_code = fac.lower()
            if is_junk_or_noise(text, fac_code):
                continue

            if fac_code not in output_data["fin254"]:
                output_data["fin254"][fac_code] = []
                seen_per_fac[fac_code] = set()

            if text in seen_per_fac[fac_code]:
                continue

            if len(output_data["fin254"][fac_code]) < 20:
                seen_per_fac[fac_code].add(text)
                rating = classify_rating(text)
                output_data["fin254"][fac_code].append({
                    "review": text,
                    "rating": rating
                })

    out_file = 'finance/fin254_detailed_reviews.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print("=== FIN254 Faculty Review Processing Summary ===")
    total_reviews = 0
    for fac, revs in output_data["fin254"].items():
        ratings = [r['rating'] for r in revs]
        rating_counts = dict((r, ratings.count(r)) for r in set(ratings))
        print(f"{fac.upper()}: {len(revs)} reviews -> {rating_counts}")
        total_reviews += len(revs)
    print(f"Total processed detailed reviews saved: {total_reviews}")

if __name__ == '__main__':
    process_fin254()
