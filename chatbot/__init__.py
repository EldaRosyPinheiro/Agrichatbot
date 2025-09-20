# Agriculture Chatbot Module
"""
Agriculture Chatbot - A specialized AI assistant for farming and agriculture queries.

This module provides:
- AgricultureBot: Main bot response generator
- AgricultureKnowledgeBase: Knowledge management system
- Utility functions for text processing and agriculture-specific operations

Author: Agriculture AI Team
Version: 1.0.0
"""

from .response_generator import AgricultureBot
from .knowledge_base import AgricultureKnowledgeBase
from .utils import clean_text, find_best_match, is_agriculture_related

__version__ = "1.0.0"
__author__ = "Agriculture AI Team"

__all__ = [
    'AgricultureBot',
    'AgricultureKnowledgeBase',
    'clean_text',
    'find_best_match',
    'is_agriculture_related'
]
