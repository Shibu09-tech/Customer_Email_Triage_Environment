"""
Deterministic graders for each task in the Customer Email Triage environment.
All graders return float scores in [0.0, 1.0].
"""
from __future__ import annotations

from typing import Any, Dict, List

from server.models import Priority, Category, TriageAction

# Priority adjacency map for partial credit
PRIORITY_ADJACENCY: Dict[str, List[str]] = {
    "urgent": ["high"],
    "high": ["urgent", "medium"],
    "medium": ["high", "low"],
    "low": ["medium"],
    "spam": [],
}


def grade_priority(action_priority: str, true_priority: str) -> float:
    """
    Score the priority assignment.
    - Exact match: 1.0
    - Adjacent priority (off by one): 0.5
    - Correct identification of spam: 1.0
    - Everything else: 0.0
    """
    if action_priority == true_priority:
        return 1.0
    adjacents = PRIORITY_ADJACENCY.get(true_priority, [])
    if action_priority in adjacents:
        return 0.5
    return 0.0


def grade_category(action_category: str, true_category: str) -> float:
    """
    Score the routing category assignment.
    - Exact match: 1.0
    - Wrong category: 0.0
    Special rule: if true_category is spam and priority is also spam, still 1.0.
    """
    return 1.0 if action_category == true_category else 0.0


def grade_reply(reply_draft: str, expected_keywords: List[str]) -> float:
    """
    Score the quality of the reply draft (for hard task).
    Score = fraction of expected keywords present in the reply (case-insensitive).
    Minimum 0.2 for any non-empty reply (agent gets credit for trying).
    Empty reply when keywords expected = 0.0.
    """
    if not expected_keywords:
        # Spam email — reply should be empty; penalise if agent replies to spam
        return 1.0 if not reply_draft.strip() else 0.3

    if not reply_draft.strip():
        return 0.0

    reply_lower = reply_draft.lower()
    matched = sum(1 for kw in expected_keywords if kw.lower() in reply_lower)
    raw_score = matched / len(expected_keywords)

    # Ensure at least 0.2 for any non-empty attempt, but scale up to 1.0
    return max(0.2, min(raw_score, 1.0))


def grade_step(
    task_name: str,
    action: TriageAction,
    ground_truth: Dict[str, Any],
) -> Dict[str, float]:
    """
    Aggregate grader scores for a single email triage step.
    Returns a dict with keys: priority_score, category_score, reply_score, total.
    
    Task scoring weights:
      - priority-triage:  priority=1.0, category=0.0, reply=0.0
      - full-routing:     priority=0.5, category=0.5, reply=0.0
      - full-pipeline:    priority=0.3, category=0.3, reply=0.4
    """
    true_priority = ground_truth["priority"]
    true_category = ground_truth["category"]
    reply_keywords = ground_truth.get("reply_keywords", [])

    priority_score = grade_priority(action.priority.value, true_priority)
    category_score = grade_category(action.category.value, true_category)
    reply_score = grade_reply(action.reply_draft, reply_keywords)

    if task_name == "priority-triage":
        total = priority_score * 1.0
        category_score = 0.0
        reply_score = 0.0
    elif task_name == "full-routing":
        total = priority_score * 0.5 + category_score * 0.5
        reply_score = 0.0
    else:  # full-pipeline
        total = priority_score * 0.3 + category_score * 0.3 + reply_score * 0.4

    return {
        "priority_score": round(priority_score, 4),
        "category_score": round(category_score, 4),
        "reply_score": round(reply_score, 4),
        "total": round(total, 4),
    }
