# Customer Email Triage — OpenEnv 📧

[![OpenEnv](https://img.shields.io/badge/OpenEnv-1.0.0-blue)](https://openenv.dev)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://python.org)
[![HuggingFace](https://img.shields.io/badge/🤗-Space-yellow)](https://huggingface.co)

An **OpenEnv** environment where AI agents learn to triage customer support emails — a real task performed daily by thousands of support professionals worldwide.

---

## 🎯 Why Email Triage?

Customer support email triage is a high-value, real-world task:
- Companies receive **hundreds to thousands** of emails daily
- Misrouted or delayed urgent emails cause revenue loss and churn
- Current AI approaches are brittle at priority + routing decisions
- Reply quality directly impacts customer satisfaction (CSAT)

This environment faithfully models the full triage pipeline and provides fine-grained reward signals for every decision.

---

## 📊 Observation Space

| Field | Type | Description |
|-------|------|-------------|
| `email_id` | str | Unique email identifier |
| `subject` | str | Email subject line |
| `body` | str | Full email body text |
| `sender` | str | Sender email address |
| `sender_tier` | str | `free` / `pro` / `enterprise` |
| `timestamp` | str | ISO-8601 receipt timestamp |
| `thread_length` | int | Emails in this thread |
| `previous_interactions` | int | Prior tickets from this sender |
| `task_name` | str | Active task name |
| `step_number` | int | Current step number |
| `emails_remaining` | int | Queue depth remaining |
| `episode_reward_so_far` | float | Cumulative episode reward |

---

## 🎮 Action Space

| Field | Type | Values |
|-------|------|--------|
| `priority` | enum | `urgent`, `high`, `medium`, `low`, `spam` |
| `category` | enum | `billing`, `technical`, `refunds`, `general`, `account`, `compliance`, `spam` |
| `reply_draft` | str | Professional reply (max 2000 chars) |

---

## 🏆 Tasks

| Task | Difficulty | Emails | Score Formula | Success |
|------|-----------|--------|---------------|---------|
| `priority-triage` | 🟢 Easy | 10 | `priority_score` | ≥ 0.70 |
| `full-routing` | 🟡 Medium | 12 | `0.5×priority + 0.5×category` | ≥ 0.60 |
| `full-pipeline` | 🔴 Hard | 15 | `0.3×priority + 0.3×category + 0.4×reply` | ≥ 0.50 |

### Grader Details

**Priority grader** (partial credit):
- Exact match → 1.0
- Adjacent priority (e.g. urgent↔high) → 0.5
- Wrong → 0.0

**Category grader**: Exact match → 1.0, Wrong → 0.0

**Reply grader**: Fraction of expected keywords present in the reply (case-insensitive). Any non-empty reply ≥ 0.2.

---

## 🔁 Reward Function

```
step_reward = task_score − 0.02  (efficiency penalty per step)
```

Episode-end bonus: `+0.10` if average step reward ≥ 0.80

The shaped reward provides **dense signal** throughout the episode — not just binary success/failure.

---

## 📦 Setup & Usage

### Local Development

```bash
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 8000
# Open http://localhost:8000/web/ for the interactive dashboard
```

### Docker

```bash
docker build -t email-triage .
docker run -p 8000:7860 email-triage
# Server at http://localhost:8000
```

### API Quickstart

```python
import requests

BASE = "http://localhost:8000"  # or your HF Space URL

# Start episode
obs = requests.post(f"{BASE}/reset", json={"task": "priority-triage"}).json()

# Take a step
result = requests.post(f"{BASE}/step", json={
    "priority": "urgent",
    "category": "technical",
    "reply_draft": ""
}).json()

print(f"Reward: {result['reward']}, Done: {result['done']}")
```

---

## 🤖 Inference Script

```bash
export HF_TOKEN="hf_your_token_here"
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
export ENV_BASE_URL="http://localhost:8000"

python inference.py
```

Expected output format:
```
[START] task=priority-triage env=customer-email-triage model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=priority=urgent,category=technical reward=0.78 done=false error=null
...
[END] success=true steps=10 score=0.724 rewards=0.78,0.48,0.78,...
```

---

## 📈 Baseline Scores

Run with `Qwen/Qwen2.5-72B-Instruct` via HuggingFace router:

| Task | Avg Score | Success |
|------|-----------|---------|
| `priority-triage` | ~0.72 | ✅ |
| `full-routing` | ~0.61 | ✅ |
| `full-pipeline` | ~0.47 | ❌ (hard!) |

---

## 📁 Project Structure

```
├── Dockerfile              # Container build (HF port 7860)
├── openenv.yaml            # OpenEnv spec metadata
├── requirements.txt        # Python dependencies
├── inference.py            # Mandatory inference script (root)
├── README.md
└── server/
    ├── main.py             # FastAPI app
    ├── environment.py      # Core env logic
    ├── models.py           # Pydantic typed models
    ├── graders.py          # Deterministic task graders
    ├── email_dataset.py    # 30+ realistic emails
    ├── tasks.py            # Task definitions
    └── web/                # Interactive dashboard
        ├── index.html
        ├── style.css
        └── app.js
```

---

## 🔗 Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/reset` | POST | Start new episode (body: `{task, seed?}`) |
| `/step` | POST | Submit action (body: `{priority, category, reply_draft}`) |
| `/state` | GET | Full state snapshot |
| `/tasks` | GET | List all tasks |
| `/health` | GET | Health check |
| `/web/` | GET | Interactive dashboard |

---

## License

MIT
