import { db } from '../db/client';
import { webcams } from '../db/schema';
import { eq } from 'drizzle-orm';

export async function saveWebcamUrl(id: number, url: string | null): Promise<void> {
  if (!url) return;

  const timestamp = new Date().toLocaleString('en-GB', {
    timeZone: 'Europe/Prague',
    hour12: true,
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  await db.update(webcams)
    .set({
      sourceUrl: url,
      description: `Updated at: ${timestamp}`
    })
    .where(eq(webcams.id, id));

  console.log(`Updated webcam ${id} with URL: ${url}`);
}
