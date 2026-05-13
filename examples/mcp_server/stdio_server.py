#!/usr/bin/env python3
"""
STDIO MCP Server Example

Run ShadowBot as an MCP server using STDIO transport.
This is the recommended transport for Claude Desktop integration.

Usage:
    python stdio_server.py

Or via CLI:
    shadowbot mcp serve --transport stdio
"""


def main():
    """Run MCP server with STDIO transport."""
    from shadowbot.mcp_server.server import MCPServer
    from shadowbot.mcp_server.adapters import register_all
    
    # Register all tools, resources, and prompts
    register_all()
    
    # Create and run server
    server = MCPServer(
        name="shadowbot",
        version="1.0.0",
        instructions="ShadowBot MCP Server - AI agent capabilities via MCP protocol.",
    )
    
    # Run with STDIO transport
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
