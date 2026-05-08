# Troubleshooting

Use these checks when EAS metadata commands fail or when the repository state and App Store Connect drift apart.

## Project Is Not Linked To EAS

Common symptoms:

- metadata commands do not resolve the current project correctly
- `extra.eas.projectId` is missing from app config
- the project was never initialized for EAS services

What to do:

- run `eas init` or `eas project:init`
- verify the expected app config now contains `extra.eas.projectId`
- if the project belongs to a different Expo account or organization, make that ownership explicit before continuing

## Expo Authentication Blocks Automation

Common symptoms:

- `eas login` is required
- SSO or 2FA prompts interrupt non-interactive execution
- the user is not in the correct Expo account or organization

What to do:

- log in with the correct Expo account or set `EXPO_TOKEN` when appropriate
- hand off the login step when the agent cannot complete the required interactive authentication safely
- resume the metadata flow only after authentication is confirmed

## Private Key Lives Inside The Repository

Common symptoms:

- `ascApiKeyPath` points to `./credentials/...` or another path under the checkout
- the team relies on `.gitignore` instead of a real secret boundary

What to do:

- move the `.p8` file to a user-private local directory outside the repository
- recommended best default on macOS: a per-user private Application Support directory outside the checkout
- update only the untracked local config or environment variable that references that key
- if the key was ever committed or shared, rotate it instead of assuming deletion is enough

## ASC_API_KEY_PATH Is Unset Or Not Resolved

Common symptoms:

- tracked `eas.json` uses `"ascApiKeyPath": "$ASC_API_KEY_PATH"`
- EAS falls back to prompting for the API key path or warns that the referenced file does not exist
- the command works in one shell but fails in another

What to do:

- export `ASC_API_KEY_PATH` from untracked local shell config, direnv, or another local-only runner setup
- confirm the variable points to the outside-repo `.p8` file that should be used on this machine
- if the project also env-backs `ascApiKeyIssuerId` or `ascApiKeyId`, confirm those variables are set too
- avoid fixing the problem by committing the resolved absolute path into `eas.json`

## App Does Not Exist On App Store Connect Yet

Common symptoms:

- `eas metadata:pull` cannot bootstrap a local config because there is no existing app listing

What to do:

- start from a new local store-config template instead of expecting pull to generate it
- make app creation or first-submission prerequisites explicit in the release handoff

## Push Fails Because No Target Draft Exists

Common symptoms:

- metadata push expects a version draft or processed binary state that is not ready yet

What to do:

- create the target App Store Connect version draft first if the project requires it
- make sure the binary upload and processing state matches the release step you are attempting
- retry the metadata push only after the listing state is ready

## Partial Metadata Upload

Common symptoms:

- some locales or screenshots upload while others fail

What to do:

- review the exact failing fields or assets
- correct the local source of truth
- rerun lint and push intentionally instead of assuming the partial result is acceptable

## Dashboard Drift After Manual UI Edits

Common symptoms:

- the App Store Connect web UI and local files disagree
- a fresh push would overwrite recent manual edits

What to do:

- pull first with `eas metadata:pull`
- review the diff
- only then make new local edits and push again

## Screenshot Paths Or Locale Assets Fail

Common symptoms:

- screenshot upload fails for one locale or one device family
- relative paths in metadata do not exist locally

What to do:

- verify file existence from the repository root
- confirm the locale and device directory layout matches the metadata references
- keep path conventions consistent instead of patching one path at a time without a policy

## EAS CLI Reports Success Despite Partial Screenshot Upload Failure

Common symptoms:

- `eas metadata:push` exits with code `0`
- but the same run prints lines such as:
  - `✖ Failed uploading screenshot <name> (<locale>)`
  - `✖ Failed deleting screenshot <name> (<locale>)`
  - `Unexpected response: [object Object]`
  - `Store configuration upload encountered an error.`
- App Store Connect ends up partially synced

Why this happens:

- EAS CLI catches and logs per-asset failures during the screenshot phase but does not propagate them into the process exit code in every release. Treat the exit code as advisory, not authoritative, for `metadata:push`.

What to do:

- Do not gate "did push succeed" on `$?` alone. Capture stdout and stderr to a log and grep it for the failure markers above.
- Treat the run as failed if any of these strings appear: `Failed uploading screenshot`, `Failed deleting screenshot`, `Failed reordering screenshots`, `Failed creating screenshot set`, `Unexpected response`, `Store configuration upload encountered an error`.
- Re-run `eas metadata:push` until a full pass with none of those markers in the output. The push step is idempotent: completed assets match by filename + filesize and are skipped on the next run.
- Use [assets/eas-metadata-push-retry.sh](../assets/eas-metadata-push-retry.sh) as a reference wrapper.

## App Store Connect Screenshot Order Drifts From Local Config

Common symptoms:

- after a push that eventually exits 0, the screenshot order shown in App Store Connect does not match the array order in `store.config.json`
- some locales or device families are correct, others are scrambled
- earlier runs in the same release cycle had transient `Failed (uploading|deleting) screenshot` lines

Why this happens:

- For each `(locale × screenshotDisplayType)` pair, EAS CLI runs in this order: diff existing vs config, delete obsolete, upload missing, then call `screenshotSet.reorderScreenshotsAsync` to align the App Store Connect order with the config array order.
- The reorder step is the **last** step in the pair's loop. If any earlier delete or upload throws, the pair aborts before it reaches reorder, leaving App Store Connect in whatever order assets happened to land in chronologically.
- A subsequent retry that finds all assets already matching by filename + filesize will still call reorder for that pair — but only if the entire pair completes without errors that run.
- After many retries with overlapping partial failures, some pairs may never have completed a clean pass that hit reorder.

What to do (in order):

1. Re-run `eas metadata:push --profile <profile>` once until it completes with **no** failure markers in stdout (see the previous section). Reorder is idempotent; a clean pass repairs every pair.
2. Verify by running `eas metadata:pull --profile <profile>` and diffing against the local source of truth. The pull download step preserves App Store Connect's current order, so a clean diff means orders are aligned.
3. If a specific pair refuses to reorder cleanly through EAS CLI, write a small App Store Connect API helper that uses the same `.p8`:
   - `GET /v1/appStoreVersionLocalizations/{id}/appScreenshotSets`
   - `GET /v1/appScreenshotSets/{setId}?include=appScreenshots` to inspect the live order
   - `PATCH /v1/appScreenshotSets/{setId}/relationships/appScreenshots` with the desired ID array to force the order
4. As a last resort, delete the affected screenshot set entirely (App Store Connect web UI or API), then re-push. Fresh uploads land in config order naturally and the reorder step still fires as a safety net.

Do not "fix" order drift by editing the array in `store.config.json`. The local file is the intended order; the dashboard is the side that must converge.

## Long Pushes Need A Stdout-Aware Retry Loop

Common symptoms:

- the project ships many locales × devices and `eas metadata:push` takes long enough to hit transient App Store Connect API hiccups
- transitions between iPhone and iPad sets, or between locale boundaries, are statistically the most flaky points
- a single manual rerun is not enough to converge

What to do:

- Wrap the push in a retry loop that:
  1. tees stdout and stderr to a per-attempt log file
  2. greps the log for the failure markers listed two sections up
  3. only declares success when the markers are absent
  4. caps the attempt count and surfaces the last log path on giving up
- Run it inside a stable shell session (the loop can be long-lived). Capture exit reasons; do not silently keep retrying forever.
- Use [assets/eas-metadata-push-retry.sh](../assets/eas-metadata-push-retry.sh) as a reference template.

## Shell Quoting Pitfalls When Wrapping eas-cli On macOS

Common symptoms:

- a heredoc or inline retry script that worked for the agent in one shell explodes into `dquote>`/`then>` continuations in the user's interactive shell
- background jobs survive an editor crash but their PIDs are no longer reachable
- `setsid` is missing on macOS

What to do:

- zsh's interactive history expansion will rewrite a literal `$!` (last-background-job PID) inside double-quoted strings. When scripting around `nohup … & echo $!`, write the loop to a file (`/tmp/eas-push-retry.sh`) and execute it instead of pasting it into an interactive shell, or run `setopt no_bang_hist` for the session.
- macOS does not ship `setsid`. To detach a long-running retry from the controlling terminal, prefer `nohup ./eas-push-retry.sh >log 2>&1 & disown`. If the agent invoking it has a long-enough sync timeout, run it in the foreground instead of trying to detach.
- After re-creating an executable script via a file-write tool, re-apply `chmod +x` — write tools commonly drop the executable bit.

## Gitignored Screenshot Trees Lost Across Worktree Or Branch Operations

Common symptoms:

- the project gitignores raw or final screenshot directories so they stay local
- merging a feature branch into the release branch does not bring the freshly captured PNGs along
- the next push tries to upload paths that exist in the merged `store.config.json` but not on disk in the current worktree

What to do:

- Treat regenerated screenshots as a deployment artifact, not a merge artifact. Re-run the project's capture/export pipeline on the branch from which the push will happen.
- Document this constraint in the project's release runbook so the same surprise does not bite the next maintainer.
- If the project legitimately wants screenshots to follow merges, lift the gitignore for the final-export directory and accept the larger repository — but make that decision deliberately, not by accident.
