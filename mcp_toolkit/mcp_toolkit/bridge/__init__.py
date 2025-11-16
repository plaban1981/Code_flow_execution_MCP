"""
Bridge Module

Integration layers for MCP with various frameworks
"""
from .langchain import (
    register_langchain_tools_sync,
    register_langchain_tools_async,
    quick_test_registration
)

__all__ = [
    'register_langchain_tools_sync',
    'register_langchain_tools_async',
    'quick_test_registration',
]
