# Oroboro MemoryOS Pilot Pricing and Success Metrics

## Pilot Offer
30-day guided pilot for one team.

## Packaging
### Starter Pilot
- Team size: up to 10 users
- Scope: one project workflow
- Includes:
  - setup and onboarding
  - weekly review
  - baseline and endline report

### Growth Pilot
- Team size: up to 30 users
- Scope: up to 3 workflows
- Includes:
  - everything in Starter
  - extended event taxonomy tuning
  - response policy calibration

## Suggested Pricing (Initial)
- Starter Pilot: $4,000 for 30 days
- Growth Pilot: $12,000 for 30 days

## Pilot KPIs
1. Context Retention Rate
Definition: percent of sessions where prior decisions are correctly reflected.
Target: >= 80%

2. Rework Reduction
Definition: drop in repeated clarification prompts or re-decisions.
Target: >= 30%

3. Cycle-Time Improvement
Definition: faster decision-to-execution transition.
Target: >= 20%

4. Trust Signal
Definition: user rating on "responses match project context".
Target: >= 4.0 / 5.0

## Instrumentation Plan
- Log /api/loop and /api/event outcomes.
- Track state graph transitions per session.
- Sample user feedback after key decision points.

## Pilot Milestones
1. Week 1: setup and baseline capture
2. Week 2: active usage and taxonomy tuning
3. Week 3: policy refinement and usage expansion
4. Week 4: outcome review and production recommendation

## Go/No-Go Criteria for Expansion
Go if:
- 3 or more KPI targets are met
- at least one workflow demonstrates measurable cycle-time gain
- stakeholders confirm explainability value

No-Go if:
- context retention remains below 60%
- users do not perceive response quality improvement
- event quality is too noisy for stable adaptation
