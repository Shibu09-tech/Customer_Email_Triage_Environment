"""
inference.py — Customer Email Triage OpenEnv
============================================================
Mandatory inference script for the OpenEnv hackathon submission.

Environment variables:
  API_BASE_URL   LLM API endpoint (default: HuggingFace router)
  MODEL_NAME     Model identifier (default: Qwen/Qwen2.5-72B-Instruct)
  HF_TOKEN       HuggingFace API key (also accepts API_KEY)

Stdout format (strictly followed):
  [START] task=<task_name> env=customer-email-triage model=<model>
  [STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
  [END]   success=<true|false> steps=<n> score=<0.000> rewards=<r1,r2,...>
"""
import os
import json
import textwrap
import requests
from typing import List, Optional

from openai import OpenAI

# ── Configuration ─────────────────────────────────────────────────────────────
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:8000")

MAX_STEPS = 15          # max per task episode
TEMPERATURE = 0.3       # lower = more deterministic
MAX_TOKENS = 512
SUCCESS_SCORE_THRESHOLD = 0.5   # normalized score to count as "success"

TASKS = ["priority-triage", "full-routing", "full-pipeline"]

PRIORITY_VALUES = ["urgent", "high", "medium", "low", "spam"]
CATEGORY_VALUES = ["billing", "technical", "refunds", "general", "account", "compliance", "spam"]

# ── Logging helpers ───────────────────────────────────────────────────────────

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# ── Environment helpers ───────────────────────────────────────────────────────

def env_reset(task: str) -> dict:
    resp = requests.post(
        f"{ENV_BASE_URL}/reset",
        json={"task": task},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def env_step(action: dict) -> dict:
    resp = requests.post(
        f"{ENV_BASE_URL}/step",
        json=action,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


# ── LLM helpers ───────────────────────────────────────────────────────────────

SYSTEM_PROMPT = textwrap.dedent("""
You are an expert customer support triage agent. For each email you receive,
you must classify it and decide how to handle it.

You MUST respond with a valid JSON object with exactly these fields:
{
  "priority": "<one of: urgent, high, medium, low, spam>",
  "category": "<one of: billing, technical, refunds, general, account, compliance, spam>",
  "reply_draft": "<a professional reply to send to the customer>"
}

Priority guidelines:
- urgent: production down, security breach, immediate financial loss
- high: significant disruption, enterprise customer, time-sensitive billing
- medium: non-urgent billing, account changes, feature requests from paying customers
- low: general questions, feature suggestions, free-tier users
- spam: promotional, phishing, irrelevant

Category guidelines:
- billing: payments, invoices, subscriptions, pricing
- technical: bugs, API issues, integrations, errors
- refunds: refund or cancellation requests
- general: general inquiries, feature requests, praise
- account: login, password, ownership transfer, permissions
- compliance: GDPR, legal, audits, SOC 2
- spam: spam or phishing emails

For spam emails, set priority=spam, category=spam, and reply_draft="" (empty string).
Respond with ONLY the JSON object, no markdown, no explanation.
""").strip()


def get_triage_decision(
    client: OpenAI,
    obs: dict,
    task_name: str,
    history: List[str],
) -> dict:
    """Ask the LLM to triage the current email. Returns parsed action dict."""
    history_block = "\n".join(history[-3:]) if history else "None"
    user_msg = textwrap.dedent(f"""
    Task: {task_name}
    Step: {obs.get('step_number', '?')} of ~{obs.get('emails_remaining', '?') + obs.get('step_number', 1) - 1}
    Cumulative reward so far: {obs.get('episode_reward_so_far', 0.0):.4f}

    === EMAIL ===
    From: {obs['sender']} ({obs['sender_tier']} tier)
    Thread: {obs.get('thread_length', 1)} email(s) | Prior tickets: {obs.get('previous_interactions', 0)}
    Subject: {obs['subject']}

    {obs['body']}
    === END EMAIL ===

    Recent history:
    {history_block}

    Respond with a JSON object: {{"priority": "...", "category": "...", "reply_draft": "..."}}
    """).strip()

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()

        # Strip potential markdown fences
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.lower().startswith("json"):
                text = text[4:]
        text = text.strip()

        action = json.loads(text)

        # Validate / clamp enum values
        if action.get("priority") not in PRIORITY_VALUES:
            action["priority"] = "medium"
        if action.get("category") not in CATEGORY_VALUES:
            action["category"] = "general"
        if not isinstance(action.get("reply_draft"), str):
            action["reply_draft"] = ""

        return action

    except Exception as exc:
        print(f"[DEBUG] LLM parse error: {exc}", flush=True)
        return {"priority": "medium", "category": "general", "reply_draft": ""}


# ── Main episode loop ─────────────────────────────────────────────────────────

def run_task(client: OpenAI, task_name: str) -> None:
    """Run a single task episode and emit [START]/[STEP]/[END] logs."""
    log_start(task=task_name, env="customer-email-triage", model=MODEL_NAME)

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False
    error_msg = None
    history: List[str] = []

    try:
        # ── Reset ──
        reset_result = env_reset(task_name)
        obs = reset_result["observation"]
        total_emails = reset_result.get("total_emails", MAX_STEPS)
        done = False

        for step in range(1, MAX_STEPS + 1):
            if done:
                break

            # Get LLM decision
            action = get_triage_decision(client, obs, task_name, history)
            action_str = f"priority={action['priority']},category={action['category']}"

            # Step in environment
            step_result = env_step(action)
            reward = step_result.get("reward", 0.0)
            done = step_result.get("done", False)
            next_obs = step_result.get("observation")
            err = step_result.get("info", {}).get("error")

            rewards.append(reward)
            steps_taken = step

            log_step(step=step, action=action_str, reward=reward, done=done, error=err)

            # Update history summary
            truth = step_result.get("info", {}).get("ground_truth", {})
            history.append(
                f"Step {step}: priority={action['priority']}(truth={truth.get('priority','?')}) "
                f"category={action['category']}(truth={truth.get('category','?')}) reward={reward:.4f}"
            )

            if done:
                ep_summary = step_result.get("info", {}).get("episode_summary", {})
                success = ep_summary.get("success", False)
                break

            obs = next_obs

        # Compute normalized score
        total_reward = sum(rewards)
        # Max possible reward per step ≈ 1.0 (full score) - 0.02 (penalty) = 0.98
        max_possible = total_emails * 0.98
        score = min(max(total_reward / max_possible if max_possible > 0 else 0.0, 0.0), 1.0)
        if not success:
            success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as exc:
        error_msg = str(exc)
        print(f"[DEBUG] Task {task_name} error: {exc}", flush=True)

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    for task_name in TASKS:
        run_task(client, task_name)
        print("", flush=True)  # blank line between tasks for readability


if __name__ == "__main__":
    main()
