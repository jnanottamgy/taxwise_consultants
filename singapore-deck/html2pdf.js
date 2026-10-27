const { chromium } = require('playwright');
(async () => {
  const [src, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + src, { waitUntil: 'networkidle' });

  // Keep the head styles (slide geometry lives in CSS vars there) but rebuild
  // the body as a bare stack of slides, so each one prints as its own page.
  const n = await page.evaluate(() => {
    const slides = [...document.querySelectorAll('.slide')];
    const holder = document.createElement('div');
    slides.forEach(s => holder.appendChild(s));
    document.body.replaceChildren(holder);
    return slides.length;
  });
  await page.addStyleTag({ content: `
    @page { size: 960pt 540pt; margin: 0; }
    html, body { background: #0E1B2F !important; display: block !important;
                 height: auto !important; overflow: visible !important; margin: 0 !important; }
    .slide-notes, .slide-label { display: none !important; }
    .slide { box-shadow: none !important; border-radius: 0 !important;
             margin: 0 !important; transform: none !important;
             break-after: page; page-break-after: always; }
    .slide:last-child { break-after: auto; page-break-after: auto; }
  `});
  await page.pdf({ path: out, printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('slides:', n);
})();
