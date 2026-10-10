import json
import glob
import os

files = sorted(glob.glob("History/q_*.json"))
print(f"{'Course':<15} | {'Posts':<8} | {'Comments':<10}")
print("-" * 38)
total_p = 0
total_c = 0
for f in files:
    try:
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            p_cnt = len(data)
            c_cnt = sum(len(x.get("comments", [])) for x in data)
            total_p += p_cnt
            total_c += c_cnt
            print(f"{os.path.basename(f):<15} | {p_cnt:<8} | {c_cnt:<10}")
    except Exception as e:
        print(f"{os.path.basename(f):<15} | ERR: {e}")
print("-" * 38)
print(f"{'Total':<15} | {total_p:<8} | {total_c:<10}")
