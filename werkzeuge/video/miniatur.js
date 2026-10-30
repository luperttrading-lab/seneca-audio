// YouTube-Miniaturbild: node miniatur.js <kapitel|-> <aus.png>   („-“: ohne Kapitel, nur „Hörbuch“)
// Gerendert mit Faktor 1,5, also 1920 × 1080 (16:9 wie empfohlen, schärfer auf großen Bildschirmen, weit unter 2 MB).
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [kap, aus] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + path.join(__dirname, 'miniatur.html') + (kap !== '-' ? '?kapitel=' + kap : ''), { waitUntil: 'networkidle' });
  await p.evaluate(() => bereit());
  const breit = await p.evaluate(() => Math.max(...[...document.body.children].map(e => e.getBoundingClientRect().width)));
  if (breit > 1200) console.log('Warnung: Zeile', Math.round(breit), 'px breit');
  await p.screenshot({ path: aus }); await b.close();
})();
