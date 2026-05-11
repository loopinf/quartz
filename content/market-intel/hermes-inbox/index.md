---
title: Hermes inbox
description: Local queue for stage-2 discussion requests submitted from market-intel pages.
---

# Hermes inbox

Local queue for **stage-2** Hermes discussion requests submitted from the
Quartz site.

## Flow

1. On entity/stock pages the `HermesTrigger` card shows a "Hermes 토론 요청" form.
2. Submitting POSTs to the local helper `scripts/hermes_inbox_server.py` (port 8765).
3. The helper writes one markdown file per request into this folder.

## File schema

Each request file has this frontmatter:

- `request_id` — timestamp + short uuid suffix; matches the filename
- `created_at` — ISO-8601 UTC
- `source_page_title` / `source_page_path` / `source_page_url`
- `entity_type` / `entity_name` (from page frontmatter, may be empty)
- `request_status` — defaults to `queued`
- `request_text` — the user-typed body

A future Hermes consumer is expected to watch this directory, pick up
`request_status: queued` files, and flip the status when handled. Stage-2
deliberately stops at the queue.

## Local run

```sh
# Terminal 1: Quartz preview
./scripts/serve-market-intel.sh

# Terminal 2: inbox helper
python3 scripts/hermes_inbox_server.py
```

## LaunchAgent auto-restart

For macOS login-time auto-recovery, install the repo-managed LaunchAgent:

```sh
./scripts/install-hermes-inbox-launchagent.sh
```

Managed files:
- template: `launchd/com.gbserver.market-intel-hermes-inbox.plist`
- wrapper: `scripts/run-hermes-inbox-helper.sh`
- installed plist: `~/Library/LaunchAgents/com.gbserver.market-intel-hermes-inbox.plist`

`scripts/sync-market-intel.sh` excludes this folder from its rsync `--delete`,
so queued requests survive sync.
