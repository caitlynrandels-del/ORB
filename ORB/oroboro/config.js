const DEFAULT_CONTROLS = {
  up: 'KeyW',
  down: 'KeyS',
  left: 'KeyA',
  right: 'KeyD',
  interact: 'Space',
  menu: 'KeyM'
};

function loadControls() {
  try {
    const saved = localStorage.getItem('orb-controls');
    return saved ? { ...DEFAULT_CONTROLS, ...JSON.parse(saved) } : { ...DEFAULT_CONTROLS };
  } catch (e) {
    return { ...DEFAULT_CONTROLS };
  }
}

function saveControls(controls) {
  localStorage.setItem('orb-controls', JSON.stringify(controls));
}

window.DEFAULT_CONTROLS = DEFAULT_CONTROLS;
window.loadControls = loadControls;
window.saveControls = saveControls;
