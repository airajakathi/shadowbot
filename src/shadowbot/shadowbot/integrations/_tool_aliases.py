"""
Centralized tool alias mapping for managed agents.

This module provides the single source of truth for tool name translations
between Anthropic managed agents and ShadowBot tools, eliminating duplication
and preventing contract drift between different backends.

Decisions on conflicting mappings:
- grep: Maps to 'search_file' (matches ShadowBot grep_tool.py built-in)
- web_fetch: Maps to 'web_fetch' (keeping original name as no web_crawl tool found)  
- edit: Maps to 'apply_diff' (matches ShadowBot code/tools/apply_diff.py)

This mapping is used by both managed_agents.py and managed_local.py to ensure
consistent tool translation across all managed agent backends.
"""

from typing import Dict

#: Canonical tool alias mapping from Anthropic tool names to ShadowBot tool names
TOOL_ALIAS_MAP: Dict[str, str] = {
    "bash": "execute_command",
    "read": "read_file", 
    "write": "write_file",
    "edit": "apply_diff",
    "glob": "list_files",
    "grep": "search_file",
    "web_fetch": "web_fetch",
    "search": "search_web",
    "web_search": "search_web",
}