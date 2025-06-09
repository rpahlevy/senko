"""
Prompt template loading and management utilities.
"""

import os
from typing import Dict, Any


def load_prompt(prompt_name: str, prompts_dir: str = "prompts") -> str:
  """
  Load prompt template from file.

  Args:
    prompt_name: Name of the prompt file (without .txt extension)
    prompts_dir: Directory containing prompt files

  Returns:
    Prompt template content as string

  Raises:
    FileNotFoundError: If prompt file doesn't exist
  """
  prompt_path = os.path.join(prompts_dir, f"{prompt_name}.txt")

  try:
    with open(prompt_path, 'r', encoding='utf-8') as f:
      return f.read().strip()
  except FileNotFoundError:
    raise FileNotFoundError(f"Prompt file not found: {prompt_path}")


def format_prompt(template: str, **kwargs: Any) -> str:
  """
  Format prompt template with provided variables.

  Args:
    template: Prompt template string
    **kwargs: Variables to substitute in template

  Returns:
    Formatted prompt string

  Raises:
    KeyError: If required template variables are missing
  """
  try:
    return template.format(**kwargs)
  except KeyError as e:
    raise KeyError(f"Missing required template variable: {e}")


def load_and_format_prompt(prompt_name: str, **kwargs: Any) -> str:
  """
  Convenience function to load and format prompt in one call.

  Args:
    prompt_name: Name of the prompt file (without .txt extension)
    **kwargs: Variables to substitute in template

  Returns:
    Formatted prompt string
  """
  template = load_prompt(prompt_name)
  return format_prompt(template, **kwargs)
