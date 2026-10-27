const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, colorScheme: process.argv[3] || 'dark', hasTouch: true, isMobile: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('http://127.0.0.1:8766/test.html', { waitUntil: 'networkidle' });
  const r = {};
  const spiel = (id, t) => p.$eval('#' + id, (a, t) => new Promise(res => { a.muted = true; a.preload = 'auto'; const go = () => { a.currentTime = t; a.play().then(res); }; if (a.readyState >= 1) go(); else { a.addEventListener('loadedmetadata', go, { once: true }); a.load(); } }), t);
  await spiel('a-lupert_ruhig', 40); await p.waitForTimeout(1200);
  // 4 s lang jede Frame die Verschiebung und das aktuelle Wort aufzeichnen
  const spur = await p.evaluate(() => new Promise(res => { const inh = document.getElementById('lesen-inhalt'), out = []; const t0 = performance.now();
    (function f(now) { const m = /translate3d\(0px?, ?(-?[\d.]+)px/.exec(inh.style.transform); const j = document.querySelector('#lesen-text .lw.jetzt');
      out.push([now - t0, m ? -parseFloat(m[1]) : null, j ? +j.dataset.i : -1, j ? parseFloat(j.style.getPropertyValue('--f') || '0') : null]);
      if (now - t0 < 4000) requestAnimationFrame(f); else res(out); })(t0); }));
  const ys = spur.map(s => s[1]), dts = spur.slice(1).map((s, k) => s[0] - spur[k][0]), dys = spur.slice(1).map((s, k) => s[1] - spur[k][1]);
  const v = dys.map((d, k) => d / dts[k] * 1000);
  r.frames = spur.length; r.yBereich = [ys[0], ys[ys.length - 1]];
  r.maxSchrittPx = Math.max(...dys.map(Math.abs)).toFixed(2); r.rueckwaerts = dys.filter(d => d < -0.01).length;
  r.geschwPxS = { min: Math.min(...v).toFixed(1), max: Math.max(...v).toFixed(1), mittel: (v.reduce((a, c) => a + c, 0) / v.length).toFixed(1) };
  const fs = spur.filter(s => s[3] !== null).map(s => s[3]); r.fuellung = { werte: fs.length, zwischenwerte: fs.filter(f => f > 0.05 && f < 0.95).length };
  // Lage des aktuellen Worts zum Streifen
  r.lage = await p.evaluate(() => { const t = document.getElementById('lesen-text'), s = t.querySelector('.lw.jetzt'), band = t.querySelector('.lesen-band').getBoundingClientRect(), sr = s.getBoundingClientRect();
    return { wort: s.textContent, abstandZurMitteInZeilen: (((sr.top + sr.bottom) / 2 - (band.top + band.bottom) / 2) / 33).toFixed(2) }; });
  await p.screenshot({ path: process.argv[2] + '/tele_' + (process.argv[3] || 'dark') + '.png' });
  // Ziehen: Text nach unten ziehen (zurückblättern), dann loslassen; nach 3 s gleitet er zurück
  const box = await p.$eval('#lesen-text', e => { const r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; });
  const yVor = await p.evaluate(() => -parseFloat(/translate3d\(0px?, ?(-?[\d.]+)px/.exec(document.getElementById('lesen-inhalt').style.transform)[1]));
  await p.mouse.move(box[0], box[1]); await p.mouse.down(); for (let k = 1; k <= 10; k++) await p.mouse.move(box[0], box[1] + k * 10); await p.mouse.up();
  const yNach = await p.evaluate(() => -parseFloat(/translate3d\(0px?, ?(-?[\d.]+)px/.exec(document.getElementById('lesen-inhalt').style.transform)[1]));
  await p.waitForTimeout(1500); const yWarten = await p.evaluate(() => -parseFloat(/translate3d\(0px?, ?(-?[\d.]+)px/.exec(document.getElementById('lesen-inhalt').style.transform)[1]));
  await p.waitForTimeout(2500); const yZurueck = await p.evaluate(() => -parseFloat(/translate3d\(0px?, ?(-?[\d.]+)px/.exec(document.getElementById('lesen-inhalt').style.transform)[1]));
  r.ziehen = { vor: yVor.toFixed(1), nachZiehen: yNach.toFixed(1), nach1_5s: yWarten.toFixed(1), nach4s: yZurueck.toFixed(1), offen: await p.$eval('#lesen', d => d.open), spielt: !(await p.$eval('#a-lupert_ruhig', a => a.paused)) };
  r.lageNachZurueck = await p.evaluate(() => { const t = document.getElementById('lesen-text'), s = t.querySelector('.lw.jetzt'), band = t.querySelector('.lesen-band').getBoundingClientRect(), sr = s.getBoundingClientRect();
    return (((sr.top + sr.bottom) / 2 - (band.top + band.bottom) / 2) / 33).toFixed(2); });
  // Wort antippen
  await p.$eval('#lesen-text .lw[data-i="20"]', s => s.click()); await p.waitForTimeout(1500);
  r.tipp = await p.evaluate(() => { const t = document.getElementById('lesen-text'), s = t.querySelector('.lw.jetzt'), band = t.querySelector('.lesen-band').getBoundingClientRect(), sr = s.getBoundingClientRect();
    return { wort: s.dataset.i + ' ' + s.textContent, abstand: (((sr.top + sr.bottom) / 2 - (band.top + band.bottom) / 2) / 33).toFixed(2), zeit: document.getElementById('a-lupert_ruhig').currentTime.toFixed(1) }; });
  // Ende: schließt
  await spiel('a-lupert_ruhig', 99.5); await p.waitForTimeout(4500); r.ende = { offen: await p.$eval('#lesen', d => d.open), ended: await p.$eval('#a-lupert_ruhig', a => a.ended) };
  // andere Fassungen kurz
  for (const id of ['a-eleven_ganz', 'a-neufassung2', 'a-lupert_exp']) { await spiel(id, 50); await p.waitForTimeout(1200);
    r[id] = await p.evaluate(() => { const t = document.getElementById('lesen-text'), s = t.querySelector('.lw.jetzt'), band = t.querySelector('.lesen-band').getBoundingClientRect(); if (!s) return null; const sr = s.getBoundingClientRect();
      return { wort: s.textContent, abstand: (((sr.top + sr.bottom) / 2 - (band.top + band.bottom) / 2) / 33).toFixed(2) }; }); }
  r.horiz = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  r.errs = errs; console.log(JSON.stringify(r, null, 1)); await b.close();
})();
