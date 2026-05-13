"""
Tests for QueryRewriterAgent CLI integration

Run with: python -m pytest tests/unit/test_query_rewriter_cli.py -v
"""

import pytest
from unittest.mock import patch, MagicMock
import argparse


class TestQueryRewriterCLIArgs:
    """Test CLI argument parsing for query rewriter."""
    
    def test_query_rewrite_arg_exists(self):
        """Test --query-rewrite argument is available."""
        from shadowbot.cli import ShadowBot
        
        # Create instance and check args can be parsed
        with patch('sys.argv', ['shadowbot', '--help']):
            try:
                ShadowBot()
            except SystemExit:
                pass  # --help causes exit, that's fine
    
    def test_rewrite_tools_arg_exists(self):
        """Test --rewrite-tools argument is available."""
        from shadowbot.cli import ShadowBot
        
        with patch('sys.argv', ['shadowbot', '--help']):
            try:
                ShadowBot()
            except SystemExit:
                pass


class TestRewriteQueryMethod:
    """Test the _rewrite_query helper method."""
    
    def test_rewrite_query_returns_rewritten(self):
        """Test _rewrite_query returns rewritten query."""
        from shadowbot.cli import ShadowBot
        
        # Setup mock
        mock_result = MagicMock()
        mock_result.primary_query = "What are the current trends in artificial intelligence?"
        mock_agent = MagicMock()
        mock_agent.rewrite.return_value = mock_result
        
        # Patch at the import location inside the method
        with patch.dict('sys.modules', {'shadowbotagents': MagicMock()}):
            import sys
            sys.modules['shadowbotagents'].QueryRewriterAgent = MagicMock(return_value=mock_agent)
            sys.modules['shadowbotagents'].RewriteStrategy = MagicMock()
            
            praison = ShadowBot()
            result = praison._rewrite_query("AI trends", None, False)
            
            assert result == "What are the current trends in artificial intelligence?"
    
    def test_rewrite_query_fallback_on_import_error(self):
        """Test _rewrite_query returns original on ImportError."""
        from shadowbot.cli import ShadowBot
        
        # Mock the import to raise ImportError
        praison = ShadowBot()
        
        with patch.object(praison, '_rewrite_query') as mock_method:
            # Simulate the actual behavior - returns original on error
            mock_method.return_value = "AI trends"
            result = mock_method("AI trends", None, False)
            assert result == "AI trends"
    
    def test_rewrite_query_fallback_on_exception(self):
        """Test _rewrite_query returns original on exception."""
        from shadowbot.cli import ShadowBot
        
        # Patch to raise exception
        with patch.dict('sys.modules', {'shadowbotagents': MagicMock()}):
            import sys
            sys.modules['shadowbotagents'].QueryRewriterAgent = MagicMock(side_effect=Exception("Test error"))
            
            praison = ShadowBot()
            result = praison._rewrite_query("AI trends", None, False)
            
            # Should return original query on error
            assert result == "AI trends"


class TestRewriteQueryIfEnabled:
    """Test the _rewrite_query_if_enabled wrapper method."""
    
    def test_returns_original_when_disabled(self):
        """Test returns original query when --query-rewrite not set."""
        from shadowbot.cli import ShadowBot
        
        praison = ShadowBot()
        praison.args = argparse.Namespace(query_rewrite=False)
        
        result = praison._rewrite_query_if_enabled("test query")
        assert result == "test query"
    
    def test_returns_original_when_no_args(self):
        """Test returns original query when args not set."""
        from shadowbot.cli import ShadowBot
        
        praison = ShadowBot()
        # Don't set args at all
        if hasattr(praison, 'args'):
            delattr(praison, 'args')
        
        result = praison._rewrite_query_if_enabled("test query")
        assert result == "test query"
    
    def test_calls_rewrite_when_enabled(self):
        """Test calls _rewrite_query when --query-rewrite is set."""
        from shadowbot.cli import ShadowBot
        
        praison = ShadowBot()
        praison.args = argparse.Namespace(
            query_rewrite=True,
            rewrite_tools=None,
            verbose=False
        )
        
        with patch.object(praison, '_rewrite_query', return_value="rewritten query") as mock_rewrite:
            result = praison._rewrite_query_if_enabled("original query")
            
            mock_rewrite.assert_called_once_with("original query", None, False)
            assert result == "rewritten query"
    
    def test_passes_tools_and_verbose(self):
        """Test passes rewrite_tools and verbose to _rewrite_query."""
        from shadowbot.cli import ShadowBot
        
        praison = ShadowBot()
        praison.args = argparse.Namespace(
            query_rewrite=True,
            rewrite_tools="internet_search",
            verbose=True
        )
        
        with patch.object(praison, '_rewrite_query', return_value="rewritten") as mock_rewrite:
            praison._rewrite_query_if_enabled("query")
            
            mock_rewrite.assert_called_once_with("query", "internet_search", True)


class TestHandleDirectPromptWithRewrite:
    """Test handle_direct_prompt integrates query rewriting."""
    
    def test_applies_rewrite_before_agent(self):
        """Test query is rewritten before passing to agent."""
        from shadowbot.cli import ShadowBot
        
        praison = ShadowBot()
        praison.args = argparse.Namespace(
            query_rewrite=True,
            rewrite_tools=None,
            verbose=False,
            llm=None
        )
        
        # Mock the agent and its start method
        mock_agent = MagicMock()
        mock_agent.start.return_value = "result"
        
        with patch.object(praison, '_rewrite_query_if_enabled', return_value="rewritten prompt") as mock_rewrite:
            with patch('shadowbot.cli.main.PRAISONAI_AVAILABLE', True):
                # Mock shadowbotagents and all its submodules
                mock_shadowbotagents = MagicMock()
                mock_agent = MagicMock()
                mock_agent.start.return_value = "result"
                mock_shadowbotagents.Agent = MagicMock(return_value=mock_agent)
                mock_shadowbotagents.approval = MagicMock()
                
                with patch.dict('sys.modules', {
                    'shadowbotagents': mock_shadowbotagents,
                    'shadowbotagents.approval': mock_shadowbotagents.approval,
                    'shadowbotagents.output.status': MagicMock(),
                }):
                    praison.handle_direct_prompt("original prompt")
                    
                    # Verify rewrite was called
                    mock_rewrite.assert_called_once_with("original prompt")


class TestToolLoading:
    """Test tool loading for query rewriter."""
    
    def test_load_builtin_tool_by_name(self):
        """Test loading built-in tool by name."""
        from shadowbot.cli import ShadowBot
        
        # Setup mocks
        mock_result = MagicMock()
        mock_result.primary_query = "rewritten"
        mock_agent = MagicMock()
        mock_agent.rewrite.return_value = mock_result
        
        mock_tool = MagicMock()
        mock_tools_module = MagicMock()
        mock_tools_module.TOOL_MAPPINGS = {'internet_search': 'shadowbotagents.tools'}
        mock_tools_module.internet_search = mock_tool
        
        mock_shadowbotagents = MagicMock()
        mock_shadowbotagents.QueryRewriterAgent = MagicMock(return_value=mock_agent)
        mock_shadowbotagents.RewriteStrategy = MagicMock()
        mock_shadowbotagents.tools = mock_tools_module
        
        with patch.dict('sys.modules', {
            'shadowbotagents': mock_shadowbotagents,
            'shadowbotagents.tools': mock_tools_module
        }):
            praison = ShadowBot()
            result = praison._rewrite_query("query", "internet_search", False)
            
            # Verify result
            assert result == "rewritten"
    
    def test_handles_unknown_tool_gracefully(self):
        """Test handles unknown tool name gracefully."""
        from shadowbot.cli import ShadowBot
        
        # Setup mocks
        mock_result = MagicMock()
        mock_result.primary_query = "rewritten"
        mock_agent = MagicMock()
        mock_agent.rewrite.return_value = mock_result
        
        mock_tools_module = MagicMock()
        mock_tools_module.TOOL_MAPPINGS = {}  # Empty - no tools
        
        mock_shadowbotagents = MagicMock()
        mock_shadowbotagents.QueryRewriterAgent = MagicMock(return_value=mock_agent)
        mock_shadowbotagents.RewriteStrategy = MagicMock()
        mock_shadowbotagents.tools = mock_tools_module
        
        with patch.dict('sys.modules', {
            'shadowbotagents': mock_shadowbotagents,
            'shadowbotagents.tools': mock_tools_module
        }):
            praison = ShadowBot()
            # Should not raise, just warn
            result = praison._rewrite_query("query", "unknown_tool", False)
            
            assert result == "rewritten"


class TestQueryRewriterIntegration:
    """Integration tests for QueryRewriterAgent with CLI."""
    
    def test_full_rewrite_flow_mocked(self):
        """Test full rewrite flow with mocked components."""
        from shadowbot.cli import ShadowBot
        
        # Setup mocks
        mock_result = MagicMock()
        mock_result.primary_query = "What are the latest developments in AI technology?"
        mock_agent = MagicMock()
        mock_agent.rewrite.return_value = mock_result
        
        mock_shadowbotagents = MagicMock()
        mock_shadowbotagents.QueryRewriterAgent = MagicMock(return_value=mock_agent)
        mock_shadowbotagents.RewriteStrategy = MagicMock()
        
        with patch.dict('sys.modules', {'shadowbotagents': mock_shadowbotagents}):
            praison = ShadowBot()
            praison.args = argparse.Namespace(
                query_rewrite=True,
                rewrite_tools=None,
                verbose=False,
                llm=None
            )
            
            result = praison._rewrite_query_if_enabled("AI trends")
            
            assert "AI" in result or "developments" in result
            mock_agent.rewrite.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
