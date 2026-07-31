# ORB

ORB is a small, expandable prototype for an Oroboro-inspired system that combines:

- a core mind loop
- memory and entity tracking
- language interpretation
- simple game and input layers
- browser-based experiments preserved in docs/experiments

## Structure

- core/ - the mind, state, memory, and entity system
- game/ - world, player, events, and UI modules
- language/ - interpretation logic
- input/ - keyboard and MIDI handling
- docs/ - documentation and archived experiments
- tests/ - future regression and behavior tests

## Quick Start (Windows)

From the project root:

1. Create a virtual environment (one-time):

```powershell
python -m venv .venv
```

2. Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Run the core prototype:

```powershell
.\.venv\Scripts\python.exe main.py
```

4. Run tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

5. Run import smoke check:

```powershell
.\.venv\Scripts\python.exe verify_import.py
```

## Browser Experiments

Use the helper script to host the local HTML experiments:

```powershell
start_server.bat
```

Then open http://localhost:8000 in your browser.

## Phase 2: API Bridge (Core Loop + AIO)

Start the Python API bridge in one terminal:

```powershell
start_api.bat
```

Start the static web server in another terminal:

```powershell
start_server.bat
```

Then open http://localhost:8000/AIO.html.

The AIO page will call the core loop through `POST /api/loop` and display core-derived intent/action/state.
If the API is offline, it falls back to local simulation mode.

## Notes

- The optional pygame runtime paths need pygame installed.
- The core loop in main.py does not require pygame.
