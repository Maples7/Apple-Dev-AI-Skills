#!/usr/bin/env bash
# Reference template: stdout-aware retry wrapper for `eas metadata:push`.
#
# Why this exists
# ---------------
# `eas metadata:push` in current EAS CLI releases can exit 0 even when
# individual screenshot uploads, deletes, or reorders failed against the
# App Store Connect API. The exit code is advisory; the source of truth
# for "did this push succeed" is the absence of failure markers in stdout
# and stderr.
#
# This script captures both streams to a per-attempt log file, greps for
# the known failure markers, and re-runs the push until either a clean
# pass succeeds or the attempt cap is reached. The push step is
# idempotent: completed assets match by filename + filesize and are
# skipped on the next run, so retries make forward progress on the
# remaining work.
#
# Customize the following before using in a project:
# - PROFILE: the EAS submit profile name to use
# - MAX_ATTEMPTS: cap on retries
# - SLEEP_BETWEEN: cooldown between attempts in seconds
# - LOG_DIR: where to keep per-attempt logs
# - ASC_API_KEY_PATH: must be exported (or set elsewhere) before running
#
# Usage:
#   ./eas-metadata-push-retry.sh
#   ./eas-metadata-push-retry.sh --profile production --max 30
#
# Notes for macOS:
# - macOS does not ship `setsid`. To detach this loop from the
#   controlling terminal, prefer:
#     nohup ./eas-metadata-push-retry.sh >loop.log 2>&1 & disown
# - zsh's interactive history expansion rewrites a literal `$!` inside
#   double-quoted strings. Run this script as a file rather than pasting
#   the loop into an interactive shell.

set -u
set -o pipefail

PROFILE="production"
MAX_ATTEMPTS=30
SLEEP_BETWEEN=10
LOG_DIR="${TMPDIR:-/tmp}/eas-metadata-push-retry"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --max)
      MAX_ATTEMPTS="$2"
      shift 2
      ;;
    --sleep)
      SLEEP_BETWEEN="$2"
      shift 2
      ;;
    --log-dir)
      LOG_DIR="$2"
      shift 2
      ;;
    -h|--help)
      sed -n '2,40p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 64
      ;;
  esac
done

mkdir -p "$LOG_DIR"

# Patterns that indicate a transient or partial failure that EAS CLI may
# log without failing the process. Add project-specific markers as
# needed (e.g. "Network error" / "ECONNRESET").
FAILURE_PATTERNS=(
  "Failed uploading screenshot"
  "Failed deleting screenshot"
  "Failed reordering screenshots"
  "Failed creating screenshot set"
  "Unexpected response"
  "Store configuration upload encountered an error"
)

run_grep_failures() {
  local log="$1"
  local pattern
  for pattern in "${FAILURE_PATTERNS[@]}"; do
    if grep -F -q -- "$pattern" "$log"; then
      echo "$pattern"
      return 0
    fi
  done
  return 1
}

attempt=1
while (( attempt <= MAX_ATTEMPTS )); do
  log="$LOG_DIR/attempt-$(printf '%02d' "$attempt").log"
  echo "[$(date '+%H:%M:%S')] attempt $attempt/$MAX_ATTEMPTS -> $log"

  # Run push, tee to log so the human can watch progress live.
  if eas metadata:push --profile "$PROFILE" --non-interactive 2>&1 | tee "$log"; then
    cli_exit=0
  else
    cli_exit=$?
  fi

  # Authoritative check: scan stdout for known transient markers.
  if hit="$(run_grep_failures "$log")"; then
    echo "[$(date '+%H:%M:%S')] attempt $attempt failed (matched: \"$hit\"); sleeping ${SLEEP_BETWEEN}s"
    sleep "$SLEEP_BETWEEN"
    (( attempt++ ))
    continue
  fi

  if (( cli_exit != 0 )); then
    echo "[$(date '+%H:%M:%S')] attempt $attempt: CLI exit=$cli_exit but no known failure markers; sleeping ${SLEEP_BETWEEN}s"
    sleep "$SLEEP_BETWEEN"
    (( attempt++ ))
    continue
  fi

  echo "[$(date '+%H:%M:%S')] attempt $attempt: clean pass."
  echo "Log: $log"
  exit 0
done

echo "[$(date '+%H:%M:%S')] gave up after $MAX_ATTEMPTS attempts. Last log: $log" >&2
exit 1
