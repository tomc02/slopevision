import { db } from '../db/client';
import { webcams } from '../db/schema';
import { eq } from 'drizzle-orm';
import { findVideoUrl } from '../utils/fetchVideoUrl';
import { saveWebcamUrl } from '../utils/saveWebcamUrl';

export async function updateScrapeWebcams() {
  const cams = await db.select().from(webcams).where(eq(webcams.sourceType, 'SCRAPE'));

  for (const cam of cams) {
    const url = await findVideoUrl(cam.pageUrl!);
    await saveWebcamUrl(cam.id, url);
  }
}
