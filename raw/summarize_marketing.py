import glob
import json
import os

files = sorted([f for f in glob.glob('marketing/q_mkt*.json') if not f.endswith('.cur') and not f.endswith('.done')])
total_posts = 0
total_comments = 0

print(f"{'Course File':<22} | {'Posts':<7} | {'Comments':<10} | {'Size (KB)':<10}")
print("-" * 58)
for f in files:
    with open(f, encoding='utf-8') as fp:
        data = json.load(fp)
    p = len(data)
    c = sum(len(x.get('comments', [])) for x in data)
    size = os.path.getsize(f) / 1024
    total_posts += p
    total_comments += c
    print(f"{os.path.basename(f):<22} | {p:<7} | {c:<10} | {size:<10.1f}")

print("-" * 58)
print(f"{'TOTAL':<22} | {total_posts:<7} | {total_comments:<10}")
