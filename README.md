# Minions — minions.embohpokoke.my.id

## Status: Replaced by Paperclip (2026-04-05)

The custom Minions Command Center (FastAPI + SQLite) has been **retired** and replaced by [Paperclip](https://github.com/hostinger/hvps-paperclip), a managed automation platform running as a Docker container.

### What changed

| Before | After |
|--------|-------|
| FastAPI + SQLite (`api/main.py`) | Paperclip Docker container |
| systemd: `minions-api` on port 8010 | Docker: `paperclip-esrd-paperclip-1` on port 3100 |
| Custom dashboard (`dashboard/index.html`) | Paperclip built-in UI |
| Agent inbox poll/ack pattern (cron → curl) | Paperclip native workflows |
| `/root/embohpokoke.my.id/minions/` | `/docker/paperclip-esrd/` |

### Domain

`https://minions.embohpokoke.my.id` — same domain, now serves Paperclip.

### Paperclip details

- **Docker Compose:** `/docker/paperclip-esrd/docker-compose.yml`
- **Config:** `/docker/paperclip-esrd/data/instances/default/config.json`
- **Admin:** Erik (embohpokoke@gmail.com)
- **DB:** Embedded PostgreSQL (auto-backup hourly, 30-day retention)
- **LLM:** Anthropic API (Claude) integrated

### Removed during migration

1. `minions-api.service` — stopped, disabled, deleted
2. 4 heartbeat cron entries in root crontab
3. OpenClaw cron jobs: Kartolo, Dono, Livvy inbox polls
4. Port 8010 freed

---

## Archive: Original Structure

This repo contains the **old** Minions system (no longer running):

- `api/` — FastAPI Knowledge Service (port 8010)
- `dashboard/` — Mission Control frontend
- `data/` — Shared data/config
- `scripts/` — Utility scripts
- `docs/` — Documentation
