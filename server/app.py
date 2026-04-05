"""
FastAPI server for the Customer Email Triage OpenEnv environment.
Exposes: POST /reset, POST /step, GET /state, GET /tasks, GET /web (dashboard)
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from server.environment import EmailTriageEnv
from server.models import (
    EnvironmentState,
    ResetRequest,
    ResetResult,
    StepResult,
    TriageAction,
)
from server.tasks import list_tasks

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Customer Email Triage — OpenEnv",
    description=(
        "An OpenEnv environment where AI agents learn to triage customer support emails: "
        "classify priority, route to the correct department, and draft professional replies."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single shared environment instance (suitable for demo / single-agent eval)
env = EmailTriageEnv()

# Serve web dashboard
_WEB_DIR = Path(__file__).parent / "web"
if _WEB_DIR.exists():
    app.mount("/web", StaticFiles(directory=str(_WEB_DIR), html=True), name="web")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root() -> HTMLResponse:
    """Redirect root to the web dashboard."""
    return HTMLResponse(
        '<html><head><meta http-equiv="refresh" content="0; url=/web/"></head></html>'
    )


@app.post("/reset", response_model=ResetResult, tags=["OpenEnv"])
async def reset(request: ResetRequest = ResetRequest()) -> ResetResult:
    """
    Start a new episode.
    Returns the first email observation for the selected task.
    """
    try:
        result = env.reset(task_name=request.task, seed=request.seed)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/step", response_model=StepResult, tags=["OpenEnv"])
async def step(action: TriageAction) -> StepResult:
    """
    Take a triage action on the current email.
    Returns next observation, reward, done flag, and reward breakdown.
    """
    try:
        result = env.step(action)
        return result
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@app.get("/state", response_model=EnvironmentState, tags=["OpenEnv"])
async def state() -> EnvironmentState:
    """Return the full current environment state snapshot."""
    return env.state()


@app.get("/tasks", tags=["OpenEnv"])
async def get_tasks() -> Dict[str, Any]:
    """List all available tasks with metadata."""
    return {"tasks": list_tasks()}


@app.get("/health", tags=["Meta"])
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "env": "customer-email-triage", "version": "1.0.0"}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)
