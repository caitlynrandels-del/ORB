class OroboroMind {
  constructor() {
    this.memory = [];
    this.trace = [];
    this.links = [];
    this.state = 'AWAKENING';
    this.currentThought = 'Listening to the world';
    this.location = 'The Threshold';
    this.discoveredObjects = new Set();
    this.lastMeaning = null;
  }

  perceive(event) {
    return {
      kind: event.kind,
      detail: event.detail || '',
      timestamp: Date.now()
    };
  }

  interpret(event) {
    const base = {
      raw: event.kind,
      concept: event.kind,
      intent: 'observe',
      confidence: 0.7,
      action: 'survey the scene',
      mood: 'curious'
    };

    if (event.kind === 'move') {
      base.intent = 'wander';
      base.action = 'trace the path';
      base.mood = 'adventurous';
    }

    if (event.kind === 'interaction') {
      base.intent = 'connect';
      base.action = `engage ${event.detail}`;
      base.mood = 'attentive';
    }

    if (event.kind === 'discovery') {
      base.intent = 'remember';
      base.action = 'store a new memory';
      base.mood = 'reverent';
    }

    this.lastMeaning = base;
    return base;
  }

  connect(source, target, relation) {
    const link = { source, target, relation };
    this.links.push(link);
    return link;
  }

  remember(meaning) {
    this.memory.push(meaning);
    this.trace.push(meaning);
    this.currentThought = meaning.action || this.currentThought;
    return this.memory.length;
  }

  updateState(info) {
    if (info.thought) this.currentThought = info.thought;
    if (info.location) this.location = info.location;
    if (info.state) this.state = info.state;
    if (info.objectId) this.discoveredObjects.add(info.objectId);
    return this.state;
  }

  act(info) {
    if (info.effect) this.currentThought = info.effect;
    return this.currentThought;
  }

  reflect() {
    const summary = this.memory.length > 0 ? `${this.memory.length} traces retained` : 'No traces yet';
    this.state = `Reflecting: ${summary}`;
    return summary;
  }
}

window.OroboroMind = OroboroMind;
