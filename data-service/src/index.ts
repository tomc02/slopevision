import { Hono } from 'hono';
import { serve } from '@hono/node-server';
import { updateHzsWebcams } from './tasks/updateHzsWebcams';
import { updateScrapeWebcams } from './tasks/updateScrapeWebcams';
import 'dotenv/config';

const app = new Hono();

app.get('/', (c) => c.text('✅ Bun Hono API on Cloud Run'));
app.get('/update/hzs', async (c) => {
  await updateHzsWebcams();
  return c.json({ message: 'Updated hzs webcams' });
});
app.get('/update/scrape', async (c) => {
  await updateScrapeWebcams();
  return c.json({ message: 'Updated scraped webcams' });
});

// Run server
serve({
  fetch: app.fetch,
  port: parseInt(process.env.PORT || '8080')
});