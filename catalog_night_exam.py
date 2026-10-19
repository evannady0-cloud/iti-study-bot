import zipfile
import xml.etree.ElementTree as ET
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r'C:\Users\tonyn\Desktop\ITI_Preparation_Material\Night_Before_Exam\IQ_Exam_Night_ملف_ليلة_الامتحان.docx'
with zipfile.ZipFile(docx_path) as z:
    doc_xml = z.read('word/document.xml')
    rels_xml = z.read('word/_rels/document.xml.rels')

root = ET.fromstring(doc_xml)
rels_root = ET.fromstring(rels_xml)
rel_map = {r.attrib.get('Id'): r.attrib.get('Target') for r in rels_root}

ns = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
}

paragraphs = root.findall('.//w:p', ns)

elements = []
for p in paragraphs:
    t = ''.join([elem.text for elem in p.findall('.//w:t', ns) if elem.text]).strip()
    blips = p.findall('.//a:blip', ns)
    img_names = []
    for b in blips:
        eid = b.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if eid in rel_map:
            img_names.append(os.path.basename(rel_map[eid]))
    if t or img_names:
        elements.append({'text': t, 'images': img_names})

# Catalog all switch problems
switch_pairs = []
curr_q = None
for i in range(34, 78):
    el = elements[i]
    if el['text'].endswith('-') and el['text'][:-1].isdigit():
        q_num = el['text'][:-1]
        curr_q = {'num': q_num, 'q_img': None, 'sol_img': None}
    elif curr_q and el['images']:
        if curr_q['q_img'] is None:
            curr_q['q_img'] = el['images'][0]
        elif curr_q['sol_img'] is None:
            curr_q['sol_img'] = el['images'][0]
            switch_pairs.append(curr_q)
            curr_q = None

print(f"Cataloged {len(switch_pairs)} Switch Problem pairs:")
for sp in switch_pairs:
    print(f"  Q{sp['num']}: Question={sp['q_img']}, Solution={sp['sol_img']}")

# Catalog pattern questions
pattern_items = []
for i in range(80, 376):
    el = elements[i]
    if el['images']:
        # Find following answer
        ans_text = ""
        explain_text = ""
        for j in range(i+1, min(i+5, len(elements))):
            t = elements[j]['text']
            if 'ANSWER' in t.upper() or 'الحل' in t:
                ans_text = t
            elif 'EXPLAIN' in t.upper() or ans_text:
                explain_text += " " + t
            if elements[j]['images']:
                break
        pattern_items.append({
            'index': i,
            'images': el['images'],
            'answer': ans_text,
            'explain': explain_text.strip()
        })

print(f"\nCataloged {len(pattern_items)} Pattern items:")
for pi in pattern_items[:15]:
    print(f"  Img: {pi['images']} | Ans: {pi['answer']} | Explain: {pi['explain'][:50]}")
