const Language = {
  interpret(input) {
    const text = String(input || '').toLowerCase();

    let meaning = {
      raw: input,
      concept: text,
      intent: 'observe',
      confidence: 0.7,
      action: 'watch',
      mood: 'curious'
    };

    if (text.includes('explore') || text.includes('find') || text.includes('artifact') || text.includes('forest')) {
      meaning.intent = 'discover';
      meaning.action = 'seek the hidden path';
      meaning.mood = 'adventurous';
    }

    if (text.includes('heart') || text.includes('shrine')) {
      meaning.intent = 'protect';
      meaning.action = 'guard the relic';
      meaning.mood = 'devoted';
    }

    if (text.includes('monster') || text.includes('threat') || text.includes('enemy')) {
      meaning.intent = 'defend';
      meaning.action = 'brace for the encounter';
      meaning.mood = 'alert';
    }

    if (text.includes('midi') || text.includes('note')) {
      meaning.intent = 'resonate';
      meaning.action = 'follow the tone';
      meaning.mood = 'dreamlike';
    }

    if (text.includes('remember') || text.includes('memory')) {
      meaning.intent = 'remember';
      meaning.action = 'store trace';
      meaning.mood = 'reflective';
    }

    return { meaning };
  }
};

window.Language = Language;
