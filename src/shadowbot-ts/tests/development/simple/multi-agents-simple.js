const { Agent, ShadowBotAgents } = require('shadowbot');

const researchAgent = new Agent({ instructions: 'Research about AI' });
const summariseAgent = new Agent({ instructions: 'Summarise research agent\'s findings' });

const agents = new ShadowBotAgents({ agents: [researchAgent, summariseAgent] });
agents.start();
