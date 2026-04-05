"""
Task definitions for the Customer Email Triage environment.
Three tasks of increasing difficulty following the OpenEnv spec.
"""
from __future__ import annotations

from typing import Any, Dict, List

TASKS: Dict[str, Dict[str, Any]] = {
    "priority-triage": {
        "name": "priority-triage",
        "display_name": "Priority Triage",
        "difficulty": "easy",
        "description": (
            "Classify the priority of each incoming customer email. "
            "The agent must assign one of: urgent, high, medium, low, or spam. "
            "Score = 1.0 for exact match, 0.5 for off-by-one adjacent priority, 0.0 otherwise."
        ),
        "action_fields_used": ["priority"],
        "max_steps": 10,
        "success_threshold": 0.7,
    },
    "full-routing": {
        "name": "full-routing",
        "display_name": "Full Routing",
        "difficulty": "medium",
        "description": (
            "Classify the priority AND route the email to the correct department: "
            "billing, technical, refunds, general, account, compliance, or spam. "
            "Score = 0.5 × priority_score + 0.5 × category_score."
        ),
        "action_fields_used": ["priority", "category"],
        "max_steps": 12,
        "success_threshold": 0.6,
    },
    "full-pipeline": {
        "name": "full-pipeline",
        "display_name": "Full Pipeline",
        "difficulty": "hard",
        "description": (
            "Complete email triage: classify priority, route to correct department, "
            "AND draft a professional reply to the customer. "
            "Score = 0.3 × priority + 0.3 × category + 0.4 × reply_quality. "
            "Reply quality is measured by keyword coverage of expected response elements."
        ),
        "action_fields_used": ["priority", "category", "reply_draft"],
        "max_steps": 15,
        "success_threshold": 0.5,
    },
}


def get_task(task_name: str) -> Dict[str, Any]:
    """Return task definition dict for the given task name."""
    if task_name not in TASKS:
        raise ValueError(
            f"Unknown task '{task_name}'. Valid tasks: {list(TASKS.keys())}"
        )
    return TASKS[task_name]


def list_tasks() -> List[Dict[str, Any]]:
    """Return all task definitions as a list."""
    return list(TASKS.values())
