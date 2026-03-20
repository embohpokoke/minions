"""
Minions API v2.3 — OpenClaw Live Command Center
Migrated to PostgreSQL (psycopg2)
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone, UTC
import zoneinfo
WIB = zoneinfo.ZoneInfo("Asia/Jakarta")
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("minions")

app = FastAPI(title="Minions Command Center", version="2.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_URL = "postgresql://livin:L1v1n!B1nt4r0_2026@172.17.0.2:5432/livininbintaro"
DOCS_DIR = "/root/embohpokoke.my.id/minions/docs"

# ── Models ────────────────────────────────────────────────────────────────
class RuleEntry(BaseModel):
    title: str
    content: str
    category: str = "general"
    is_active: bool = True

class LogEntry(BaseModel):
    agent_id: str
    level: str = "info"
    message: str
    context: Optional[dict] = {}

class AgentHeartbeat(BaseModel):
    agent_id: str
    host: str
    status: str = "online"
    current_task: Optional[str] = None
    rule_version_ack: Optional[str] = None
    metadata: Optional[dict] = {}

class TaskEntry(BaseModel):
    agent_id: str
    title: str
    description: Optional[str] = ""
    status: str = "todo"
    priority: str = "medium"
    tags: Optional[List[str]] = []

class KnowledgeEntry(BaseModel):
    agent_id: str
    subject: str
    content: str
    tags: Optional[List[str]] = []
    metadata: Optional[dict] = {}

# ── Database ──────────────────────────────────────────────────────────────
def get_db():
    conn = psycopg2.connect(DB_URL, options='-c search_path=minions')
    return conn

def now_iso():
    return datetime.now(WIB).isoformat()

# ── Endpoints ─────────────────────────────────────────────────────────────
@app.get("/dashboard/stats")
def get_dashboard_stats():
    conn = get_db()
    c = conn.cursor(cursor_factory=RealDictCursor)
    five_mins_ago = (datetime.now(WIB) - timedelta(minutes=5)).isoformat()
    c.execute("SELECT COUNT(*) as cnt FROM agents WHERE last_seen > %s", (five_mins_ago,))
    active_agents = c.fetchone()["cnt"]
    c.execute("SELECT status, COUNT(*) as cnt FROM tasks GROUP BY status")
    task_stats = {r["status"]: r["cnt"] for r in c.fetchall()}
    c.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 50")
    recent_logs = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"active_agents": active_agents, "task_stats": task_stats, "recent_logs": recent_logs}

@app.post("/agents/heartbeat")
def heartbeat(data: AgentHeartbeat):
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO agents (id, host, status, last_seen, current_task, rule_version_ack, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            host = EXCLUDED.host, status = EXCLUDED.status, last_seen = EXCLUDED.last_seen,
            current_task = EXCLUDED.current_task, rule_version_ack = EXCLUDED.rule_version_ack,
            metadata = EXCLUDED.metadata
    ''', (data.agent_id, data.host, data.status, now_iso(),
          data.current_task, data.rule_version_ack, json.dumps(data.metadata)))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/agents")
def list_agents():
    conn = get_db()
    c = conn.cursor(cursor_factory=RealDictCursor)
    c.execute("SELECT * FROM agents ORDER BY display_order ASC NULLS LAST, last_seen DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"agents": rows}

@app.get("/rules")
def get_rules():
    conn = get_db()
    c = conn.cursor(cursor_factory=RealDictCursor)
    c.execute("SELECT * FROM rules WHERE is_active = TRUE ORDER BY id DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"rules": rows}

@app.post("/rules")
def add_rule(rule: RuleEntry):
    conn = get_db()
    c = conn.cursor()
    version = datetime.now(WIB).strftime("%Y%m%d%H%M")
    c.execute('''INSERT INTO rules (title, content, category, version, is_active, updated_at)
                 VALUES (%s, %s, %s, %s, %s, %s)''',
              (rule.title, rule.content, rule.category, version, rule.is_active, now_iso()))
    conn.commit()
    conn.close()
    return {"status": "created"}

@app.get("/kb")
def list_knowledge(limit: int = 50, agent_id: Optional[str] = None):
    conn = get_db()
    c = conn.cursor(cursor_factory=RealDictCursor)
    if agent_id:
        c.execute("SELECT * FROM knowledge WHERE agent_id = %s ORDER BY created_at DESC LIMIT %s", (agent_id, limit))
    else:
        c.execute("SELECT * FROM knowledge ORDER BY created_at DESC LIMIT %s", (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"entries": rows}

@app.get("/kb/search")
def search_knowledge(q: str = "", limit: int = 50):
    conn = get_db()
    c = conn.cursor(cursor_factory=RealDictCursor)
    if q:
        search = f"%{q}%"
        c.execute('''SELECT * FROM knowledge
                     WHERE subject ILIKE %s OR content ILIKE %s OR tags ILIKE %s
                     ORDER BY created_at DESC LIMIT %s''',
                  (search, search, search, limit))
    else:
        c.execute("SELECT * FROM knowledge ORDER BY created_at DESC LIMIT %s", (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"entries": rows, "count": len(rows)}

@app.post("/kb")
def create_knowledge(entry: KnowledgeEntry):
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO knowledge (agent_id, subject, content, tags, metadata, created_at, updated_at)
                 VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id''',
              (entry.agent_id, entry.subject, entry.content,
               json.dumps(entry.tags), json.dumps(entry.metadata), now_iso(), now_iso()))
    new_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return {"status": "created", "id": new_id}

@app.get("/tasks")
def list_tasks():
    conn = get_db()
    c = conn.cursor(cursor_factory=RealDictCursor)
    c.execute("SELECT * FROM tasks ORDER BY updated_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"tasks": rows}

@app.post("/tasks")
def create_task(task: TaskEntry):
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO tasks (agent_id, title, description, status, priority, tags, created_at, updated_at)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
              (task.agent_id, task.title, task.description, task.status,
               task.priority, json.dumps(task.tags), now_iso(), now_iso()))
    conn.commit()
    conn.close()
    return {"status": "created"}

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, status: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = %s, updated_at = %s WHERE id = %s", (status, now_iso(), task_id))
    conn.commit()
    conn.close()
    return {"status": "updated"}

@app.get("/list-docs")
def list_docs():
    files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]
    return {"docs": files}

@app.get("/get-doc/{filename}")
def get_doc(filename: str):
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path) or ".." in filename:
        raise HTTPException(status_code=404, detail="Doc not found")
    with open(path, "r") as f:
        return {"filename": filename, "content": f.read()}

@app.post("/logs")
def push_log(log: LogEntry):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO logs (agent_id, level, message, context, timestamp) VALUES (%s, %s, %s, %s, %s)",
              (log.agent_id, log.level, log.message, json.dumps(log.context), now_iso()))
    conn.commit()
    conn.close()
    return {"status": "ok"}

# ── MESSAGING API (Agent Communication Bus) ────────────────────────────
class MessageEntry(BaseModel):
    from_agent: str
    to_agent: str
    subject: Optional[str] = None
    content: str
    priority: str = "normal"

@app.post("/messages")
def send_message(msg: MessageEntry):
    """Send message from one agent to another"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (from_agent, to_agent, subject, content, priority, created_at, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'pending') RETURNING id
    ''', (msg.from_agent, msg.to_agent, msg.subject, msg.content, msg.priority, now_iso()))
    msg_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    logger.info(f"[MSG] {msg.from_agent} → {msg.to_agent} (priority: {msg.priority})")
    return {"message_id": msg_id, "status": "sent"}

@app.get("/messages/{agent_id}")
def get_messages(agent_id: str, status: str = "pending"):
    """Get messages for specific agent"""
    conn = get_db()
    c = conn.cursor(cursor_factory=RealDictCursor)
    c.execute('''
        SELECT * FROM messages
        WHERE to_agent = %s AND status = %s
        ORDER BY created_at DESC
    ''', (agent_id, status))
    messages = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"agent": agent_id, "messages": messages, "count": len(messages)}

@app.post("/messages/{msg_id}/ack")
def ack_message(msg_id: int):
    """Mark message as read/acknowledged"""
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE messages SET status = 'read', read_at = %s WHERE id = %s", (now_iso(), msg_id))
    conn.commit()
    conn.close()
    return {"message_id": msg_id, "status": "acknowledged"}

@app.get("/messages")
def list_all_messages(limit: int = 100):
    """List all messages (for Erik dashboard)"""
    conn = get_db()
    c = conn.cursor(cursor_factory=RealDictCursor)
    c.execute('SELECT * FROM messages ORDER BY created_at DESC LIMIT %s', (limit,))
    messages = [dict(r) for r in c.fetchall()]
    conn.close()
    return {"messages": messages, "total": len(messages)}
