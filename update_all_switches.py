# -*- coding: utf-8 -*-
import json, os, sys

switch_data = {
    241: {
        'switch': 'Switch C', 'opt': 'C', 'correct': 2, 'lights_changed': '1 و 3',
        'fig1': '(0, 0, 1, 0)', 'fig2': '(1, 0, 0, 0)', 'seq': 'C ➔ B ➔ D ➔ A',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (0, 0, 1, 0)',
            '2. المفتاح C (معطل): لا يحدث أي تغيير -> الحالة تظل (0, 0, 1, 0)',
            '3. المفتاح B (يعمل): يقلب المصباحين 2 و 4 -> تصبح (0, 1, 1, 1)',
            '4. المفتاح D (يعمل): يقلب المصباحين 3 و 4 -> تصبح (0, 1, 0, 0)',
            '5. المفتاح A (يعمل): يقلب المصباحين 1 و 2 -> تصبح (1, 0, 0, 0)'
        ]
    },
    242: {
        'switch': 'Switch B', 'opt': 'B', 'correct': 1, 'lights_changed': '2 و 4',
        'fig1': '(0, 1, 0, 1)', 'fig2': '(0, 0, 0, 0)', 'seq': 'B ➔ C ➔ A ➔ D',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (0, 1, 0, 1)',
            '2. المفتاح B (معطل): لا يحدث أي تغيير -> الحالة تظل (0, 1, 0, 1)',
            '3. المفتاح C (يعمل): يقلب المصباحين 1 و 3 -> تصبح (1, 1, 1, 1)',
            '4. المفتاح A (يعمل): يقلب المصباحين 1 و 2 -> تصبح (0, 0, 1, 1)',
            '5. المفتاح D (يعمل): يقلب المصباحين 3 و 4 -> تصبح (0, 0, 0, 0)'
        ]
    },
    243: {
        'switch': 'Switch B', 'opt': 'B', 'correct': 1, 'lights_changed': '2 و 4',
        'fig1': '(0, 0, 1, 1)', 'fig2': '(0, 1, 1, 0)', 'seq': 'C ➔ A ➔ B ➔ D',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (0, 0, 1, 1)',
            '2. المفتاح C (يعمل): يقلب المصباحين 1 و 3 -> تصبح (1, 0, 0, 1)',
            '3. المفتاح A (يعمل): يقلب المصباحين 1 و 2 -> تصبح (0, 1, 0, 1)',
            '4. المفتاح B (معطل): لا يحدث أي تغيير -> الحالة تظل (0, 1, 0, 1)',
            '5. المفتاح D (يعمل): يقلب المصباحين 3 و 4 -> تصبح (0, 1, 1, 0)'
        ]
    },
    244: {
        'switch': 'Switch C', 'opt': 'C', 'correct': 2, 'lights_changed': '1 و 3',
        'fig1': '(0, 1, 1, 0)', 'fig2': '(1, 1, 0, 0)', 'seq': 'D ➔ A ➔ B ➔ C',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (0, 1, 1, 0)',
            '2. المفتاح D (يعمل): يقلب المصباحين 3 و 4 -> تصبح (0, 1, 0, 1)',
            '3. المفتاح A (يعمل): يقلب المصباحين 1 و 2 -> تصبح (1, 0, 0, 1)',
            '4. المفتاح B (يعمل): يقلب المصباحين 2 و 4 -> تصبح (1, 1, 0, 0)',
            '5. المفتاح C (معطل): لا يحدث أي تغيير -> الحالة تظل (1, 1, 0, 0)'
        ]
    },
    245: {
        'switch': 'Switch D', 'opt': 'D', 'correct': 3, 'lights_changed': '3 و 4',
        'fig1': '(1, 1, 0, 0)', 'fig2': '(1, 1, 1, 1)', 'seq': 'C ➔ A ➔ D ➔ B',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (1, 1, 0, 0)',
            '2. المفتاح C (يعمل): يقلب المصباحين 1 و 3 -> تصبح (0, 1, 1, 0)',
            '3. المفتاح A (يعمل): يقلب المصباحين 1 و 2 -> تصبح (1, 0, 1, 0)',
            '4. المفتاح D (معطل): لا يحدث أي تغيير -> الحالة تظل (1, 0, 1, 0)',
            '5. المفتاح B (يعمل): يقلب المصباحين 2 و 4 -> تصبح (1, 1, 1, 1)'
        ]
    },
    246: {
        'switch': 'Switch A', 'opt': 'A', 'correct': 0, 'lights_changed': '1 و 2',
        'fig1': '(1, 1, 0, 1)', 'fig2': '(0, 0, 0, 1)', 'seq': 'C ➔ B ➔ A ➔ D',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (1, 1, 0, 1)',
            '2. المفتاح C (يعمل): يقلب المصباحين 1 و 3 -> تصبح (0, 1, 1, 1)',
            '3. المفتاح B (يعمل): يقلب المصباحين 2 و 4 -> تصبح (0, 0, 1, 0)',
            '4. المفتاح A (معطل): لا يحدث أي تغيير -> الحالة تظل (0, 0, 1, 0)',
            '5. المفتاح D (يعمل): يقلب المصباحين 3 و 4 -> تصبح (0, 0, 0, 1)'
        ]
    },
    247: {
        'switch': 'Switch A', 'opt': 'A', 'correct': 0, 'lights_changed': '1 و 2',
        'fig1': '(0, 1, 1, 0)', 'fig2': '(1, 0, 1, 0)', 'seq': 'D ➔ C ➔ B ➔ A',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (0, 1, 1, 0)',
            '2. المفتاح D (يعمل): يقلب المصباحين 3 و 4 -> تصبح (0, 1, 0, 1)',
            '3. المفتاح C (يعمل): يقلب المصباحين 1 و 3 -> تصبح (1, 1, 1, 1)',
            '4. المفتاح B (يعمل): يقلب المصباحين 2 و 4 -> تصبح (1, 0, 1, 0)',
            '5. المفتاح A (معطل): لا يحدث أي تغيير -> الحالة تظل (1, 0, 1, 0)'
        ]
    },
    248: {
        'switch': 'Switch D', 'opt': 'D', 'correct': 3, 'lights_changed': '3 و 4',
        'fig1': '(0, 1, 0, 1)', 'fig2': '(0, 1, 1, 0)', 'seq': 'A ➔ D ➔ B ➔ C',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (0, 1, 0, 1)',
            '2. المفتاح A (يعمل): يقلب المصباحين 1 و 2 -> تصبح (1, 0, 0, 1)',
            '3. المفتاح D (معطل): لا يحدث أي تغيير -> الحالة تظل (1, 0, 0, 1)',
            '4. المفتاح B (يعمل): يقلب المصباحين 2 و 4 -> تصبح (1, 1, 0, 0)',
            '5. المفتاح C (يعمل): يقلب المصباحين 1 و 3 -> تصبح (0, 1, 1, 0)'
        ]
    },
    249: {
        'switch': 'Switch A', 'opt': 'A', 'correct': 0, 'lights_changed': '1 و 2',
        'fig1': '(0, 1, 0, 0)', 'fig2': '(1, 0, 0, 0)', 'seq': 'B ➔ A ➔ C ➔ D',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (0, 1, 0, 0)',
            '2. المفتاح B (يعمل): يقلب المصباحين 2 و 4 -> تصبح (0, 0, 0, 1)',
            '3. المفتاح A (معطل): لا يحدث أي تغيير -> الحالة تظل (0, 0, 0, 1)',
            '4. المفتاح C (يعمل): يقلب المصباحين 1 و 3 -> تصبح (1, 0, 1, 1)',
            '5. المفتاح D (يعمل): يقلب المصباحين 3 و 4 -> تصبح (1, 0, 0, 0)'
        ]
    },
    250: {
        'switch': 'Switch D', 'opt': 'D', 'correct': 3, 'lights_changed': '3 و 4',
        'fig1': '(0, 0, 1, 1)', 'fig2': '(0, 0, 0, 0)', 'seq': 'D ➔ B ➔ A ➔ C',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (0, 0, 1, 1)',
            '2. المفتاح D (معطل): لا يحدث أي تغيير -> الحالة تظل (0, 0, 1, 1)',
            '3. المفتاح B (يعمل): يقلب المصباحين 2 و 4 -> تصبح (0, 1, 1, 0)',
            '4. المفتاح A (يعمل): يقلب المصباحين 1 و 2 -> تصبح (1, 0, 1, 0)',
            '5. المفتاح C (يعمل): يقلب المصباحين 1 و 3 -> تصبح (0, 0, 0, 0)'
        ]
    },
    251: {
        'switch': 'Switch C', 'opt': 'C', 'correct': 2, 'lights_changed': '1 و 3',
        'fig1': '(0, 0, 0, 1)', 'fig2': '(1, 0, 1, 1)', 'seq': 'A ➔ C ➔ D ➔ B',
        'steps': [
            '1. البداية (Figure 1): الحالة هي (0, 0, 0, 1)',
            '2. المفتاح A (يعمل): يقلب المصباحين 1 و 2 -> تصبح (1, 1, 0, 1)',
            '3. المفتاح C (معطل): لا يحدث أي تغيير -> الحالة تظل (1, 1, 0, 1)',
            '4. المفتاح D (يعمل): يقلب المصباحين 3 و 4 -> تصبح (1, 1, 1, 0)',
            '5. المفتاح B (يعمل): يقلب المصباحين 2 و 4 -> تصبح (1, 0, 1, 1)'
        ]
    }
}

def make_reasoning(d):
    steps_txt = '\n'.join('• ' + s for s in d['steps'])
    return (
        f"💡 <b>الإجابة الصحيحة رياضياً هي: {d['switch']} (الاختيار {d['opt']})</b>\n\n"
        f"🔍 <b>قاعدة الحل السريع في 5 ثوانٍ (قاعدة التغيير الصافي Net Change):</b>\n"
        f"• الدائرة بها 4 مصابيح (● = مضاء ON، ○ = مطفأ OFF):\n"
        f"  - المفتاح A يقلب المصباحين (1 و 2)\n"
        f"  - المفتاح B يقلب المصباحين (2 و 4)\n"
        f"  - المفتاح C يقلب المصباحين (1 و 3)\n"
        f"  - المفتاح D يقلب المصباحين (3 و 4)\n\n"
        f"• <b>السر الرياضي:</b> كل مصباح في الدائرة متصل بمفتاحين بالضبط!\n"
        f"  إذا كانت جميع المفاتيح تعمل، سينقلب كل مصباح مرتين (عدد زوجي)، وبالتالي يعود لحالته الأصلية تماماً دون أي تغيير (Figure 2 يطابق Figure 1).\n"
        f"• عند تعطل مفتاح واحد، المصباحان المتصلان به فقط ينقلبان مرة واحدة ويتغيران، بينما المصباحان الآخران يظلان دون تغيير!\n\n"
        f"📌 <b>التطبيق المباشر على المسألة:</b>\n"
        f"• الحالة الابتدائية (Figure 1): {d['fig1']}\n"
        f"• الحالة النهائية (Figure 2): {d['fig2']}\n"
        f"• المصابيح التي تغيرت حالتها فقط: <b>المصباحان {d['lights_changed']}</b>!\n"
        f"• المفتاح المسؤول عن المصباحين ({d['lights_changed']}) هو <b>{d['switch']}</b>، إذن هو المفتاح المعطل!\n\n"
        f"📋 <b>التأكيد الرياضي خطوة بخطوة (ترتيب المفاتيح: {d['seq']}):</b>\n"
        f"{steps_txt}\n"
        f"✅ <b>النتيجة النهائية تطابق Figure 2 تماماً!</b>"
    )

bot_dir = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot'

# 1. Update large_iq_bank.json
large_path = os.path.join(bot_dir, 'large_iq_bank.json')
with open(large_path, 'r', encoding='utf-8') as f:
    bank = json.load(f)

updated_count = 0
for q in bank:
    qid = q.get('id')
    if qid in switch_data:
        d = switch_data[qid]
        q['correct'] = d['correct']
        q['reasoning'] = make_reasoning(d)
        updated_count += 1

with open(large_path, 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)
print(f'Updated {updated_count} questions in large_iq_bank.json')

# 2. Update exam_models.json
models_path = os.path.join(bot_dir, 'exam_models.json')
with open(models_path, 'r', encoding='utf-8') as f:
    models = json.load(f)

models_updated = 0
for cat, sub in models.items():
    for mname, qlist in sub.items():
        for q in qlist:
            qid = q.get('id')
            if qid in switch_data:
                d = switch_data[qid]
                q['correct'] = d['correct']
                q['reasoning'] = make_reasoning(d)
                models_updated += 1

with open(models_path, 'w', encoding='utf-8') as f:
    json.dump(models, f, ensure_ascii=False, indent=2)
print(f'Updated {models_updated} entries in exam_models.json')

# 3. Update bank_data.js
bank_data_path = os.path.join(bot_dir, 'bank_data.js')
if os.path.exists(bank_data_path):
    with open(bank_data_path, 'r', encoding='utf-8') as f:
        content = f.read()
    prefix = 'window.EXAM_MODELS = '
    if content.startswith(prefix):
        with open(bank_data_path, 'w', encoding='utf-8') as f:
            f.write(prefix + json.dumps(models, ensure_ascii=False) + ';')
        print('Updated bank_data.js successfully!')

print('ALL SWITCHES UPDATED AND SYNCHRONIZED!')
