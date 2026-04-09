# src/__init__.py
import torch


from .engine import CopilotEngine
from .store import KnowledgeBase
from .tools import search_kb, create_ticket

__all__ = ["CopilotEngine", "KnowledgeBase", "search_kb", "create_ticket"]

# This version string is helpful for your evaluation/demo metrics
__version__ = "0.1.0"