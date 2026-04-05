"""
Core Customer Email Triage environment logic.
Implements reset(), step(), state() per the OpenEnv spec.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from server.email_dataset import get_emails_for_task
from server.graders import grade_step
from server.models import (
    EmailObservation,
    EnvironmentState,
    Priority,
    Category,
    ResetResult,
    RewardBreakdown,
    StepResult,
    TriageAction,
)
from server.tasks import get_task

# Per-step efficiency penalty (encourages concise, decisive triage)
STEP_PENALTY = 0.02


class EmailTriageEnv:
    """
    Customer Email Triage OpenEnv environment.

    Episode flow:
      1. reset(task_name, seed) → returns first email observation
      2. step(action) × N → agent triages emails one by one
      3. episode ends when all emails in the queue are processed
    """

    def __init__(self) -> None:
        self._task_name: str = "priority-triage"
        self._task_def: Dict[str, Any] = {}
        self._email_queue: List[Dict[str, Any]] = []
        self._current_index: int = 0
        self._step_number: int = 0
        self._episode_reward: float = 0.0
        self._done: bool = True
        self._history: List[Dict[str, Any]] = []
        self._seed: Optional[int] = None
        self._started_at: float = 0.0

    # ── Public API ────────────────────────────────────────────────────────────

    def reset(self, task_name: str = "priority-triage", seed: Optional[int] = None) -> ResetResult:
        """Start a new episode. Returns first email observation."""
        self._task_def = get_task(task_name)
        self._task_name = task_name
        self._email_queue = get_emails_for_task(task_name, seed=seed)
        self._current_index = 0
        self._step_number = 0
        self._episode_reward = 0.0
        self._done = False
        self._history = []
        self._seed = seed
        self._started_at = time.time()

        first_obs = self._make_observation()
        return ResetResult(
            observation=first_obs,
            task_name=task_name,
            total_emails=len(self._email_queue),
            info={"seed": seed, "task": self._task_def},
        )

    def step(self, action: TriageAction) -> StepResult:
        """Process the agent's triage action for the current email."""
        if self._done:
            raise RuntimeError(
                "Episode is done. Call reset() to start a new episode."
            )

        current_email = self._email_queue[self._current_index]
        self._step_number += 1

        # Grade the action
        scores = grade_step(self._task_name, action, current_email["ground_truth"])

        # Shape reward: step score - efficiency penalty
        step_reward = max(0.0, scores["total"] - STEP_PENALTY)

        self._episode_reward += step_reward

        # Record in history
        self._history.append({
            "step": self._step_number,
            "email_id": current_email["id"],
            "subject": current_email["subject"],
            "action": {
                "priority": action.priority.value,
                "category": action.category.value,
                "reply_draft": action.reply_draft[:80] + "..." if len(action.reply_draft) > 80 else action.reply_draft,
            },
            "ground_truth": current_email["ground_truth"],
            "scores": scores,
            "step_reward": round(step_reward, 4),
        })

        # Advance to next email
        self._current_index += 1
        self._done = self._current_index >= len(self._email_queue)

        # Build next observation (None if done)
        next_obs = None if self._done else self._make_observation()

        # Episode-end bonus for excellent performance
        info: Dict[str, Any] = {
            "email_id": current_email["id"],
            "grader_scores": scores,
            "ground_truth": current_email["ground_truth"],
        }
        if self._done:
            avg = self._episode_reward / max(self._step_number, 1)
            if avg >= 0.8:
                step_reward += 0.1  # Bonus for high-quality episode
                info["episode_bonus"] = 0.1
            info["episode_summary"] = {
                "total_reward": round(self._episode_reward, 4),
                "steps": self._step_number,
                "average_step_reward": round(self._episode_reward / max(self._step_number, 1), 4),
                "success": avg >= self._task_def.get("success_threshold", 0.6),
            }

        reward_breakdown = RewardBreakdown(
            priority_score=scores["priority_score"],
            category_score=scores["category_score"],
            reply_score=scores["reply_score"],
            step_penalty=-STEP_PENALTY,
            total=round(step_reward, 4),
        )

        return StepResult(
            observation=next_obs,
            reward=round(step_reward, 4),
            done=self._done,
            info=info,
            reward_breakdown=reward_breakdown,
        )

    def state(self) -> EnvironmentState:
        """Return the full current state snapshot."""
        emails_done = self._current_index
        emails_remaining = max(0, len(self._email_queue) - self._current_index)
        current_email_id = (
            self._email_queue[self._current_index]["id"]
            if not self._done and self._current_index < len(self._email_queue)
            else None
        )
        avg = (
            self._episode_reward / self._step_number
            if self._step_number > 0
            else 0.0
        )
        return EnvironmentState(
            task_name=self._task_name,
            step_number=self._step_number,
            total_emails=len(self._email_queue),
            emails_done=emails_done,
            emails_remaining=emails_remaining,
            episode_reward=round(self._episode_reward, 4),
            average_step_reward=round(avg, 4),
            done=self._done,
            current_email_id=current_email_id,
            history=self._history,
        )

    # ── Internals ─────────────────────────────────────────────────────────────

    def _make_observation(self) -> EmailObservation:
        """Build an EmailObservation from the current email in the queue."""
        email = self._email_queue[self._current_index]
        return EmailObservation(
            email_id=email["id"],
            subject=email["subject"],
            body=email["body"],
            sender=email["sender"],
            sender_tier=email["sender_tier"],
            timestamp=email["timestamp"],
            thread_length=email.get("thread_length", 1),
            previous_interactions=email.get("previous_interactions", 0),
            task_name=self._task_name,
            step_number=self._step_number + 1,
            emails_remaining=len(self._email_queue) - self._current_index,
            episode_reward_so_far=round(self._episode_reward, 4),
        )
