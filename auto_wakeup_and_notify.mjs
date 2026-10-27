import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read token from .env
const envPath = path.join(__dirname, '.env');
let token = null;
if (fs.existsSync(envPath)) {
  const content = fs.readFileSync(envPath, 'utf8');
  const match = content.match(/TELEGRAM_BOT_TOKEN=(.*)/);
  if (match) token = match[1].trim();
}

const chatId = '1101834204';
const logPath = path.join(__dirname, 'wakeup.log');

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}\n`;
  fs.appendFileSync(logPath, line, 'utf8');
  console.log(line.trim());
}

async function sendTelegramMessage(text) {
  if (!token) {
    log('ERROR: No token found in .env');
    return;
  }
  try {
    const url = `https://api.telegram.org/bot${token}/sendMessage`;
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: text,
        parse_mode: 'HTML'
      })
    });
    const data = await res.json();
    log(`Telegram response: ok=${data.ok}`);
  } catch (err) {
    log(`Failed to send telegram message: ${err.message}`);
  }
}

async function main() {
  log('Wakeup script triggered.');

  // Check if bot port 8080 is already responding
  let isRunning = false;
  try {
    const res = await fetch('http://127.0.0.1:8080', { signal: AbortSignal.timeout(1500) });
    if (res.ok) isRunning = true;
  } catch (e) {
    isRunning = false;
  }

  if (!isRunning) {
    log('Bot is not running. Starting node bot.mjs in background...');
    const child = spawn('node', ['bot.mjs'], {
      cwd: __dirname,
      detached: true,
      stdio: 'ignore'
    });
    child.unref();
    log(`Spawned bot child process PID: ${child.pid}`);
    // Wait 3 seconds for bot to initialize
    await new Promise(r => setTimeout(r, 3000));
  } else {
    log('Bot is already running on port 8080.');
  }

  // Send notification to user
  const nowStr = new Date().toLocaleTimeString('ar-EG', { hour: '2-digit', minute: '2-digit' });
  const msg = `🔔 <b>تم تشغيل البوت بنجاح!</b>\n\n⏰ الوقت الآن: <b>${nowStr}</b>\n🤖 البوت شغال الآن ولايف (LIVE) وجاهز لمتابعة تدريبك ومذاكرتك للاختبار! 🚀🎯\n\nاضغط /start في أي وقت للمتابعة.`;
  await sendTelegramMessage(msg);
  log('Wakeup procedure complete.');
}

main();
