// Rendert Bilder eines Teils: node render.js <daten.json> <ausordner> <fps> <nr> <anzahl> [<von s> <bis s>]
// Prozess nr von anzahl übernimmt jedes anzahl-te Bild, damit mehrere Prozesse parallel rendern können.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [datei, aus, fps, nr, anzahl] = [process.argv[2], process.argv[3], +process.argv[4], +process.argv[5], +process.argv[6]];
  const D = JSON.parse(fs.readFileSync(datei)); fs.mkdirSync(aus, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.join(__dirname, 'bild.html'), { waitUntil: 'networkidle' }); await p.evaluate(() => bereit());
  const info = await p.evaluate(d => lade(d), D);
  const k0 = process.argv[7] ? Math.round(+process.argv[7] * fps) : 0;   // Ausschnitt: Bilder ab 0 nummeriert
  const n = (process.argv[8] ? Math.ceil(+process.argv[8] * fps) : Math.ceil(D.ende * fps)) - k0;
  for (let k = nr; k < n; k += anzahl) {
    await p.evaluate(t => zeige(t), (k0 + k) / fps);
    await p.screenshot({ path: path.join(aus, String(k).padStart(6, '0') + '.jpg'), type: 'jpeg', quality: 92 });
  }
  if (nr === 0) console.log(JSON.stringify({ bilder: n, ...info, errs }));
  await b.close();
})();
