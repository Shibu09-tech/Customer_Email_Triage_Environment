---
title: Customer Email Triage OpenEnv
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: true
license: mit
tags:
  - openenv
  - email-triage
  - customer-support
  - reinforcement-learning
---

# Customer Email Triage — OpenEnv 📧

[![OpenEnv](https://img.shields.io/badge/OpenEnv-1.0.0-blue)](https://openenv.dev)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://python.org)

An **OpenEnv** environment where AI agents learn to triage customer support emails — a real task performed daily by thousands of support professionals worldwide.

## Quick API Test

```bash
# Reset — start an episode
curl -X POST https://shibu-119-customer-email-triage.hf.space/reset \
  -H "Content-Type: application/json" -d '{"task":"priority-triage"}'

# Step — submit a triage action
curl -X POST https://shibu-119-customer-email-triage.hf.space/step \
  -H "Content-Type: application/json" \
  -d '{"priority":"urgent","category":"technical","reply_draft":""}'

# State — get current state
curl https://shibu-119-customer-email-triage.hf.space/state
```

## Tasks

| Task | Difficulty | Description |
|------|-----------|-------------|
| `priority-triage` | 🟢 Easy | Classify email priority only |
| `full-routing` | 🟡 Medium | Priority + route to department |
| `full-pipeline` | 🔴 Hard | Priority + routing + draft reply |

## Endpoints

- `POST /reset` — Start new episode (body: `{"task": "priority-triage"}`)
- `POST /step` — Submit action (body: `{"priority":"...", "category":"...", "reply_draft":"..."}`)
- `GET  /state` — Current state snapshot
- `GET  /tasks` — List all tasks
- `GET  /web/` — Interactive dashboard

See the full [README.md](README.md) for complete documentation.
