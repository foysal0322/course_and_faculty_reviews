import sys
import json
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r'C:\Users\SMFoysalAhmed\.gemini\antigravity\brain\2a52cc50-4419-49a3-8dea-9e4922438798\.system_generated\logs\transcript_full.jsonl'

step_to_file = {}
with open(transcript_path, encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        step = data.get('step_index')
        if 730 <= step <= 995:
            c = str(data.get('content', ''))
            if 'Full snapshot saved to: ' in c:
                fn = c.split('Full snapshot saved to: ')[1].split(']')[0].strip()
                step_to_file[step] = fn

print(f'Total snapshot files: {len(step_to_file)}')

posts_by_permalink = {}

for step, filepath in sorted(step_to_file.items()):
    if not os.path.exists(filepath):
        continue
    with open(filepath, encoding='utf-8') as f:
        text = f.read()

    p_match = re.search(r'groups/nsu\.bba/permalink/(\d+)', text)
    if not p_match:
        continue
    pid = p_match.group(1)
    permalink = f'https://www.facebook.com/groups/nsu.bba/permalink/{pid}/'

    d_match = re.search(r'dialog\s+\"([^\"]+)\"\s+modal', text)
    if not d_match:
        continue

    d_start = text.find(d_match.group(0))
    d_text = text[d_start:]

    comment_articles = re.split(r'article\s+\"Comment by\s+([^\"]+)\"', d_text)
    post_header_chunk = comment_articles[0]

    header_texts = []
    for line in post_header_chunk.split('\n'):
        if 'button "Like"' in line or 'button "React"' in line or 'button "Leave a comment"' in line:
            break
        st_m = re.search(r'StaticText\s+\"(.*)\"', line)
        if st_m:
            t = st_m.group(1).strip()
            if t not in ['NSU BBA Courses and Faculty Assessment', 'Shared with Private group', 'Â', 'I?'] and len(t) > 2:
                header_texts.append(t)

    post_body = '\n'.join(header_texts).strip()

    comments = []
    for i in range(1, len(comment_articles), 2):
        author_info = comment_articles[i]
        c_body = comment_articles[i+1] if i+1 < len(comment_articles) else ''

        c_texts = []
        for line in c_body.split('\n'):
            if 'button "Like"' in line or 'button "Reply"' in line or 'button "React"' in line:
                break
            st_m = re.search(r'StaticText\s+\"(.*)\"', line)
            if st_m:
                t = st_m.group(1).strip()
                if t not in ['Â', 'I?', 'Like', 'Reply'] and len(t) > 1:
                    c_texts.append(t)

        c_text = ' '.join(c_texts).strip()
        if c_text:
            comments.append({
                'label': f'Comment by {author_info}',
                'text': c_text,
                'image_alt': []
            })

    if pid not in posts_by_permalink or len(comments) >= len(posts_by_permalink[pid].get('comments', [])):
        posts_by_permalink[pid] = {
            'text': post_body,
            'image_alt': [],
            'comments': comments,
            'permalink': permalink
        }

print(f'Successfully reconstructed {len(posts_by_permalink)} HRM360 posts!')
target_out = r'c:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\HR\q_hrm360.json'
with open(target_out, 'w', encoding='utf-8') as out:
    json.dump(list(posts_by_permalink.values()), out, indent=2, ensure_ascii=False)
print('Saved HR/q_hrm360.json!')
