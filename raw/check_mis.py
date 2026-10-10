import json, glob, os

files = sorted(glob.glob('MIS/q_mis*.json'))
total_posts = 0
total_comments = 0
print(f"{'Course':<15} | {'Posts':<8} | {'Comments':<10}")
print("-" * 38)
for f in files:
    try:
        data = json.load(open(f, encoding='utf-8'))
        p_cnt = len(data)
        c_cnt = sum(len(p.get('comments', [])) for p in data)
        total_posts += p_cnt
        total_comments += c_cnt
        name = os.path.basename(f)
        print(f"{name:<15} | {p_cnt:<8} | {c_cnt:<10}")
    except Exception as e:
        print(f"{f}: error {e}")
print("-" * 38)
print(f"{'Total':<15} | {total_posts:<8} | {total_comments:<10}")
