import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

full_bank_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\full_exam_bank.mjs'
situational_json_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\extracted_situational.json'

with open(full_bank_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

with open(situational_json_path, 'r', encoding='utf-8') as f:
    new_sit_questions = json.load(f)

# Let's extract existing english array from full_exam_bank.mjs
# It starts at: english: [ ... ]
m = re.search(r'english:\s*\[([\s\S]*?)\]\s*};', js_content)
if not m:
    print("Could not find english array in full_exam_bank.mjs")
    sys.exit(1)

# Format the 62 new situational questions as JS objects starting from id: 41
curr_id = 41
new_items_js = []
for q in new_sit_questions:
    q_str = json.dumps(q['question'], ensure_ascii=False)
    opts_str = json.dumps(q['options'], ensure_ascii=False)
    cat_str = json.dumps(q['category'], ensure_ascii=False)
    reas_str = json.dumps(q['reasoning'], ensure_ascii=False)
    corr = q['correct']
    
    item_code = f"""    {{
      id: {curr_id},
      category: {cat_str},
      question: {q_str},
      options: {opts_str},
      correct: {corr},
      reasoning: {reas_str}
    }}"""
    new_items_js.append(item_code)
    curr_id += 1

merged_english_items = m.group(1).rstrip() + ",\n" + ",\n".join(new_items_js) + "\n  "

new_js_content = js_content[:m.start(1)] + merged_english_items + js_content[m.end(1):]

with open(full_bank_path, 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print(f"Successfully added {len(new_sit_questions)} questions to full_exam_bank.mjs!")
print(f"Total English questions is now {40 + len(new_sit_questions)}!")
