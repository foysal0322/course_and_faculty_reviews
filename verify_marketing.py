import os, json

COURSES = ['MKT202', 'MKT330', 'MKT337', 'MKT344', 'MKT355', 'MKT382', 'MKT412', 'MKT417', 'MKT450', 'MKT460', 'MKT465', 'MKT470', 'MKT475']

print(f"Total target Marketing courses: {len(COURSES)}")
print("=" * 55)

total_posts = 0
for c in COURSES:
    path = f"markating/q_{c.lower()}.json"
    if os.path.exists(path):
        data = json.load(open(path, encoding="utf-8"))
        count = len(data)
        total_posts += count
        print(f"  {c:<10}: {count:3d} posts -> {path}")
    else:
        print(f"  {c:<10}: MISSING")

print("=" * 55)
print(f"TOTAL SCRAPED POSTS ACROSS ALL MARKETING COURSES: {total_posts}")
