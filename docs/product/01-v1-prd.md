# Oroboro MemoryOS V1 PRD

## Product Name
Oroboro MemoryOS

## Industry Variable Assignment
- Industry: B2B AI collaboration and workflow software
- Industry variable: Decision continuity
- Product assignment: Oroboro MemoryOS is the decision continuity layer that preserves shared context across team surfaces.

## Problem
Teams lose decision context across chat, creative work, and execution tools.
AI assistants answer each prompt in isolation, which causes:
- repeated work
- contradictory decisions
- weak handoffs
- low trust in AI output

## Product Thesis
A shared memory and state layer can preserve semantic continuity and improve AI response quality across workflows.

## V1 Scope (Decision Memory)
V1 covers one core workflow:
- ingest events from multiple surfaces
- infer meaning (intent, entities, priority)
- maintain a project state graph (trust, tension, preference)
- adapt response strategy
- expose explainable memory and state to users

## Target Users
- Product managers
- Designers
- Creative leads
- Small cross-functional teams (5-50 users)

## User Stories
1. As a PM, I want AI to remember prior decisions so planning does not restart from zero.
2. As a designer, I want canvas interactions to influence AI tone and suggestions.
3. As a team lead, I want to see why the assistant answered a specific way.

## Functional Requirements
1. Event ingestion API
- Accept structured events and free text loop inputs.
- Persist a recent event stream.

2. Meaning inference
- Infer intent, entities, confidence, and priority from incoming signals.

3. State graph
- Maintain trust, tension, preference, and marker.
- Update state after each processed event.

4. Decision policy
- Choose strategy and action_hint from state + meaning + memory history.

5. Confidence review loop
- Run iterative observe-interpret-refine passes before action.
- Use confidence threshold and progress gating to avoid low-quality decisions.
- Fall back to best-guess with explicit uncertainty when confidence is insufficient.

6. Explainability
- Return response plus state changes and memory summary.

7. Shared UX support
- Expose shared state endpoint for multi-view UI sync.

## Non-Goals (V1)
- model training pipelines
- enterprise SSO
- broad third-party integrations
- autonomous agent swarms

## Current System Mapping
- API bridge: ORB/api_server.py
- Base cognition loop: ORB/core/oroboro_mind.py
- Adaptive state graph layer: Oroboro/UpgradeModule.py
- Chat surface: ORB/ORB/AIO.html
- World surface: ORB/ORB/Index.html
- Studio surface: ORB/ORB/CreativeStudio.html

## Success Criteria
- 30% reduction in repeated clarification prompts in pilot teams.
- 20% faster decision-to-execution cycle time in pilot projects.
- 80%+ user agreement on "assistant responses reflect project context".

## Risks
- Over-complex messaging (appears abstract or non-practical).
- Drift between state policy and user expectations.
- Latency if event volume spikes without batching.

## Mitigations
- Keep UX language concrete (decision memory, shared context, explainability).
- Add test scenarios for expected state transitions.
- Add event retention bounds and simple snapshots.

## V1 Exit Criteria
- Stable API endpoints for loop, event, and state.
- Shared state visible in at least one production-like UI flow.
- Pilot pack ready: demo script, pricing, and measurable outcomes.
