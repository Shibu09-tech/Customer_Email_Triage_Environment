"""
Pydantic models for the Customer Email Triage OpenEnv environment.
Defines typed Observation, Action, and Reward models per the OpenEnv spec.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────────────────────────────

class Priority(str, Enum):
    """Email priority levels an agent can assign."""
    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SPAM = "spam"


class Category(str, Enum):
    """Routing categories for customer emails."""
    BILLING = "billing"
    TECHNICAL = "technical"
    REFUNDS = "refunds"
    GENERAL = "general"
    SPAM = "spam"
    ACCOUNT = "account"
    COMPLIANCE = "compliance"


# ── Observation ───────────────────────────────────────────────────────────────

class EmailObservation(BaseModel):
    """
    What the agent sees each step: the current email to triage.
    """
    email_id: str = Field(..., description="Unique identifier for this email")
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Full email body text")
    sender: str = Field(..., description="Sender email address")
    sender_tier: str = Field(..., description="Customer tier: free / pro / enterprise")
    timestamp: str = Field(..., description="ISO-8601 timestamp when email was received")
    thread_length: int = Field(default=1, description="Number of emails in this thread")
    previous_interactions: int = Field(default=0, description="Prior tickets opened by this sender")
    task_name: str = Field(..., description="Name of the active task")
    step_number: int = Field(..., description="Current step in the episode")
    emails_remaining: int = Field(..., description="Emails left to triage in this episode")
    episode_reward_so_far: float = Field(default=0.0, description="Cumulative reward so far")


# ── Action ────────────────────────────────────────────────────────────────────

class TriageAction(BaseModel):
    """
    Agent's triage decision for the current email.
    For easy task: only priority matters.
    For medium task: priority + category matter.
    For hard task: all three fields matter.
    """
    priority: Priority = Field(..., description="Assigned email priority")
    category: Category = Field(..., description="Routing department/category")
    reply_draft: str = Field(
        default="",
        description="Draft reply to send to the customer (required for hard task)",
        max_length=2000,
    )


# ── Reward breakdown ──────────────────────────────────────────────────────────

class RewardBreakdown(BaseModel):
    """Detailed breakdown of the reward for a single step."""
    priority_score: float = Field(default=0.0, description="Score for priority correctness [0,1]")
    category_score: float = Field(default=0.0, description="Score for category correctness [0,1]")
    reply_score: float = Field(default=0.0, description="Score for reply quality [0,1]")
    step_penalty: float = Field(default=0.0, description="Small per-step efficiency penalty")
    total: float = Field(default=0.0, description="Total step reward")


# ── Step result ───────────────────────────────────────────────────────────────

class StepResult(BaseModel):
    """Full result returned by POST /step."""
    observation: Optional[EmailObservation] = Field(
        None, description="Next email to triage (None if episode done)"
    )
    reward: float = Field(..., description="Reward earned this step")
    done: bool = Field(..., description="Whether the episode has ended")
    info: Dict[str, Any] = Field(default_factory=dict, description="Auxiliary info")
    reward_breakdown: RewardBreakdown = Field(
        default_factory=RewardBreakdown,
        description="Detailed reward breakdown for this step",
    )


# ── Reset request / result ────────────────────────────────────────────────────

class ResetRequest(BaseModel):
    """Request body for POST /reset."""
    task: str = Field(
        default="priority-triage",
        description="Task name: priority-triage | full-routing | full-pipeline",
    )
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")


class ResetResult(BaseModel):
    """Response from POST /reset."""
    observation: EmailObservation
    task_name: str
    total_emails: int
    info: Dict[str, Any] = Field(default_factory=dict)


# ── State ─────────────────────────────────────────────────────────────────────

class EnvironmentState(BaseModel):
    """Full state snapshot returned by GET /state."""
    task_name: str
    step_number: int
    total_emails: int
    emails_done: int
    emails_remaining: int
    episode_reward: float
    average_step_reward: float
    done: bool
    current_email_id: Optional[str] = None
    history: List[Dict[str, Any]] = Field(default_factory=list)
