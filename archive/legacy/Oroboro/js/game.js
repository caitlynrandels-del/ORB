const TILE_SIZE = 48;
const canvas = document.getElementById('worldCanvas');
const ctx = canvas.getContext('2d');

const world = [
  '##############',
  '#............#',
  '#..TT...H....#',
  '#....T.......#',
  '#....T..S....#',
  '#......T.....#',
  '#............#',
  '##############'
];

const player = { x: 1, y: 1 };
const monster = { x: 8, y: 5, dir: 0 };
const quest = { heart: false, shrine: false };
let demoTimer = null;
let lastMonsterStep = 0;

function canEnter(x, y) {
  const tile = world[y] && world[y][x];
  return Boolean(tile) && tile !== '#';
}

function updateStatus() {
  const lines = [
    `State: ${OroboroMind.state || 'AWAKENING'}`,
    `Memory: ${OroboroMind.memory.length}`,
    `Quest: ${quest.heart ? 'heart found' : 'seek heart'} / ${quest.shrine ? 'shrine visited' : 'find shrine'}`
  ];
  document.getElementById('status').innerHTML = lines.join('<br>');
}

function feedMind(label, detail) {
  const thought = Language.interpret(label);
  thought.meaning.detail = detail;
  OroboroMind.think(thought.meaning);
  updateStatus();
}

function collectTile() {
  const tile = world[player.y][player.x];
  if (tile === 'H') {
    quest.heart = true;
    world[player.y] = world[player.y].slice(0, player.x) + '.' + world[player.y].slice(player.x + 1);
    feedMind('heart piece', 'the relic answers the explorer');
    OroboroMind.remember({ raw: 'heart', concept: 'heart', intent: 'protect', action: 'keep the relic close' });
  }

  if (tile === 'S') {
    quest.shrine = true;
    feedMind('shrine', 'the old sanctuary opens');
    OroboroMind.remember({ raw: 'shrine', concept: 'shrine', intent: 'remember', action: 'gather the lesson' });
  }
}

function movePlayer(dx, dy) {
  const nextX = player.x + dx;
  const nextY = player.y + dy;

  if (canEnter(nextX, nextY)) {
    player.x = nextX;
    player.y = nextY;
    collectTile();
  }

  if (player.x === monster.x && player.y === monster.y) {
    feedMind('monster', 'a shadow blocks the path');
  } else {
    feedMind('forest', 'the path shifts with each step');
  }

  render();
}

function stepMonster() {
  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  const [dx, dy] = dirs[monster.dir % dirs.length];
  const nextX = monster.x + dx;
  const nextY = monster.y + dy;

  if (canEnter(nextX, nextY)) {
    monster.x = nextX;
    monster.y = nextY;
  } else {
    monster.dir += 1;
  }

  if (player.x === monster.x && player.y === monster.y) {
    feedMind('monster', 'the enemy has found the hero');
  }
}

function startDemo() {
  if (demoTimer) return;
  const route = [
    [1, 0], [1, 0], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0], [0, 1], [0, -1], [1, 0]
  ];
  let index = 0;
  demoTimer = setInterval(() => {
    if (index >= route.length) {
      clearInterval(demoTimer);
      demoTimer = null;
      return;
    }
    const [dx, dy] = route[index];
    movePlayer(dx, dy);
    index += 1;
  }, 320);
}

function drawTile(x, y, color) {
  ctx.fillStyle = color;
  ctx.fillRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
  ctx.strokeStyle = '#1d2434';
  ctx.strokeRect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE);
}

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let y = 0; y < world.length; y += 1) {
    for (let x = 0; x < world[y].length; x += 1) {
      const tile = world[y][x];
      if (tile === '#') {
        drawTile(x, y, '#2b3a4f');
      } else if (tile === 'T') {
        drawTile(x, y, '#1f5b2e');
      } else if (tile === 'H') {
        drawTile(x, y, '#ff5d73');
      } else if (tile === 'S') {
        drawTile(x, y, '#f1d96a');
      } else {
        drawTile(x, y, '#3f8f41');
      }
    }
  }

  ctx.fillStyle = '#f3c75d';
  ctx.beginPath();
  ctx.arc(player.x * TILE_SIZE + TILE_SIZE / 2, player.y * TILE_SIZE + TILE_SIZE / 2, 14, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#c24a4a';
  ctx.beginPath();
  ctx.arc(monster.x * TILE_SIZE + TILE_SIZE / 2, monster.y * TILE_SIZE + TILE_SIZE / 2, 13, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#fff';
  ctx.font = '16px Arial';
  ctx.fillText('Hero', player.x * TILE_SIZE + 6, player.y * TILE_SIZE + 36);
  ctx.fillText('Shadow', monster.x * TILE_SIZE + 6, monster.y * TILE_SIZE + 36);
}

function animateMonster() {
  const now = performance.now();
  if (now - lastMonsterStep > 700) {
    lastMonsterStep = now;
    stepMonster();
    render();
  }
  requestAnimationFrame(animateMonster);
}

window.explore = function () {
  feedMind('explore artifact', 'the forest opens a secret path');
};
window.movePlayer = movePlayer;
window.startDemo = startDemo;

document.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowLeft') movePlayer(-1, 0);
  if (event.key === 'ArrowRight') movePlayer(1, 0);
  if (event.key === 'ArrowUp') movePlayer(0, -1);
  if (event.key === 'ArrowDown') movePlayer(0, 1);
  if (event.key === 'w') movePlayer(0, -1);
  if (event.key === 'a') movePlayer(-1, 0);
  if (event.key === 's') movePlayer(0, 1);
  if (event.key === 'd') movePlayer(1, 0);
});

updateStatus();
render();
animateMonster();
