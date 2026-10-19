import os
import pymupdf
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def parse_situational_pdf(pdf_path, category_name):
    doc = pymupdf.open(pdf_path)
    full_text = '\n'.join([p.get_text() for p in doc])
    
    # Extract Answer Key
    key_match = re.search(r'Answer Key:\s*([\s\S]*?)(?:Situational|$)', full_text)
    ans_key = {}
    if key_match:
        for line in key_match.group(1).split('\n'):
            m = re.match(r'(\d+)\s*:\s*([A-E])', line.strip())
            if m:
                ans_key[int(m.group(1))] = m.group(2)
                
    body_text = full_text.split('Answer Key:')[0]
    q_blocks = re.split(r'\n\s*(\d+)\.\s*', body_text)
    questions = []
    
    letter_to_idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    
    for i in range(1, len(q_blocks), 2):
        q_num = int(q_blocks[i])
        content = q_blocks[i+1].strip()
        
        if 'A)' not in content:
            continue
        prompt_raw = content.split('A)')[0].strip()
        prompt = " ".join(prompt_raw.split())
        
        opt_matches = re.findall(r'([A-E])\)\s*([\s\S]*?)(?=(?:[A-E]\)|$))', content)
        options = []
        for let, val in opt_matches:
            clean_val = " ".join(val.split())
            options.append(clean_val)
            
        corr_letter = ans_key.get(q_num, 'A')
        corr_idx = letter_to_idx.get(corr_letter, 0)
        
        corr_text = options[corr_idx] if corr_idx < len(options) else ''
        reasoning = f"Official Correct Answer: {corr_letter}) \"{corr_text}\"\nالرد الأكثر ملاءمة وسياقية وأدباً في هذا الموقف."
        
        questions.append({
            'category': category_name,
            'question': prompt,
            'options': options,
            'correct': corr_idx,
            'reasoning': reasoning
        })
        
    return questions

base_en = r'C:\Users\tonyn\Desktop\ITI_Preparation_Material\English'
q_test1 = parse_situational_pdf(os.path.join(base_en, '1_Situational_Responses_Test_1_Answers.pdf'), 'English Situations (Test 1)')
q_test3 = parse_situational_pdf(os.path.join(base_en, '2_Situational_Responses_Test_3_Answers.pdf'), 'English Situations (Test 3)')
q_adv   = parse_situational_pdf(os.path.join(base_en, '3_Situational_Expression_Advanced_Answers.pdf'), 'English Situations (Advanced)')

print(f"Test 1: {len(q_test1)} questions")
print(f"Test 3: {len(q_test3)} questions")
print(f"Advanced: {len(q_adv)} questions")

all_situational = q_test1 + q_test3 + q_adv
print(f"Total new situational questions: {len(all_situational)}")

# Save to a json scratch file
out_json = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\extracted_situational.json'
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump(all_situational, f, ensure_ascii=False, indent=2)

print(f"Saved {out_json}")
