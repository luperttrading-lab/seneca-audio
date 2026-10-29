const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const V = process.argv[2], E = JSON.parse(fs.readFileSync(V + '/ereignisse.json'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + V + '/bild.html', { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(d => lade(d), E.daten); fs.mkdirSync(V + '/bilder', { recursive: true });
  const liste = [];
  for (let k = 0; k < E.ereignisse.length; k++) {
    const e = E.ereignisse[k], f = 'bilder/' + String(k).padStart(4, '0') + '.png';
    await p.evaluate(z => zeige(z), e.z); await p.screenshot({ path: V + '/' + f });
    const bis = k + 1 < E.ereignisse.length ? E.ereignisse[k + 1].t : E.ende;
    liste.push(`file '${f}'\nduration ${(bis - e.t).toFixed(3)}`);
  }
  liste.push(`file 'bilder/${String(E.ereignisse.length - 1).padStart(4, '0')}.png'`);
  fs.writeFileSync(V + '/liste.txt', liste.join('\n') + '\n');
  const fonts = await p.evaluate(() => Array.from(document.fonts).filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.style + ' ' + f.weight));
  console.log(JSON.stringify({ bilder: E.ereignisse.length, fonts: [...new Set(fonts)], errs })); await b.close();
})();
