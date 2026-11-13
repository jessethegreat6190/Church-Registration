const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const BASE = 'http://localhost/churchregistration';
const outDir = 'C:\\xampp\\htdocs\\churchregistration\\report_screenshots';

async function capture() {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  const shots = [
    { name: '01-homepage.png', url: `${BASE}/index.html#home`, selector: '#home', full: false },
    { name: '02-about-section.png', url: `${BASE}/index.html#about`, selector: '#about', full: false },
    { name: '03-plan-your-visit.png', url: `${BASE}/index.html#programs`, selector: '#programs', full: false },
    { name: '04-registration-form.png', url: `${BASE}/index.html#register`, selector: '#register', full: false },
    { name: '05-giving-section.png', url: `${BASE}/index.html#giving`, selector: '#giving', full: false },
    { name: '06-sermons-section.png', url: `${BASE}/index.html#sermons`, selector: '#sermons', full: false },
    { name: '07-contact-section.png', url: `${BASE}/index.html#contact`, selector: '#contact', full: false },
    { name: '08-footer.png', url: `${BASE}/index.html`, selector: '.footer', full: false },
    { name: '09-dashboard.png', url: `${BASE}/dashboard.html`, full: true },
    { name: '10-hero-full.png', url: `${BASE}/index.html`, full: true },
  ];

  for (const shot of shots) {
    try {
      await page.goto(shot.url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(2000);
      if (shot.selector) {
        const el = await page.$(shot.selector);
        if (el) {
          await el.screenshot({ path: path.join(outDir, shot.name) });
          console.log('Captured:', shot.name);
        } else {
          console.log('Selector not found:', shot.selector);
          await page.screenshot({ path: path.join(outDir, shot.name), fullPage: shot.full || false });
        }
      } else {
        await page.screenshot({ path: path.join(outDir, shot.name), fullPage: shot.full || false });
        console.log('Captured:', shot.name);
      }
    } catch (err) {
      console.log('Failed:', shot.name, err.message);
    }
  }

  await browser.close();
  console.log('All screenshots captured!');
}

capture();
