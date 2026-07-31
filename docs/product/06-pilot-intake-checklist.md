# Oroboro MemoryOS Pilot Intake Checklist

Date: 2026-07-31
Purpose: Standardize qualification, setup, and success tracking for every pilot.
Owner: Founder or pilot lead

## 1. Company Qualification
- Company name:
- Primary contact name and role:
- Team size in target workflow (5-50 ideal):
- Industry:
- Decision velocity pain confirmed (yes/no):
- AI tooling currently used:

Qualification gate:
- Must have at least one recurring decision workflow with measurable delay or rework.

## 2. Pilot Scope Definition
- Pilot package selected: Starter or Growth
- Workflow selected for week 1:
- Additional workflows (if Growth):
- Surfaces used in pilot:
  - AIO
  - Index
  - CreativeStudio
  - Other (list)
- Success owner on customer side:
- Success owner on Oroboro side:

Scope guardrails:
- Keep initial scope to one workflow until baseline quality is stable.

## 3. Baseline Metrics Capture (Pre-Pilot)
- Current context retention estimate (%):
- Repeated clarification/re-decision rate (weekly count):
- Average decision-to-execution cycle time (hours/days):
- Team trust score for AI context fit (1-5):
- Key decision artifacts to monitor:

Data source confirmation:
- Where KPI evidence will come from (logs, survey, PM tracker, meeting notes).

## 4. Technical Readiness
- API service reachable in customer environment (yes/no)
- Event ingestion endpoint validated (yes/no)
- Shared state endpoint validated (yes/no)
- Fallback behavior confirmed (yes/no)
- Named pilot workspace created (yes/no)

Runbook checks:
- start_api.bat launches successfully
- start_server.bat serves pilot surfaces
- At least one end-to-end loop call and one event call tested

## 5. Event Taxonomy Setup
- Priority event types selected:
- Required entity labels selected:
- Noise filters defined:
- Confidence threshold guidance set:

Event quality rule:
- Every event should map to an observable team decision or creative action.

## 6. Explainability and Trust Protocol
- Shared state review cadence agreed (weekly minimum)
- Marker/trust/tension interpretation agreed
- Escalation path for incorrect adaptation defined
- Response policy calibration owner assigned

Trust protocol:
- If context mismatch occurs twice in a week, trigger calibration session within 48 hours.

## 7. Week-by-Week Execution
### Week 1
- Environment setup complete
- Baseline captured
- Initial events flowing

### Week 2
- Active usage in selected workflow
- Event taxonomy tuning pass complete

### Week 3
- Decision policy refinement pass complete
- Usage expanded (if quality threshold met)

### Week 4
- KPI comparison and stakeholder readout
- Go/No-Go recommendation documented

## 8. KPI Tracking Template
1. Context Retention Rate
- Baseline:
- Endline:
- Target: >= 80%

2. Rework Reduction
- Baseline:
- Endline:
- Target: >= 30%

3. Cycle-Time Improvement
- Baseline:
- Endline:
- Target: >= 20%

4. Trust Signal
- Baseline:
- Endline:
- Target: >= 4.0 / 5.0

## 9. Go/No-Go Decision
Go criteria:
- Three or more KPI targets met
- At least one workflow shows measurable cycle-time gain
- Stakeholders confirm explainability value

No-Go criteria:
- Context retention below 60%
- No meaningful trust improvement
- Event quality too noisy for stable adaptation

## 10. Sign-Off
Customer lead sign-off:
Date:

Oroboro lead sign-off:
Date:
