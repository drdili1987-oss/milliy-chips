const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 860, height: 1200 }, deviceScaleFactor: 1.5 });
  const fs = require('fs');
  await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>' + fs.readFileSync('catalog.html','utf8') + '</body></html>', { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: 'Milliy-Chips-katalog.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
