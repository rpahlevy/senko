"""
OpenRouter client management for LLM API interactions.
"""

from typing import Optional
from openai import OpenAI
from utils.config import get_config_value, load_config


def setup_openrouter_client(api_key: Optional[str] = None) -> OpenAI:
  """
  Initialize OpenRouter client with API key from config or parameter.

  Args:
    api_key: Optional API key. If None, reads from config

  Returns:
    Configured OpenAI client pointing to OpenRouter

  Raises:
    ValueError: If no API key is provided or found in config
  """
  if api_key is None:
    api_key = get_config_value("openrouter.api_key")

  if not api_key:
    raise ValueError(
      "Please set your OPENROUTER_API_KEY in the .env file or pass it as parameter"
    )

  base_url = get_config_value("openrouter.base_url", "https://openrouter.ai/api/v1")

  client = OpenAI(
    base_url=base_url,
    api_key=api_key,
  )

  return client


def get_model_name() -> str:
  """
  Get configured model from config system.

  Returns:
    Model name to use for API calls
  """
  config = load_config()
  model = config["openrouter"]["model"]
  default_model = config["openrouter"]["default_model"]

  if not model:
    print(f"Model not set in .env, using default: {default_model}")
    return default_model

  return model
