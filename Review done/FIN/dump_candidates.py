import json

candidates = json.load(open('finance/fin254_llm_candidates.json', encoding='utf-8'))
with open('finance/all_candidates_dump.txt', 'w', encoding='utf-8') as f:
    for i, c in enumerate(candidates):
        facs = c.get('faculties', [])
        txt = c.get('text', '')
        f.write(f"=== CANDIDATE {i+1} / {len(candidates)} ===\n")
        f.write(f"Faculties: {facs}\n")
        f.write(f"Text: {txt}\n\n")

print("Dump completed.")
