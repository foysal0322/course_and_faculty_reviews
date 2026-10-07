import os, json, re

remaining_courses = ['eee111', 'eee141', 'eee211', 'eee221', 'eee241', 'eee299', 'eee311', 'eee312', 'eee321', 'eee342', 'eee361', 'eee362', 'eee363', 'eee410', 'eee411', 'eee452', 'eee498', 'eee499a']

os.makedirs('eee', exist_ok=True)

STOP_WORDS = {'THE', 'AND', 'FOR', 'NOT', 'YOU', 'WAS', 'ARE', 'THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'THEY', 'WILL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'SOON', 'SOME', 'GOOD', 'BEST', 'FINE', 'LIKE', 'JUST', 'NOW', 'OUT', 'ALL', 'ANY', 'MAY', 'BUT', 'HER', 'HIS', 'HAS', 'HAD', 'HOW', 'WHY', 'WHO', 'CAN', 'SEE', 'WAY', 'NEW', 'DAY', 'MAN', 'BOY', 'GET', 'SET', 'PUT', 'RUN', 'END', 'TOO', 'OLD', 'LOW', 'HIGH', 'FAR', 'BIG', 'TOP', 'TRY', 'USE', 'LET', 'OFF', 'ON', 'UP', 'DOWN', 'IN', 'OUT', 'NO', 'YES', 'OK', 'MID', 'LAB', 'SEC', 'SECTION', 'GROUP', 'POST', 'POSTS', 'TAKE', 'TAKEN', 'GIVE', 'GIVEN', 'KNOW', 'THINK', 'NEED', 'PLEASE', 'HELP', 'INFO', 'GRADE', 'GRADES', 'QUIZ', 'EXAM', 'FINAL', 'SLIDE', 'CLASS', 'MARKS', 'COURSE', 'REVIEWS', 'REVIEW', 'FACULTY', 'TEACHER', 'TEACHING', 'STUDENT', 'STUDENTS', 'MEMBER', 'MEMBERS', 'NSU', 'EEE', 'CSE', 'MAT', 'PHY', 'ENG', 'BUS', 'ACT', 'FIN', 'MKT', 'MGT', 'CHE', 'BIO', 'LAW'}

for c_lower in remaining_courses:
    path = f"eee/q_{c_lower}.json"
    cand_path = f"eee/{c_lower}_llm_candidates.json"
    
    if not os.path.exists(path):
        print(f"Skipping {c_lower}: file not found")
        continue

    data = json.load(open(path, encoding='utf-8'))
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
            
    with open(cand_path, 'w', encoding='utf-8') as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
        
    print(f"Extracted {len(candidates)} candidates for {c_lower.upper()} -> {cand_path}")

print("Remaining EEE candidate extraction completed!")
