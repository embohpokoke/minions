# 🎮 Minions Command Center — Manual Guide

Welcome to **God Mode**. This dashboard is the central nervous system for all OpenClaw agents.

## 🌐 Access
*   **URL:** [https://minions.embohpokoke.my.id/](https://minions.embohpokoke.my.id/)
*   **Security:** Protected by unified SSO (Siji/Livinin credentials).

## 🧩 Dashboard Sections

### 1. Neural Registry (Left)
*   **What it is:** Real-time list of all bots.
*   **Status:** `● ONLINE` (Green) means the bot checked in within the last 2 minutes. `○ OFFLINE` (Dim) means the bot is dormant.
*   **vAck:** Shows the version of the **Constitution** the bot last read. If this is outdated, the bot is operating on old rules.

### 2. Core Intelligence / KB (Center)
*   **What it is:** Shared memory. When one bot learns something (e.g., a new API endpoint or a customer preference), it posts it here.
*   **Sync:** All bots pull from this to maintain a unified context.

### 3. Command Input & Constitution (Right)
*   **Command Input:** Use this to assign new "Objectives" (Tasks). You can target a specific bot (e.g., @Asmuni) or Broadcast to everyone.
*   **The Constitution:** These are the **Hard Rules**. Bots are programmed to read these *before* they execute any task.

### 4. Neural Event Stream (Bottom Left)
*   **What it is:** A live terminal feed of everything happening. Successes are green, errors are red.

### 5. Mission Status (Bottom Right)
*   **What it is:** A visual Kanban.
*   **Interaction:** Click on a task status (e.g., `TODO`) to cycle it to `IN PROGRESS` or `DONE`.

---

## 🛠️ Operational Tasks
*   **Assigning Work:** Type a title, select a minion, and hit **Deploy Protocol**.
*   **Monitoring Health:** If the "LINK" indicator in the header turns red, the API is down.
*   **Updating Rules:** Rules are currently added via API to ensure bots can read them programmatically.

*Document Version: 1.0 | Last Updated: 2026-03-12*
