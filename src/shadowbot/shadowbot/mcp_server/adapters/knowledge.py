"""
Knowledge Adapter

Maps ShadowBot knowledge operations to MCP tools.
"""

import logging

from ..registry import register_tool

logger = logging.getLogger(__name__)


def register_knowledge_tools() -> None:
    """Register knowledge-related MCP tools."""
    
    @register_tool("shadowbot.knowledge.add")
    def knowledge_add(
        source: str,
        source_type: str = "text",
    ) -> str:
        """Add a knowledge source (text, file, or URL)."""
        try:
            from shadowbotagents.knowledge import Knowledge
            
            knowledge = Knowledge()
            knowledge.add(source, source_type=source_type)
            return f"Knowledge added from {source_type}"
        except ImportError:
            return "Error: Knowledge module not available"
        except Exception as e:
            return f"Error: {e}"
    
    @register_tool("shadowbot.knowledge.query")
    def knowledge_query(
        query: str,
        limit: int = 5,
    ) -> str:
        """Query the knowledge base."""
        try:
            from shadowbotagents.knowledge import Knowledge
            
            knowledge = Knowledge()
            results = knowledge.query(query, limit=limit)
            return str(results)
        except ImportError:
            return "Error: Knowledge module not available"
        except Exception as e:
            return f"Error: {e}"
    
    @register_tool("shadowbot.knowledge.list")
    def knowledge_list() -> str:
        """List all knowledge sources."""
        try:
            from shadowbotagents.knowledge import Knowledge
            
            knowledge = Knowledge()
            sources = knowledge.list_sources()
            return str(sources)
        except ImportError:
            return "Error: Knowledge module not available"
        except Exception as e:
            return f"Error: {e}"
    
    @register_tool("shadowbot.knowledge.clear")
    def knowledge_clear() -> str:
        """Clear all knowledge."""
        try:
            from shadowbotagents.knowledge import Knowledge
            
            knowledge = Knowledge()
            knowledge.clear()
            return "Knowledge cleared"
        except ImportError:
            return "Error: Knowledge module not available"
        except Exception as e:
            return f"Error: {e}"
    
    @register_tool("shadowbot.knowledge.stats")
    def knowledge_stats() -> str:
        """Get knowledge base statistics."""
        try:
            from shadowbotagents.knowledge import Knowledge
            
            knowledge = Knowledge()
            stats = knowledge.stats()
            return str(stats)
        except ImportError:
            return "Error: Knowledge module not available"
        except Exception as e:
            return f"Error: {e}"
    
    logger.info("Registered knowledge MCP tools")
