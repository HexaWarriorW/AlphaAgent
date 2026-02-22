from __future__ import annotations

from pathlib import Path

from alphaagent.core.conf import ExtendedBaseSettings


class LLMSettings(ExtendedBaseSettings):
    log_llm_chat_content: bool = True
    max_retry: int = 10
    retry_wait_seconds: int = 1
    dump_chat_cache: bool = False
    use_chat_cache: bool = False
    dump_embedding_cache: bool = False
    use_embedding_cache: bool = False
    prompt_cache_path: str = str(Path.cwd() / "prompt_cache.db")
    max_past_message_include: int = 10

    # Behavior of returning answers to the same question when caching is enabled
    use_auto_chat_cache_seed_gen: bool = False
    """
    `_create_chat_completion_inner_function` provdies a feature to pass in a seed to affect the cache hash key
    We want to enable a auto seed generator to get different default seed for `_create_chat_completion_inner_function`
    if seed is not given.
    So the cache will only not miss you ask the same question on same round.
    """
    init_chat_cache_seed: int = 42

    # Chat configs
    openai_api_key: str = ""  # TODO: simplify the key design.
    openai_base_url: str = ""
    chat_openai_api_key: str = ""
    chat_model: str = "gpt-4-turbo"
    reasoning_model: str = ""
    chat_max_tokens: int = 3000
    chat_temperature: float = 0.5
    chat_stream: bool = True
    chat_seed: int | None = None
    chat_frequency_penalty: float = 0.0
    chat_presence_penalty: float = 0.0
    chat_token_limit: int = (
        100000  # 100000 is the maximum limit of gpt4, which might increase in the future version of gpt
    )
    default_system_prompt: str = "You are an AI assistant who helps to answer user's questions."
    factor_mining_timeout: int = 36000 # 10小时，单位：秒

    # Embedding configs
    embedding_openai_api_key: str = ""
    embedding_model: str = ""
    embedding_max_str_num: int = 50
    embedding_api_key: str = ""
    embedding_base_url: str = ""

    # server served endpoints
    chat_model_map: str = "{}"


LLM_SETTINGS = LLMSettings()
