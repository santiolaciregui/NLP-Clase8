# agents.py
import os
import streamlit as st
from typing import Dict, Any
from openai import OpenAI

class TokenCounter:
    """Cuenta y gestiona los tokens utilizados."""
    def __init__(self):
        self.input_tokens = 0
        self.output_tokens = 0
        self.reasoning_tokens = 0

    def add_input(self, tokens: int):
        self.input_tokens += tokens

    def add_output(self, tokens: int):
        self.output_tokens += tokens

    def add_reasoning(self, tokens: int):
        self.reasoning_tokens += tokens

    def get_stats(self) -> Dict[str, int]:
        total = self.input_tokens + self.output_tokens + self.reasoning_tokens
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "total_tokens": total
        }

    def reset(self):
        self.input_tokens = self.output_tokens = self.reasoning_tokens = 0

class Agent:
    """Abstracto: envía prompts a OpenAI y contabiliza tokens."""
    def __init__(self, name: str, counter: TokenCounter, model: str, reasoning: bool = False):
        self.name = name
        self.counter = counter
        self.model = model
        self.reasoning = reasoning

        api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            st.error("Falta la OpenAI API Key en entorno o secrets.")
            st.stop()
        self.client = OpenAI(api_key=api_key)

    def process(self, query: str, history: list = None) -> Dict[str, Any]:
        system_msg = f"Eres un agente especializado en {self.name}."
        if self.reasoning:
            system_msg += (
                "\nProporciona un análisis paso a paso.\n"
                "Presenta:\nRAZONAMIENTO: (tu lógica)\nRESPUESTA FINAL: (conclusión concisa)"
            )
        else:
            system_msg += " Proporciona un análisis detallado paso a paso."

        messages = [{"role": "system", "content": system_msg}]
        if history:
            messages += history
        messages.append({"role": "user", "content": query})

        with st.spinner(f"{self.name} procesando..."):
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )

        usage = resp.usage
        self.counter.add_input(usage.prompt_tokens)
        self.counter.add_output(usage.completion_tokens)

        content = resp.choices[0].message.content
        reasoning_text = ""
        if self.reasoning:
            parts = content.split("RESPUESTA FINAL:")
            if len(parts) == 2:
                reasoning_text = parts[0].replace("RAZONAMIENTO:", "").strip()
                content = parts[1].strip()
                est = int(len(reasoning_text.split()) * 1.3)
                self.counter.add_reasoning(est)

        return {
            "content": content,
            "reasoning": reasoning_text,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens
            }
        }
