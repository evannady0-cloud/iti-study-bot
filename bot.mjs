import fs from 'fs';
import path from 'path';
import http from 'http';
import { fileURLToPath } from 'url';
import { fullExamBank } from './full_exam_bank.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Lightweight web server for 24/7 cloud hosting health checks (Render, Koyeb, Railway, VPS)
const PORT = process.env.PORT || 8080;
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('🤖 ITI Study Telegram Bot is running 24/7!\nStatus: Operational\nQuestions Bank: 322 IQ + 102 English');
});
server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.log(`Port ${PORT} busy, binding to dynamic port...`);
    server.listen(0);
  } else {
    console.error('Server error:', err);
  }
});
server.listen(PORT, () => {
  const addr = server.address();
  const actualPort = typeof addr === 'object' ? addr.port : PORT;
  console.log(`🌐 Cloud health server listening on port ${actualPort}`);
});

const TOKEN = '8744413280:AAHPubO0X9WA0OgAeb5kKFGqO6VCwMfFDKs';
const API_BASE = `https://api.telegram.org/bot${TOKEN}`;
const IMAGES_DIR = path.join(__dirname, 'images');

// Load 300+ IQ Bank
const largeIqJson = path.join(__dirname, 'large_iq_bank.json');
let largeIqQuestions = [];
if (fs.existsSync(largeIqJson)) {
  largeIqQuestions = JSON.parse(fs.readFileSync(largeIqJson, 'utf-8'));
}

// Load Profit & Loss Bank (IndiaBIX + Fatma El-Zahraa)
const profitLossJson = path.join(__dirname, 'profit_loss_bank.json');
let profitLossQuestions = [];
if (fs.existsSync(profitLossJson)) {
  profitLossQuestions = JSON.parse(fs.readFileSync(profitLossJson, 'utf-8'));
}

// User state: supports randomized non-repeating queue
const userSessions = new Map();

function shuffleArray(array) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function getUserState(chatId) {
  if (!userSessions.has(chatId)) {
    userSessions.set(chatId, {
      activeMode: 'large_iq', // 'large_iq' (300+ questions) or 'english' (40) or 'ultimate_40'
      score: 0,
      totalAnswered: 0,
      queue: [],
      currentIndex: 0
    });
  }
  return userSessions.get(chatId);
}

function initUserQueue(chatId, mode) {
  const state = getUserState(chatId);
  state.activeMode = mode;
  state.score = 0;
  state.totalAnswered = 0;
  state.currentIndex = 0;

  let sourcePool = [];
  if (mode === 'large_iq') {
    sourcePool = largeIqQuestions;
  } else if (mode === 'ultimate_40') {
    sourcePool = fullExamBank.iq;
  } else if (mode === 'english') {
    sourcePool = fullExamBank.english;
  } else if (mode === 'profit_loss') {
    sourcePool = profitLossQuestions;
  } else if (mode === 'night_exam') {
    sourcePool = largeIqQuestions.filter(q => (q.category || '').includes('Exam Night'));
  }

  // Shuffle questions randomly so questions never repeat until all are exhausted!
  state.queue = shuffleArray(sourcePool);
  console.log(`Initialized shuffled queue for chat ${chatId}: ${state.queue.length} questions in mode [${mode}]`);
}

// API Helper
async function apiCall(method, body) {
  try {
    const res = await fetch(`${API_BASE}/${method}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    return await res.json();
  } catch (err) {
    console.error(`Error calling ${method}:`, err);
    return null;
  }
}

// Send Photo using multipart/form-data
async function sendPhoto(chatId, photoPath, caption, replyMarkup) {
  const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
  const fileBuffer = fs.readFileSync(photoPath);
  const fileName = path.basename(photoPath);

  let body = '';
  body += `--${boundary}\r\n`;
  body += `Content-Disposition: form-data; name="chat_id"\r\n\r\n${chatId}\r\n`;

  if (caption) {
    body += `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="caption"\r\n\r\n${caption}\r\n`;
    body += `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="parse_mode"\r\n\r\nHTML\r\n`;
  }

  if (replyMarkup) {
    body += `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="reply_markup"\r\n\r\n${JSON.stringify(replyMarkup)}\r\n`;
  }

  body += `--${boundary}\r\n`;
  body += `Content-Disposition: form-data; name="photo"; filename="${fileName}"\r\n`;
  body += `Content-Type: image/png\r\n\r\n`;

  const headerBuf = Buffer.from(body, 'utf-8');
  const footerBuf = Buffer.from(`\r\n--${boundary}--\r\n`, 'utf-8');
  const fullBuffer = Buffer.concat([headerBuf, fileBuffer, footerBuf]);

  try {
    const res = await fetch(`${API_BASE}/sendPhoto`, {
      method: 'POST',
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`
      },
      body: fullBuffer
    });
    return await res.json();
  } catch (err) {
    console.error('Error sending photo:', err);
    return null;
  }
}

// Send Next Question from randomized queue
async function sendQuestion(chatId) {
  const state = getUserState(chatId);

  if (state.currentIndex >= state.queue.length) {
    // All questions in queue finished! Re-shuffle!
    const summaryMsg = `🎉 <b>ما شاء الله! أنت خلصت بنك الأسئلة بالكامل!</b>\n\n` +
      `📊 <b>درجتك النهائية:</b> ${state.score} / ${state.totalAnswered} ` +
      `(${Math.round((state.score / Math.max(1, state.totalAnswered)) * 100)}%)\n\n` +
      `تم تجديد البنك وعمل Shuffle عشوائي جديد. اضغط للبدء من جديد:`;

    await apiCall('sendMessage', {
      chat_id: chatId,
      text: summaryMsg,
      parse_mode: 'HTML',
      reply_markup: {
        inline_keyboard: [
          [{ text: '⭐ إعادة ملف ليلة الامتحان 2026 (111 سؤال)', callback_data: 'mode_night_exam' }],
          [{ text: '🔄 بنك الـ 380+ سؤال IQ الشامل عشوائياً', callback_data: 'mode_large_iq' }],
          [{ text: '💰 مسائل الربح والخسارة (IndiaBIX + فاطمة الزهراء)', callback_data: 'mode_profit_loss' }],
          [{ text: '🇬🇧 بنك الإنجليزي (100+ سؤال)', callback_data: 'mode_english' }]
        ]
      }
    });
    return;
  }

  const q = state.queue[state.currentIndex];
  const total = state.queue.length;

  // Smart inline keyboard builder for mobile
  const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
  const allShort = q.options.every(opt => String(opt).trim().length <= 4);
  
  let buttons = [];
  if (allShort && q.options.length <= 5) {
    // Place all short options in a single horizontal row for sleek mobile UI
    buttons = [q.options.map((opt, idx) => ({
      text: String(opt).trim().toUpperCase() === letters[idx] ? `[ ${letters[idx]} ]` : `${letters[idx]} ) ${opt}`,
      callback_data: `ans_${q.id}_${idx}`
    }))];
  } else if (allShort && q.options.length > 5) {
    // Place in two neat rows
    const r1 = [];
    const r2 = [];
    q.options.forEach((opt, idx) => {
      const btn = {
        text: String(opt).trim().toUpperCase() === letters[idx] ? `[ ${letters[idx]} ]` : `${letters[idx]} ) ${opt}`,
        callback_data: `ans_${q.id}_${idx}`
      };
      if (idx < 4) r1.push(btn);
      else r2.push(btn);
    });
    buttons = [r1, r2];
  } else {
    // Longer text options: 1 per line
    buttons = q.options.map((opt, idx) => [{
      text: `${letters[idx]} )  ${opt}`,
      callback_data: `ans_${q.id}_${idx}`
    }]);
  }

  const categoryLabel = q.category || 'IQ Question';
  const captionText = `🎯 <b>[${categoryLabel}] Question ${state.currentIndex + 1} / ${total}</b>\n\n` +
    `<b>${q.question}</b>`;

  if (q.image) {
    const photoPath = path.join(IMAGES_DIR, q.image);
    if (fs.existsSync(photoPath)) {
      await sendPhoto(chatId, photoPath, captionText, { inline_keyboard: buttons });
      return;
    }
  }

  // Text-only question
  await apiCall('sendMessage', {
    chat_id: chatId,
    text: captionText,
    parse_mode: 'HTML',
    reply_markup: { inline_keyboard: buttons }
  });
}

// Long Polling Loop
let offset = 0;

async function pollUpdates() {
  try {
    const res = await fetch(`${API_BASE}/getUpdates?offset=${offset}&timeout=30`);
    const data = await res.json();

    if (data.ok && data.result.length > 0) {
      for (const update of data.result) {
        offset = update.update_id + 1;

        if (update.message) {
          const chatId = update.message.chat.id;
          const text = (update.message.text || '').trim();

          if (text === '/start' || text === '/quiz' || text === '/help') {
            await apiCall('sendMessage', {
              chat_id: chatId,
              text: `👋 <b>أهلاً بك في بوت بنك أسئلة ITI الشامل!</b> 🎓\n\n` +
                `⭐ <b>تم دمج جميع أنواع أسئلة ليلة الامتحان والخلاصة 2026 كاملة (سويتشات، عناوين، باترن، صلة قرابة، سرعة وقطارات، وقت وعمل)!</b>\n` +
                `💰 <b>مع قسم خاص لمسائل الربح والخسارة Profit & Loss من IndiaBIX وشرح م/ فاطمة الزهراء!</b>\n\n` +
                `✨ <b>ميزة عدم التكرار (No Repeat Shuffle):</b> الأسئلة تظهر بترتيب عشوائي تماماً، والسؤال لا يتكرر حتى تنتهي من كامل البنك!\n\n` +
                `اختر نوع الاختبار لتبدأ فوراً:`,
              parse_mode: 'HTML',
              reply_markup: {
                inline_keyboard: [
                  [{ text: '⭐ ملف ليلة الامتحان 2026 كامل (111 سؤال - سويتشات وباترن وعناوين)', callback_data: 'mode_night_exam' }],
                  [{ text: '💰 مسائل الربح والخسارة Profit & Loss (الهند وبيكس + فاطمة الزهراء)', callback_data: 'mode_profit_loss' }],
                  [{ text: '🔥 بنك الـ 380+ سؤال IQ الشامل (ليلة الامتحان + ألتيمت كامل)', callback_data: 'mode_large_iq' }],
                  [{ text: '🇬🇧 بنك الـ 100+ سؤال English (المواقف وقواعد ليلة الامتحان)', callback_data: 'mode_english' }],
                  [{ text: '📘 40 سؤال Ultimate IQ (نموذج امتحان تجريبي قياسي)', callback_data: 'mode_ultimate_40' }]
                ]
              }
            });
          }
        }

        if (update.callback_query) {
          const query = update.callback_query;
          const chatId = query.message.chat.id;
          const state = getUserState(chatId);

          await apiCall('answerCallbackQuery', { callback_query_id: query.id });

          if (query.data === 'mode_night_exam') {
            initUserQueue(chatId, 'night_exam');
            await sendQuestion(chatId);
          } else if (query.data === 'mode_large_iq') {
            initUserQueue(chatId, 'large_iq');
            await sendQuestion(chatId);
          } else if (query.data === 'mode_profit_loss') {
            initUserQueue(chatId, 'profit_loss');
            await sendQuestion(chatId);
          } else if (query.data === 'mode_ultimate_40') {
            initUserQueue(chatId, 'ultimate_40');
            await sendQuestion(chatId);
          } else if (query.data === 'mode_english') {
            initUserQueue(chatId, 'english');
            await sendQuestion(chatId);
          } else if (query.data === 'next_q') {
            state.currentIndex++;
            await sendQuestion(chatId);
          } else if (query.data.startsWith('ans_')) {
            const parts = query.data.split('_');
            const qId = parseInt(parts[1], 10);
            const userChoice = parseInt(parts[2], 10);

            const q = state.queue.find(item => item.id === qId);
            if (!q) continue;

            const isCorrect = (userChoice === q.correct);
            state.totalAnswered++;
            if (isCorrect) state.score++;

            const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            const corrLetter = letters[q.correct] || 'A';
            const corrText = q.options[q.correct] || '';
            const displayAns = (String(corrText).trim().toUpperCase() === corrLetter)
              ? `<b>[ ${corrLetter} ]</b>`
              : `<b>${corrLetter} ) ${corrText}</b>`;

            const feedbackHeader = isCorrect
              ? `✅ <b>إجابة صحيحة! الله ينور!</b>`
              : `❌ <b>إجابة غير صحيحة!</b>\nالإجابة الصحيحة هي: ${displayAns}`;

            const feedbackMsg = `${feedbackHeader}\n\n` +
              `💡 <b>Reasoning (التفسير والتعليل):</b>\n${q.reasoning}\n\n` +
              `📊 درجاتك الحالية: <b>${state.score} / ${state.totalAnswered}</b>\n` +
              `🔄 المتبقي في هذا الاختبار: <b>${state.queue.length - (state.currentIndex + 1)}</b> سؤال.`;

            await apiCall('sendMessage', {
              chat_id: chatId,
              text: feedbackMsg,
              parse_mode: 'HTML',
              reply_markup: {
                inline_keyboard: [
                  [{ text: '➡️ السؤال التالي', callback_data: 'next_q' }]
                ]
              }
            });
          }
        }
      }
    }
  } catch (err) {
    console.error('Polling error:', err);
  }

  setTimeout(pollUpdates, 500);
}

console.log(`🤖 ITI Mega Bank Bot (300+ IQ + English) is LIVE!`);
pollUpdates();
