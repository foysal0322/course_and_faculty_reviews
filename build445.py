import json

reviews = {
    "cse445": {
        "jsa": [
            {
                "review": "JSA RTK MAQM SMF1 better for good grade",
                "rating": "great"
            }
        ],
        "maqm": [
            {
                "review": "JSA RTK MAQM SMF1 better for good grade",
                "rating": "great"
            }
        ],
        "rtk": [
            {
                "review": "JSA RTK MAQM SMF1 better for good grade",
                "rating": "great"
            }
        ],
        "sfm1": [
            {
                "review": "JSA RTK MAQM SMF1 better for good grade",
                "rating": "great"
            }
        ],
        "sfr1": [
            {
                "review": "Sfr1 onek bhalo porai\nBut if you want a peaceful semester i wouldn't recommend onek pera dibe and if you can't keep up you'll do bad and sir has very high expectations he's hard to please\nJSA RTK MAQM SMF1 better for good grade",
                "rating": "harsh"
            },
            {
                "review": "Onek assignments dei and ek ek ta assignment is very tough\nProject o nei na\nYou gotta work hard study after everyclass and definitely attend every class",
                "rating": "harsh"
            },
            {
                "review": "Er moddhe quiz final mid tou asei ek ek ta onek marks 20,50 erokom\nTar upor assignments er report\nReport e 100% format na maintain korte parle onek marks kaate\nAnd you have to write the reports in LaTeX",
                "rating": "harsh"
            }
        ]
    }
}

with open("cse445_detailed_reviews.json", "w", encoding="utf-8") as f:
    json.dump(reviews, f, ensure_ascii=False, indent=2)

print("Saved cse445_detailed_reviews.json successfully!")
