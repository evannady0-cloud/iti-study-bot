import fs from 'fs';

const largeBank = JSON.parse(fs.readFileSync('large_iq_bank.json', 'utf8'));

// Import english from full_exam_bank.mjs
const fullExam = (await import('./full_exam_bank.mjs')).fullExamBank;
const englishPool = fullExam.english;

// Categorize IQ questions into distinct pools
function getPool(filterFn) {
  return largeBank.filter(filterFn);
}

const switchPool = getPool(q => (q.category || '').includes('مسائل السويتشات'));
const addressPool = getPool(q => (q.category || '').includes('Address Matching'));
const profitPool = getPool(q => (q.category || '').includes('Profit & Loss'));
const bloodPool = getPool(q => (q.category || '').includes('Blood Relations'));
const timeWorkPool = getPool(q => (q.category || '').includes('Time & Work'));
const speedPool = getPool(q => (q.category || '').includes('Speed & Trains'));
const directionPool = getPool(q => (q.category || '').includes('Direction Sense'));
const clockPool = getPool(q => (q.category || '').includes('Clocks & Calendars'));
const agePool = getPool(q => (q.category || '').includes('Ages & Averages'));

// Visual patterns (Night Exam & Ultimate with images)
const patternPool = getPool(q => ((q.category || '').includes('باترن ليلة الامتحان') || (q.image && !q.category.includes('السويتشات'))));

// Ultimate verbal, puzzles, socks, logic
const ultimatePool = getPool(q => (q.category || '').startsWith('Ultimate IQ Test') && !q.image);

console.log('--- Pools Summary ---');
console.log('Switch:', switchPool.length);
console.log('Address:', addressPool.length);
console.log('Profit & Loss:', profitPool.length);
console.log('Blood Relations:', bloodPool.length);
console.log('Time & Work:', timeWorkPool.length);
console.log('Speed & Trains:', speedPool.length);
console.log('Direction Sense:', directionPool.length);
console.log('Clocks & Calendars:', clockPool.length);
console.log('Ages & Averages:', agePool.length);
console.log('Patterns & Visual:', patternPool.length);
console.log('Ultimate Verbal & Logic:', ultimatePool.length);

function takeN(pool, n, modelIndex) {
  const result = [];
  const start = (modelIndex * n) % pool.length;
  for (let i = 0; i < n; i++) {
    result.push(pool[(start + i) % pool.length]);
  }
  return result;
}

const iqModels = {};

for (let m = 0; m < 6; m++) {
  const modelNum = m + 1;
  const questions = [
    ...takeN(addressPool, 4, m),      // 4 Address Matching
    ...takeN(switchPool, 2, m),       // 2 Switch Problems
    ...takeN(profitPool, 2, m),       // 2 Profit & Loss
    ...takeN(patternPool, 12, m),     // 12 Visual Patterns & Shapes
    ...takeN(bloodPool, 2, m),        // 2 Blood Relations
    ...takeN(timeWorkPool, 2, m),     // 2 Time & Work
    ...takeN(speedPool, 2, m),        // 2 Speed & Trains
    ...takeN(directionPool, 2, m),    // 2 Direction Sense
    ...takeN(clockPool, 2, m),        // 2 Clocks & Calendars
    ...takeN(agePool, 2, m),          // 2 Ages & Averages
    ...takeN(ultimatePool, 8, m)      // 8 Ultimate Verbal & Logic
  ];

  // Randomize question order inside the model for an authentic exam feel
  for (let i = questions.length - 1; i > 0; i--) {
    const j = (i * 7 + 3) % (i + 1);
    [questions[i], questions[j]] = [questions[j], questions[i]];
  }

  iqModels[`iq_model_${modelNum}`] = questions;
  console.log(`Model IQ ${modelNum}: ${questions.length} questions`);
}

// Assemble English Models 1 and 2 (26 questions each)
const sitPool = englishPool.filter(q => (q.category || '').includes('Situations'));
const grammarPool = englishPool.filter(q => !(q.category || '').includes('Situations'));

console.log('English Situations Pool:', sitPool.length);
console.log('English Grammar & Vocab Pool:', grammarPool.length);

const englishModels = {};
for (let em = 0; em < 2; em++) {
  const modelNum = em + 1;
  const questions = [
    ...takeN(sitPool, 14, em),        // 14 Situational Questions
    ...takeN(grammarPool, 12, em)     // 12 Grammar & Vocabulary Questions
  ];
  englishModels[`english_model_${modelNum}`] = questions;
  console.log(`Model English ${modelNum}: ${questions.length} questions`);
}

const allExamModels = {
  iq: iqModels,
  english: englishModels
};

fs.writeFileSync('exam_models.json', JSON.stringify(allExamModels, null, 2));
console.log('exam_models.json written successfully!');
