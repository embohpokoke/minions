# ACTIVE TASKS
*Last updated: 2026-03-10 12:00 WIB*


## 11) IVR 188 Smart IVR Presentation — DELIVERED ✅
**Status:** DONE (2026-03-10 05:28)
- 7-page interactive HTML + mobile version
- Files: `~/clawd/tmp/ivr-presentation/` (index, research, audit, existing, system, calculation, visual-ivr, mobile)
- ZIP delivered to Erik via WA: `IVR_Presentation_Mobile.zip` (44KB)
- Content: Vendor comparison, UX audit (21 gaps), ROI calculation, 4-phase roadmap
- **Impact:** Q1 2026 deliverable shipped


## 12) Minions Command Center — INTEGRATED ✅
**Status:** DONE (2026-03-10 07:55)
- Dashboard: https://minions.embohpokoke.my.id
- Asmuni heartbeat working
- 4 KB entries published (Infrastructure, Roadmaps, Agent Responsibilities, Web Sync Workflow)
- Guide: `~/clawd/MINIONS-AGENT-GUIDE.md`


## 13) Meta Graph API + PropTech — IN PROGRESS
**Status:** ⚠️ Planning/Setup
- Meta App "sijibintaro" created (Development mode)
- Page ID: `101236895343925`, IG ID: `17841444713756531`
- Media folder: `/var/www/sijibintaro/media/d43d7115499b56a139094ba5/`
- PropTech pricing model defined (Rp 75K/listing or Rp 500K/mo)
- **Status update:** n8n removed (no longer used). Need alternative for automation.
- **Next:** Determine automation path (Python script vs other).


## 9) Content Generation Automation — PLANNING ✅
**Status:** Plan approved, belum build
- SIJI: Caption IG (3 format rotasi) + WA Broadcast → via GOWA SIJI
- Livinin: Deskripsi listing + Caption IG + WA follow-up template → via GOWA Livinin
- WA Delivery: **GOWA only** (Fonnte deprecated/unsubscribe)
- GOWA Send API: `POST http://localhost:3002/send/message`
- Timeline: Week 1 = SIJI, Week 2 = Livinin, Week 3 = QA + prove
- **Blocker sekarang:** Fix port 8000 conflict (PM2 vs Docker Livinin) dulu
- **Next step:** Build SIJI content cron (trigger tiap Minggu malam, generate 3 konten MWF)


## 10) Port 8000 Conflict — RESOLVED ✅
**Status:** DONE (2026-03-12 11:51)
- Standalone uvicorn running correctly on port 8000.
- PM2 conflict gone (no livininbintaro-api in PM2 list).


## 3) HR Pipeline Dashboard — LIVE ✅
**Status:** LIVE at `https://sijibintaro.id/dashboard/hr/` (deployed Feb 26)
- Verified with curl: HTTP 200 OK
- Ocha notified (mentally noted for handover)


## 8) sync_listings.py — FIXED ✅
**Status:** DONE (2026-03-12 11:53)
- Fixed potential UnboundLocalError by robustly initializing batch variables.
- Verified with live sync on Sheet 2 (29 rows).


## 4) Druygon Phase 3.1 — Pokemon Images
**Status:** ✅ DONE (2026-03-03)
- 18 Pokemon sprites downloaded from pokemondb.net
- All images converted to WebP, max 120×120px, max 8KB/file
- Total image folder: 532KB (turun 94% dari sebelumnya)
- Nav icons, game cards, player avatars, battle sprites — semua diganti Pokemon sprites
- Cache-buster updated ke v=20260303 di semua halaman
- Confirmed by Erik: done ✅


## 5) SIJI Daily Digest
**Status:** Active cron (20:00 WIB / 13:00 UTC)
- Script: `/root/sijibintaro-api/siji_daily_digest.py`
- Log: `/var/log/siji_digest.log`
- Telegram bot: `8510158455:AAHT5gd5xKtrCtzl3kAXuMVUsyCYTAyacjc` → chat_id `5309429603`
- Per-message Telegram notif: DISABLED (was too spammy)


## 6) Infrastructure Notes (Feb 25 state)
- VPS context: `/root/CONTEXT.md` (302 lines) + local mirror `memory/vps-context.md`
- Deploy workflow: edit local → `deploy-api.sh` → VPS (NOT direct VPS edits)
- Docker Desktop Mac mini: UNINSTALLED ✅ (2026-02-25, freed 1.9GB RAM)
- VPS ports: 3000=ackee, 3001=node/siji-frontend, 3002=gowa-siji, 3003=gowa-livinin, 5678=n8n, 8000=livinin-api, 8002=siji-api
---
*Resolved/Closed:*
- ~~VPS Hostinger Audit Fixes~~ → CLOSED (2026-02-27) — druygon API moved, SSL per-domain, google_credentials secured, nginx http2 fixed, docs consolidated, cleanup done. Report: memory/VPS_FIX_REPORT.md
- ~~sijibintaro.id redirect/karir incident~~ → CLOSED (nginx fixed, site stable)
- ~~livininbintaro debug~~ → DEPRIORITIZED (monitoring shows stable, no active incident)
- ~~OS cron cleanup~~ → CLOSED
- ~~SIJI cron path fix~~ → CLOSED (cron disabled, not needed)
- ~~DOC CLEANUP~~ → DONE (2026-02-23, archive/2026-02/)
- ~~Fonnte Webhook~~ → FIXED (2026-02-24, wa_webhook.py JSON parsing fix)
- ~~AUTOREPLY~~ → optional, ~2 Mar 2026 (AUTOREPLY_ENABLED = False for now)
