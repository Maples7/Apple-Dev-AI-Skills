# Security & Privacy Checklist

Surface-level security review for Apple-platform diffs. Deep audits (cryptography review, threat modeling, pen-testing) are out of scope.

## Secrets & Credentials

- No API keys, tokens, OAuth secrets, signing identities, or certificates committed in source, plists, xcconfig, or fixtures.
- No hardcoded server URLs that should be environment-driven.
- `xcconfig` / `Info.plist` keys for secrets reference build settings or environment, not literal values.
- New `.env`, `.p12`, `.mobileprovision`, `.cer`, or `GoogleService-Info.plist`-style files are reviewed for whether they belong in git or in `.gitignore`.

## Storage & Data Handling

- Sensitive data (auth tokens, refresh tokens, biometric state, health data, payment info) is stored in Keychain with appropriate `kSecAttrAccessible…` class — not in `UserDefaults`, plain files, or NSUbiquitousKeyValueStore.
- App Groups / shared containers do not leak data the extension should not see.
- New caches do not persist sensitive data beyond the user's expectation; cache directories are correctly chosen (`.cachesDirectory` vs `.applicationSupportDirectory` vs Documents).
- New CloudKit / iCloud / file-provider writes have explicit scope and are not opt-out without consent.

## Networking

- New requests go over HTTPS; no `NSAllowsArbitraryLoads = true` regression in `Info.plist`.
- ATS exceptions are domain-scoped and justified, not global.
- Certificate or public-key pinning, if used by the project, is preserved on new endpoints.
- Tokens are sent in `Authorization` headers, not query strings or logs.
- WebView (`WKWebView`) usage isolates JavaScript bridges; `javaScriptEnabled` only where required; no `loadHTMLString` from untrusted input.

## Authentication & Authorization

- Sign in with Apple / OAuth flows preserve nonce / PKCE; no shortcut that drops the nonce check.
- Biometric (`LAContext`) prompts have a clear `localizedReason`; fallback to passcode is intentional.
- New entitlements (`com.apple.developer.*`) are necessary and noted in the diff explanation.

## Permissions & Privacy

- New use of camera, microphone, location, contacts, photos, HealthKit, motion, Bluetooth, Local Network, or Tracking has the matching `NS…UsageDescription` string with user-readable wording.
- Privacy manifest (`PrivacyInfo.xcprivacy`) is updated when new tracking domains, required-reason APIs (file timestamps, disk space, system boot time, user defaults), or data categories are added.
- Tracking transparency (`ATTrackingManager`) is requested before any IDFA or cross-app tracking.
- Sensitive data (health, location, contacts, payment) is not written to logs, analytics events, or crash reports.

## Input Handling & Injection

- User input is not concatenated into shell commands, SQL strings, predicates, or `NSPredicate(format:)` without parameterization.
- File paths derived from user input are validated to stay within the expected directory (no path-traversal).
- Deep links / Universal Links / custom URL schemes validate parameters before acting on them.
- Pasteboard reads are intentional and follow the iOS 16+ `UIPasteControl` / explicit-permission pattern.

## Cryptography & Randomness

- New cryptographic code uses `CryptoKit` (or established libraries), not hand-rolled algorithms.
- Random values for security purposes use `SystemRandomNumberGenerator` / `SecRandomCopyBytes`, not `arc4random` for keys / nonces / IDs.
- Hashing for passwords or secrets uses a slow, salted KDF (e.g., `HKDF`, `PBKDF2`, `Argon2` via a library) — never raw SHA / MD5.

## Red Flags To Always Surface

- Any literal that looks like a secret (long base64, JWT, hex of plausible key length).
- New unencrypted persistence of tokens or PII.
- New `print` / `NSLog` / analytics event logging a value that includes auth, health, location, or payment data.
- ATS opened up globally or for a top-level domain.
- Disabling certificate validation (`URLSession` delegate trusting all challenges).
- New required-reason API usage without a corresponding privacy-manifest update.
