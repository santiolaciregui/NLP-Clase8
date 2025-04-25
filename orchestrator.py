# orchestrator.py
import time
import json
import pandas as pd
from typing import Dict
from agents import TokenCounter, Agent

class AgentOrchestrator:
    """Coordina múltiples agentes y combina sus respuestas."""
    def __init__(self):
        self.counter = TokenCounter()
        self.agents: Dict[str, Agent] = {}
        self.coordinator: Agent = None

    def add_agent(self, agent: Agent):
        self.agents[agent.name] = agent

    def set_coordinator(self, agent: Agent):
        self.coordinator = agent

    def process_query(self, query: str) -> Dict:
        self.counter.reset()
        start = time.time()
        est_input = int(len(query.split()) * 1.3)
        self.counter.add_input(est_input)

        responses = {}
        for name, ag in self.agents.items():
            responses[name] = ag.process(query)

        final = None
        if self.coordinator:
            summary = json.dumps({n: r["content"] for n, r in responses.items()}, indent=2)
            coord_q = f"Consulta: {query}\nRespuestas: {summary}"
            final = self.coordinator.process(coord_q)
            est_out = int(len(final["content"].split()) * 1.3)
            self.counter.add_output(est_out)

        elapsed = time.time() - start
        return {
            "agents": responses,
            "final": final,
            "stats": self.counter.get_stats(),
            "time": elapsed
        }

    def create_token_chart(self):
        stats = self.counter.get_stats()
        df = pd.DataFrame({
            'Categoría': ['Entrada','Razonamiento','Salida','Total'],
            'Tokens': [
                stats['input_tokens'],
                stats['reasoning_tokens'],
                stats['output_tokens'],
                stats['total_tokens']
            ]
        })
        return df
