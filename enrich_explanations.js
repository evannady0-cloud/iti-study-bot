import fs from 'fs';

const largeBank = JSON.parse(fs.readFileSync('large_iq_bank.json', 'utf8'));

// Detailed explanations enrichment engine
for (const q of largeBank) {
  let exp = q.reasoning || '';

  // 1. Switch Problems
  if ((q.category || '').includes('السويتشات')) {
    q.reasoning = `🔍 <b>الشرح التفصيلي لخطوات الحل:</b>\n` +
      `• <b>الإجابة الصحيحة:</b> ${q.options[q.correct]}\n` +
      `• <b>طريقة التفكير (Logic Breakdown):</b>\n` +
      `في دوائر المحولات الكهربائية، كل مفتاح وظيفته تبديل مواقع عناصر محددة (Swap elements).\n` +
      `للوصول للمفتاح المعطل في ثوانٍ: تتبع مسار شكل واحد فقط (مثلاً الشكل الأسود أو المثلث) من البداية عبر المفاتيح وصولاً للمخرج النهائي.\n` +
      `ستلاحظ أن ${q.options[q.correct]} هو المفتاح الوحيد الذي لم ينفذ التبديل المبرمج له فمرت العناصر من خلاله دون تغيير في ترتيبها!`;
  }

  // 2. Address Matching
  else if ((q.category || '').includes('Address Matching')) {
    if (!exp.includes('🔍')) {
      q.reasoning = `🔍 <b>التدقيق المقارن حرفاً بحرف:</b>\n` +
        `• <b>الإجابة الصحيحة:</b> الاختيار (${['A','B','C','D'][q.correct]}) هو النسخة المطابقة 100% للأصل دون أي زيادة أو نقصان.\n` +
        `• <b>أماكن الأخطاء في باقي الاختيارات:</b> واضع الامتحان يغير دائماً رقماً في الـ ZIP Code، أو يحذف حرفاً مضاعفاً، أو يبدل رقمين متجاورين في رقم الشارع/الجناح.\n` +
        `• ${exp}`;
    }
  }

  // 3. Profit & Loss
  else if ((q.category || '').includes('Profit & Loss')) {
    if (!exp.includes('القانون')) {
      q.reasoning = `💰 <b>الخطوات الرياضية والقانون المستخدم:</b>\n` +
        `${exp}\n\n` +
        `💡 <b>كسب الوقت في الامتحان:</b> النسبة المئوية للربح أو الخسارة تُحسب دائماً منسوبة إلى <b>سعر الشراء والتكلفة (Cost Price)</b> وليس سعر البيع ما لم يُذكر خلاف ذلك!`;
    }
  }

  // 4. Blood Relations
  else if ((q.category || '').includes('Blood Relations')) {
    if (!exp.includes('شجرة العائلة')) {
      q.reasoning = `👥 <b>فك شجرة العائلة خطوة بخطوة:</b>\n` +
        `• <b>طريقة التفكير السريعة:</b> فكك العبارة دائماً <b>من اليمين إلى اليسار (من آخر الجملة للبداية)</b>:\n` +
        `${exp}\n` +
        `• <b>الخلاصة:</b> صلة القرابة الدقيقة هي <b>${q.options[q.correct]}</b>.`;
    }
  }

  // 5. Time & Work
  else if ((q.category || '').includes('Time & Work')) {
    if (!exp.includes('القاعدة')) {
      q.reasoning = `⏱️ <b>القاعدة الرياضية لحساب معدل الإنجاز:</b>\n` +
        `${exp}\n` +
        `💡 <b>القانون السريع:</b> عند عمل طرفين معاً، الزمن المشترك = (حاصل ضرب الزمنين) ÷ (مجموع الزمنين).`;
    }
  }

  // 6. Speed & Trains
  else if ((q.category || '').includes('Speed & Trains')) {
    if (!exp.includes('التحويل')) {
      q.reasoning = `🚆 <b>خطوات حل مسائل السرعة والقطارات:</b>\n` +
        `${exp}\n` +
        `💡 <b>تذكر دائماً:</b>\n` +
        `• التحويل من km/hr إلى m/s: اضرب في (5 / 18).\n` +
        `• عند عبور القطار لعمود أو شخص: المسافة = طول القطار فقط.\n` +
        `• عند عبور رصيف أو نفق: المسافة = طول القطار + طول الرصيف/النفق.`;
    }
  }

  // 7. Direction Sense
  else if ((q.category || '').includes('Direction Sense')) {
    if (!exp.includes('المحاور')) {
      q.reasoning = `🧭 <b>تتبع الحركة على المحاور الجغرافية:</b>\n` +
        `${exp}\n` +
        `💡 <b>طريقة الرسم الذهني:</b>\n` +
        `شمال (+Y) ⬆️ | جنوب (-Y) ⬇️ | شرق (+X) ➡️ | غرب (-X) ⬅️\n` +
        `الدوران لليمين من الشمال = شرق، والدوران لليمين من الجنوب = غرب.`;
    }
  }

  // 8. Clocks & Calendars
  else if ((q.category || '').includes('Clocks & Calendars')) {
    if (!exp.includes('القانون السحري')) {
      q.reasoning = `⏰ <b>القانون السحري لمسائل الساعات والتقويم:</b>\n` +
        `${exp}\n` +
        `💡 زاوية عقربي الساعة = |30 × الساعات - 5.5 × الدقائق|.\n` +
        `💡 لحساب اليوم بعد عدد معين من الأيام: احسب باقي قسمة الأيام على 7، وزود الباقي على يوم البداية.`;
    }
  }

  // 9. Ages & Averages
  else if ((q.category || '').includes('Ages & Averages')) {
    if (!exp.includes('المتوسط')) {
      q.reasoning = `🎂 <b>طريقة الحل الحسابية:</b>\n` +
        `${exp}\n` +
        `💡 المجموع الكلي = المتوسط الحسابي × عدد العناصر. فرق العمر بين أي شخصين يظل ثابتاً مدى الحياة ولا يتغير بمرور السنين.`;
    }
  }

  // 10. Patterns & Visual Shapes (Night Exam & Ultimate)
  else if ((q.category || '').includes('باترن') || q.image) {
    if (exp.length < 120 && !exp.includes('💡')) {
      q.reasoning = `🧩 <b>التحليل البصري للنمط (Pattern Analysis):</b>\n` +
        `• ${exp}\n` +
        `💡 <b>القاعدة الحاكمة للشكل:</b> حركة العناصر تعتمد إما على التدوير بزاوية ثابتة (45° أو 90° مع أو عكس عقارب الساعة)، أو تبادل الألوان (أبيض/أسود)، أو حذف الخطوط المتطابقة (XOR Cancellation).`;
    }
  }
}

fs.writeFileSync('large_iq_bank.json', JSON.stringify(largeBank, null, 2));
console.log('Successfully enriched all explanations in large_iq_bank.json!');
