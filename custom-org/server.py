#!/usr/bin/env python3
"""
Custom AI Organization — Web Dashboard Server
기존 CLI(bin/org)를 REST API로 래핑하고, 단일 HTML 대시보드를 서빙합니다.

Usage: python3 server.py [--port 8080]
"""

import http.server
import json
import os
import re
import glob
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ORG_DIR = os.environ.get("ORG_COMPANY_DIR", os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(ORG_DIR, "state")
AGENTS_DIR = os.path.join(ORG_DIR, "agents")
PORT = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8080


# ── YAML-lite parser (no dependencies) ──────────────────────────────────────

def parse_yaml_simple(text):
    """Minimal YAML parser for our flat/shallow files."""
    result = {}
    current_key = None
    list_key = None

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        # Handle list items
        if stripped.startswith("- "):
            item_val = stripped[2:].strip()
            if list_key:
                if list_key not in result:
                    result[list_key] = []
                if not isinstance(result[list_key], list):
                    result[list_key] = []
                # Check if it's a dict-style list item (e.g. "- author: foo")
                if ":" in item_val and list_key == "comments":
                    k, v = item_val.split(":", 1)
                    result[list_key].append({k.strip(): v.strip().strip('"')})
                else:
                    result[list_key].append(item_val)
            continue

        if ":" not in stripped:
            continue

        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip().strip('"')

        # Empty value = dict or list header
        if val == "" or val == "|":
            if indent == 0:
                current_key = key
                list_key = key  # might be a list, decided when we see "- "
                result[key] = {}
            continue

        # Scalar value
        if val == "null":
            val = None
        elif val == "true":
            val = True
        elif val == "false":
            val = False
        else:
            try:
                val = int(val)
            except (ValueError, TypeError):
                pass

        if indent == 0:
            result[key] = val
            current_key = key
            list_key = None
        elif indent > 0 and current_key:
            if isinstance(result.get(current_key), dict):
                result[current_key][key] = val
            elif isinstance(result.get(current_key), list):
                # dict item continuation (e.g. comments list)
                if result[current_key] and isinstance(result[current_key][-1], dict):
                    result[current_key][-1][key] = val

    return result


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file."""
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except FileNotFoundError:
        return {}

    if not content.startswith("---"):
        return {}

    end = content.find("---", 3)
    if end == -1:
        return {}

    return parse_yaml_simple(content[3:end])


# ── Data layer ──────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_activity(actor, action, entity, details=None):
    entry = {"ts": now_iso(), "actor": actor, "action": action, "entity": entity, "details": details or {}}
    with open(os.path.join(STATE_DIR, "activity.jsonl"), "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def get_agents():
    agents = []
    for agent_dir in sorted(glob.glob(os.path.join(AGENTS_DIR, "*"))):
        if not os.path.isdir(agent_dir):
            continue
        slug = os.path.basename(agent_dir)
        agents_file = os.path.join(agent_dir, "AGENTS.md")
        state_file = os.path.join(STATE_DIR, "agents", f"{slug}.yaml")

        meta = parse_frontmatter(agents_file)
        state = {}
        if os.path.exists(state_file):
            with open(state_file) as f:
                state = parse_yaml_simple(f.read())

        agents.append({
            "slug": slug,
            "name": meta.get("name", slug),
            "title": meta.get("title", ""),
            "role": meta.get("slug", slug),
            "reportsTo": meta.get("reportsTo"),
            "skills": meta.get("skills", []),
            "status": state.get("status", "unknown"),
            "lastHeartbeatAt": state.get("lastHeartbeatAt"),
            "spentMonthlyCents": state.get("spentMonthlyCents", 0),
        })
    return agents


def get_tasks():
    tasks = []
    tasks_dir = os.path.join(STATE_DIR, "tasks")
    if not os.path.isdir(tasks_dir):
        return tasks
    for tf in sorted(glob.glob(os.path.join(tasks_dir, "*.yaml"))):
        with open(tf) as f:
            task = parse_yaml_simple(f.read())
        tasks.append(task)
    return tasks


def get_budgets():
    bfile = os.path.join(STATE_DIR, "budgets.yaml")
    if not os.path.exists(bfile):
        return {}
    with open(bfile) as f:
        return parse_yaml_simple(f.read())


def get_approvals():
    approvals = []
    adir = os.path.join(STATE_DIR, "approvals")
    if not os.path.isdir(adir):
        return approvals
    for af in sorted(glob.glob(os.path.join(adir, "*.yaml"))):
        with open(af) as f:
            approvals.append(parse_yaml_simple(f.read()))
    return approvals


def get_activity(limit=20):
    afile = os.path.join(STATE_DIR, "activity.jsonl")
    if not os.path.exists(afile):
        return []
    with open(afile) as f:
        lines = f.readlines()
    entries = []
    for line in lines[-limit:]:
        try:
            entries.append(json.loads(line.strip()))
        except json.JSONDecodeError:
            pass
    entries.reverse()
    return entries


def create_task(data):
    counter_file = os.path.join(STATE_DIR, "counter.yaml")
    with open(counter_file) as f:
        counter = parse_yaml_simple(f.read())
    prefix = counter.get("prefix", "ORG")
    next_num = counter.get("next", 1)
    task_id = f"{prefix}-{next_num:03d}"

    ts = now_iso()
    task = {
        "id": task_id,
        "title": data.get("title", "Untitled"),
        "description": data.get("description", ""),
        "status": "todo",
        "priority": data.get("priority", "medium"),
        "assignee": data.get("assignee"),
        "createdBy": data.get("createdBy", "board"),
        "parentId": data.get("parentId"),
        "goalSlug": data.get("goalSlug"),
        "projectSlug": data.get("projectSlug"),
        "checkoutBy": None,
        "checkoutAt": None,
        "createdAt": ts,
        "updatedAt": ts,
        "completedAt": None,
        "comments": [],
    }

    # Write task file
    task_file = os.path.join(STATE_DIR, "tasks", f"{task_id}.yaml")
    write_task_yaml(task_file, task)

    # Update counter
    with open(counter_file, "w") as f:
        f.write(f"prefix: {prefix}\nnext: {next_num + 1}\n")

    log_activity(task["createdBy"], "task.create", task_id,
                 {"assignee": task["assignee"], "priority": task["priority"]})
    return task


def write_task_yaml(filepath, task):
    def fmt(v):
        if v is None:
            return "null"
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, str) and (" " in v or '"' in v or ":" in v or v == ""):
            return f'"{v}"'
        return str(v)

    lines = []
    for key in ["id", "title", "description", "status", "priority", "assignee",
                 "createdBy", "parentId", "goalSlug", "projectSlug",
                 "checkoutBy", "checkoutAt", "createdAt", "updatedAt", "completedAt"]:
        lines.append(f"{key}: {fmt(task.get(key))}")

    lines.append("comments:")
    for c in task.get("comments", []):
        lines.append(f"  - author: {c.get('author', 'unknown')}")
        lines.append(f"    body: {fmt(c.get('body', ''))}")
        lines.append(f"    at: {fmt(c.get('at', ''))}")

    with open(filepath, "w") as f:
        f.write("\n".join(lines) + "\n")


def update_task(task_id, data):
    task_file = os.path.join(STATE_DIR, "tasks", f"{task_id}.yaml")
    if not os.path.exists(task_file):
        return None

    with open(task_file) as f:
        task = parse_yaml_simple(f.read())

    old_status = task.get("status")
    ts = now_iso()

    for key in ["status", "priority", "assignee", "description"]:
        if key in data and data[key] is not None:
            task[key] = data[key]

    task["updatedAt"] = ts

    if data.get("status") == "done":
        task["completedAt"] = ts
    if data.get("status") == "in_progress" and data.get("assignee"):
        task["checkoutBy"] = data["assignee"]
        task["checkoutAt"] = ts

    if data.get("comment"):
        if "comments" not in task or not isinstance(task["comments"], list):
            task["comments"] = []
        task["comments"].append({
            "author": data.get("actor", "board"),
            "body": data["comment"],
            "at": ts,
        })

    write_task_yaml(task_file, task)

    if old_status != task.get("status"):
        log_activity(data.get("actor", "board"), "task.update", task_id,
                     {"previousStatus": old_status, "newStatus": task["status"]})

    return task


def update_agent_status(slug, status, reason="manual"):
    state_file = os.path.join(STATE_DIR, "agents", f"{slug}.yaml")
    if not os.path.exists(state_file):
        return False
    with open(state_file) as f:
        content = f.read()
    content = re.sub(r"^status: .*", f"status: {status}", content, flags=re.MULTILINE)
    with open(state_file, "w") as f:
        f.write(content)
    action = "agent.pause" if status == "paused" else "agent.resume"
    log_activity("board", action, slug, {"reason": reason})
    return True


def create_agent(data):
    slug = data.get("slug", "").strip().lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    if not slug:
        return {"error": "Slug is required"}
    agent_dir = os.path.join(AGENTS_DIR, slug)
    if os.path.exists(agent_dir):
        return {"error": f"Agent '{slug}' already exists"}

    os.makedirs(agent_dir, exist_ok=True)

    # Create AGENTS.md
    skills_list = "\n".join(f"  - {s}" for s in data.get("skills", ["org-heartbeat"]))
    agents_md = f"""---
schema: agentcompanies/v1
kind: agent
slug: {slug}
name: {data.get('name', slug)}
title: {data.get('title', '')}
reportsTo: {data.get('reportsTo', 'ceo')}
skills:
{skills_list}
budget:
  monthlyCents: {data.get('budgetMonthlyCents', 20000)}
---

# {data.get('name', slug)} Instructions

{data.get('instructions', f'당신은 {data.get("title", slug)}입니다.')}
"""
    with open(os.path.join(agent_dir, "AGENTS.md"), "w") as f:
        f.write(agents_md)

    # Create state file
    ts = now_iso()
    state_file = os.path.join(STATE_DIR, "agents", f"{slug}.yaml")
    with open(state_file, "w") as f:
        f.write(f'slug: {slug}\nstatus: active\nlastHeartbeatAt: null\nspentMonthlyCents: 0\ninitializedAt: "{ts}"\n')

    # Add to budgets
    budgets_file = os.path.join(STATE_DIR, "budgets.yaml")
    if os.path.exists(budgets_file):
        with open(budgets_file, "a") as f:
            f.write(f"  {slug}:\n    monthlyCents: {data.get('budgetMonthlyCents', 20000)}\n    spentMonthlyCents: 0\n")

    log_activity("board", "agent.create", slug, {"name": data.get("name"), "title": data.get("title")})
    return {"slug": slug, "name": data.get("name"), "status": "active"}


# ── HTTP Server ─────────────────────────────────────────────────────────────

class OrgHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/dashboard":
            self.serve_file(os.path.join(ORG_DIR, "dashboard.html"), "text/html")
        elif path == "/api/dashboard":
            self.json_response({
                "agents": get_agents(),
                "tasks": get_tasks(),
                "budgets": get_budgets(),
                "approvals": get_approvals(),
                "activity": get_activity(20),
            })
        elif path == "/api/agents":
            self.json_response(get_agents())
        elif path == "/api/tasks":
            self.json_response(get_tasks())
        elif path == "/api/budgets":
            self.json_response(get_budgets())
        elif path == "/api/approvals":
            self.json_response(get_approvals())
        elif path == "/api/activity":
            self.json_response(get_activity(50))
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {}

        path = urllib.parse.urlparse(self.path).path

        if path == "/api/tasks":
            task = create_task(data)
            self.json_response(task, 201)

        elif path.startswith("/api/tasks/") and path.count("/") == 3:
            task_id = path.split("/")[3]
            task = update_task(task_id, data)
            if task:
                self.json_response(task)
            else:
                self.send_error(404, "Task not found")

        elif path == "/api/agents":
            result = create_agent(data)
            if result and "error" not in result:
                self.json_response(result, 201)
            else:
                err = result.get("error", "Agent creation failed") if result else "Agent creation failed"
                self.json_response({"error": err}, 400)

        elif path.startswith("/api/agents/") and "/pause" in path:
            slug = path.split("/")[3]
            if update_agent_status(slug, "paused"):
                self.json_response({"status": "paused"})
            else:
                self.send_error(404)

        elif path.startswith("/api/agents/") and "/resume" in path:
            slug = path.split("/")[3]
            if update_agent_status(slug, "active"):
                self.json_response({"status": "active"})
            else:
                self.send_error(404)

        else:
            self.send_error(404)

    def json_response(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, filepath, content_type):
        try:
            with open(filepath, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {args[0]}" if args else "")


if __name__ == "__main__":
    os.makedirs(os.path.join(STATE_DIR, "tasks"), exist_ok=True)
    os.makedirs(os.path.join(STATE_DIR, "agents"), exist_ok=True)
    os.makedirs(os.path.join(STATE_DIR, "approvals"), exist_ok=True)

    server = http.server.HTTPServer(("0.0.0.0", PORT), OrgHandler)
    print(f"""
╔══════════════════════════════════════════════════╗
║   Custom AI Organization — Dashboard Server      ║
║   http://localhost:{PORT}                          ║
╚══════════════════════════════════════════════════╝
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
