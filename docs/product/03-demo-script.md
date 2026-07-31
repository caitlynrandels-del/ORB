# Oroboro MemoryOS 3-Minute Demo Script

## Goal
Show that Oroboro preserves decision continuity across surfaces and adapts behavior over time.

## Variable Frame
- Industry variable: Decision continuity
- Product claim: Oroboro MemoryOS operationalizes decision continuity in real workflows.

## Demo Setup (before call)
1. Start API: start_api.bat
2. Start static server: start_server.bat
3. Open:
- http://localhost:8000/AIO.html
- http://localhost:8000/Index.html
- http://localhost:8000/CreativeStudio.html

## Talk Track
### 0:00-0:30 Problem
"Most AI tools forget what your team already decided. Oroboro solves that by maintaining decision continuity through shared memory and adaptive state across modes."

### 0:30-1:15 AIO (Chat Signal)
1. In AIO, send: "remember artifact path".
2. Show Shared Core State panel.
3. Narrate:
"Intent and memory are stored. State shifts and the system explains its response."

### 1:15-2:00 World Mode (Environment Signal)
1. Move in Index and interact with an object.
2. Trigger a world interaction event.
3. Narrate:
"Now a different interface sends a meaning-bearing event into the same brain."

### 2:00-2:30 Creative Studio (Creative Signal)
1. Draw a gesture or change preset.
2. Show event contribution from Studio.
3. Narrate:
"Creative interactions also update shared state and influence subsequent responses."

### 2:30-3:00 Explainability and Value
1. Return to AIO and send another prompt.
2. Point out updated marker/trust/tension and event count.
3. Close:
"This is not stateless generation. It is decision memory with adaptive response policy."

## Demo Success Checklist
- API online and responding.
- Shared state visible in AIO.
- At least one world event recorded.
- At least one studio event recorded.
- Follow-up response reflects updated context.

## Backup Plan
If API is offline:
- Show fallback behavior in AIO.
- Explain that V1 includes graceful degradation.
