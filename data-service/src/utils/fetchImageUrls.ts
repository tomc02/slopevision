import { chromium } from 'playwright';

export async function getImageUrls(imageIds: string[]): Promise<Record<string, string | null>> {
  const browser = await chromium.launch({ headless: true });
  
  // Create a new browser context that ignores HTTPS errors
  const context = await browser.newContext({ ignoreHTTPSErrors: true });
  const page = await context.newPage();

  const imgUrls: Record<string, string | null> = {};

  try {
    await page.goto('https://meteo.hzs.sk/', { waitUntil: 'load' });
    await page.waitForTimeout(3000);

    for (const id of imageIds) {
      const img = await page.$(`#${id}`);
      if (img) {
        const src = await img.getAttribute('src');
        imgUrls[id] = src?.startsWith('http') ? src : `https://meteo.hzs.sk${src}`;
      } else {
        imgUrls[id] = null;
      }
    }
  } catch (err) {
    console.error('Playwright error:', err);
  } finally {
    await browser.close();
  }

  return imgUrls;
}
