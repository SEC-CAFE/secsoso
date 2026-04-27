#!/usr/bin/env python
# encoding: utf-8

from typing import Dict

from openai import OpenAI

from src.conf.config import get_app_settings


class LLM:
    def __init__(self) -> None:
        self.settings = get_app_settings()

    def _resolve_params(self) -> Dict[str, str]:
        provider = (self.settings.llm_provider or "").strip().lower()
        base_url = (self.settings.llm_base_url or "").strip()
        api_key = (self.settings.llm_api_key or "").strip()

        # Keep compatibility with existing ollama deployment style:
        # when provider is ollama and LLM_* is not set, derive OpenAI-compatible endpoint
        # from OLLAMA_URL + optional PROXY_AUTH.
        if provider == "ollama" and not base_url:
            auth = (self.settings.proxy_auth or "").strip()
            endpoint = (self.settings.ollama_url or "").strip()
            if endpoint:
                if auth:
                    base_url = f"http://{auth}@{endpoint}/v1"
                else:
                    base_url = f"http://{endpoint}/v1"
            if not api_key:
                api_key = "ollama"

        if not api_key:
            api_key = "EMPTY_API_KEY"

        params: Dict[str, str] = {"api_key": api_key}
        if base_url:
            params["base_url"] = base_url
        return params

    def _call_llm(self, system: str, content: str, stream: bool = True):
        client = OpenAI(**self._resolve_params())
        return client.chat.completions.create(
            model=self.settings.llm_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": content},
            ],
            stream=stream,
        )

    def chat(self, system: str, content: str, stream: bool = False):
        return self._call_llm(system=system, content=content, stream=stream)

    def chat_stream(self, system: str, content: str):
        return self.chat(system=system, content=content, stream=True)
