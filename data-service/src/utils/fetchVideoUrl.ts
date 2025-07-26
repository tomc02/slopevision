import axios from 'axios';

export async function findVideoUrl(pageUrl: string): Promise<string | null> {
  try {
    if (pageUrl.includes('chatanagruni')) {
      // simulate the selenium logic
      // if needed, replicate via Playwright with more specific scraping
      return null; // Replace with logic if needed
    }

    const { data } = await axios.get(pageUrl, { httpsAgent: new (require('https').Agent)({ rejectUnauthorized: false }) });
    const match = data.match(/https?:\/\/[^\s'"]+\.mp4/);
    return match ? match[0] : null;
  } catch (err) {
    console.log('Fetch error:', err);
    return null;
  }
}
