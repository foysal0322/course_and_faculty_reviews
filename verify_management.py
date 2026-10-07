import os, json

COURSES = ['MGT210', 'MGT212', 'MGT314', 'MGT321', 'MGT330', 'MGT351', 'MGT360', 'MGT368', 'MGT410', 'MGT460', 'MGT470', 'MGT489', 'MGT490']

print(f"Total target Management courses: {len(COURSES)}")
print("=" * 55)

total_posts = 0
for c in COURSES:
    path = f"Management/q_{c.lower()}.json"
    if os.path.exists(path):
        data = json.load(open(path, encoding="utf-8"))
        count = len(data)
        total_posts += count
        print(f"  {c:<10}: {count:3d} posts -> {path}")
    else:
        print(f"  {c:<10}: MISSING")

print("=" * 55)
print(f"TOTAL SCRAPED POSTS ACROSS ALL MANAGEMENT COURSES: {total_posts}")
