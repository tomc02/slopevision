import {
    pgTable,
    text,
    varchar,
    timestamp,
    doublePrecision,
    integer,
    primaryKey,
    serial,
    uuid,
    boolean,
    index,
} from 'drizzle-orm/pg-core';

import { relations } from 'drizzle-orm';

// === Place ===
export const places = pgTable('rest_api_place', {
    id: serial('id').primaryKey(),
    name: varchar('name', { length: 255 }).notNull(),
    latitude: doublePrecision('latitude').notNull(),
    longitude: doublePrecision('longitude').notNull(),
    description: text('description'),
    country: varchar('country', { length: 100 }).notNull(),
    nearestCity: varchar('nearest_city', { length: 100 }),
    mounainRange: varchar('mounain_range', { length: 100 }),
    firstWebcamId: integer('first_webcam_id').references(() => webcams.id, {
        onDelete: 'set null',
    }),
});

// === Webcam ===
export const webcams = pgTable('rest_api_webcam', {
    id: serial('id').primaryKey(),
    name: varchar('name', { length: 100 }).notNull(),
    placeId: integer('place_id').references(() => places.id, {
        onDelete: 'cascade',
    }),
    sourceType: varchar('source_type', { length: 10 }).default('IPCAM'),
    sourceUrl: varchar('source_url', { length: 1000 }),
    pageUrl: varchar('page_url', { length: 200 }),
    imgPageUrl: varchar('img_page_url', { length: 200 }),
    imgTagId: varchar('img_tag_id', { length: 100 }),
    lastUpdated: timestamp('last_updated', { withTimezone: true }).defaultNow(),
    historyRate: integer('history_rate').default(30),
    latestHistoryId: integer('latest_history_id').references(() => webcamHistories.id, {
        onDelete: 'set null',
    }),
});

// === WebcamHistory ===
export const webcamHistories = pgTable('rest_api_webcamhistory', {
    id: serial('id').primaryKey(),
    webcamId: integer('webcam_id').references(() => webcams.id, {
        onDelete: 'cascade',
    }),
    timestamp: timestamp('timestamp', { withTimezone: true }).defaultNow(),
    image: varchar('image', { length: 500 }),
    video: varchar('video', { length: 500 }),
}, (table) => ({
    idxTimestamp: index('idx_webcam_timestamp').on(table.timestamp),
    idxWebcamTime: index('idx_webcam_webcamid_time').on(table.webcamId, table.timestamp.desc()),
}));