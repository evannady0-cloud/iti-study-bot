import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const chrome = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"';
const imgDir = 'C:\\Users\\tonyn\\.gemini\\antigravity\\scratch\\iti_telegram_bot\\images';

function renderCard(htmlBody, outPng, width = 600, height = 450) {
  const fullHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #0f172a;
    color: #f8fafc;
    margin: 0;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .card {
    background: #1e293b;
    border: 2px solid #38bdf8;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    width: 100%;
    box-sizing: border-box;
    text-align: center;
  }
  .title {
    font-size: 1.2em;
    font-weight: bold;
    color: #38bdf8;
    margin-bottom: 15px;
    border-bottom: 1px solid #334155;
    padding-bottom: 8px;
  }
  /* 3x3 Matrix */
  .matrix {
    display: grid;
    grid-template-columns: repeat(3, 85px);
    grid-template-rows: repeat(3, 85px);
    gap: 10px;
    justify-content: center;
    margin: 15px auto;
  }
  .cell {
    background: #0f172a;
    border: 2px solid #64748b;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.2em;
    color: #f8fafc;
  }
  .cell-q {
    background: #1e3a8a;
    border: 2px dashed #38bdf8;
    color: #38bdf8;
    font-weight: bold;
  }
  /* Cube Net */
  .cube-grid {
    display: grid;
    grid-template-columns: repeat(4, 55px);
    grid-template-rows: repeat(3, 55px);
    gap: 6px;
    justify-content: center;
    margin: 15px auto;
  }
  .cube-cell {
    background: #0f172a;
    border: 2px solid #64748b;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5em;
    font-weight: bold;
  }
  .empty { border: none; background: transparent; }
  /* Dominoes */
  .domino-row {
    display: flex;
    gap: 15px;
    justify-content: center;
    align-items: center;
    margin: 20px auto;
  }
  .domino {
    width: 55px;
    height: 100px;
    background: #f8fafc;
    color: #0f172a;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    border: 2px solid #cbd5e1;
    font-size: 1.4em;
    font-weight: bold;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  }
  .d-half {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .d-divider {
    height: 2px;
    background: #94a3b8;
    width: 100%;
  }
  .q-mark {
    background: #1e3a8a;
    color: #38bdf8;
    border: 2px dashed #38bdf8;
  }
  /* Gears */
  .gears-row {
    display: flex;
    gap: 10px;
    justify-content: center;
    align-items: center;
    margin: 25px auto;
  }
  .gear {
    width: 85px;
    height: 85px;
    border-radius: 50%;
    border: 6px dashed #38bdf8;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #0f172a;
    font-size: 1.1em;
    font-weight: bold;
  }
</style>
</head>
<body>
  <div class="card">
    ${htmlBody}
  </div>
</body>
</html>`;

  const tmpHtml = path.join(imgDir, 'temp.html');
  fs.writeFileSync(tmpHtml, fullHtml);
  const outPath = path.join(imgDir, outPng);
  const cmd = `${chrome} --headless=new --disable-gpu --screenshot="${outPath}" --window-size=${width},${height} "${tmpHtml}"`;
  execSync(cmd);
  console.log(`Rendered: ${outPng}`);
}

// 1. Matrix 1: Arrow Rotation
renderCard(`
  <div class="title">3x3 Visual Matrix: Arrow Rotation</div>
  <div class="matrix">
    <div class="cell">↑</div>
    <div class="cell">↗</div>
    <div class="cell">→</div>
    <div class="cell">↘</div>
    <div class="cell">↓</div>
    <div class="cell">↙</div>
    <div class="cell">←</div>
    <div class="cell">↖</div>
    <div class="cell cell-q">?</div>
  </div>
  <div style="color: #94a3b8; font-size: 0.95em;">What replaces the question mark [ ? ] ?</div>
`, 'matrix_arrow.png', 500, 480);

// 2. Cube 1: Opposite Faces
renderCard(`
  <div class="title">Unfolded Cube Net: Opposite Faces</div>
  <div style="color: #cbd5e1; font-size: 0.95em; margin-bottom: 5px;">When folded into a 3D cube, which face is OPPOSITE to [ A ]?</div>
  <div class="cube-grid">
    <div class="cube-cell empty"></div>
    <div class="cube-cell" style="background:#1e3a8a; border-color:#38bdf8; color:#38bdf8;">A</div>
    <div class="cube-cell empty"></div>
    <div class="cube-cell empty"></div>

    <div class="cube-cell">B</div>
    <div class="cube-cell" style="background:#064e3b; border-color:#10b981;">C</div>
    <div class="cube-cell">D</div>
    <div class="cube-cell">E</div>

    <div class="cube-cell empty"></div>
    <div class="cube-cell" style="background:#78350f; border-color:#f59e0b; color:#fde68a;">F</div>
    <div class="cube-cell empty"></div>
    <div class="cube-cell empty"></div>
  </div>
`, 'cube_net_1.png', 500, 420);

// 3. Domino Sequence:
renderCard(`
  <div class="title">Domino Sequence Logic</div>
  <div style="color: #cbd5e1; font-size: 0.9em;">Numbers cycle: 0 ➔ 1 ➔ 2 ➔ 3 ➔ 4 ➔ 5 ➔ 6 ➔ 0</div>
  <div class="domino-row">
    <div class="domino"><div class="d-half">1</div><div class="d-divider"></div><div class="d-half">4</div></div>
    <div class="domino"><div class="d-half">2</div><div class="d-divider"></div><div class="d-half">5</div></div>
    <div class="domino"><div class="d-half">3</div><div class="d-divider"></div><div class="d-half">6</div></div>
    <div class="domino"><div class="d-half">4</div><div class="d-divider"></div><div class="d-half">0</div></div>
    <div class="domino q-mark"><div class="d-half">?</div><div class="d-divider"></div><div class="d-half">?</div></div>
  </div>
  <div style="color: #94a3b8; font-size: 0.95em;">What is the next domino tile?</div>
`, 'domino_seq.png', 550, 400);

// 4. Gears Physics:
renderCard(`
  <div class="title">3 Meshed Gears in a Line</div>
  <div style="color: #cbd5e1; font-size: 0.9em;">Gear A rotates CLOCKWISE (↻)</div>
  <div class="gears-row">
    <div class="gear" style="border-color:#38bdf8;">Gear A<br><span style="font-size:1.4em;">↻</span></div>
    <div class="gear" style="border-color:#a855f7;">Gear B<br><span style="font-size:1.4em;">?</span></div>
    <div class="gear" style="border-color:#10b981;">Gear C<br><span style="font-size:1.4em;">?</span></div>
  </div>
  <div style="color: #94a3b8; font-size: 0.95em;">In which direction will Gear C rotate?</div>
`, 'gears_3.png', 550, 380);

// 5. Matrix 2: Dot Count Pattern
renderCard(`
  <div class="title">3x3 Visual Matrix: Dot Addition</div>
  <div class="matrix">
    <div class="cell">●</div>
    <div class="cell">●●</div>
    <div class="cell">●●●</div>
    <div class="cell">●●</div>
    <div class="cell">●●●</div>
    <div class="cell">●●●●</div>
    <div class="cell">●●●</div>
    <div class="cell">●●●●</div>
    <div class="cell cell-q">?</div>
  </div>
  <div style="color: #94a3b8; font-size: 0.95em;">How many dots belong in the missing box [ ? ] ?</div>
`, 'matrix_dots.png', 500, 480);
