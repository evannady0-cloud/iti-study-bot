import pymupdf
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'C:\Users\tonyn\Desktop\ITI_Preparation_Material\IQ\Ultimate_IQ_Tests_كتاب_ألتيمت.pdf'
doc = pymupdf.open(pdf_path)

# Let's inspect where each Test's answers start from page 275 to 295
tests_answers = {}
for p_idx in range(275, 295):
    txt = doc[p_idx].get_text()
    for m in re.finditer(r'Test\s+(\d+):\s*Answers', txt):
        t_num = int(m.group(1))
        tests_answers[t_num] = p_idx + 1

print("Tests answers starting pages:", tests_answers)
