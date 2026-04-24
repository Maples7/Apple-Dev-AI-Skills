# Project Layout

Keep the screenshot pipeline organized so raw captures, review assets, and final deliverables are easy to understand and rerun.

## Recommended Layout

```text
app-store-assets/
├── app-store-preview-pipeline-profile.yaml
├── capture-manifest.yaml
├── raw/
│   ├── iphone/
│   │   └── en-US/
│   └── ipad/
│       └── en-US/
├── review/
│   └── proof/
├── preview-app/
│   ├── public/
│   └── src/
└── export/
    ├── iphone/
    └── ipad/
```

## Purpose Of Each Layer

- `app-store-preview-pipeline-profile.yaml`: project-wide policy such as locales, sample-data strategy, and export rules
- `capture-manifest.yaml`: per-screen scope, navigation intent, and proof or batch rollout
- `raw/`: direct simulator captures before the final marketing composition layer
- `review/proof/`: small sample outputs used for approval loops
- `preview-app/`: local web preview and export source when the project uses a browser-based composition tool
- `export/`: final delivery outputs ready for App Store Connect upload

## Layout Rules

- Keep raw captures separate from final exports.
- Keep proof outputs separate from full batch exports.
- Do not bury the profile or manifest inside generated folders.
- Treat the preview app as reproducible source, not as a scratch directory.
- Keep locale and device names explicit in folder names.

## When To Deviate

Use the project's existing conventions when they are already clear and stable. The goal is reproducibility and reviewability, not enforcing one exact folder tree.
