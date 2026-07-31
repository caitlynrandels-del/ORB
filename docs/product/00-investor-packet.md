# Oroboro MemoryOS Investor Packet (V1)

Date: 2026-07-31
Status: Pilot-ready

## Industry Variable Assignment
- Industry: B2B AI collaboration and workflow software
- Industry variable: Decision continuity
- Product assignment: Oroboro MemoryOS is the decision continuity layer for AI-native teams.

## 1. Executive Summary
Oroboro MemoryOS is the decision memory layer for AI-native teams. It converts fragmented activity across chat, creative, and execution surfaces into shared context that improves response quality and team velocity.

### The market problem
AI output is still mostly stateless at the team level. As a result, teams repeat decisions, lose handoff context, and spend expensive time rebuilding shared understanding.

### Why this matters now
AI usage has moved from experimentation to daily operations. Continuity is becoming the bottleneck between "interesting demos" and measurable team performance.

### Core thesis
Persistent shared memory plus adaptive state policy turns prompt-by-prompt assistance into context-aware decision support.

## 2. Investment Snapshot
### What we are building
An API-first memory and state layer that any team surface can publish to and read from.

### Initial wedge
Decision Memory for 5-50 person product and creative teams.

### Monetization motion
Paid 30-day pilots that convert into recurring workflow subscriptions.

## 3. Product Definition (V1)
Product name: Oroboro MemoryOS

### V1 scope: Decision Memory
- Ingest events from multiple surfaces.
- Infer meaning (intent, entities, confidence, priority).
- Maintain a project state graph (trust, tension, preference).
- Choose adaptive response strategy.
- Return explainable output with memory and state transitions.

### Target users
- Product managers
- Designers
- Creative leads
- Small cross-functional teams (5-50 users)

### V1 non-goals
- Model training pipelines
- Enterprise SSO
- Broad third-party integrations
- Autonomous agent swarms

## 4. Architecture Snapshot
Input/Event -> Meaning -> State Graph -> Decision -> Response -> State Change

### Current implementation mapping
- API bridge: ORB/api_server.py
- Core cognition loop: ORB/core/oroboro_mind.py
- Adaptive state graph: Oroboro/UpgradeModule.py
- Chat surface: ORB/ORB/AIO.html
- World surface: ORB/ORB/Index.html
- Studio surface: ORB/ORB/CreativeStudio.html

## 5. Value Proposition
### Shared context
Events from different work surfaces enter one cognitive timeline.

### Adaptive intelligence
Responses shift using state (trust, tension, preference), not only latest prompt text.

### Explainable output
Each response is traceable to meaning, memory, and state transitions.

## 6. Go-To-Market Message
### Headline
Your AI should remember what your team already learned.

### Subheadline
Oroboro MemoryOS keeps context alive across chat, world-building, and creative workflows.

### CTAs
- Start a Pilot
- Watch 3-Minute Demo

### Proof-style benefit statement
Oroboro turns fragmented signals into one continuous decision memory, reducing repeated clarification and improving execution speed.

## 7. 3-Minute Demo Narrative
### Setup
1. Start API: start_api.bat
2. Start static server: start_server.bat
3. Open:
- http://localhost:8000/AIO.html
- http://localhost:8000/Index.html
- http://localhost:8000/CreativeStudio.html

### Script
1. 0:00-0:30: Frame the stateless AI problem and continuity thesis.
2. 0:30-1:15: In AIO, send "remember artifact path" and show shared state.
3. 1:15-2:00: In Index, trigger world interaction events.
4. 2:00-2:30: In CreativeStudio, draw/change preset and show event effect.
5. 2:30-3:00: Return to AIO and show marker/trust/tension/event count changes.

### Demo success criteria
- API responds.
- Shared state visible.
- World and studio events recorded.
- Follow-up response reflects updated context.

## 8. Pilot Packaging and Pricing
### Offer
30-day guided pilot for one team.

### Starter Pilot
- Up to 10 users
- One workflow
- Setup, onboarding, weekly review, baseline/endline report
- Price: $4,000

### Growth Pilot
- Up to 30 users
- Up to 3 workflows
- Starter plus taxonomy tuning and policy calibration
- Price: $12,000

## 9. KPI Framework
1. Context Retention Rate
- Definition: sessions where prior decisions are correctly reflected
- Target: >= 80%

2. Rework Reduction
- Definition: drop in repeated clarification prompts or re-decisions
- Target: >= 30%

3. Cycle-Time Improvement
- Definition: faster decision-to-execution transition
- Target: >= 20%

4. Trust Signal
- Definition: user rating for response-context fit
- Target: >= 4.0 / 5.0

## 10. Pilot Execution Plan
1. Week 1: Setup and baseline capture
2. Week 2: Active usage and taxonomy tuning
3. Week 3: Policy refinement and usage expansion
4. Week 4: Outcome review and production recommendation

### Instrumentation
- Log /api/loop and /api/event outcomes.
- Track state graph transitions per session.
- Sample user feedback at key decision points.

## 11. Expansion Decision Criteria
### Go
- Three or more KPI targets met
- At least one workflow shows cycle-time gain
- Stakeholders confirm explainability value

### No-Go
- Context retention below 60%
- No perceived response-quality improvement
- Event quality too noisy for stable adaptation

## 12. Risk and Mitigation
### Risks
- Message sounds abstract
- State-policy/user-expectation drift
- Latency under event spikes

### Mitigations
- Keep language concrete: decision memory, shared context, explainability
- Add expected-state transition test scenarios
- Add bounded event retention and snapshotting

## 13. Immediate Next Moves
1. Convert this packet into a 10-slide investor deck.
2. Publish a one-page pilot signup landing page using the existing copy.
3. Run one starter pilot and collect baseline KPI data in week 1.
4. Produce a short case study from pilot outcomes.
