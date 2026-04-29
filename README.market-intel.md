# Market Intel browser viewer

This Quartz site publishes the Obsidian vault folder `market-intel/` as a browser-friendly knowledge graph.

## Paths

- Source vault: `${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}/market-intel`
- Quartz site: `~/market-intel-site`

## Commands

- Sync notes into Quartz content:
  - `./scripts/sync-market-intel.sh`
- Commit/push only the `market-intel/` subtree in the vault repo:
  - `./scripts/git-sync-market-intel.sh`
- Auto-sync + auto-push loop:
  - `./scripts/auto-sync-market-intel.sh`
- Start local preview server:
  - `PORT=8081 ./scripts/serve-market-intel.sh`
- Start the Hermes inbox helper (stage-3: dedicated Discord thread per request):
  - `python3 scripts/hermes_inbox_server.py`
  - Defaults:
    - helper listens on `0.0.0.0:8765` so the same Quartz page can submit from localhost, Tailscale, or another device on the private network
    - preview origins are accepted on port `8081` for localhost / `.local` hostnames / private IPs (including Tailscale)
  - Optional hardening / overrides:
    - local-only helper: `HERMES_INBOX_BIND=127.0.0.1 python3 scripts/hermes_inbox_server.py`
    - custom preview port: `HERMES_PREVIEW_PORT=8081 python3 scripts/hermes_inbox_server.py`
    - explicit extra origins: `HERMES_INBOX_ALLOWED_ORIGINS=http://example-host:8081 python3 scripts/hermes_inbox_server.py`
  - For each Quartz "Hermes 토론 요청" submission the helper:
    1. Posts a starter message in the configured Discord parent channel,
    2. Creates a brand new public thread off that starter,
    3. Posts a kickoff message inside the new thread with full page context + the user's request,
    4. Generates and posts the first Hermes reply automatically in that new thread,
    5. Writes an auditable markdown record (including `discord_thread_id` / `discord_thread_url` and auto-kickoff status) into `content/market-intel/hermes-inbox/`.
  - Reads `DISCORD_BOT_TOKEN` from `~/.hermes/.env` (override via env). Parent channel is configurable via `HERMES_DISCORD_PARENT_CHANNEL` (default `1493792291150762115`). Auto-kickoff is on by default and can be disabled with `HERMES_AUTO_KICKOFF=0`. No cron, no automatic note finalization.
- Build static site only:
  - `./scripts/sync-market-intel.sh && npx quartz build -d content`

## Access

- Local browser: `http://localhost:8081`
- If Tailscale is active: `http://<tailscale-ip>:8081`

## Notes

- `templates/` is excluded from the published site.
- The Obsidian vault remains the source of truth.
- Re-run sync before building if the notes changed.
- `git-sync-market-intel.sh` stages only `market-intel/`, so unrelated vault files are not auto-committed.
- macOS LaunchAgent startup serves the last synced `content/` snapshot with `SYNC_ON_START=0`; this avoids `Operation not permitted` failures against `~/Documents/Obsidian Vault` during background boot/login startup.
- If you want fresh vault content, run `./scripts/sync-market-intel.sh` manually from an interactive shell before or after starting the preview server.
- The `com.gbserver.market-intel-sync` LaunchAgent is not reliable without granting background access to the protected Obsidian Vault path; treat sync as an interactive/manual step unless that permission model is redesigned.
