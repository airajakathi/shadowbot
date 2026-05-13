#!/bin/bash
# MCP CLI Tools Examples
#
# Demonstrates the new CLI commands for MCP tool management:
# - shadowbot mcp tools search
# - shadowbot mcp tools info
# - shadowbot mcp tools schema
# - shadowbot mcp list-tools (with pagination)
#
# Usage:
#   chmod +x cli_tools_example.sh
#   ./cli_tools_example.sh

echo "========================================"
echo "MCP CLI Tools Examples"
echo "MCP Protocol Version: 2025-11-25"
echo "========================================"

echo ""
echo "--- List Tools (with pagination) ---"
echo "Command: shadowbot mcp list-tools --limit 5"
shadowbot mcp list-tools --limit 5

echo ""
echo "--- List Tools (JSON output) ---"
echo "Command: shadowbot mcp list-tools --json --limit 3"
shadowbot mcp list-tools --json --limit 3

echo ""
echo "--- Tools Help ---"
echo "Command: shadowbot mcp tools --help"
shadowbot mcp tools --help

echo ""
echo "--- Search Tools ---"
echo "Command: shadowbot mcp tools search 'workflow'"
shadowbot mcp tools search "workflow"

echo ""
echo "--- Search Read-Only Tools ---"
echo "Command: shadowbot mcp tools search --read-only"
shadowbot mcp tools search --read-only

echo ""
echo "--- Search with JSON Output ---"
echo "Command: shadowbot mcp tools search 'memory' --json"
shadowbot mcp tools search "memory" --json

echo ""
echo "========================================"
echo "Examples completed!"
echo "========================================"
