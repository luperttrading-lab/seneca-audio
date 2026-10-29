// Rendert Bilder eines Teils: node render.js <daten.json> <ausordner> <fps> <nr> <anzahl>
// Prozess nr von anzahl übernimmt jedes anzahl-te Bild, damit mehrere Prozesse parallel rendern können.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [datei, aus, fps, nr, anzahl] = [process.argv[2], process.argv[3], +process.argv[4], +process.argv[5], +process.argv[6]];
  const D = JSON.parse(fs.readFileSync(datei)); fs.mkdirSync(aus, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.join(__dirname, 'bild.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => bereit());
  const info = await p.evaluate(d => lade(d), D);
  const n = Math.ceil(D.ende * fps);
  for (let k = nr; k < n; k += anzahl) {
    await p.evaluate(t => zeige(t), k / fps);
    await p.screenshot({ path: path.join(aus, String(k).padStart(6, '0') + '.jpg'), type: 'jpeg', quality: 92 });
  }
  if (nr === 0) console.log(JSON.stringify({ bilder: n, ...info, errs }));
  await b.close();
})();
