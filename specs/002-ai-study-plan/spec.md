# Feature Specification: AI Study-Plan Generator

**Feature Branch**: `002-ai-study-plan`
**Created**: 2 March 2026
**Status**: Draft

## Purpose

Users generate a gamified, week-by-week study plan for learning Agentic DevOps:
Microsoft Foundry agents and GitHub Actions.
Topics earn XP, unlock levels, and award badges to keep learners engaged.

## User Stories

### 1. Generate a Plan (P1)

**Given** a user provides a learning goal and time budget,
**When** they submit a request,
**Then** they receive a weekly plan with Foundry/CI topics, XP values, and milestones.

### 2. Personalise by Skill Level (P2)

**Given** a user selects beginner / intermediate / advanced,
**When** the plan is generated,
**Then** topics are tailored — beginners start with Foundry basics, advanced learners dive into multi-agent orchestration.

### 3. Complete Topics & Earn XP (P1)

**Given** a plan has been generated,
**When** the user marks a week's topic as completed,
**Then** they earn XP, their level updates, and badges unlock at milestones.

### 4. Save & Retrieve (P2)

**Given** a plan has been generated,
**When** the user requests it later,
**Then** the same plan (with completion state) is returned.

### 5. Refine a Plan (P3)

**Given** a user has a plan,
**When** they submit a refinement instruction,
**Then** the plan is regenerated accordingly.

## Requirements

- **FR-001**: Accept a goal (3-500 chars), skill level, hours/week, and total weeks.
- **FR-002**: Generate a plan with Foundry/DevOps topics, XP per topic, and milestones with badges.
- **FR-003**: Mark individual topics as completed; recalculate XP, level, and badges.
- **FR-004**: Store and retrieve plans with completion state.
- **FR-005**: Support plan refinement via follow-up instructions.
- **FR-006**: Default to beginner / 5 hrs/week / 12 weeks when not specified.

## Success Criteria

- **SC-001**: Plan generated in under 2 seconds.
- **SC-002**: Time allocations never exceed user-stated hours/week.
- **SC-003**: Plans at different skill levels produce noticeably different Foundry topics.
