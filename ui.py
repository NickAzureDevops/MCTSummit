"""AI Study-Plan Generator — Gamified Streamlit frontend.

Run:  streamlit run ui.py
"""

from __future__ import annotations

import random

import requests
import streamlit as st

API = "http://localhost:8000"

# ── Page config ────────────────────────────────────────────────────────────

st.set_page_config(page_title="AI Study-Plan Generator", page_icon="🤖", layout="wide")

# Fun CSS: animated gradient header, glowing XP bar, emoji badges
st.markdown("""
<style>
    .level-badge {
        display: inline-block; padding: 4px 14px; border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; font-weight: bold; font-size: 1.1em;
    }
    .xp-bar-bg {
        background: #23272f; border-radius: 12px; padding: 3px; margin: 8px 0;
    }
    .xp-bar-fill {
        background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
        border-radius: 10px; height: 22px; text-align: center;
        color: #23272f; font-weight: bold; font-size: 0.85em;
        line-height: 22px; transition: width 0.5s ease;
    }
    .badge-shelf { font-size: 1.6em; letter-spacing: 6px; }
    .fun-quote {
        font-style: italic; color: #888; text-align: center;
        padding: 8px; border-left: 3px solid #764ba2;
        margin: 12px 0;
    }
    .week-done { opacity: 0.55; }
</style>
""", unsafe_allow_html=True)

FUN_QUOTES = [
    "🤖 Agents don't build themselves — but you can build them!",
    "🚀 Ship it, learn it, repeat.",
    "⚡ Every commit is a step toward agentic mastery.",
    "🧠 The pipeline is your dojo. Train hard.",
    "🔥 You're one deploy away from greatness.",
    "🏗️ Build the future, one agent at a time.",
    "💡 Prompt wisely, deploy boldly.",
]

st.title("🤖 AI Study-Plan Generator")
st.caption("Master **Agentic DevOps** — Microsoft Foundry & GitHub Actions.")

# ── Sidebar: inputs ───────────────────────────────────────────────────────

with st.sidebar:
    st.header("🎮 New Quest")
    goal = st.text_input(
        "Learning goal",
        placeholder="e.g. Build a Foundry agent that auto-triages CI failures",
    )
    skill_level = st.selectbox(
        "Skill level",
        ["beginner", "intermediate", "advanced"],
        format_func=lambda x: {
            "beginner": "🌱 Beginner",
            "intermediate": "⚙️ Intermediate",
            "advanced": "🏛️ Advanced",
        }[x],
    )
    hours_per_week = st.slider("Hours / week", 1, 40, 5)
    total_weeks = st.slider("Total weeks", 1, 52, 12)
    generate = st.button("⚡ Generate Plan", type="primary", use_container_width=True)

    st.divider()
    st.markdown(f'<div class="fun-quote">{random.choice(FUN_QUOTES)}</div>', unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────


def _complete_week(plan_id: str, week: int) -> dict | None:
    """Mark a week complete and return refreshed plan."""
    try:
        r = requests.post(f"{API}/plans/{plan_id}/complete", json={"week": week}, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


# ── Generate ───────────────────────────────────────────────────────────────

if generate and goal:
    with st.spinner("⚡ Generating your quest…"):
        try:
            resp = requests.post(
                f"{API}/plans",
                json={
                    "goal": goal,
                    "skill_level": skill_level,
                    "hours_per_week": hours_per_week,
                    "total_weeks": total_weeks,
                },
                timeout=30,
            )
            resp.raise_for_status()
            st.session_state["plan"] = resp.json()
            st.balloons()
        except requests.ConnectionError:
            st.error("🔌 Cannot reach API. Start it with: `uvicorn src.app:app --reload`")
        except requests.HTTPError as e:
            st.error(f"API error: {e.response.text}")

# ── Display plan ───────────────────────────────────────────────────────────

if "plan" in st.session_state:
    plan = st.session_state["plan"]
    plan_id = plan["id"]

    st.divider()

    # ── Scoreboard ─────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎯 Goal", plan["goal"][:40] + ("…" if len(plan["goal"]) > 40 else ""))
    col2.metric("⚡ XP", f"{plan.get('xp_earned', 0)} / {plan.get('xp_total', 0)}")
    col3.markdown(
        f'<span class="level-badge">{plan.get("level_name", "🌱 Rookie")}</span>',
        unsafe_allow_html=True,
    )
    col4.metric("📅 Schedule", f"{plan['hours_per_week']}h × {plan['total_weeks']}wk")

    # ── XP Progress Bar ────────────────────────────────────────────────────
    xp_total = plan.get("xp_total", 1)
    xp_earned = plan.get("xp_earned", 0)
    pct = min(100, int(xp_earned / max(xp_total, 1) * 100))

    st.markdown(f"""
    <div class="xp-bar-bg">
        <div class="xp-bar-fill" style="width: {max(pct, 2)}%">{pct}%</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Badges Earned ──────────────────────────────────────────────────────
    badges = plan.get("badges_earned", [])
    if badges:
        st.markdown("### 🏅 Badges Earned")
        st.markdown(f'<div class="badge-shelf">{" ".join(badges)}</div>', unsafe_allow_html=True)
    else:
        st.info("Complete your first topic to earn the **🚀 First Commit** badge!")

    st.divider()

    # ── Weekly Schedule with Completion Buttons ────────────────────────────
    st.subheader("📅 Weekly Quest Log")

    done_count = sum(1 for p in plan["periods"] if p.get("completed"))
    total_count = len(plan["periods"])
    st.progress(
        done_count / max(total_count, 1),
        text=f"{done_count}/{total_count} topics completed",
    )

    for period in plan["periods"]:
        is_done = period.get("completed", False)
        xp_val = period.get("xp", 0)
        icon = "✅" if is_done else "📖"

        header = f"{icon} **Week {period['week']}** — {period['topic']}  |  `+{xp_val} XP`"
        if is_done:
            header += "  *(completed)*"

        with st.expander(header, expanded=not is_done and period["week"] <= done_count + 2):
            st.write(f"Dedicate **{period['hours']} hours** to: **{period['topic']}**")
            st.write(f"🎯 Reward: **+{xp_val} XP**")

            if not is_done:
                if st.button(
                    f"✓ Mark Complete — Earn {xp_val} XP!",
                    key=f"complete_{period['week']}",
                    type="primary",
                ):
                    result = _complete_week(plan_id, period["week"])
                    if result:
                        st.session_state["plan"] = result
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Failed to mark complete. Is the API running?")
            else:
                st.success(f"Done! You earned **+{xp_val} XP** 🎉")

    st.divider()

    # ── Milestones ─────────────────────────────────────────────────────────
    st.subheader("🏁 Milestones & Badges")
    for ms in plan["milestones"]:
        badge = ms.get("badge", "🏅")
        st.success(f"{badge} **Week {ms['target_week']}**: {ms['description']}")

    # ── Fun footer ─────────────────────────────────────────────────────────
    st.divider()
    st.markdown(
        f'<div class="fun-quote">{random.choice(FUN_QUOTES)}</div>',
        unsafe_allow_html=True,
    )

elif generate and not goal:
    st.warning("⚠️ Enter a learning goal to start your quest!")
