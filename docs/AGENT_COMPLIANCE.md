# 🤖 Agent Compliance Mandate

Every OpenClaw Minion **MUST** comply with the following neural sync protocols to ensure ecosystem integrity.

## 📡 1. Heartbeat Protocol
*   **Action:** Every 15–30 minutes, or at the start of a session.
*   **Endpoint:** `POST /api/agents/heartbeat`
*   **Mandatory Payload:**
    ```json
    {
      "agent_id": "your_id",
      "host": "current_host",
      "status": "online/working/idle",
      "current_task": "What you are doing right now",
      "rule_version_ack": "v1.0"
    }
    ```

## 📜 2. The Constitution (Rules) Sync
*   **Requirement:** Agents **MUST** fetch active rules before performing any write operations to the database or external APIs.
*   **Endpoint:** `GET /api/rules`
*   **Goal:** Ensure the agent is aware of safety constraints, coding standards, and Juragan's latest preferences.

## 🧠 3. Knowledge Base Contribution
*   **Requirement:** If an agent discovers a persistence-worthy fact (e.g., "Meta Graph API limit reached" or "New customer contact added"), it **MUST** post to the KB.
*   **Endpoint:** `POST /api/kb`

## 📝 4. Telemetry Logging
*   **Requirement:** Critical errors or successful major milestones **MUST** be logged to the Neural Stream.
*   **Endpoint:** `POST /api/logs`
*   **Levels:** `info`, `warning`, `error`, `success`.

## 🛑 5. Failure to Comply
Agents found operating without an active heartbeat for >24h or operating on an un-acknowledged rule version (`rule_version_ack` missing) will be marked as **LEGACY/DANGEROUS** in the Command Center.

---
*By Order of Juragan Erik Mahendra*
