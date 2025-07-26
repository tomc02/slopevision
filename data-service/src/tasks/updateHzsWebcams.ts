import { db } from '../db/client';
import { webcams } from '../db/schema';
import { eq, like } from 'drizzle-orm';
import { getImageUrls } from '../utils/fetchImageUrls';
import { saveWebcamUrl } from '../utils/saveWebcamUrl';

export async function updateHzsWebcams() {
  const cams = await db.select().from(webcams).where(
    eq(webcams.sourceType, 'IMG_TAG')
  ).where(like(webcams.imgPageUrl, '%meteo.hzs%'));

  const ids = cams.map(cam => cam.imgTagId).filter(Boolean) as string[];

  const urls = await getImageUrls(ids);

  for (const cam of cams) {
    const url = urls[cam.imgTagId!];
    await saveWebcamUrl(cam.id, url);
  }
}
