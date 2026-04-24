# Capture Automation

Use automation to create the raw device captures that will feed the final App Store compositions.

## Script Design Goals

Your script should be able to:

- choose or boot the target simulator
- verify required tools and app installation before doing work
- launch the app with sample-data and locale parameters
- navigate to specific screens reliably
- save screenshots into a deterministic directory structure
- run in a small proof mode before any batch generation

For native Apple apps, use [native-apple-capture-checklist.md](./native-apple-capture-checklist.md) to verify that sample data, routes, identifiers, simulator inputs, and rerun commands are ready before writing the raw capture script.

## Language Choice

- Prefer Python, JavaScript, or the language the project already uses for automation.
- Use Python when the workflow is mostly orchestration over `simctl`, accessibility inspection, file operations, and structured manifests.
- Use JavaScript or TypeScript when the project already has Node-based tooling or wants to reuse Playwright-style helpers.

## Navigation Preference Order

Use the most stable navigation layer the project can support:

1. Existing UI tests or accessibility identifiers.
2. Deep links or launch routes that open the requested screen directly.
3. Accessibility tree queries with semantic labels or identifiers.
4. Coordinate taps only as a last resort.

Do not start with raw coordinates if the project can expose stable identifiers instead.

## Preflight Checks

Before capturing anything, verify:

- the simulator runtime and requested device are available
- the app is installed on the target simulator
- the sample-data mode exists and is reachable
- any required command-line tools are installed
- the output directory is writable

Fail early with actionable messages instead of silently continuing in a broken state.

## Proof Mode Rules

- Default to one locale and a small subset of screens.
- Keep proof mode fast enough that the user can iterate repeatedly.
- Include the exact command needed to rerun only one locale, one device, or one screen.

A generic proof command might look like:

```text
python3 scripts/generate_screenshots.py --locale en-US --device iphone --screens home,report --proof
```

## Output Layout

Use a stable relative output tree, for example:

```text
app-store-captures/raw/{device}/{locale}/{screen}.png
```

Keep raw captures separate from final exported store assets.

## Locale Handling

- Pass locale configuration through automation rather than manually changing simulator settings.
- Keep locale names explicit in both the manifest and the output tree.
- Make sure proof mode can run on a single locale without rewriting the whole configuration.

## Visual Stabilization

When the project needs repeatable screenshots, consider stabilizing:

- status bar state
- appearance mode
- first-run prompts
- network-driven refreshes
- background sync or live updates

Only override what is necessary for consistent captures.
