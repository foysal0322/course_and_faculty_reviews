import os, json

COURSES = ['EEE413', 'EEE414', 'EEE415', 'EEE461', 'EEE462', 'EEE464', 'EEE465', 'EEE422', 'EEE424', 'EEE426', 'EEE427', 'EEE428', 'EEE432', 'EEE433', 'EEE436', 'EEE453', 'EEE468', 'EEE331', 'EEE421', 'EEE423', 'EEE451', 'EEE471']

print(f"Total target EEE courses: {len(COURSES)}")
print("=" * 45)

total_posts = 0
for c in COURSES:
    path = f"eee/q_{c.lower()}.json"
    if os.path.exists(path):
        data = json.load(open(path, encoding="utf-8"))
        count = len(data)
        total_posts += count
        print(f"  {c:<10}: {count} posts -> {path}")
    else:
        print(f"  {c:<10}: MISSING")

print("=" * 45)
print(f"TOTAL SCRAPED POSTS ACROSS ALL EEE COURSES: {total_posts}")
