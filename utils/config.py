"""
Configuration management for the Advanced Product Review Analyzer.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables once when module is imported
load_dotenv()

# Cache for configuration - loaded once and reused
_config_cache: Optional[Dict[str, Any]] = None


def get_default_config() -> Dict[str, Any]:
  """
  Get default configuration values.

  Returns:
    Dictionary containing default configuration
  """
  return {
    "openrouter": {
      "default_model": "google/gemini-flash-1.5",
      "temperature": 0.3,
      "base_url": "https://openrouter.ai/api/v1"
    },
    "prompts": {
      "directory": "prompts"
    },
    "analysis": {
      "system_message": "You are an expert in sentiment analysis. Always respond with valid JSON only."
    }
  }


def load_config(force_reload: bool = False) -> Dict[str, Any]:
  """
  Load configuration from environment variables with defaults.
  Uses caching to avoid repeated loading and duplicate messages.

  Args:
    force_reload: If True, ignore cache and reload configuration

  Returns:
    Dictionary containing merged configuration (defaults + environment)
  """
  global _config_cache

  # Return cached config if available and not forcing reload
  if _config_cache is not None and not force_reload:
    return _config_cache

  config = get_default_config()

  # Override with environment variables if present
  if api_key := os.getenv("OPENROUTER_API_KEY"):
    config["openrouter"]["api_key"] = api_key

  if model := os.getenv("OPENROUTER_MODEL"):
    config["openrouter"]["model"] = model
    print(f"Using custom model from env: {model}")
  else:
    config["openrouter"]["model"] = config["openrouter"]["default_model"]

  if temperature := os.getenv("OPENROUTER_TEMPERATURE"):
    try:
      config["openrouter"]["temperature"] = float(temperature)
      print(f"Using custom temperature from env: {temperature}")
    except ValueError:
      print(f"Invalid temperature value in env: {temperature}, using default")

  # Cache the configuration
  _config_cache = config
  return config


def get_config_value(key_path: str, default: Any = None) -> Any:
  """
  Get a specific configuration value using dot notation.
  Uses cached configuration for performance.

  Args:
    key_path: Dot-separated path to config value (e.g., "openrouter.model")
    default: Default value if key not found

  Returns:
    Configuration value or default

  Example:
    >>> get_config_value("openrouter.model")
    "google/gemini-flash-1.5"
  """
  config = load_config()
  keys = key_path.split('.')

  current = config
  for key in keys:
    if isinstance(current, dict) and key in current:
      current = current[key]
    else:
      return default

  return current


def clear_config_cache():
  """
  Clear the configuration cache.
  Useful for testing or when environment variables change.
  """
  global _config_cache
  _config_cache = None


def reload_config() -> Dict[str, Any]:
  """
  Force reload configuration from environment variables.

  Returns:
    Fresh configuration dictionary
  """
  return load_config(force_reload=True)


def print_config_summary():
  """
  Print a summary of the current configuration.
  Useful for debugging and verification.
  """
  config = load_config()
  print("📋 Configuration Summary:")
  print(f"  Model: {config['openrouter']['model']}")
  print(f"  Temperature: {config['openrouter']['temperature']}")
  print(f"  Base URL: {config['openrouter']['base_url']}")
  print(f"  API Key: {'✅ Set' if config['openrouter'].get('api_key') else '❌ Missing'}")
  print(f"  Prompts Dir: {config['prompts']['directory']}")
  print(f"  Config Status: {'🔄 Cached' if _config_cache is not None else '🆕 Fresh'}")
