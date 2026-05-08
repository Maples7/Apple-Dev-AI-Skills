#!/usr/bin/env node
/**
 * Reference template: Playwright-based App Store screenshot exporter.
 *
 * This script is a STARTING POINT. Copy it into the project's own
 * scripts directory and adapt the locale list, device list, route
 * scheme, and output layout to the app's compose web app.
 *
 * Use this layer ONLY when the App Store deliverable is a composed
 * image (device frame + headline + background + raw simulator capture).
 * If the simulator capture is the deliverable, skip this layer entirely.
 *
 * Architecture assumed:
 * - The project has a small web app (Next.js, Vite, plain HTML, ...)
 *   that renders one composition per `(device, locale, screen)` URL.
 *   For example: http://127.0.0.1:3000/<locale>/<device>/<screen>.
 * - The web app is already running at BASE_URL (the caller is
 *   responsible for `pnpm dev`, `npm run dev`, etc., before invoking
 *   this script).
 * - Each composition page renders at the exact pixel size required by
 *   the App Store target slot.
 *
 * Requirements:
 *   pnpm add -D @playwright/test
 *   npx playwright install chromium
 *
 * Usage:
 *   node scripts/compose-screenshots.mjs --proof
 *   node scripts/compose-screenshots.mjs --proof --locale ja --device iphone
 *   node scripts/compose-screenshots.mjs --batch
 *   node scripts/compose-screenshots.mjs --batch --locale ja --device iphone
 */

import { chromium } from '@playwright/test';
import { mkdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';
import yaml from 'js-yaml';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

// ---------- Project-specific configuration (edit this block) ----------

const BASE_URL = process.env.SCREENSHOT_BASE_URL ?? 'http://127.0.0.1:3000';

// Locale list. Must match what the compose web app supports.
const LOCALES = [
  'en-US', 'de-DE', 'es-ES', 'fr-FR', 'it-IT',
  'ja', 'ko', 'pt-BR', 'zh-Hans', 'zh-Hant',
];

// Device families. Sizes are the pixel dimensions of the composition
// page rendered headlessly; they should match the App Store Connect
// slot the project targets.
const DEVICES = {
  iphone: {
    label: 'iPhone 6.9"',
    folder: 'APP_IPHONE_67',
    width: 1290,
    height: 2796,
  },
  ipad: {
    label: 'iPad Pro 12.9"',
    folder: 'APP_IPAD_PRO_3GEN_129',
    width: 2048,
    height: 2732,
  },
};

// Default output root. Adjust to wherever the project's metadata config
// expects screenshot files (for example a `store/<vendor>/screenshot/`
// tree referenced from `store.config.json`).
const OUTPUT_ROOT = path.join(PROJECT_ROOT, 'store', 'apple', 'screenshot');

// Validation root for proof exports.
const VALIDATION_ROOT = path.join(PROJECT_ROOT, '.validation-previews');

// Default capture-manifest location.
const DEFAULT_MANIFEST = path.join(PROJECT_ROOT, 'capture-manifest.yaml');

// ---------- Generic helpers ----------

function buildUrl(locale, deviceKey, screenId) {
  // Adjust to match the compose web app's route scheme.
  return `${BASE_URL}/${encodeURIComponent(locale)}/${encodeURIComponent(deviceKey)}/${encodeURIComponent(screenId)}`;
}

function exportFilename(index, screenId, device) {
  // Numeric prefix preserves slide order on disk so a downstream
  // store-config sync script can rebuild the path array deterministically.
  const prefix = String(index + 1).padStart(2, '0');
  return `${prefix}-${screenId}-${device.width}x${device.height}.png`;
}

function exportDir(rootBase, locale, device) {
  return path.join(rootBase, locale, device.folder);
}

async function loadManifest(manifestPath) {
  const raw = await readFile(manifestPath, 'utf8');
  return yaml.load(raw);
}

function resolveRuns(manifest, options) {
  const block = manifest[options.mode];
  let locales = options.locale ? [options.locale]
    : (Array.isArray(block.locales) ? block.locales : [block.locale]);
  let devices = options.device ? [options.device] : block.devices;
  const screenIds = options.screen ? [options.screen]
    : (block.screens ?? manifest.screens.map((s) => s.id));
  const screensById = Object.fromEntries(manifest.screens.map((s) => [s.id, s]));

  const runs = [];
  for (const deviceKey of devices) {
    for (const locale of locales) {
      screenIds.forEach((id, index) => {
        const meta = screensById[id];
        if (!meta) {
          throw new Error(`Manifest is missing screen ${id}`);
        }
        runs.push({ index, deviceKey, locale, screenId: id, meta });
      });
    }
  }
  return runs;
}

async function exportOne(browser, run, outputRootBase) {
  const device = DEVICES[run.deviceKey];
  if (!device) {
    throw new Error(`Unknown device key: ${run.deviceKey}`);
  }

  const context = await browser.newContext({
    viewport: { width: device.width, height: device.height },
    deviceScaleFactor: 1,
  });
  const page = await context.newPage();

  const url = buildUrl(run.locale, run.deviceKey, run.screenId);
  await page.goto(url, { waitUntil: 'networkidle' });

  // Allow any web fonts and lazy assets to settle. Replace this with a
  // project-specific readiness signal (a data-testid="ready" attribute
  // on the page root, for example) when available.
  await page.waitForFunction(() => document.fonts?.ready ?? true);
  await page.waitForTimeout(150);

  const dir = exportDir(outputRootBase, run.locale, device);
  await mkdir(dir, { recursive: true });
  const file = path.join(dir, exportFilename(run.index, run.screenId, device));

  await page.screenshot({
    path: file,
    fullPage: false,
    omitBackground: false, // App Store deliverables must be opaque.
    type: 'png',
  });

  await context.close();
  return file;
}

async function main() {
  const { values } = parseArgs({
    options: {
      manifest: { type: 'string', default: DEFAULT_MANIFEST },
      proof: { type: 'boolean', default: false },
      batch: { type: 'boolean', default: false },
      locale: { type: 'string' },
      device: { type: 'string' },
      screen: { type: 'string' },
    },
  });

  if (!values.proof && !values.batch) {
    console.error('Specify --proof or --batch.');
    process.exit(64);
  }

  const manifest = await loadManifest(values.manifest);
  const runs = resolveRuns(manifest, {
    mode: values.proof ? 'proof' : 'batch',
    locale: values.locale,
    device: values.device,
    screen: values.screen,
  });

  if (runs.length === 0) {
    console.error('No runs to export. Check manifest filters.');
    process.exit(1);
  }

  const outputRootBase = values.proof ? VALIDATION_ROOT : OUTPUT_ROOT;
  const browser = await chromium.launch();
  try {
    for (const run of runs) {
      const file = await exportOne(browser, run, outputRootBase);
      console.log(`Exported ${file}`);
    }
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(2);
});
