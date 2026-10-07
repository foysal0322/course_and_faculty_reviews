import os, json, re

target_courses = ['CSE417', 'CSE401', 'CSE418', 'CSE426', 'CSE473', 'CSE422', 'CSE485', 'CSE486', 'CSE433', 'CSE414', 'CSE419', 'CSE467', 'CSE468', 'CSE470', 'CSE446', 'CSE447', 'CSE448', 'CSE449']

os.makedirs('cse', exist_ok=True)

STOP_WORDS = {'THE', 'AND', 'FOR', 'NOT', 'YOU', 'WAS', 'ARE', 'THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'THEY', 'WILL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'SOON', 'SOME', 'GOOD', 'BEST', 'FINE', 'LIKE', 'JUST', 'NOW', 'OUT', 'ALL', 'ANY', 'MAY', 'BUT', 'HER', 'HIS', 'HAS', 'HAD', 'HOW', 'WHY', 'WHO', 'CAN', 'SEE', 'WAY', 'NEW', 'DAY', 'MAN', 'BOY', 'GET', 'SET', 'PUT', 'RUN', 'END', 'TOO', 'OLD', 'LOW', 'HIGH', 'FAR', 'BIG', 'TOP', 'TRY', 'USE', 'LET', 'OFF', 'ON', 'UP', 'DOWN', 'IN', 'OUT', 'NO', 'YES', 'OK', 'MID', 'LAB', 'SEC', 'SECTION', 'GROUP', 'POST', 'POSTS', 'TAKE', 'TAKEN', 'GIVE', 'GIVEN', 'KNOW', 'THINK', 'NEED', 'PLEASE', 'HELP', 'INFO', 'GRADE', 'GRADES', 'QUIZ', 'EXAM', 'FINAL', 'SLIDE', 'CLASS', 'MARKS', 'COURSE', 'REVIEWS', 'REVIEW', 'FACULTY', 'TEACHER', 'TEACHING', 'STUDENT', 'STUDENTS', 'MEMBER', 'MEMBERS', 'NSU', 'EEE', 'CSE', 'MAT', 'PHY', 'ENG', 'BUS', 'ACT', 'FIN', 'MKT', 'MGT', 'CHE', 'BIO', 'LAW'}

for course in target_courses:
    c_lower = course.lower()
    paths = [f"cse/q_{c_lower}.json", f"raw/q_{c_lower}.json", f"q_{c_lower}.json"]
    found_path = None
    for p in paths:
        if os.path.exists(p):
            found_path = p
            break
            
    if not found_path:
        print(f"Skipping {course}: raw data file not found")
        continue

    data = json.load(open(found_path, encoding='utf-8'))
    texts = []
    for item in data:
        if 'raw' in item:
            texts.append(item['raw'])
        else:
            if item.get('text'): texts.append(item['text'])
            for comm in item.get('comments', []):
                if comm.get('text'): texts.append(comm['text'])
                
    candidates = []
    seen = set()
    for t in texts:
        t_clean = t.strip()
        if len(t_clean) < 10 or t_clean in seen: continue
        seen.add(t_clean)
        
        tokens = re.findall(r'\b[a-zA-Z]{2,4}\b', t_clean)
        facs = set()
        for tok in tokens:
            u = tok.upper()
            if u not in STOP_WORDS and not u.startswith('EEE') and not u.startswith('CSE'):
                if len(u) >= 2 and u not in ['DON', 'GET', 'HAS', 'HAD', 'WAS', 'IS', 'NOT', 'CAN', 'MAY']:
                    facs.add(u.lower())
                    
        if facs:
            candidates.append({
                'text': t_clean,
                'faculties': list(facs)
            })
            
    cand_path = f"cse/{c_lower}_llm_candidates.json"
    with open(cand_path, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
        
    print(f"Extracted {len(candidates)} candidates for {course} from {found_path} -> {cand_path}")

print("CSE candidate extraction completed!")
