# Batch Pipeline

Use this reference when the project is past the proof stage and is about to capture, compose, and validate the full locale and device matrix. The goal is concrete tool selection and concrete control flow so the agent does not have to rediscover the workflow by trial and error.

## Tool Layer Cheatsheet

Pick the lowest layer that gives stable behavior for each step. Climbing higher adds dependencies; staying lower adds fragility.

| Step | First choice | When to climb |
| --- | --- | --- |
| Boot, install, launch, locale, appearance, status bar, privacy grants | `xcrun simctl` | Always start here. `simctl` has no extra runtime and ships with Xcode. |
| App-internal navigation between screens | Existing UI tests, deep links, or accessibility identifiers exposed by the app | Climb to a UI tree query layer only when the app cannot expose a direct route. |
| Reading the live UI tree to find a label or identifier and tapping it | `idb ui describe-all` + `idb ui tap` | Use when accessibility identifiers exist but the project has no XCUITest harness. |
| Coordinate taps | `xcrun simctl io … tap` or `idb ui tap` with absolute points | Last resort. Fragile across device sizes and locale-driven layout shifts. |
| Adding device frames, marketing copy, gradient backgrounds, or compositing several captures into one image | A local web app (Next.js, Vite, plain HTML) rendered headless with Playwright or Puppeteer | Use when the App Store deliverable is a composed image, not a raw simulator capture. |
| Final image-format validation (size, opacity, count) | A small Python script using Pillow | Always include this before considering the batch ready for upload. |

## Required Stabilization Before Capture

Inconsistent baseline state is the most common reason "the same script captured a different image" mysteries appear. Before any capture run:

- Lock the appearance: `xcrun simctl ui <udid> appearance light` (or `dark`).
- Override the status bar: `xcrun simctl status_bar <udid> override --dataNetwork wifi --wifiBars 3 --batteryState charged --batteryLevel 100 …`. Note that some `simctl` releases reject `--time` formats; if so, accept the live clock rather than fighting it.
- Pre-grant any privacy prompts the app would otherwise show mid-capture (location, photos, contacts): `xcrun simctl privacy <udid> grant <service> <bundleId>`.
- Terminate the running app before relaunching to clear navigation state: `xcrun simctl terminate <udid> <bundleId>`.
- Pass locale via launch arguments rather than mutating simulator settings: `-AppleLanguages "(<lang>)" -AppleLocale <locale>`.
- Pass screenshot mode through a project-owned launch flag (for example `-UseScreenshotSampleData` or `-UsePreviewSampleData`) so the app boots into deterministic data without opening a non-shipping debug surface.

If a step in this list is not in the capture script, the script is not yet stable enough for batch.

## Navigation Pattern: Accessibility-First With idb

When deep links are not available, prefer the accessibility tree.

```python
tree = json.loads(run(["idb", "ui", "describe-all", "--udid", udid, "--json"]).stdout)
node = next(n for n in tree if n.get("AXUniqueId") == "home.tab.reports")
frame = node["frame"]
run(["idb", "ui", "tap", "--udid", udid,
     str(int(frame["x"] + frame["width"] / 2)),
     str(int(frame["y"] + frame["height"] / 2))])
```

Rules:

- Resolve a node by stable identifier first (`AXUniqueId`), then by label, then by type. Avoid label-only lookups in localized apps because the label changes with locale.
- Tap via the node's reported center, not by hardcoded coordinates. Layout shifts across device sizes break hardcoded coordinates first.
- Wait for stability between taps. After a tap, poll `describe-all` for the expected target node before screenshotting; do not rely on `time.sleep` alone.

If the agent finds itself writing a chain of fixed coordinate taps, that is a signal the app is missing accessibility identifiers and the right next step is to add them, not to brute-force coordinates.

## Manifest-Driven Capture

Drive batch from a single manifest so the matrix lives in the repository, not in chat history.

Recommended shape (see [../assets/capture-manifest.yaml](../assets/capture-manifest.yaml)):

```yaml
proof:
  locale: en-US
  devices: [iphone]
  screens: [home, primary-feature]

batch:
  locales: [en-US, de-DE, ...]
  devices: [iphone, ipad]

screens:
  - id: home
    appearances: [light]
    filename: 01-home.png
    navigation: { strategy: launch }
  - id: report
    appearances: [light]
    filename: 02-report.png
    navigation:
      strategy: accessibility
      steps:
        - { tap_uid: home.tab.reports }
        - { wait_for_uid: report.title }
```

The capture script's job is to walk this manifest, not to embed any of those names. The reference template at [../assets/capture-screenshots.py](../assets/capture-screenshots.py) shows one minimal implementation.

## Proof Mode And Batch Mode

Every long-running script in this pipeline must support a small proof mode:

- proof = one locale, one device, a subset of screens, a single appearance
- batch = the full locale × device × screen × appearance matrix

The proof command should run end-to-end in a few minutes. If proof is not fast enough to iterate on, batch will be unusable.

A minimal CLI surface:

```text
python3 scripts/capture-screenshots.py --proof
python3 scripts/capture-screenshots.py --proof --locale ja --device iphone
python3 scripts/capture-screenshots.py --batch
python3 scripts/capture-screenshots.py --batch --locale ja
python3 scripts/capture-screenshots.py --batch --screen report
```

## Parallel Device Runners

For batch mode, run iPhone and iPad in parallel processes against separate simulator UDIDs. They are independent simulators with independent app installations; serializing them doubles wall-clock time for no benefit.

A safe pattern:

- Start each device worker as a child process with its own log file under a per-run output directory.
- Stream-merge logs at the end, or surface only the failure summary when something fails.
- Keep retries device-scoped: a single locale failing on iPhone should not invalidate completed iPad locales.

Do not mix two device families on one simulator UDID; `simctl` and `idb` both treat the simulator as a singleton bound to that UDID.

## Compose And Export Layer

If the App Store deliverable is a composed image (device frame + headline + background), the raw simulator capture is the input, not the output.

Recommended flow:

1. The app captures `app-store-assets/raw/<device>/<locale>/<screen>.png` from the simulator.
2. A local web app (Next.js, Vite, or static HTML) renders one composition per `(device, locale, screen)` URL, reading the raw capture, the locale's marketing copy, and the device frame asset.
3. A Playwright (or Puppeteer) script visits each URL at the device's exact pixel size, snapshots the full page, and writes the PNG into the final output tree.

See [../assets/compose-screenshots.mjs](../assets/compose-screenshots.mjs) for a minimal Playwright export template.

If composition is not needed (the app's UI is shippable as-is), skip this layer entirely. Do not introduce a compose step because it looks more polished; introduce it only when the design actually requires it.

## Filesystem-First, Config-Second

Once raw captures and final exports settle on a stable on-disk layout, regenerating the metadata config from the filesystem is much safer than hand-editing arrays.

Pattern:

- The store config (for example `store.config.json` for EAS metadata) holds a per-locale, per-device list of screenshot paths in display order.
- Slide order is encoded by a numeric prefix in the filename (`01-home`, `02-report`, ...).
- A small script walks `<root>/<locale>/<deviceFolder>/` and rebuilds the array in numeric-prefix order, replacing the existing array. See [../assets/sync-store-config-screenshots.py](../assets/sync-store-config-screenshots.py).

This keeps the manifest, the filesystem, and the upstream config in sync without hand-editing one when the others change.

## Validation Before Upload

Always run a project-owned validator before treating a batch as ready. At minimum:

- every expected `(locale, device)` cell exists
- every expected `screenshot.png` is present
- pixel dimensions match the active App Store Connect spec for the chosen device family
- final images are fully opaque (no alpha)

Use [../assets/validate-exported-images.py](../assets/validate-exported-images.py) as the size + opacity validator and add a small completeness check (count parity with the manifest) on top when the project ships many locales.

If validation fails, fix the source (script, manifest, raw capture) and re-run the affected cells. Do not patch the failing PNG by hand; the next regeneration will silently revert it.

## Common Failure Modes To Plan For

These bite during long-running batch runs in particular. Plan for them in the script rather than catching them by surprise.

- `idb_companion` can die if its parent worktree or terminal is removed. After any environment change, re-run `idb connect <udid>` before the next batch.
- A permission prompt that was suppressed last release can re-appear after an iOS update; re-grant permissions in the launch helper rather than tapping them away in the capture script.
- A screen whose layout depends on network data (live charts, web embeds) needs a deterministic seed inside the app, not a wait loop in the script. If the script is full of `time.sleep`, the app is missing seed data.
- Long captures may hit `idb` timeouts on the first call after a cold simulator boot. Wrap the first describe / first screenshot per device in a single retry; do not generalize retries everywhere.
- Gitignored raw or final screenshot directories do not follow `git merge`. Treat regenerated screenshots as a deployment artifact: re-run the pipeline on whichever branch you are about to upload from.
