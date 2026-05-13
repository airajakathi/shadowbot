"""
Unit tests verifying that all modules use paths.py instead of hardcoded paths.

Tests every module fixed in Phases 2, 3, and 3.5 of the path standardization effort.
Validates both source-level absence of hardcoded strings AND runtime behavior.
"""

import inspect
import os
from pathlib import Path
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# Phase 2 Modules (SDK core)
# ---------------------------------------------------------------------------

class TestPolicyConfigWiring:
    """Verify policy/config.py routes through paths.py."""

    def test_default_rules_dir_matches_paths(self):
        from shadowbotagents.policy.config import DEFAULT_RULES_DIR
        from shadowbotagents.paths import get_rules_dir
        assert DEFAULT_RULES_DIR == str(get_rules_dir())

    def test_no_hardcoded_expanduser(self):
        from shadowbotagents.policy import config
        source = inspect.getsource(config)
        assert 'expanduser("~"), ".shadowbot", "rules"' not in source
        assert 'os.path.join(os.path.expanduser("~")' not in source


class TestAutonomyWiring:
    """Verify agent/autonomy.py routes through paths.py."""

    def test_default_snapshot_dir_matches_paths(self):
        from shadowbotagents.agent.autonomy import AutonomyConfig
        from shadowbotagents.paths import get_snapshots_dir
        config = AutonomyConfig()
        assert config.snapshot_dir == str(get_snapshots_dir())

    def test_snapshot_dir_respects_env(self):
        from shadowbotagents.paths import _clear_cache
        _clear_cache()
        with patch.dict(os.environ, {"PRAISONAI_HOME": "/custom"}):
            from shadowbotagents.agent.autonomy import AutonomyConfig
            config = AutonomyConfig()
            assert config.snapshot_dir == str(Path("/custom/snapshots"))
        _clear_cache()

    def test_no_hardcoded_expanduser(self):
        from shadowbotagents.agent import autonomy
        source = inspect.getsource(autonomy.AutonomyConfig.__post_init__)
        assert 'expanduser' not in source


class TestSchedulerStoreWiring:
    """Verify scheduler/store.py routes through paths.py."""

    def test_default_dir_matches_paths(self):
        from shadowbotagents.scheduler.store import _DEFAULT_DIR
        from shadowbotagents.paths import get_schedules_dir
        assert _DEFAULT_DIR == str(get_schedules_dir())

    def test_no_hardcoded_expanduser(self):
        from shadowbotagents.scheduler import store
        source = inspect.getsource(store)
        assert 'expanduser("~"), ".shadowbot"' not in source


class TestStorageBackendsWiring:
    """Verify storage/backends.py routes through paths.py."""

    def test_sqlite_init_uses_get_storage_path(self):
        from shadowbotagents.storage.backends import SQLiteBackend
        source = inspect.getsource(SQLiteBackend.__init__)
        assert "get_storage_path" in source
        assert '"~/.shadowbot/storage.db"' not in source


# ---------------------------------------------------------------------------
# Phase 3 Modules (project-local)
# ---------------------------------------------------------------------------

class TestSessionApiWiring:
    """Verify session/api.py routes through paths.py."""

    def test_no_hardcoded_shadowbot_sessions(self):
        from shadowbotagents.session import api
        source = inspect.getsource(api)
        assert '".shadowbot/sessions/' not in source
        assert "f'.shadowbot/sessions" not in source

    def test_has_get_session_dir_method(self):
        from shadowbotagents.session.api import Session
        assert hasattr(Session, '_get_session_dir')

    def test_get_session_dir_uses_paths(self):
        from shadowbotagents.session.api import Session
        source = inspect.getsource(Session._get_session_dir)
        assert "get_project_sessions_dir" in source


class TestKnowledgeWiring:
    """Verify knowledge/knowledge.py routes through paths.py."""

    def test_no_hardcoded_shadowbot_literal(self):
        from shadowbotagents.knowledge import knowledge
        source = inspect.getsource(knowledge)
        # Should not have hardcoded path construction with ".shadowbot"
        # But it's OK in docstrings/comments
        lines = source.split('\n')
        code_lines = [l for l in lines
                      if l.strip() and not l.strip().startswith('#')
                      and not l.strip().startswith('"""')
                      and not l.strip().startswith("'''")
                      and 'docstring' not in l.lower()]
        code_text = '\n'.join(code_lines)
        assert 'Path(".shadowbot"' not in code_text
        assert '".shadowbot"' not in code_text or 'DEFAULT_DIR_NAME' in source


class TestContextAgentWiring:
    """Verify agent/context_agent.py routes through paths.py."""

    def test_prp_dir_uses_paths(self):
        from shadowbotagents.agent import context_agent
        source = inspect.getsource(context_agent)
        assert "get_project_prp_dir" in source

    def test_no_hardcoded_prp_path(self):
        from shadowbotagents.agent import context_agent
        source = inspect.getsource(context_agent)
        assert 'Path(".shadowbot/prp")' not in source


class TestSummarizerWiring:
    """Verify rag/summarizer.py routes through paths.py."""

    def test_default_persist_path_matches_paths(self):
        from shadowbotagents.rag.summarizer import HierarchicalSummarizer
        from shadowbotagents.paths import get_project_summaries_dir
        hs = HierarchicalSummarizer()
        assert hs._persist_path == str(get_project_summaries_dir())

    def test_no_hardcoded_summaries_path(self):
        from shadowbotagents.rag import summarizer
        source = inspect.getsource(summarizer.HierarchicalSummarizer.__init__)
        assert '".shadowbot/summaries"' not in source


class TestRetrievalConfigWiring:
    """Verify rag/retrieval_config.py routes through paths.py."""

    def test_default_persist_path_matches_paths(self):
        from shadowbotagents.rag.retrieval_config import RetrievalConfig
        from shadowbotagents.paths import get_project_data_dir
        rc = RetrievalConfig()
        assert rc.persist_path == str(get_project_data_dir())

    def test_no_hardcoded_persist_path(self):
        from shadowbotagents.rag import retrieval_config
        source = inspect.getsource(retrieval_config)
        assert 'persist_path: str = ".shadowbot"' not in source


# ---------------------------------------------------------------------------
# Phase 3.5 Modules (batch fix)
# ---------------------------------------------------------------------------

class TestMemoryMemoryWiring:
    """Verify memory/memory.py routes through paths.py."""

    def test_no_hardcoded_makedirs(self):
        from shadowbotagents.memory import memory
        source = inspect.getsource(memory.Memory.__init__)
        assert 'makedirs(".shadowbot"' not in source

    def test_no_hardcoded_short_db(self):
        from shadowbotagents.memory import memory
        source = inspect.getsource(memory.Memory.__init__)
        assert '".shadowbot/short_term.db"' not in source

    def test_no_hardcoded_long_db(self):
        from shadowbotagents.memory import memory
        source = inspect.getsource(memory.Memory.__init__)
        assert '".shadowbot/long_term.db"' not in source




class TestMemoryHooksWiring:
    """Verify memory/hooks.py routes through paths.py."""

    def test_config_file_uses_default_dir_name(self):
        from shadowbotagents.memory import hooks
        source = inspect.getsource(hooks)
        # Should use DEFAULT_DIR_NAME for CONFIG_FILE
        assert "DEFAULT_DIR_NAME" in source or "_DIR_NAME" in source

    def test_no_hardcoded_config_file(self):
        from shadowbotagents.memory import hooks
        # Check the HooksManager class body for hardcoded CONFIG_FILE
        source = inspect.getsource(hooks.HooksManager)
        assert 'CONFIG_FILE = ".shadowbot/hooks.json"' not in source

    def test_workspace_dir_uses_default_dir_name(self):
        from shadowbotagents.memory import hooks
        source = inspect.getsource(hooks.HooksManager.__init__)
        assert 'workspace_path / ".shadowbot"' not in source


class TestDocsManagerWiring:
    """Verify memory/docs_manager.py routes through paths.py."""

    def test_no_hardcoded_docs_dir_name(self):
        from shadowbotagents.memory import docs_manager
        source = inspect.getsource(docs_manager.DocsManager)
        assert 'DOCS_DIR_NAME = ".shadowbot/docs"' not in source

    def test_global_docs_path_uses_get_docs_dir(self):
        from shadowbotagents.memory import docs_manager
        source = inspect.getsource(docs_manager.DocsManager.__init__)
        assert "get_docs_dir" in source

    def test_no_hardcoded_home_shadowbot_docs(self):
        from shadowbotagents.memory import docs_manager
        source = inspect.getsource(docs_manager.DocsManager.__init__)
        assert 'Path.home() / ".shadowbot" / "docs"' not in source


class TestRulesManagerWiring:
    """Verify memory/rules_manager.py routes through paths.py."""

    def test_no_hardcoded_rules_dir_name(self):
        from shadowbotagents.memory import rules_manager
        source = inspect.getsource(rules_manager.RulesManager)
        assert 'RULES_DIR_NAME = ".shadowbot/rules"' not in source

    def test_global_rules_path_uses_get_rules_dir(self):
        from shadowbotagents.memory import rules_manager
        source = inspect.getsource(rules_manager.RulesManager.__init__)
        assert "get_rules_dir" in source

    def test_no_hardcoded_home_shadowbot_rules(self):
        from shadowbotagents.memory import rules_manager
        source = inspect.getsource(rules_manager.RulesManager.__init__)
        assert 'Path.home() / ".shadowbot" / "rules"' not in source


class TestMcpConfigWiring:
    """Verify memory/mcp_config.py routes through paths.py."""

    def test_no_hardcoded_mcp_dir_name(self):
        from shadowbotagents.memory import mcp_config
        source = inspect.getsource(mcp_config.MCPConfigManager)
        assert 'MCP_DIR_NAME = ".shadowbot/mcp"' not in source

    def test_global_mcp_path_uses_get_mcp_dir(self):
        from shadowbotagents.memory import mcp_config
        source = inspect.getsource(mcp_config.MCPConfigManager.__init__)
        assert "get_mcp_dir" in source

    def test_no_hardcoded_home_shadowbot_mcp(self):
        from shadowbotagents.memory import mcp_config
        source = inspect.getsource(mcp_config.MCPConfigManager.__init__)
        assert 'Path.home() / ".shadowbot" / "mcp"' not in source


class TestFileMemoryWiring:
    """Verify memory/file_memory.py routes through paths.py."""

    def test_no_hardcoded_base_path(self):
        from shadowbotagents.memory import file_memory
        source = inspect.getsource(file_memory.FileMemory.__init__)
        assert 'Path(".shadowbot/memory")' not in source

    def test_uses_get_project_data_dir(self):
        from shadowbotagents.memory import file_memory
        source = inspect.getsource(file_memory.FileMemory.__init__)
        assert "get_project_data_dir" in source


class TestMemoryWorkflowsWiring:
    """Verify memory/workflows.py routes through paths.py."""

    def test_no_hardcoded_workflows_dir(self):
        from shadowbotagents.memory import workflows
        source = inspect.getsource(workflows.WorkflowManager)
        assert 'WORKFLOWS_DIR = ".shadowbot/workflows"' not in source

    def test_uses_default_dir_name(self):
        from shadowbotagents.memory import workflows
        source = inspect.getsource(workflows.WorkflowManager)
        assert "DEFAULT_DIR_NAME" in source or "_DIR_NAME" in source

    def test_no_hardcoded_checkpoints_dir(self):
        from shadowbotagents.memory import workflows
        source = inspect.getsource(workflows.WorkflowManager._get_checkpoints_dir)
        assert '".shadowbot"' not in source


class TestWorkflowsWorkflowsWiring:
    """Verify workflows/workflows.py routes through paths.py."""

    def test_no_hardcoded_workflows_dir(self):
        from shadowbotagents.workflows import workflows
        source = inspect.getsource(workflows.WorkflowManager)
        assert 'WORKFLOWS_DIR = ".shadowbot/workflows"' not in source

    def test_uses_default_dir_name(self):
        from shadowbotagents.workflows import workflows
        source = inspect.getsource(workflows.WorkflowManager)
        assert "DEFAULT_DIR_NAME" in source or "_DIR_NAME" in source

    def test_no_hardcoded_checkpoints_dir(self):
        from shadowbotagents.workflows import workflows
        source = inspect.getsource(workflows.WorkflowManager._get_checkpoints_dir)
        assert '".shadowbot"' not in source


class TestConfigLoaderWiring:
    """Verify config/loader.py routes through paths.py."""

    def test_no_hardcoded_plugin_dirs(self):
        from shadowbotagents.config import loader
        source = inspect.getsource(loader)
        assert '"./.shadowbot/plugins/"' not in source
        assert '"~/.shadowbot/plugins/"' not in source

    def test_config_search_uses_paths(self):
        from shadowbotagents.config import loader
        source = inspect.getsource(loader._find_config_file)
        assert "get_project_data_dir" in source or "get_data_dir" in source

    def test_global_config_path_uses_get_data_dir(self):
        from shadowbotagents.config import loader
        source = inspect.getsource(loader._find_config_file)
        assert "get_data_dir" in source


class TestAgentsAgentsWiring:
    """Verify agents/agents.py routes through paths.py."""

    def test_no_hardcoded_memory_db(self):
        from shadowbotagents.agents import agents
        source = inspect.getsource(agents)
        assert '"./.shadowbot/memory.db"' not in source

    def test_no_hardcoded_chroma_db(self):
        from shadowbotagents.agents import agents
        source = inspect.getsource(agents)
        assert '"./.shadowbot/chroma_db"' not in source

    def test_uses_get_project_data_dir(self):
        from shadowbotagents.agents import agents
        source = inspect.getsource(agents)
        assert "get_project_data_dir" in source


class TestLegacySessionWiring:
    """Verify session.py (legacy) routes through paths.py."""

    def test_has_get_session_dir_method(self):
        from shadowbotagents.session import Session
        assert hasattr(Session, '_get_session_dir')

    def test_get_session_dir_uses_paths(self):
        from shadowbotagents.session import Session
        source = inspect.getsource(Session._get_session_dir)
        assert "get_project_sessions_dir" in source

    def test_no_hardcoded_session_path(self):
        from shadowbotagents import session
        source = inspect.getsource(session.Session.__init__)
        assert 'f".shadowbot/sessions/' not in source
        assert "makedirs(f\".shadowbot" not in source


# ---------------------------------------------------------------------------
# Cross-cutting: comprehensive hardcoded path scan
# ---------------------------------------------------------------------------

class TestNoHardcodedPathsComprehensive:
    """
    Scan all fixed modules' source code for any remaining hardcoded
    .shadowbot path construction patterns.
    """

    FIXED_MODULES = [
        "shadowbotagents.policy.config",
        "shadowbotagents.agent.autonomy",
        "shadowbotagents.scheduler.store",
        "shadowbotagents.storage.backends",
        "shadowbotagents.session.api",
        "shadowbotagents.knowledge.knowledge",
        "shadowbotagents.agent.context_agent",
        "shadowbotagents.rag.summarizer",
        "shadowbotagents.rag.retrieval_config",
        "shadowbotagents.memory.memory",
        "shadowbotagents.memory.hooks",
        "shadowbotagents.memory.docs_manager",
        "shadowbotagents.memory.rules_manager",
        "shadowbotagents.memory.mcp_config",
        "shadowbotagents.memory.file_memory",
        "shadowbotagents.memory.workflows",
        "shadowbotagents.workflows.workflows",
        "shadowbotagents.config.loader",
        "shadowbotagents.agents.agents",
        "shadowbotagents.session",
    ]

    # Patterns that indicate hardcoded path construction (not just docs/comments)
    FORBIDDEN_PATTERNS = [
        'Path(".shadowbot"',
        'Path(".shadowbot/',
        'os.makedirs(".shadowbot"',
        "os.makedirs('.shadowbot'",
        '"./.shadowbot/',
        "'./.shadowbot/",
        '= ".shadowbot/',
        "= '.shadowbot/",
    ]

    @pytest.mark.parametrize("module_name", FIXED_MODULES)
    def test_no_forbidden_patterns_in_code(self, module_name):
        """Each fixed module should not contain forbidden path patterns in code."""
        import importlib
        mod = importlib.import_module(module_name)
        source = inspect.getsource(mod)

        # Extract only code lines (skip docstrings and comments)
        in_docstring = False
        code_lines = []
        for line in source.split('\n'):
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_docstring = not in_docstring
                continue
            if in_docstring:
                continue
            if stripped.startswith('#'):
                continue
            code_lines.append(line)

        code_text = '\n'.join(code_lines)

        for pattern in self.FORBIDDEN_PATTERNS:
            assert pattern not in code_text, (
                f"Module {module_name} still contains forbidden pattern: {pattern!r}"
            )
