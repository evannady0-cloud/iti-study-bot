import json

bank_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\large_iq_bank.json'
models_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\exam_models.json'
js_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\bank_data.js'

with open(bank_path, 'r', encoding='utf-8') as f:
    bank = json.load(f)

with open(models_path, 'r', encoding='utf-8') as f:
    models = json.load(f)

q107_reasoning = """💡 <b>الإجابة الصحيحة هي: E</b>

🔍 <b>القاعدة الحاكمة للهرم (قاعدة الحذف والدمج / XOR):</b>
كل دائرة في الصف الأعلى ناتجة من الدائرتين الواقعتين تحتها مباشرة حسب القاعدة التالية:
• <b>العنصر الموجود في دائرة واحدة فقط ⬅️ ينتقل للأعلى.</b>
• <b>العنصر المكرر في الدائرتين معاً ⬅️ يُحذف (يلغي بعضه).</b>

<b>التطبيق لإيجاد الدائرة (?) في قمة الهرم:</b>
الدائرتان الواقعتان تحت علامة الاستفهام مباشرة هما:
1. <b>الدائرة اليسرى:</b> تحتوي على (نقطة سوداء في المركز + دائرة بيضاء صغيرة بالأسفل).
2. <b>الدائرة اليمنى:</b> تحتوي على (نقطة سوداء في المركز + دائرة بيضاء صغيرة بالأسفل + قوس نصف دائري).

<b>النتيجة:</b>
• <b>النقطة السوداء في المركز:</b> مكررة في الاثنين ⬅️ <b>تُحذف كلياً.</b>
• <b>الدائرة البيضاء بالأسفل:</b> مكررة في الاثنين ⬅️ <b>تُحذف كلياً.</b>
• <b>القوس المنحني:</b> موجود في الدائرة اليمنى فقط ⬅️ <b>ينتقل وحده للأعلى.</b>

إذن الدائرة المطلوبة في القمة تحتوي على <b>القوس فقط</b> بدون أي نقاط، وهو تماماً <b>الشكل E</b>."""

for q in bank:
    if q.get('id') == 107 or (q.get('image') and 'ultimate_test3_q27.png' in q['image']):
        q['question'] = "Which circle should replace the question mark? A B C D E"
        q['options'] = ["A", "B", "C", "D", "E"]
        q['correct'] = 4 # E
        q['reasoning'] = q107_reasoning

for m, qs in models['iq'].items():
    for q in qs:
        if q.get('id') == 107 or (q.get('image') and 'ultimate_test3_q27.png' in q['image']):
            q['question'] = "Which circle should replace the question mark? A B C D E"
            q['options'] = ["A", "B", "C", "D", "E"]
            q['correct'] = 4 # E
            q['reasoning'] = q107_reasoning

with open(bank_path, 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)

with open(models_path, 'w', encoding='utf-8') as f:
    json.dump(models, f, ensure_ascii=False, indent=2)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write('window.EXAM_MODELS = ' + json.dumps(models, ensure_ascii=False) + ';\n')

print("Fixed ID 107 to Option E successfully!")
