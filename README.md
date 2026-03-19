# AI Study-Plan Generator 📚

Gamified learning for **Microsoft Foundry** and **GitHub Actions**.

Companion app for the session: *Agentic DevOps: The Future of Automation*.

Built with **FastAPI**, **Streamlit**, **Speckit**, **GitHub SDK (PyGithub)**, and **Python**.

## Quick Start

```bash
pip install ".[dev]"

# Terminal 1 — API
uvicorn src.app:app --reload

# Terminal 2 — UI
streamlit run ui.py
```

## Test

```bash
pytest tests/ -v
```

## Try It

```bash
# Create a plan
curl -X POST http://localhost:8000/plans \
  -H "Content-Type: application/json" \
  -d '{"goal": "Build a Foundry agent for CI triage", "hours_per_week": 5, "total_weeks": 12}'

# Complete a topic & earn XP
curl -X POST http://localhost:8000/plans/<PLAN_ID>/complete \
  -H "Content-Type: application/json" \
  -d '{"week": 1}'
```

## API

| Method | Path                       | Description                  |
|--------|----------------------------|------------------------------|
| `GET`  | `/`                        | App info & links             |
| `POST` | `/plans`                   | Generate a study plan        |
| `GET`  | `/plans`                   | List all plans               |
| `GET`  | `/plans/{id}`              | Get a plan                   |
| `PATCH`| `/plans/{id}`              | Refine a plan                |
| `POST` | `/plans/{id}/complete`     | Mark a topic done & earn XP  |
| `GET`  | `/healthz`                 | Health check                 |

## Gamification

- **XP** — Earn points for each completed topic
- **Levels** — Rookie → Explorer → Automator → Pipeline Pro → Agent Builder → DevOps Engineer → Agentic Architect
- **Badges** — 🚀 First Commit · 🏅 Pipeline Apprentice · ⭐ Agent Adept · 🔥 DevOps Dynamo · 🏆 Agentic DevOps Master

## Project Structure

```
src/app.py                        FastAPI app (single file)
ui.py                             Streamlit frontend with gamification
tests/test_plans.py               Integration tests
specs/                            Speckit specifications
scripts/update_pr_description.py  GitHub SDK — sync PR body with spec
.github/workflows/ci.yml          CI: lint → test → PR sync
.specify/                         Speckit project memory
```

## Tech Stack

- **FastAPI + Pydantic v2** — API & validation
- **Streamlit** — Gamified frontend with XP, levels & badges
- **Speckit** — spec-first development ([specs/](specs/))
- **PyGithub** — PR description auto-sync ([scripts/](scripts/))
- **GitHub Actions** — CI pipeline
