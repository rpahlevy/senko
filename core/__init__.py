"""
Core utilities for the Advanced Product Review Analyzer.

This package contains the fundamental components for OpenRouter integration
and prompt management.
"""

from .client import setup_openrouter_client
from .prompt_loader import load_prompt

__all__ = [
  "setup_openrouter_client",
  "load_prompt"
]
