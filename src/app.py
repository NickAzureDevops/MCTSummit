"""AI Study-Plan Generator — gamified learning for Microsoft Foundry.

Single-file FastAPI app. Stores plans in memory (swap to a DB when ready).
Companion app for the "Agentic DevOps: The Future of Automation" session.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, Field

# ── App ────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="AI Study-Plan Generator",
    version="0.1.0",
    description=(
        "Gamified study plans for mastering Agentic DevOps: "
        "Microsoft Foundry agents and GitHub Actions."
    ),
)

# In-memory store
PLANS: dict[str, dict] = {}


@app.get("/")
async def root():
    """Landing page."""
    return {
        "app": "AI Study-Plan Generator",
        "session": "Agentic DevOps: The Future of Automation",
        "docs": "/docs",
        "health": "/healthz",
    }


# ── Schemas ────────────────────────────────────────────────────────────────


class PlanCreate(BaseModel):
    goal: str = Field(
        ...,
        min_length=3,
        max_length=500,
        examples=["Build a Foundry agent that auto-triages CI failures"],
    )
    skill_level: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")
    hours_per_week: int = Field(default=5, ge=1, le=80)
    total_weeks: int = Field(default=12, ge=1, le=104)


class PlanRefine(BaseModel):
    instruction: str = Field(..., min_length=3, max_length=1000)


class CompleteTopic(BaseModel):
    week: int = Field(..., ge=1)


class Period(BaseModel):
    week: int
    topic: str
    hours: int
    xp: int
    completed: bool = False


class Milestone(BaseModel):
    description: str
    target_week: int
    badge: str


class PlanOut(BaseModel):
    id: str
    goal: str
    skill_level: str
    hours_per_week: int
    total_weeks: int
    xp_total: int
    xp_earned: int
    level: int
    level_name: str
    badges_earned: list[str]
    periods: list[Period]
    milestones: list[Milestone]
    created_at: str


# ── Agentic DevOps curriculum by skill level ───────────────────────────────
# Each topic carries an XP reward — harder topics earn more!

_CURRICULUM: dict[str, list[dict[str, str | int]]] = {
    "beginner": [
        {"topic": "🤖 What is Agentic DevOps?", "xp": 10},
        {"topic": "🌐 Explore the Foundry portal", "xp": 10},
        {"topic": "🗂️ Model catalog & deployments", "xp": 15},
        {"topic": "💬 Prompt engineering 101", "xp": 15},
        {"topic": "⚡ GitHub Actions crash course", "xp": 20},
        {"topic": "🔧 CI/CD pipeline design patterns", "xp": 20},
        {"topic": "🐍 Foundry SDK quickstart", "xp": 25},
        {"topic": "🛠️ Build a chat-completion CI check", "xp": 25},
        {"topic": "🕵️ Create your first Foundry Agent", "xp": 30},
        {"topic": "🚀 Run an agent in GitHub Actions", "xp": 30},
        {"topic": "📊 Evaluate agent responses", "xp": 25},
        {"topic": "🏆 Capstone: end-to-end agent pipeline", "xp": 40},
    ],
    "intermediate": [
        {"topic": "🔐 RBAC & managed identity for agents", "xp": 20},
        {"topic": "📚 RAG — build a knowledge index", "xp": 25},
        {"topic": "🧰 Tool-use & function calling", "xp": 25},
        {"topic": "🔄 Multi-turn agent conversations", "xp": 25},
        {"topic": "🩺 Self-healing pipelines with AI", "xp": 30},
        {"topic": "🔗 Service hooks & event triggers", "xp": 25},
        {"topic": "🎲 Dynamic matrix builds in Actions", "xp": 30},
        {"topic": "🛡️ Content safety & guardrails", "xp": 30},
        {"topic": "📈 Evaluation metrics deep-dive", "xp": 30},
        {"topic": "📡 Monitoring agents in production", "xp": 30},
        {"topic": "🧪 Prompt flow orchestration", "xp": 35},
        {"topic": "🏆 Capstone: self-healing CI with agents", "xp": 50},
    ],
    "advanced": [
        {"topic": "🤝 Multi-agent orchestration patterns", "xp": 35},
        {"topic": "🔌 MCP (Model Context Protocol)", "xp": 35},
        {"topic": "🧠 Semantic Kernel integration", "xp": 35},
        {"topic": "🔄 Self-adjusting deployment strategies", "xp": 40},
        {"topic": "📚 Advanced RAG — hybrid search & reranking", "xp": 40},
        {"topic": "🌉 AI Gateway with API Management", "xp": 35},
        {"topic": "🎯 BYOM — bring your own model", "xp": 40},
        {"topic": "🏢 Enterprise agent governance", "xp": 35},
        {"topic": "📊 Observability & distributed tracing", "xp": 40},
        {"topic": "🛡️ Red-teaming & safety testing", "xp": 40},
        {"topic": "♾️ GitOps for agent deployments", "xp": 40},
        {"topic": "🏆 Capstone: production multi-agent system", "xp": 60},
    ],
}

# ── Levels & badges ────────────────────────────────────────────────────────

_LEVELS: list[tuple[int, str]] = [
    (0, "🌱 Rookie"),
    (200, "🔍 Explorer"),
    (500, "⚙️ Automator"),
    (1000, "🔥 Pipeline Pro"),
    (1750, "🤖 Agent Builder"),
    (2500, "🛠️ DevOps Engineer"),
    (3500, "🏛️ Agentic Architect"),
]

_BADGE_THRESHOLDS: list[tuple[float, str, str]] = [
    (0.01, "first_step", "🚀 First Commit"),
    (0.25, "quarter", "🏅 Pipeline Apprentice"),
    (0.50, "halfway", "⭐ Agent Adept"),
    (0.75, "three_quarter", "🔥 DevOps Dynamo"),
    (1.00, "completer", "🏆 Agentic DevOps Master"),
]

def _calc_level(xp: int) -> tuple[int, str]:
    """Return (level_number, level_name) for a given XP total."""
    level, name = 0, _LEVELS[0][1]
    for i, (threshold, label) in enumerate(_LEVELS):
        if xp >= threshold:
            level, name = i, label
    return level, name


def _calc_badges(plan: dict) -> list[str]:
    """Return earned badge names based on completion fraction."""
    periods = plan.get("periods", [])
    if not periods:
        return []
    done = sum(1 for p in periods if p.get("completed"))
    frac = done / len(periods)
    return [badge for threshold, _key, badge in _BADGE_THRESHOLDS if frac >= threshold]


def _enrich_plan(plan: dict) -> dict:
    """Add computed gamification fields to a plan before returning it."""
    periods = plan.get("periods", [])
    xp_total = sum(p.get("xp", 0) for p in periods)
    xp_earned = sum(p.get("xp", 0) for p in periods if p.get("completed"))
    level, level_name = _calc_level(xp_earned)
    badges = _calc_badges(plan)
    plan.update(
        xp_total=xp_total,
        xp_earned=xp_earned,
        level=level,
        level_name=level_name,
        badges_earned=badges,
    )
    return plan


def generate_plan(goal: str, skill_level: str, hours_per_week: int, total_weeks: int) -> dict:
    """Build a Foundry-focused study plan with XP rewards."""
    topics = _CURRICULUM.get(skill_level, _CURRICULUM["beginner"])

    # Spread curriculum across the requested weeks
    periods: list[dict] = []
    for w in range(1, total_weeks + 1):
        entry = topics[(w - 1) % len(topics)]
        periods.append({
            "week": w,
            "topic": entry["topic"],
            "hours": hours_per_week,
            "xp": entry["xp"],
            "completed": False,
        })

    # Milestones at quarter marks with badges
    quarter = max(1, total_weeks // 4)
    badge_map = {0: "🚀 First Commit", 1: "🏅 Pipeline Apprentice",
                 2: "⭐ Agent Adept", 3: "🔥 DevOps Dynamo"}
    milestones = []
    for i, w in enumerate(range(quarter, total_weeks + 1, quarter)):
        milestones.append({
            "description": f"Checkpoint — review weeks 1-{w}",
            "target_week": w,
            "badge": badge_map.get(i, "🏆 Agentic DevOps Master"),
        })

    return {"periods": periods, "milestones": milestones}


# ── Middleware ─────────────────────────────────────────────────────────────

@app.middleware("http")
async def add_request_id(request: Request, call_next) -> Response:  # type: ignore[no-untyped-def]
    rid = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    response: Response = await call_next(request)
    response.headers["X-Request-Id"] = rid
    return response


# ── Routes ─────────────────────────────────────────────────────────────────

@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/plans", status_code=201, response_model=PlanOut)
async def create_plan(body: PlanCreate) -> dict:
    content = generate_plan(body.goal, body.skill_level, body.hours_per_week, body.total_weeks)
    plan = {
        "id": str(uuid.uuid4()),
        "goal": body.goal,
        "skill_level": body.skill_level,
        "hours_per_week": body.hours_per_week,
        "total_weeks": body.total_weeks,
        "periods": content["periods"],
        "milestones": content["milestones"],
        "created_at": datetime.now(UTC).isoformat(),
    }
    return _enrich_plan(PLANS.setdefault(plan["id"], plan))


@app.get("/plans", response_model=list[PlanOut])
async def list_plans() -> list[dict]:
    return [_enrich_plan(p) for p in PLANS.values()]


@app.get("/plans/{plan_id}", response_model=PlanOut)
async def get_plan(plan_id: str) -> dict:
    if plan_id not in PLANS:
        raise HTTPException(status_code=404, detail="Plan not found")
    return _enrich_plan(PLANS[plan_id])


@app.patch("/plans/{plan_id}", response_model=PlanOut)
async def refine_plan(plan_id: str, body: PlanRefine) -> dict:
    if plan_id not in PLANS:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan = PLANS[plan_id]
    content = generate_plan(
        plan["goal"], plan["skill_level"], plan["hours_per_week"], plan["total_weeks"]
    )
    plan["periods"] = content["periods"]
    plan["milestones"] = content["milestones"]
    return _enrich_plan(plan)


@app.post("/plans/{plan_id}/complete", response_model=PlanOut)
async def complete_topic(plan_id: str, body: CompleteTopic) -> dict:
    """Mark a week's topic as completed and earn XP! 🎉"""
    if plan_id not in PLANS:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan = PLANS[plan_id]
    for period in plan["periods"]:
        if period["week"] == body.week:
            period["completed"] = True
            return _enrich_plan(plan)
    raise HTTPException(status_code=404, detail=f"Week {body.week} not found")
