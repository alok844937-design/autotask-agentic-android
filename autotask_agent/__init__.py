"""
AutoTask Agentic Android
Natural language Android automation powered by Claude AI
"""

__version__ = "1.0.0"
__author__ = "Solo Developer"

from .agent import AutoTaskAgent
from .planner import TaskPlanner
from .actions import AndroidActions
from .memory import AgentMemory

__all__ = [
    'AutoTaskAgent',
    'TaskPlanner', 
    'AndroidActions',
    'AgentMemory'
]