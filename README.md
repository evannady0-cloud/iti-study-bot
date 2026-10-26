---
title: ITI Study Exam Portal
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: static
pinned: false
license: mit
---

# 🎓 ITI Admission Exam Mega Preparation Bot (@Studdyhelpbot)

بوت تدريب واختبارات القبول المكثفة لمعهد تكنولوجيا المعلومات (ITI) في مجالي الـ **IQ** والـ **English** بأحدث التوزيعات المعتمدة ونماذج ليلة الامتحان.

---

## 🌟 مميزات البوت (Features)

### 1. نماذج الامتحانات الواقعية (Authentic Exam Models)
- **6 نماذج IQ متطابقة مع الامتحان الفعلي (نموذج 1 إلى 6):**
  - كل نموذج يحتوي على **40 سؤالاً** بنفس توزيع ونسب الامتحان الحقيقي بالمللي:
    - 4 أسئلة مطابقة عناوين (Address Matching).
    - 2 أسئلة سويتشات ودوائر كهربائية (Switch Problems).
    - 2 أسئلة مكسب وخسارة (Quantitative: Profit & Loss).
    - 12 سؤال أشكال وباترن بصرية من ملف ليلة الامتحان و Ultimate IQ مع صور عالية الدقة.
    - 2 أسئلة شجرة العائلة (Blood Relations).
    - 2 أسئلة سرعة وقطارات (Speed & Trains).
    - 2 أسئلة زمن وإنجاز عمل (Time & Work).
    - 2 أسئلة اتجاهات وساعات (Direction Sense & Clocks/Calendars).
    - 2 أسئلة أعمار ومتوسطات (Ages & Averages).
    - 8 أسئلة لفظية ومنطقية من كتاب Ultimate IQ.
- **2 نموذج English متطابقين مع الامتحان الفعلي (نموذج 1 و 2):**
  - كل نموذج يحتوي على **26 سؤالاً**:
    - 14 موقفاً من مواقف الحياة والعمل (Situational Expressions).
    - 12 سؤال قواعد وتراكيب ومفردات (Grammar & Vocabulary).

### 2. بنوك التدريب المفتوحة (Open Practice Banks)
- ⭐ **ملف ليلة الامتحان الشامل (111 سؤالاً كاملاً):** يشمل كافة أسئلة السويتشات، الباترن، المسائل اللفظية، وشجرة العائلة.
- 💰 **مسائل المكسب والخسارة (Profit & Loss):** 22 مسألة أساسية من IndiaBIX مع شرح تفصيلي بالخطوات.
- 🔥 **بنك الـ IQ الشامل المفتوح (400+ سؤال):** تدريب عشوائي لا نهائي مع أسئلة كتاب Ultimate IQ المقصوصة بدقة.

### 3. الشرح الرياضي والمنطقي الدقيق (Enriched Explanations)
- كل سؤال يحتوي على تفسير تفصيلي (`💡 Reasoning`):
  - **القوانين الرياضية:** قانون التحويل للسرعة ($\times \frac{5}{18}$)، قانون الزمن المشترك ($\frac{A \times B}{A + B}$)، قانون زوايا الساعات ($|30H - 5.5M|$)، وقوانين الربح والخسارة.
  - **طريقة التفكير السريعة:** تفكيك شجرة العائلة من اليمين لليسار، وقواعد حركة الأشكال وإلغاء الخطوط المتشابهة (XOR Cancellation).
- زرار مساعدة مباشر في كل سؤال: **`[ ❓ مش عارف (اشرحلي الحل) ]`** يعرض الإجابة الصحيحة والشرح فوراً دون توتر.

---

## 🚀 تشغيل البوت سحابياً 24/7 (Cloud Deployment)

المشروع مبني بـ Node.js خالص (Vanilla Node.js) دون أي Dependencies خارجية، ومزود بسيرفر ويب داخلي خفيف على المنفذ `8080` لفحص الصحة (Health Checks)، مما يجعله جاهزاً للنشر المجاني بنقرة واحدة على:

### 1. النشر على Render.com (موصى به - مجاني)
1. سجل دخول إلى [dashboard.render.com](https://dashboard.render.com) عبر حساب GitHub.
2. اضغط على **New +** واختر **Web Service**.
3. اختر المستودع `iti-study-bot`.
4. أضف متغير البيئة التالي في قسم **Environment Variables**:
   - `TELEGRAM_BOT_TOKEN`: التوكن الخاص ببوتك من `@BotFather`.
5. اضغط **Create Web Service**.

### 2. التشغيل باستخدام Docker
```bash
docker build -t iti-study-bot .
docker run -d --name iti-bot -e TELEGRAM_BOT_TOKEN="YOUR_TOKEN_HERE" -p 8080:8080 iti-study-bot
```

### 3. التشغيل محلياً (Local Development)
```bash
# تثبيت والتشغيل
npm start
```
*(احرص على إنشاء ملف `.env` ووضع `TELEGRAM_BOT_TOKEN=your_token` بداخله).*

---

## 📂 هيكلة المشروع (Project Structure)
```
├── bot.mjs                 # المحرك الأساسي للبوت وخادم الويب
├── exam_models.json        # الـ 6 نماذج IQ + 2 نماذج English الموزعة واقعياً
├── large_iq_bank.json      # بنك الـ IQ الشامل (419 سؤالاً مع الشروحات)
├── profit_loss_bank.json   # بنك مسائل المكسب والخسارة
├── full_exam_bank.mjs      # بنك أسئلة الإنجليزي ومواقف ليلة الامتحان
├── images/                 # مئات الصور المقصوصة عالية الدقة لأسئلة الأشكال والسويتشات
├── Dockerfile              # إعدادات حاوية الدوكر للتشغيل السحابي
├── render.yaml             # إعدادات النشر التلقائي على Render
└── package.json            # إعدادات المشروع
```

---

*بالتوفيق لجميع المتقدمين لاختبارات الـ ITI!* 🎯
