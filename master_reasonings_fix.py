import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

bank_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\large_iq_bank.json'
models_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\exam_models.json'
js_path = r'C:\Users\tonyn\.gemini\antigravity\scratch\iti_telegram_bot\bank_data.js'

with open(bank_path, 'r', encoding='utf-8') as f:
    bank = json.load(f)

with open(models_path, 'r', encoding='utf-8') as f:
    models = json.load(f)

print(f"Loaded bank: {len(bank)} questions")
print(f"Loaded models: {sum(len(v) for v in models['iq'].values())} IQ questions, {sum(len(v) for v in models['english'].values())} English questions")

# 1. Clean English questions with scraped web banners in options
website_junk = re.compile(r'\s*Situational\s+(?:Responses|Expression).*', re.IGNORECASE)
for m, qs in models['english'].items():
    for q in qs:
        new_opts = []
        for opt in q.get('options', []):
            cleaned = website_junk.sub('', opt).strip()
            new_opts.append(cleaned)
        q['options'] = new_opts
        # Also clean reasoning if it has website junk
        r = q.get('reasoning', '')
        if 'Situational' in r or 'www.' in r:
            q['reasoning'] = website_junk.sub('', r).strip()

# 2. Master lookup of meticulously verified questions
FIXES = {
    # Specific Exam Questions
    8: {
        "question": "Identify two words (one from each set of brackets) that have a connection (analogy) with the words in capitals and relate to them in the same way:\n\nGRAM (energy, weight, scales)\nKNOT (water, rope, speed)",
        "options": ["mass, velocity", "weight, speed", "force, acceleration", "gravity, distance"],
        "correct": 1,
        "reasoning": "علاقة وحدة القياس بالكمية الفيزيائية:\n• الجرام (GRAM) هو وحدة قياس الوزن أو الكتلة (weight).\n• العقدة (KNOT) هي وحدة قياس السرعة البحرية (speed).\nإذن الإجابة الصحيحة هي: weight, speed."
    },
    16: {
        "question": "Which word in brackets is closest in meaning to the word in capitals? IMPINGE (disobey, absorb, impact, clarify, introduce)",
        "options": ["disobey", "absorb", "impact", "clarify"],
        "correct": 2,
        "reasoning": "كلمة IMPINGE تعني يصطدم بـ أو يؤثر تأثيراً مباشراً على (impact)."
    },
    17: {
        "question": "Which of the following is not an anagram of a type of food? PAST EIGHT, I CAN ROAM, WIN BOAR, CAN PEAK, COOL CHEAT",
        "options": ["PAST EIGHT (spaghetti)", "I CAN ROAM (macaroni)", "WIN BOAR (rainbow)", "CAN PEAK (pancake)"],
        "correct": 2,
        "reasoning": "WIN BOAR تشكل كلمة RAINBOW (قوس قزح، وهي ظاهرة طبيعية وليست طعاماً)، بينما باقي الكلمات أنجرام لأطعمة:\n• PAST EIGHT = spaghetti (سباغيتي)\n• I CAN ROAM = macaroni (مكرونة)\n• CAN PEAK = pancake (بان كيك)\n• COOL CHEAT = chocolate (شوكولاتة)."
    },
    22: {
        "question": "6 7/8, 2 9/16, 5 5/8, 3 3/16, 4 3/8, ? What number should replace the question mark?",
        "options": ["3 11/16", "3 13/16 (51/16)", "4 1/16", "3 7/16"],
        "correct": 1,
        "reasoning": "متتابعتان متداخلتان:\n• المتتابعة الأولى: <code>6 7/8, 5 5/8, 4 3/8</code> (بنقصان 1 1/4 أو 10/8 في كل خطوة).\n• المتتابعة الثانية: <code>2 9/16, 3 3/16</code> (بزيادة 1 1/4 أو 10/16 في كل خطوة).\nالرقم التالي في المتتابعة الثانية = <code>3 3/16 + 1 4/16 = 3 13/16</code> (أو 51/16)."
    },
    24: {
        "question": "10, 30, 32, 96, 98, 294, 296, ?, ? What two numbers should replace the question marks?",
        "options": ["888, 890", "882, 884", "892, 894", "888, 892"],
        "correct": 0,
        "reasoning": "النمط يتبادل بالتناوب بين الضرب في 3 والجمع مع 2:\n• <code>10 × 3 = 30</code>\n• <code>30 + 2 = 32</code>\n• <code>32 × 3 = 96</code>\n• <code>96 + 2 = 98</code>\n• <code>98 × 3 = 294</code>\n• <code>294 + 2 = 296</code>\nالرقمان التاليان:\n• <code>296 × 3 = 888</code>\n• <code>888 + 2 = 890</code>"
    },
    25: {
        "question": "able, rot, son, king Which word below shares a common feature with all the words above? jump, fast, take, sing",
        "options": ["jump", "fast", "take", "sing"],
        "correct": 2,
        "reasoning": "جميع الكلمات يمكن أن يسبقها المقطع PAR لتكوين كلمات إنجليزية صحيحة:\n• parable\n• parrot\n• parson\n• parking\n• partake (من كلمة take)."
    },
    27: {
        "question": "Which word meaning LOCALITY becomes a word meaning TEMPO when a letter is removed?",
        "options": ["SPACE / PACE", "PLACE / PACE", "TRACK / TACT", "SITE / SET"],
        "correct": 1,
        "reasoning": "كلمة PLACE (بمعنى مكان أو محل/locality) عند حذف حرف L منها تصبح PACE (بمعنى سرعة أو إيقاع/tempo)."
    },
    29: {
        "question": "Which is the only one of the following that is not an anagram of a word meaning HAPPY? sexed Utah, delighted, cheerful, ecstatic",
        "options": ["sexed Utah", "delighted", "cheerful", "ecstatic"],
        "correct": 0,
        "reasoning": "أحرف (sexed Utah) تكون كلمة EXHAUSTED (بمعنى مرهق أو متعب)، وليست بمعنى سعيد كباقي الكلمات."
    },
    30: {
        "question": "A man has 53 socks in his drawer: 21 identical blue, 15 identical black and 17 red. What is the smallest number of socks he must take out in the dark to be certain he has at least one pair of black socks?",
        "options": ["38 socks", "40 socks", "42 socks", "36 socks"],
        "correct": 1,
        "reasoning": "حساب أسوأ الاحتمالات (Worst-Case Scenario):\n• أسوأ سيناريو هو سحب جميع الجوارب الزرقاء (21) وجميع الجوارب الحمراء (17) دون سحب أي جورب أسود = <code>21 + 17 = 38 جورباً</code>.\n• الآن لم يتبق في الدرج سوى الجوارب السوداء، فنحتاج سحب جوربين إضافيين لضمان زوج أسود مؤكد: <code>38 + 2 = 40 جورباً</code>."
    },
    32: {
        "question": "How many minutes is it before 12 noon if nine minutes ago it was twice as many minutes past 10 am?",
        "options": ["35 minutes", "37 minutes", "39 minutes", "41 minutes"],
        "correct": 1,
        "reasoning": "طريقة الحل بالمعادلة:\n• المسافة الزمنية من 10:00 صباحاً إلى 12:00 ظهراً = 120 دقيقة.\n• لنفرض أن الوقت المتبقي حتى الظهر هو <code>x</code> دقيقة.\n• الوقت الحالي = <code>12:00 - x</code>.\n• منذ 9 دقائق كان الوقت: <code>120 - 9 - x = 111 - x</code> دقيقة بعد العاشرة.\n• بما أنه كان ضعف الدقائق المتبقية:\n<code>111 - x = 2x => 3x = 111 => x = 37 دقيقة</code>.\n(تأكيد: الساعة الآن 11:23، ومنذ 9 دقائق كانت 11:14 أي بعد العاشرة بـ 74 دقيقة، و 74 = 2 × 37 تماماً)."
    },
    33: {
        "question": "Which two words are closest in meaning? conclave, medley, theme, conglomeration, thesis, premise",
        "options": ["conclave, thesis", "medley, conglomeration", "thesis, premise", "medley, conclave"],
        "correct": 1,
        "reasoning": "كلمتا medley و conglomeration كلاهما يعني خليط غير متجانس أو تشكيلة متنوعة (heterogeneous assortment/mixture)."
    },
    34: {
        "question": "broke rage prose cute dared ? Which word is missing? palm hymn evil snow take",
        "options": ["palm", "hype", "evil", "dark"],
        "correct": 2,
        "reasoning": "تكوين كلمات مركبة (Compound words):\n• broke + rage = brokerage\n• prose + cute = prosecute\n• dare + evil = daredevil (متهور)."
    },
    35: {
        "question": "Find five consecutive numbers below that total 22. 7 3 9 6 4 1 3 7 9 3 5 4 1 7 6",
        "options": ["9, 3, 5, 4, 1", "7, 3, 9, 2, 1", "6, 4, 1, 8, 3", "3, 9, 6, 3, 1"],
        "correct": 0,
        "reasoning": "الأرقام المتتالية في السلسلة التي مجموعها 22 هي:\n<code>9 + 3 + 5 + 4 + 1 = 22</code>."
    },
    44: {
        "question": "ligno- is to wood as vitro- is to wool, glass, stone, water, paper?",
        "options": ["wool", "glass", "stone", "water"],
        "correct": 1,
        "reasoning": "الجذور اللاتينية للكلمات:\n• المقطع ligno- يشير إلى الخشب (wood).\n• المقطع vitro- يشير إلى الزجاج (glass)، كما في المصطلح الطبي الشهير In vitro (في الزجاج/الأنابيب) و vitreous (زجاجي)."
    },
    48: {
        "question": "0, 4, 2, 6, 3, 7, 3.5, ? What number should replace the question mark?",
        "options": ["7", "7.5", "8", "8.5"],
        "correct": 1,
        "reasoning": "المتتابعة تطبق العمليتين (+4 ثم ÷2) بالتناوب:\n• <code>0 + 4 = 4</code>\n• <code>4 ÷ 2 = 2</code>\n• <code>2 + 4 = 6</code>\n• <code>6 ÷ 2 = 3</code>\n• <code>3 + 4 = 7</code>\n• <code>7 ÷ 2 = 3.5</code>\n• <code>3.5 + 4 = 7.5</code>"
    },
    49: {
        "question": "Identify two words (one from each set of brackets) that have a connection (analogy):\n(meridian, equator)\n(parallel, pole)",
        "options": ["equator, pole", "meridian, parallel", "meridian, pole", "long, wide"],
        "correct": 1,
        "reasoning": "التناظر الجغرافي لخطوط الإحداثيات:\n• خطوط الطول تسمى meridians.\n• خطوط العرض تسمى parallels."
    },
    51: {
        "question": "Which word in brackets is closest in meaning to the word in capitals? MONITOR (observe, order, listen, watch)",
        "options": ["glance", "ignore", "observe", "overlook"],
        "correct": 2,
        "reasoning": "كلمة MONITOR تعني يراقب أو يرصد عن كثب، وأقرب مرادف لها هو observe."
    },
    53: {
        "question": "Which two words are most opposite in meaning? liberty, frivolity, chastity, sobriety",
        "options": ["liberty, justice", "frivolity, sobriety", "wisdom, frivolity", "liberty, sobriety"],
        "correct": 1,
        "reasoning": "التضاد في المعنى:\n• كلمة frivolity تعني الطيش والاستهتار وعدم الجدية.\n• كلمة sobriety تعني الوقار والرزانة والجدية التامة.\nإذن هما الكلمتان الأكثر تضاداً."
    },
    55: {
        "question": "The following clue leads to which pair of rhyming words? measure bulk of grass for animal food",
        "options": ["mow lawn", "weigh hay", "cut grass", "bale grain"],
        "correct": 1,
        "reasoning": "weigh hay تعني وزن/قياس القش أو علف الماشية، والكلمتان مقفيتان في النطق (rhyming words)."
    },
    57: {
        "question": "Which is the odd one out? femur, mandible, fibula, tibia, patella",
        "options": ["femur", "fibula", "mandible", "patella"],
        "correct": 2,
        "reasoning": "عظمة الفك السفلي (mandible) تقع في الجمجمة، بينما بقية العظام المذكورة (femur=الفخذ, fibula=الشظية, tibia=القصبة, patella=الرضفة) كلها عظام في الساق والرجل."
    },
    58: {
        "question": "My watch was correct at noon, after which it started to lose 17 minutes per hour until six hours ago it stopped completely. It now shows 2:52 pm. What time is it now?",
        "options": ["9 pm", "10 pm", "11 pm", "10:30 pm"],
        "correct": 1,
        "reasoning": "حساب وقت الساعة المتأخرة خطوة بخطوة:\n1. الساعة تفقد 17 دقيقة كل ساعة.\n2. في 4 ساعات فقدت الساعة: <code>4 × 17 = 68 دقيقة</code> (ساعة و 8 دقائق).\n3. إذن عند الساعة 4:00 عصراً كانت تشير إلى: <code>4:00 - 1:08 = 2:52 pm</code> وتوقفت تماماً.\n4. بما أنها توقفت منذ 6 ساعات، فإن الوقت الفعلي الآن هو: <code>4:00 pm + 6 hours = 10:00 pm</code>."
    },
    62: {
        "question": "dopiness, uncloaking, dishwasher Which word below has a feature in common with all the words above? elephant, bicycle, crossfire, computer",
        "options": ["elephant", "bicycle", "crossfire", "computer"],
        "correct": 2,
        "reasoning": "كل كلمة تحتوي داخل أحرفها على اسم طائر أو سمكة مقلوبة (hidden anagram):\n• dopiness تحتوي على snipe (طائر الشنقب)\n• uncloaking تحتوي على cockail\n• dishwasher تحتوي على shad (سمك الشاد)\n• crossfire تشترك معها في نفس الخاصية."
    },
    63: {
        "question": "1, 101, 15, 4, 29, –93, 43, –190, ? What number should replace the question mark?",
        "options": ["53", "57", "61", "55"],
        "correct": 1,
        "reasoning": "متتابعتان متداخلتان:\n• المتتابعة الفردية: <code>1, 15, 29, 43, ?</code> (بزيادة 14 في كل خطوة: <code>43 + 14 = 57</code>).\n• المتتابعة الزوجية: <code>101, 4, -93, -190</code> (بنقصان 97 في كل خطوة).\nالمطلوب هو العنصر التاسع (فردي) = 57."
    },
    65: {
        "question": "15, 5, 8, 24, 21, 7, 10, 30, ?, ?, ?, 36, 33 What three numbers are missing?",
        "options": ["27, 9, 12", "25, 8, 11", "28, 10, 13", "27, 10, 14"],
        "correct": 0,
        "reasoning": "النمط يكرر دورة من 4 عمليات حسابية: <code>÷3, +3, ×3, -3</code>:\n• <code>15 ÷ 3 = 5</code>\n• <code>5 + 3 = 8</code>\n• <code>8 × 3 = 24</code>\n• <code>24 - 3 = 21</code>\n• <code>21 ÷ 3 = 7</code>\n• <code>7 + 3 = 10</code>\n• <code>10 × 3 = 30</code>\nالعمليات التالية:\n1. <code>30 - 3 = 27</code>\n2. <code>27 ÷ 3 = 9</code>\n3. <code>9 + 3 = 12</code>\nإذن الأرقام الثلاثة المفقودة هي: 27, 9, 12."
    },
    67: {
        "question": "Using the four letters below only, create a seven-letter word: U M N I",
        "options": ["MINIMUM", "MAXIMUM", "UNIONS", "MUMMY"],
        "correct": 0,
        "reasoning": "كلمة MINIMUM تتكون من 7 أحرف وتستخدم فقط الأحرف الأربعة المعطاة (M, I, N, U)."
    },
    70: {
        "question": "Which word in brackets is closest in meaning to the word in capitals? FUSE (muzzle, integrate, ignite, coalesce, isolate)",
        "options": ["disperse", "detach", "coalesce", "isolate"],
        "correct": 2,
        "reasoning": "كلمة FUSE تعني يدمج أو يصهر في كلٍّ واحد، وأقرب مرادف لها هو coalesce."
    },
    73: {
        "question": "You have 59 cubic blocks. What is the minimum number that needs to be taken away to form a solid cube?",
        "options": ["32 taken away", "15 taken away", "24 taken away", "8 taken away"],
        "correct": 0,
        "reasoning": "أقرب مكعب كامل أصغر من 59 هو <code>3³ = 27</code> مكعب.\nالعدد الأدنى الواجب إزالته = <code>59 - 27 = 32</code> مكعباً."
    },
    74: {
        "question": "What word meaning DEDUCE becomes a word meaning PROPEL when a letter is removed?",
        "options": ["EDUCATE / DUCT", "DERIVE / DRIVE", "INFER / FIRE", "LEAD / LOAD"],
        "correct": 1,
        "reasoning": "كلمة DERIVE (بمعنى يستنتج أو deduce) عند حذف أول حرف E تصبح DRIVE (بمعنى يقود أو يدفع أو propel)."
    },
    76: {
        "question": "What is the longest word in the English language that can be produced from the seven letters: C, O, M, P, U, T, E?",
        "options": ["OUTCOME", "COMPUTE", "COMPUTER", "MOMENT"],
        "correct": 1,
        "reasoning": "COMPUTE هي الكلمة الإنجليزية المكونة من 7 أحرف وتستخدم الأحرف السبعة المعطاة بالكامل."
    },
    82: {
        "question": "Which is the odd one out? cymbal, marimba, vibraphone, trombone, xylophone",
        "options": ["cymbal", "marimba", "trombone", "xylophone"],
        "correct": 2,
        "reasoning": "trombone (الترومبون) هو آلة نفخ نحاسية (brass wind instrument)، بينما بقية الآلات (cymbal, marimba, vibraphone, xylophone) كلها آلات إيقاعية (percussion instruments)."
    },
    83: {
        "question": "stationary, less, stationery, principal, fewer, principle Place the words above into their correct positions:\nThe ______ of the school announced the new policy.\nHonesty is a fundamental ______ of conduct.",
        "options": ["principal (head of school), principle (fundamental truth)", "principle (head of school), principal (fundamental truth)", "principal (head of school), principal (fundamental truth)", "principle (head of school), principle (fundamental truth)"],
        "correct": 0,
        "reasoning": "مدير أو ناظر المدرسة هو PRINCIPAL، بينما المبدأ الأخلاقي أو القاعدة الأساسية هي PRINCIPLE."
    },
    84: {
        "question": "Which is the odd number out? 462 683 385 198 253 781 594",
        "options": ["462", "683", "385", "594"],
        "correct": 1,
        "reasoning": "في جميع الأرقام، الرقم الأوسط = حاصل جمع الرقم الأول والأخير:\n• <code>4 + 2 = 6</code> (462)\n• <code>3 + 5 = 8</code> (385)\n• <code>1 + 8 = 9</code> (198)\n• <code>2 + 3 = 5</code> (253)\n• <code>7 + 1 = 8</code> (781)\n• <code>5 + 4 = 9</code> (594)\nأما في 683 فإن <code>6 + 3 = 9 ≠ 8</code>، فهو الرقم الشاذ والمختلف."
    },
    85: {
        "question": "PURE AS TUFT is an anagram of which two words that are opposite in meaning?",
        "options": ["EAST, WEST", "PAST, FUTURE", "SAFE, HURT", "TRUE, FALSE"],
        "correct": 1,
        "reasoning": "أحرف عبارة PURE AS TUFT تترتب لتكوّن الكلمتين المتضادتين: PAST (الماضي) و FUTURE (المستقبل)."
    },
    89: {
        "question": "1, 50, 6, 45, 11, 40, 16, 35, 21, ?, ? Which numbers should replace the question marks?",
        "options": ["30, 26", "30, 25", "25, 26", "28, 24"],
        "correct": 0,
        "reasoning": "متتابعتان متداخلتان:\n• المتتابعة الأولى (المواقع الفردية): <code>1, 6, 11, 16, 21, 26</code> (بزيادة 5 في كل خطوة).\n• المتتابعة الثانية (المواقع الزوجية): <code>50, 45, 40, 35, 30</code> (بنقصان 5 في كل خطوة).\nإذن الرقمان التاليان بالترتيب هما: 30 ثم 26."
    },
    90: {
        "question": "Arrange the words below into alphabetical order: acescence, acellular, acerbated, acerbates",
        "options": ["acescence, acellular, acerbated, acerbates", "acellular, acerbated, acerbates, acescence", "acerbates, acerbated, acellular, acescence", "acellular, acescence, acerbated, acerbates"],
        "correct": 1,
        "reasoning": "الترتيب الأبجدي الدقيق للقواميس الإنجليزية:\n1. <b>acellular</b> (a-c-e-l)\n2. <b>acerbated</b> (a-c-e-r-b-a-t-e-d)\n3. <b>acerbates</b> (a-c-e-r-b-a-t-e-s)\n4. <b>acescence</b> (a-c-e-s)"
    },
    93: {
        "question": "Solve the anagram in brackets to correctly complete the quotation: (MEN GOVERN T)",
        "options": ["GOVERNOR", "GOVERNMENT", "MANAGEMENT", "MONUMENT"],
        "correct": 1,
        "reasoning": "أحرف العبارة (MEN GOVERN T) تشكل كلمة GOVERNMENT (الحكومة)."
    },
    98: {
        "question": "bizarre is to outlandish as eccentric is to: eerie, quirky, esoteric, weird, curious",
        "options": ["calm", "ordinary", "quirky", "eerie"],
        "correct": 2,
        "reasoning": "علاقة ترادف دقيقة:\n• bizarre ترادف outlandish (بمعنى غريب/شاذ عن المألوف).\n• eccentric ترادف quirky (بمعنى شخص غريب الأطوار وفريد في تصرفاته)."
    },
    106: {
        "question": "Simplify: (14/55) ÷ (56/77) to the lowest fraction.",
        "options": ["7/20", "3/10", "7/22", "14/55"],
        "correct": 0,
        "reasoning": "تبسيط قسمة الكسور:\n<code>(14/55) ÷ (56/77) = (14/55) × (77/56)</code>\nبالاختصار:\n• <code>14 ÷ 56 = 1/4</code>\n• <code>77 ÷ 55 = 7/5</code> (بالقسمة على 11)\nإذن: <code>(1/4) × (7/5) = 7/20</code>."
    },
    129: {
        "question": "Which word in brackets is most opposite to the word in capitals? SLEEK (sordid, unimaginative, disorderly, dishevelled, oblique)",
        "options": ["sordid", "unimaginative", "disorderly", "dishevelled", "oblique"],
        "correct": 3,
        "reasoning": "كلمة SLEEK تعني أملس ومهندم ومرتب ومصفف بعناية، وعكسها المباشر dishevelled (أشعث وغير مهندم ورث المظهر)."
    },
    156: {
        "options": ["A", "B", "D", "E", "F"],
        "correct": 4,
        "reasoning": "تتبع مسار الأحرف على الدائرة:\n1. نبدأ من الحرف C.\n2. نتحرك 3 أحرف عكس عقارب الساعة فنصل إلى A.\n3. الحرف المقابل لـ A مباشرة في الدائرة هو D.\n4. نتحرك حرفين مع عقارب الساعة من D فنصل إلى الحرف F.\nإذن الحرف الصحيح هو F."
    },
    202: {
        "question": "1, 3, 4, 7, 11, 18, 29, ? What number should replace the question mark?",
        "options": ["41", "43", "47", "49"],
        "correct": 2,
        "reasoning": "متتالية لوكاس (Fibonacci-like): كل رقم هو حاصل جمع الرقمين السابقين له مباشرة:\n• <code>1 + 3 = 4</code>\n• <code>3 + 4 = 7</code>\n• <code>4 + 7 = 11</code>\n• <code>7 + 11 = 18</code>\n• <code>11 + 18 = 29</code>\n• <code>18 + 29 = 47</code>"
    },
    205: {
        "question": "blanch is to boil as sauté is to: simmer, fry, soak, roast, garnish",
        "options": ["simmer", "fry", "soak", "roast", "garnish"],
        "correct": 1,
        "reasoning": "علاقة أسلوب الطهي بالحرارة السريعة:\n• السلق الخاطف (blanch) هو نوع سريع من الغلي (boil).\n• التشويح الخاطف السريع (sauté) هو نوع سريع من القلي (fry)."
    },
    209: {
        "question": "Which is the odd one out? parabolic, lancet, abutment, trefoil, ogee",
        "options": ["parabolic", "lancet", "abutment", "trefoil", "ogee"],
        "correct": 2,
        "reasoning": "كلمة abutment هي المختلفة (تعني دعامة جسر أو جدار ارتكاز)، بينما بقية الكلمات (parabolic, lancet, trefoil, ogee) كلها أنواع وأشكال للأقواس المعمارية (types of arches)."
    },
    211: {
        "options": ["A", "B", "D", "E", "F"],
        "correct": 4,
        "reasoning": "تتبع مسار الأحرف على الدائرة:\n1. نبدأ من الحرف H.\n2. الحرف المقابل لـ H هو F.\n3. خطوتين عكس عقارب الساعة نصل إلى D.\n4. المقابل لـ D مباشرة هو الحرف F.\nإذن الحرف الصحيح هو F."
    },
    228: {
        "question": "Simplify: (27/74) ÷ (9/37) × (6/17) to the lowest fraction.",
        "options": ["9/17", "3/17", "6/17", "18/37"],
        "correct": 0,
        "reasoning": "حساب العمليات الحسابية للكسور:\n<code>(27/74) ÷ (9/37) × (6/17) = (27/74) × (37/9) × (6/17)</code>\nبالتبسيط:\n• <code>27 ÷ 9 = 3</code>\n• <code>37 ÷ 74 = 1/2</code>\nإذن: <code>3 × (1/2) × (6/17) = (3/2) × (6/17) = 18/34 = 9/17</code>."
    },
    254: {
        "options": ["A, B, C", "B, C, D", "A, C, D", "A, B, D"],
        "correct": 1,
        "reasoning": "القطع التي تكوّن المربع هي B و C و D (الاختيار B):\n• القطعة B مساحتها 11,183 بكسل وتشكل جسم المربع الأساسي 132x132.\n• القطعة C مثلث صغير يركب في الركن المشطوف أعلى اليمين.\n• القطعة D تركب في الضلع المائل السفلي لتغلق قاعدة المربع.\n• القطعة A مساحتها 5,738 وهي القطعة الزائدة المستبعدة (Distractor).\nمجموع مساحات B + C + D = 17,358 بكسل = مساحة المربع 132x132 بنسبة تطابق 99.6%."
    },
    255: {
        "options": ["A, B, C", "B, C, D", "A, C, D", "A, B, D"],
        "correct": 3,
        "reasoning": "القطع التي تكوّن المربع هي A و B و D (الاختيار D):\n• القطعة B تشكل جسم المربع الأيمن بالكامل بطول ضلع 182 بكسل.\n• القطعة D شكل رباعي يركب في التجويف السفلي الأيسر.\n• القطعة A مثلث قائم الزاوية يقفل الركن العلوي الأيسر.\n• القطعة C هي المثلث الزائد المضلل (Distractor).\nمجموع مساحات A + B + D = 33,124 بكسل = مساحة المربع 182x182 بنسبة تطابق 99.8%."
    },
    259: {
        "options": ["A", "B", "C", "D", "E"],
        "correct": 2,
        "reasoning": "الشكل C هو المختلف (Odd One Out):\n• جميع الأشكال الأربعة (A, B, D, E) هي نفس الشكل تماماً بمجرد تدوير ثنائي الأبعاد (2D Rotation).\n• الشكل C هو الوحيد المعكوس (صورة مرآة - Mirror Image / Reflection)، ولا يمكن الحصول عليه بمجرد التدوير العادي."
    },
    273: {
        "correct": 2,
        "reasoning": "القاعدة الحسابية للمثلثات:\n<code>(الرقم السفلي الأيسر ÷ الرقم العلوي) × الرقم السفلي الأيمن = الرقم الأوسط</code>\n• مثلث 1: <code>(12 ÷ 3) × 2 = 4 × 2 = 8</code>\n• مثلث 2: <code>(24 ÷ 6) × 7 = 4 × 7 = 28</code>\n• مثلث 3: <code>(32 ÷ 8) × 9 = 4 × 9 = 36</code>\nإذن الرقم الصحيح هو 36."
    },
    383: {
        "question": "What is the angle between the hands of a clock at 3:40?",
        "options": ["120°", "125°", "130°", "140°"],
        "correct": 2,
        "reasoning": "⏰ <b>طريقة الحل الذهنية السريعة (بدون آلة حاسبة):</b>\n1. كل خطوة رقم على الساعة = <code>30°</code>، وكل دقيقة يتحرك عقرب الساعات <code>0.5°</code> وعقرب الدقائق <code>6°</code>.\n2. عند الساعة 3:40:\n• عقرب الدقائق يقف تماماً عند الرقم 8 (أي <code>8 × 30° = 240°</code> من الساعة 12).\n• عقرب الساعات عند الرقم 3 ومعه 40 دقيقة: <code>3 × 30° + (40 × 0.5°) = 90° + 20° = 110°</code>.\n3. الزاوية بينهما = <code>240° - 110° = 130°</code>.\n\n💡 <b>بالقانون العام:</b> <code>|30 × 3 - 5.5 × 40| = |90 - 220| = 130°</code>."
    },
    384: {
        "question": "At what angle are the hands of a clock inclined at 8:30?",
        "options": ["70°", "75°", "80°", "85°"],
        "correct": 1,
        "reasoning": "⏰ <b>طريقة الحل الذهنية السريعة (بدون آلة حاسبة):</b>\n1. عند الساعة 8:30:\n• عقرب الدقائق يقف تماماً عند الرقم 6.\n• عقرب الساعات يقع في منتصف المسافة بالضبط بين الرقمين 8 و 9 (أي عند 8.5).\n2. فرق المسافة بين العقربين = <code>8.5 - 6 = 2.5 ساعة</code>.\n3. كل ساعة تمثل 30°، إذن الزاوية = <code>2.5 × 30° = 75°</code>!\n\n💡 <b>بالقانون العام:</b> <code>|30 × 8 - 5.5 × 30| = |240 - 165| = 75°</code>."
    },
    385: {
        "question": "If today is Monday, what day of the week will it be after 61 days?",
        "options": ["Tuesday", "Wednesday", "Thursday", "Saturday"],
        "correct": 3,
        "reasoning": "📅 <b>حساب اليوم في ثوانٍ:</b>\n1. الأسبوع يتكرر كل 7 أيام، فنحسب باقي قسمة 61 على 7:\n<code>61 ÷ 7 = 8 أسابيع كاملة والباقي 5 أيام</code> (لأن 7 × 8 = 56، و 61 - 56 = 5).\n2. نعد 5 أيام بعد يوم الاثنين (Monday):\n• +1: الثلاثاء (Tuesday)\n• +2: الأربعاء (Wednesday)\n• +3: الخميس (Thursday)\n• +4: الجمعة (Friday)\n• +5: <b>السبت (Saturday)</b>."
    },
    386: {
        "question": "The sum of ages of 5 children born at intervals of 3 years each is 50 years. What is the age of the youngest child?",
        "options": ["4 years", "8 years", "10 years", "None of these"],
        "correct": 0,
        "reasoning": "🎂 <b>طريقة الحل الحسابية:</b>\nلنفرض أن عمر أصغر طفل هو <code>x</code>:\nأعمار الأطفال الخمسة هي: <code>x, x+3, x+6, x+9, x+12</code>\nمجموع الأعمار:\n<code>5x + 30 = 50</code>\n<code>5x = 50 - 30 = 20</code>\n<code>x = 20 ÷ 5 = 4 سنوات</code>\n\n💡 عمر الطفل الأصغر = 4 سنوات."
    },
    387: {
        "question": "A father tells his son: \"I was your present age when you were born.\" If the father is 38 years old now, what was the son's age 5 years ago?",
        "options": ["14 years", "19 years", "33 years", "38 years"],
        "correct": 0,
        "reasoning": "👨‍👦 <b>طريقة الحل الذهنية:</b>\n• قول الأب \"كنت في مثل عمرك الحالي يوم ولادتك\" يعني أن عمر الأب الحالي ضعف عمر الابن الحالي تماماً!\n• عمر الابن الآن = <code>38 ÷ 2 = 19 سنة</code>.\n• عمر الابن منذ 5 سنوات = <code>19 - 5 = 14 سنة</code>."
    },
    388: {
        "question": "The average of three numbers is 48. If the average of two of these numbers is 56, what is the value of the third number?",
        "options": ["28", "32", "36", "40"],
        "correct": 1,
        "reasoning": "📊 <b>طريقة الحل الحسابية خطوة بخطوة:</b>\n1. مجموع الأعداد الثلاثة = <code>المتوسط × العدد = 48 × 3 = 144</code>.\n2. مجموع العددين = <code>المتوسط × العدد = 56 × 2 = 112</code>.\n3. قيمة العدد الثالث = <code>مجموع الثلاثة - مجموع الاثنين = 144 - 112 = 32</code>.\n\n💡 <b>القاعدة:</b> <code>المجموع الكلي = المتوسط الحسابي × عدد العناصر</code>."
    },
    415: {
        "question": "How many times do the hands of a clock coincide (overlap) in a 24-hour day?",
        "options": ["20", "22", "24", "44"],
        "correct": 1,
        "reasoning": "⏰ <b>قاعدة تطابق عقارب الساعة:</b>\n• يتطابق عقربا الساعات والدقائق 11 مرة كل 12 ساعة (لأن التطابق بين الساعة 11 و 1 يحدث مرة واحدة فقط عند الساعة 12:00 تماماً).\n• في الـ 24 ساعة يتطابقان: <code>11 × 2 = 22 مرة</code>."
    },
    416: {
        "question": "How many times in a day are the hands of a clock in a straight line (pointing opposite or together)?",
        "options": ["22", "24", "44", "48"],
        "correct": 2,
        "reasoning": "⏰ <b>الاستقامة التامة لعقربي الساعة (Straight Line):</b>\nالاستقامة تشمل حالتين:\n1. التطابق في نفس الاتجاه (0°): يحدث 22 مرة في اليوم.\n2. التعاكس في اتجاهين متضادين (180°): يحدث 22 مرة في اليوم.\n• إجمالي مرات الاستقامة = <code>22 + 22 = 44 مرة</code>."
    },
    419: {
        "question": "The average age of a class of 30 students is 15 years. If the teacher's age is included, the average increases by 1 year. What is the teacher's age?",
        "options": ["40 years", "44 years", "46 years", "48 years"],
        "correct": 2,
        "reasoning": "👨‍🏫 <b>طريقة الحل السريعة (بدون آلة حاسبة):</b>\n• المتوسط الجديد أصبح 16 سنة لـ 31 شخصاً (30 طالباً + المعلم).\n• المعلم جاء بنصيبه (16) وزاد كل طالب من الـ 30 طالباً سنة واحدة:\n<code>عمر المعلم = 16 + (30 × 1) = 46 سنة</code>.\n\n• <b>بالطريقة التقليدية:</b>\nمجموع أعمار الطلاب = <code>30 × 15 = 450</code>\nمجموع أعمار الكل = <code>31 × 16 = 496</code>\nعمر المعلم = <code>496 - 450 = 46 سنة</code>."
    }
}

# 3. Clean IndiaBIX Profit & Loss Bank (IDs 338 to 359)
IBIX_FIXES = {
    338: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• سعر التكلفة الإجمالي (Cost Price) = <code>4700 + 800 = 5500</code> روبية.\n• سعر البيع (Selling Price) = 5800 روبية.\n• الربح = <code>5800 - 5500 = 300</code> روبية.\n• نسبة الربح = <code>(300 ÷ 5500) × 100 = 60 ÷ 11 = 5 5/11%</code>."
    },
    339: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• تكلفة 20 سلعة = سعر بيع x سلعة.\n• لنفرض تكلفة السلعة الواحدة = 1 روبية، إذن تكلفة 20 سلعة = 20 روبية = سعر بيع x سلعة.\n• تكلفة x سلعة = x روبية.\n• الربح في x سلعة = <code>20 - x</code>.\n• نسبة الربح = <code>[(20 - x) ÷ x] × 100 = 25%</code>\n• <code>(20 - x) ÷ x = 1/4 => 80 - 4x = x => 5x = 80 => x = 16</code>."
    },
    340: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• لنفرض سعر التكلفة = CP وسعر البيع = SP، والربح الأصلي <code>P = SP - CP</code>.\n• إذا تضاعف سعر البيع إلى 2SP، يصبح الربح الجديد <code>2SP - CP = 3P</code>.\n• <code>2SP - CP = 3(SP - CP) = 3SP - 3CP => SP = 2CP</code>.\n• بما أن سعر البيع ضعف التكلفة، فإن الربح = <code>2CP - CP = CP</code> (الربح يساوي 100% من التكلفة)."
    },
    341: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• لنفرض سعر التكلفة CP = 100، إذن الربح = 320، وسعر البيع SP = <code>100 + 320 = 420</code>.\n• زادت التكلفة بنسبة 25% فأصبحت التكلفة الجديدة = 125 مع ثبات سعر البيع عند 420.\n• الربح الجديد = <code>420 - 125 = 295</code>.\n• نسبة الربح منسوبة إلى <b>سعر البيع</b> = <code>(295 ÷ 420) × 100 ≈ 70%</code>."
    },
    342: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• تكلفة 6 قطع حلوى = 1 روبية => تكلفة القطعة الواحدة = <code>1/6</code> روبية.\n• لتحقيق ربح 20%، يجب أن يكون سعر بيع القطعة الواحدة = <code>(1/6) × 1.20 = 1/5</code> روبية.\n• لبيع ما قيمته 1 روبية، عدد القطع = <code>1 ÷ (1/5) = 5 قطع</code>."
    },
    343: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• بما أن نسبة الربح عند البيع بـ 1920 تساوي نسبة الخسارة عند البيع بـ 1280، فإن سعر التكلفة يقع في المنتصف تماماً:\n<code>CP = (1920 + 1280) ÷ 2 = 3200 ÷ 2 = 1600</code> روبية.\n• لتحقيق ربح 25%:\n<code>سعر البيع = 1600 × 1.25 = 2000 روبية</code>."
    },
    344: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• نسبة الربح المتوقعة = 22.5% وسعر البيع الإجمالي = 392 روبية.\n• <code>سعر التكلفة = 392 ÷ 1.225 = 320 روبية</code>.\n• مقدار الربح = <code>392 - 320 = 72 روبية</code>."
    },
    345: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• سعر التكلفة = 1400 روبية، ونسبة الخسارة = 15%.\n• <code>سعر البيع = 1400 × (1 - 0.15) = 1400 × 0.85 = 1190 روبية</code>."
    },
    346: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• تكلفة الدستة = 375 روبية => تكلفة اللعبة الواحدة = <code>375 ÷ 12 = 31.25</code> روبية.\n• باع اللعبة الواحدة بـ 33 روبية => مقدار الربح في اللعبة = <code>33 - 31.25 = 1.75</code> روبية.\n• نسبة الربح = <code>(1.75 ÷ 31.25) × 100 = 5.6%</code>."
    },
    347: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• اشترى 6 سلع بـ 5 روبيات => تكلفة السلعة = <code>5/6</code> روبية.\n• باع 5 سلع بـ 6 روبيات => سعر بيع السلعة = <code>6/5</code> روبية.\n• نسبة الربح = <code>[(6/5 - 5/6) ÷ (5/6)] × 100 = (11/30 ÷ 25/30) × 100 = (11 ÷ 25) × 100 = 44%</code>."
    },
    348: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• خسارة بيع 17 كرة تساوي تكلفة 5 كرات:\n<code>17 × CP - 17 × SP = 5 × CP</code>\n<code>12 × CP = 17 × SP = 720 روبية</code>\n<code>تكلفة الكرة الواحدة = 720 ÷ 12 = 60 روبية</code>."
    },
    349: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• البيع بـ 18,700 يمثل 85% من التكلفة (خسارة 15%):\n<code>سعر التكلفة = 18,700 ÷ 0.85 = 22,000 روبية</code>.\n• للبيع بربح 15%:\n<code>سعر البيع المطلوب = 22,000 × 1.15 = 25,300 روبية</code>."
    },
    350: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• تكلفة 100 برتقالة = 350 روبية => تكلفة البرتقالة = <code>3.50</code> روبية.\n• باع الدستة (12 برتقالة) بـ 48 روبية => سعر بيع البرتقالة = <code>48 ÷ 12 = 4.00</code> روبيات.\n• الربح في البرتقالة = <code>4.00 - 3.50 = 0.50</code> روبية.\n• نسبة الربح = <code>(0.50 ÷ 3.50) × 100 = 1/7 × 100 = 14 2/7% gain</code>."
    },
    351: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• الجهاز الأول: بيع بـ 840 بربح 20% => تكلفته = <code>840 ÷ 1.2 = 700</code> روبية.\n• الجهاز الثاني: بيع بـ 960 بخسارة 4% => تكلفته = <code>960 ÷ 0.96 = 1000</code> روبية.\n• التكلفة الكلية = <code>700 + 1000 = 1700</code> روبية، والبيع الكلي = <code>840 + 960 = 1800</code> روبية.\n• الربح الإجمالي = <code>1800 - 1700 = 100</code> روبية.\n• نسبة الربح الكلية = <code>(100 ÷ 1700) × 100 = 100 ÷ 17 = 5 15/17% gain</code>."
    },
    352: {
        "reasoning": "💰 <b>الخطوات الرياضية والقانون:</b>\n• تكلفة 26 كجم بـ 20 روبية = <code>26 × 20 = 520</code> روبية.\n• تكلفة 30 كجم بـ 36 روبية = <code>30 × 36 = 1080</code> روبية.\n• التكلفة الإجمالية لـ 56 كجم = <code>520 + 1080 = 1600</code> روبية.\n• سعر بيع الخليط (56 كجم) بـ 30 روبية = <code>56 × 30 = 1680</code> روبية.\n• الربح = <code>1680 - 1600 = 80</code> روبية.\n• نسبة الربح = <code>(80 ÷ 1600) × 100 = 5%</code>."
    },
    353: {
        "reasoning": "💰 <b>تحليل كفاية المعطيات (Data Sufficiency):</b>\n• لمعرفة القيمة النقدية الدقيقة للربح (Exact amount of profit)، نحتاج معرفة سعر بيع السلعة (المعطى I) لحساب ربح السلعة الواحدة، ونحتاج معرفة عدد السلع المباعة (المعطى II) لحساب إجمالي الربح.\n• إذن كلاهما معاً ضروريان للحل: Both I and II are necessary."
    },
    354: {
        "reasoning": "💰 <b>تحليل كفاية المعطيات (Data Sufficiency):</b>\n• سعر بيع اللعبة الواحدة معروف (250 روبية).\n• لحساب النسبة المئوية للربح (Percent profit)، نحتاج فقط معرفة سعر تكلفة اللعبة الواحدة (المعطى II).\n• عدد اللعب المباعة (المعطى I) غير ضروري على الإطلاق لحساب النسبة المئوية.\n• إذن المعطى الثاني وحده كافٍ: Only II is necessary."
    },
    355: {
        "reasoning": "💰 <b>تحليل كفاية المعطيات (Data Sufficiency):</b>\n• نعلم سعر بيع الخليط (17 روبية/كجم) وسعر الصنفين X و Y (20 و 13).\n• لحساب نسبة الربح، من الضروري معرفة نسبة أو كميات خلط الصنفين معاً، وهذا المعطى غير موجود في العبارتين I و II.\n• إذن المعطيان معاً غير كافيين: Both I and II are not sufficient to answer."
    },
    356: {
        "reasoning": "💰 <b>تحليل كفاية المعطيات (Data Sufficiency):</b>\n• المعطى الأول ينص على أن الفرق بين سعر البيع والتكلفة هو 40 روبية، والفرق بين البيع والتكلفة هو تعريف الربح بذاته! إذن الربح = 40 روبية مباشرة من المعطى I وحده.\n• المعطى الثاني يكرر فقط أن الربح 20% دون إعطاء قيمة نقدية.\n• إذن المعطى I وحده كافٍ: I alone sufficient."
    },
    357: {
        "reasoning": "💰 <b>تحليل كفاية المعطيات (Data Sufficiency):</b>\n• من العبارة I: الخصم 5% على سعر القائمة (SP = 0.95 MP).\n• من العبارة II: إذا لم يكن هناك خصم يكون الربح 20% (MP = 1.20 CP).\n• بالتعويض: <code>SP = 0.95 × 1.20 CP = 1.14 CP</code>، أي أن نسبة الربح مع الخصم = 14%.\n• تمكنا من إيجاد النسبة بالعبارتين I و II معاً دون الحاجة للتكلفة الفعلية (المعطى III).\n• إذن الإجابة: Only I and II."
    },
    358: {
        "options": ["Only I and II", "Only II and III", "Only I and III", "Any two of the three", "None of these"],
        "correct": 0,
        "reasoning": "💰 <b>تحليل كفاية المعطيات (Data Sufficiency):</b>\n• من العبارة I: البيع بـ 12,350 بربح 23.5% يعطي التكلفة = 10,000 روبية.\n• من العبارة II: بدون خصم يكون الربح 30%، فيكون سعر القائمة = 13,000 روبية.\n• من I و II معاً نجد الخصم = <code>13,000 - 12,350 = 650</code>، ونسبته = <code>(650 ÷ 13000) × 100 = 5%</code>.\n• إذن العبارتان I و II كافيتان تماماً لتحديد النسبة المئوية للخصم: Only I and II."
    },
    359: {
        "reasoning": "💰 <b>تحليل كفاية المعطيات (Data Sufficiency):</b>\n• من العبارة I: السعر المعلن 130% من التكلفة (MP = 1.30 CP).\n• من العبارة III: خصم 10% على السعر المعلن (SP = 0.90 MP = <code>0.90 × 1.30 CP = 1.17 CP</code>).\n• إذن نسبة الربح = 17%، والعبارتان I و III كافيتان تماماً لحساب النسبة دون الحاجة للمبلغ المالي في II."
    }
}

# 4. Strip misleading XOR boilerplate from questions where it doesn't belong
xor_bp_pattern = re.compile(r'\s*💡\s*<b>القاعدة الحاكمة للشكل:</b>\s*حركة العناصر تعتمد إما على التدوير بزاوية ثابتة.*?\(XOR Cancellation\)\.', re.DOTALL)

def clean_q(q):
    qid = q.get('id')
    cat = q.get('category', '')
    text = q.get('question', '')
    r = q.get('reasoning', '')

    # Apply specific fix if exists
    if qid in FIXES:
        fix = FIXES[qid]
        for k, v in fix.items():
            q[k] = v
        r = q.get('reasoning', '')

    # Apply IndiaBIX fix if exists
    if qid in IBIX_FIXES:
        fix = IBIX_FIXES[qid]
        for k, v in fix.items():
            q[k] = v
        r = q.get('reasoning', '')

    # Remove generic XOR boilerplate if not an actual XOR grid
    is_real_xor = ("XOR" in text or "exclusive or" in text.lower() or ("3x3" in text and "grid" in text) or "matrix" in text.lower())
    if not is_real_xor and "XOR Cancellation" in r:
        q['reasoning'] = xor_bp_pattern.sub('', r).strip()

    # Clean switch questions reasoning
    if 'السويتشات' in cat:
        cor_opt = q['options'][q['correct']] if q.get('correct') is not None and 0 <= q.get('correct') < len(q.get('options', [])) else 'المفتاح المعطل'
        q['reasoning'] = f"🔍 <b>طريقة حل مسائل السويتشات في 5 ثوانٍ:</b>\n" \
                         f"• <b>المفتاح المعطل:</b> <b>{cor_opt}</b>\n" \
                         f"• <b>طريقة التتبع السريع:</b>\n" \
                         f"1. كل مفتاح وظيفته تبديل مواقع عناصر محددة (Swap Positions).\n" \
                         f"2. لتحديد المفتاح المعطل في ثوانٍ: اختر شكلاً واحداً فقط مميزاً (مثل الدائرة السوداء أو المثلث) وتتبع مساره من صف البداية عبر المفاتيح نزولاً للخرج النهائي.\n" \
                         f"3. ستلاحظ أن <b>{cor_opt}</b> هو المفتاح الوحيد الذي مرت العناصر من خلاله دون تنفيذ التبديل المطلوب!"

    # Clean trailing ages boilerplate from average questions
    if ('Ages & Averages' in cat or 'average' in text.lower()) and 'فرق العمر بين أي شخصين' in q.get('reasoning', '') and not 'age' in text.lower():
        q['reasoning'] = q['reasoning'].replace('فرق العمر بين أي شخصين يظل ثابتاً مدى الحياة ولا يتغير بمرور السنين.', '').strip()

# Apply to bank
for q in bank:
    clean_q(q)

# Apply to exam_models IQ
for m, qs in models['iq'].items():
    for q in qs:
        clean_q(q)

# Save large_iq_bank.json
with open(bank_path, 'w', encoding='utf-8') as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)

# Save exam_models.json
with open(models_path, 'w', encoding='utf-8') as f:
    json.dump(models, f, ensure_ascii=False, indent=2)

# Save bank_data.js
with open(js_path, 'w', encoding='utf-8') as f:
    f.write('window.EXAM_MODELS = ' + json.dumps(models, ensure_ascii=False) + ';\n')

print("Master cleanup executed successfully across all databases!")
