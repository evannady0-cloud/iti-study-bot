import json

bank_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\large_iq_bank.json'
models_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\exam_models.json'
js_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\bank_data.js'

with open(bank_path, 'r', encoding='utf-8') as f:
    bank = json.load(f)

with open(models_path, 'r', encoding='utf-8') as f:
    models = json.load(f)

q243_reasoning = """💡 <b>الإجابة الصحيحة رياضياً هي: Switch B (الاختيار B)</b>

🔍 <b>الإثبات الرياضي القاطع خطوة بخطوة:</b>
ترتيب تشغيل المفاتيح المعطى في المسألة هو: <b>C ثم A ثم B ثم D</b>

1. <b>مقارنة البداية بالنتيجة (Figure 1 ➡️ Figure 2):</b>
• <b>اللمبة 1:</b> كانت مطفية ⚪ وفضلت مطفية ⚪ <i>(لم تتغير)</i>
• <b>اللمبة 2:</b> كانت مطفية ⚪ وبقت منورة ⚫ <b>(اتغيرت!)</b>
• <b>اللمبة 3:</b> كانت منورة ⚫ وفضلت منورة ⚫ <i>(لم تتغير)</i>
• <b>اللمبة 4:</b> كانت منورة ⚫ وبقت مطفية ⚪ <b>(اتغيرت!)</b>

2. <b>كشف المفتاح المعطل في 3 ثوانٍ:</b>
• اللمبتان الوحيدتان اللتان تغيرت حالتهما هما <b>2 و 4</b>.
• بالنظر لمعطيات المسألة: المفتاح الوحيد المسؤول عن اللمبتين 2 و 4 معاً هو <b>Switch B</b>:
<code>Switch B turns lights 2 and 4 on/off or off/on</code>
• بما أن اللمبتين 2 و 4 انقلبتا مرة واحدة فقط (بدلاً من مرتين)، فهذا يثبت أن <b>Switch B معطل ولم يعمل إطلاقاً!</b>

3. <b>تأكيد التتبع عند تعطل Switch B:</b>
• البداية (Figure 1): <code>[1: OFF, 2: OFF, 3: ON, 4: ON]</code>
• تشغيل C (يقلب 1 و 3): <code>[1: ON, 2: OFF, 3: OFF, 4: ON]</code>
• تشغيل A (يقلب 1 و 2): <code>[1: OFF, 2: ON, 3: OFF, 4: ON]</code>
• المفتاح B <b>(معطل - تم تخطيه)</b>: يبقى <code>[1: OFF, 2: ON, 3: OFF, 4: ON]</code>
• تشغيل D (يقلب 3 و 4): <code>[1: OFF, 2: ON, 3: ON, 4: OFF]</code> ➡️ <b>تطابق Figure 2 بنسبة 100%!</b>

<i>⚠️ تنبيه: لو كان Switch D هو المعطل، لكانت النتيجة أن جميع اللمبات الأربعة مطفية كلياً [OFF, OFF, OFF, OFF] وهذا يناقض Figure 2 تماماً.</i>"""

for q in bank:
    if q.get('id') == 243 or (q.get('image') and 'image205.png' in q['image']):
        q['correct'] = 1 # Switch B
        q['reasoning'] = q243_reasoning

for m, qs in models['iq'].items():
    for q in qs:
        if q.get('id') == 243 or (q.get('image') and 'image205.png' in q['image']):
            q['correct'] = 1 # Switch B
            q['reasoning'] = q243_reasoning

with open(bank_path, 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)

with open(models_path, 'w', encoding='utf-8') as f:
    json.dump(models, f, ensure_ascii=False, indent=2)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write('window.EXAM_MODELS = ' + json.dumps(models, ensure_ascii=False) + ';\n')

print("Successfully fixed ID 243 to Switch B across all files!")
