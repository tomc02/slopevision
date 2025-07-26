import fs from "fs";
import path from "path";
import { promisify } from "util";
import { pipeline } from "stream";
import { exec } from "child_process";
import axios from "axios";
import { parse } from "url";
import { Storage } from "@google-cloud/storage";
import puppeteer from "puppeteer";
import { eq } from "drizzle-orm";
import { webcams as Webcam, webcamHistories as WebcamHistory } from "../db/schema"; // your Drizzle schema
import { db } from "../db/client";
import { DateTime } from "luxon";

const execAsync = promisify(exec);
const streamPipeline = promisify(pipeline);

const BUCKET_NAME = "slopevision-dev";
const storage = new Storage();
const bucket = storage.bucket(BUCKET_NAME);

export async function captureAllWebcams() {
    const webcams = await db.select().from(Webcam).orderBy(Webcam.id);

    console.log(`Found ${webcams.length} webcams.`);

    for (const webcam of webcams) {
        const url = webcam.sourceUrl;
        if (!url) {
            console.log(`Skipping webcam '${webcam.name}' (ID: ${webcam.id}) - No URL provided.`);
            continue;
        }

        try {
            const timestamp = DateTime.now().setZone("Europe/Prague").toFormat("yyyyLLddHHmmss");
            const parsedUrl = parse(url);
            const ext = path.extname(parsedUrl.pathname || "") || ".jpg";
            const fileName = `${webcam.id}_${timestamp}${ext}`;

            if (isEmbedUrl(url)) {
                console.log(`Processing embed webcam '${webcam.name}' (ID: ${webcam.id}) - URL: ${url}`);
                await captureEmbedScreenshot(webcam, url, fileName);
            } else {
                console.log(`Processing webcam '${webcam.name}' (ID: ${webcam.id}) - URL: ${url}`);
                const response = await axios.get(url, {
                    responseType: "stream",
                    validateStatus: () => true,
                    httpsAgent: new (require("https").Agent)({ rejectUnauthorized: false }),
                });

                if (response.status !== 200) throw new Error(`Request failed with status ${response.status}`);

                const contentType = response.headers["content-type"] || "";

                if (contentType.startsWith("image")) {
                    await uploadStreamToGCS(response.data, `webcam_images/${fileName}`, contentType);
                    await logToHistory(webcam.id, `webcam_images/${fileName}`);
                    console.log(`Saved image for webcam '${webcam.name}'`);
                } else if (contentType.startsWith("video")) {
                    const localPath = `/tmp/${fileName}`;
                    const compressedPath = `/tmp/compressed_${fileName}`;

                    await streamPipeline(response.data, fs.createWriteStream(localPath));
                    await compressVideo(localPath, compressedPath);

                    await uploadFileToGCS(compressedPath, `webcam_videos/${fileName}`);
                    await logToHistory(webcam.id, undefined, `webcam_videos/${fileName}`);
                    console.log(`Saved video for webcam '${webcam.name}'`);

                    fs.unlinkSync(localPath);
                    fs.unlinkSync(compressedPath);
                }
                else if (contentType.startsWith("multipart/x-mixed-replace")) {
                    const localPath = `/tmp/${fileName}`;
                    await captureFrameWithFFmpeg(url, localPath);
                    await uploadFileToGCS(localPath, `webcam_images/${fileName}`);
                    await logToHistory(webcam.id, `webcam_images/${fileName}`);
                    fs.unlinkSync(localPath);
                }
                else {
                    console.warn(`Unsupported content type: ${contentType}`);
                }
            }
        } catch (err) {
            console.error(`Failed to process webcam '${webcam.name}' (ID: ${webcam.id}):`, err);
        }
    }
}

async function captureFrameWithFFmpeg(url: string, outputPath: string) {
    const cmd = `ffmpeg -y -i "${url}" -frames:v 1 -q:v 2 "${outputPath}"`;
    await execAsync(cmd);
}

function isEmbedUrl(url: string): boolean {
    return url.includes("embed") || url.endsWith(".html");
}

async function captureEmbedScreenshot(webcam: any, url: string, fileName: string) {
    const browser = await puppeteer.launch({ headless: "new", args: ["--no-sandbox", "--ignore-certificate-errors"] });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });

    await new Promise((r) => setTimeout(r, 15000)); // wait for stream
    const buffer = await page.screenshot();
    await browser.close();

    await uploadBufferToGCS(buffer, `webcam_images/${fileName}`, "image/png");
    await logToHistory(webcam.id, `webcam_images/${fileName}`);
    console.log(`Captured screenshot for embed webcam '${webcam.name}'`);
}

async function uploadStreamToGCS(stream: NodeJS.ReadableStream, filePath: string, contentType: string) {
    const file = bucket.file(filePath);
    const writeStream = file.createWriteStream({ metadata: { contentType } });
    await streamPipeline(stream, writeStream);
    console.log(`Uploaded to GCS: ${filePath}`);
}

async function uploadFileToGCS(localPath: string, filePath: string) {
    await bucket.upload(localPath, { destination: filePath });
    console.log(`Uploaded file to GCS: ${filePath}`);
}

async function uploadBufferToGCS(buffer: Buffer, filePath: string, contentType: string) {
    const file = bucket.file(filePath);
    await file.save(buffer, { contentType });
    console.log(`Uploaded buffer to GCS: ${filePath}`);
}

async function compressVideo(input: string, output: string) {
    const cmd = `ffmpeg -i ${input} -vf "scale=640:-1,fps=10" -c:v libx264 -crf 35 -an ${output}`;
    await execAsync(cmd);
    console.log(`Compressed video saved: ${output}`);
}

async function logToHistory(webcamId: number, imagePath?: string, videoPath?: string) {
    const insertedRows = await db.insert(WebcamHistory).values({
        webcamId,
        image: imagePath ?? null,
        video: videoPath ?? null,
        timestamp: DateTime.now().setZone("Europe/Prague").toJSDate(),
    }).returning({ insertedId: WebcamHistory.id });

    const insertedId = insertedRows[0]?.insertedId;

    if (insertedId) {
        await db.update(Webcam).set({ latestHistoryId: insertedId }).where(eq(Webcam.id, webcamId));
        console.log(`Logged history for webcam ID ${webcamId} with history ID ${insertedId}`);
    } else {
        console.error(`Failed to log history for webcam ID ${webcamId}`);
    }
}
