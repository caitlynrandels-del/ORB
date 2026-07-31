class OroboroMind {
  constructor() {
    this.nodes = [];
    this.memory = [];
    this.state = 'AWAKENING';
    this.lastMeaning = null;
    this.trace = [];
  }

  addNode(name) {
    this.nodes.push({ name, resolved: false });
  }

  think(input) {
    const meaning = typeof input === 'string' ? { raw: input } : input;
    this.lastMeaning = meaning;
    this.memory.push(meaning);
    this.trace.push(meaning);

    if (typeof meaning === 'object' && meaning.intent) {
      this.state = `PROCESSING: ${meaning.intent}`;
    } else {
      this.state = `PROCESSING: ${String(input)}`;
    }

    return this.state;
  }

  remember(meaning) {
    this.memory.push(meaning);
    this.trace.push(meaning);
    this.state = `MEMORY: ${meaning.intent || 'stored'}`;
    return this.state;
  }

  observe(label, detail) {
    const meaning = {
      raw: label,
      concept: label,
      intent: 'observe',
      action: detail || 'survey the scene',
      mood: 'curious'
    };
    this.think(meaning);
    return this.state;
  }

  allKnown() {
    return this.nodes.length > 0 && this.nodes.every(n => n.resolved);
  }

  resolveAll() {
    this.nodes.forEach(n => { n.resolved = true; });
    this.state = 'ALL_KNOWN';
  }
}

const Mind = new OroboroMind();
Mind.addNode('Player');
Mind.addNode('World');
Mind.addNode('Artifact');
window.OroboroMind = Mind;