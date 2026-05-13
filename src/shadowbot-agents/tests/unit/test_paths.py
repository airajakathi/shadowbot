"""
Unit tests for shadowbotagents.paths module.

Tests centralized path utilities for ShadowBot data storage.
TDD: These tests define the expected behavior of the paths module.
"""

import os
import warnings
from pathlib import Path
from unittest.mock import patch


class TestGetDataDir:
    """Tests for get_data_dir() function."""
    
    def test_default_returns_shadowbot_in_home(self):
        """Default data dir should be ~/.shadowbot/"""
        from shadowbotagents.paths import get_data_dir
        
        result = get_data_dir()
        expected = Path.home() / ".shadowbot"
        assert result == expected
    
    def test_env_var_override(self):
        """PRAISONAI_HOME env var should override default."""
        from shadowbotagents.paths import get_data_dir
        
        with patch.dict(os.environ, {"PRAISONAI_HOME": "/custom/path"}):
            result = get_data_dir()
            assert result == Path("/custom/path")
    
    def test_env_var_expands_tilde(self):
        """PRAISONAI_HOME should expand ~ to home directory."""
        from shadowbotagents.paths import get_data_dir
        
        with patch.dict(os.environ, {"PRAISONAI_HOME": "~/custom/praison"}):
            result = get_data_dir()
            assert result == Path.home() / "custom" / "praison"
    
    def test_legacy_fallback_with_warning(self, tmp_path):
        """Should fall back to ~/.praison/ if it exists and ~/.shadowbot/ doesn't."""
        from shadowbotagents.paths import get_data_dir, _clear_cache
        
        # Clear cache before test
        _clear_cache()
        
        # Create mock home with only legacy dir
        mock_home = tmp_path / "home"
        legacy_dir = mock_home / ".praison"
        legacy_dir.mkdir(parents=True)
        
        with patch("shadowbotagents.paths.Path.home", return_value=mock_home):
            with patch.dict(os.environ, {}, clear=True):
                # Remove PRAISONAI_HOME if set
                os.environ.pop("PRAISONAI_HOME", None)
                
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    result = get_data_dir()
                    
                    # Should return legacy path
                    assert result == legacy_dir
                    
                    # Should emit deprecation warning
                    assert len(w) == 1
                    assert issubclass(w[0].category, DeprecationWarning)
                    assert ".praison" in str(w[0].message)
        
        # Clear cache after test
        _clear_cache()


class TestGetSessionsDir:
    """Tests for get_sessions_dir() function."""
    
    def test_returns_sessions_subdir(self):
        """Should return sessions subdirectory of data dir."""
        from shadowbotagents.paths import get_sessions_dir
        
        result = get_sessions_dir()
        assert result == Path.home() / ".shadowbot" / "sessions"
    
    def test_respects_env_override(self):
        """Should respect PRAISONAI_HOME override."""
        from shadowbotagents.paths import get_sessions_dir
        
        with patch.dict(os.environ, {"PRAISONAI_HOME": "/custom"}):
            result = get_sessions_dir()
            assert result == Path("/custom/sessions")


class TestGetSkillsDir:
    """Tests for get_skills_dir() function."""
    
    def test_returns_skills_subdir(self):
        """Should return skills subdirectory of data dir."""
        from shadowbotagents.paths import get_skills_dir
        
        result = get_skills_dir()
        assert result == Path.home() / ".shadowbot" / "skills"


class TestGetPluginsDir:
    """Tests for get_plugins_dir() function."""
    
    def test_returns_plugins_subdir(self):
        """Should return plugins subdirectory of data dir."""
        from shadowbotagents.paths import get_plugins_dir
        
        result = get_plugins_dir()
        assert result == Path.home() / ".shadowbot" / "plugins"


class TestGetMcpDir:
    """Tests for get_mcp_dir() function."""
    
    def test_returns_mcp_subdir(self):
        """Should return mcp subdirectory of data dir."""
        from shadowbotagents.paths import get_mcp_dir
        
        result = get_mcp_dir()
        assert result == Path.home() / ".shadowbot" / "mcp"


class TestGetDocsDir:
    """Tests for get_docs_dir() function."""
    
    def test_returns_docs_subdir(self):
        """Should return docs subdirectory of data dir."""
        from shadowbotagents.paths import get_docs_dir
        
        result = get_docs_dir()
        assert result == Path.home() / ".shadowbot" / "docs"


class TestGetRulesDir:
    """Tests for get_rules_dir() function."""
    
    def test_returns_rules_subdir(self):
        """Should return rules subdirectory of data dir."""
        from shadowbotagents.paths import get_rules_dir
        
        result = get_rules_dir()
        assert result == Path.home() / ".shadowbot" / "rules"


class TestGetPermissionsDir:
    """Tests for get_permissions_dir() function."""
    
    def test_returns_permissions_subdir(self):
        """Should return permissions subdirectory of data dir."""
        from shadowbotagents.paths import get_permissions_dir
        
        result = get_permissions_dir()
        assert result == Path.home() / ".shadowbot" / "permissions"


class TestGetStorageDir:
    """Tests for get_storage_dir() function."""
    
    def test_returns_storage_subdir(self):
        """Should return storage subdirectory of data dir."""
        from shadowbotagents.paths import get_storage_dir
        
        result = get_storage_dir()
        assert result == Path.home() / ".shadowbot" / "storage"


class TestGetCheckpointsDir:
    """Tests for get_checkpoints_dir() function."""
    
    def test_returns_checkpoints_subdir(self):
        """Should return checkpoints subdirectory of data dir."""
        from shadowbotagents.paths import get_checkpoints_dir
        
        result = get_checkpoints_dir()
        assert result == Path.home() / ".shadowbot" / "checkpoints"


class TestGetSnapshotsDir:
    """Tests for get_snapshots_dir() function."""
    
    def test_returns_snapshots_subdir(self):
        """Should return snapshots subdirectory of data dir."""
        from shadowbotagents.paths import get_snapshots_dir
        
        result = get_snapshots_dir()
        assert result == Path.home() / ".shadowbot" / "snapshots"


class TestGetLearnDir:
    """Tests for get_learn_dir() function."""
    
    def test_returns_learn_subdir(self):
        """Should return learn subdirectory of data dir."""
        from shadowbotagents.paths import get_learn_dir
        
        result = get_learn_dir()
        assert result == Path.home() / ".shadowbot" / "learn"


class TestGetProjectDataDir:
    """Tests for get_project_data_dir() function."""
    
    def test_returns_shadowbot_in_cwd(self):
        """Should return .shadowbot/ in current working directory."""
        from shadowbotagents.paths import get_project_data_dir
        
        result = get_project_data_dir()
        assert result == Path.cwd() / ".shadowbot"
    
    def test_accepts_custom_project_path(self, tmp_path):
        """Should accept custom project path."""
        from shadowbotagents.paths import get_project_data_dir
        
        result = get_project_data_dir(tmp_path)
        assert result == tmp_path / ".shadowbot"


class TestEnsureDir:
    """Tests for ensure_dir() function."""
    
    def test_creates_directory(self, tmp_path):
        """Should create directory if it doesn't exist."""
        from shadowbotagents.paths import ensure_dir
        
        test_dir = tmp_path / "test" / "nested" / "dir"
        assert not test_dir.exists()
        
        result = ensure_dir(test_dir)
        
        assert test_dir.exists()
        assert test_dir.is_dir()
        assert result == test_dir
    
    def test_returns_existing_directory(self, tmp_path):
        """Should return existing directory without error."""
        from shadowbotagents.paths import ensure_dir
        
        test_dir = tmp_path / "existing"
        test_dir.mkdir()
        
        result = ensure_dir(test_dir)
        
        assert result == test_dir


class TestGetMcpAuthPath:
    """Tests for get_mcp_auth_path() function."""
    
    def test_returns_mcp_auth_json(self):
        """Should return path to mcp-auth.json."""
        from shadowbotagents.paths import get_mcp_auth_path
        
        result = get_mcp_auth_path()
        assert result == Path.home() / ".shadowbot" / "mcp-auth.json"


class TestConstants:
    """Tests for module constants."""
    
    def test_env_var_name(self):
        """ENV_VAR should be PRAISONAI_HOME."""
        from shadowbotagents.paths import ENV_VAR
        
        assert ENV_VAR == "PRAISONAI_HOME"
    
    def test_default_dir_name(self):
        """DEFAULT_DIR_NAME should be .shadowbot."""
        from shadowbotagents.paths import DEFAULT_DIR_NAME
        
        assert DEFAULT_DIR_NAME == ".shadowbot"
    
    def test_legacy_dir_name(self):
        """LEGACY_DIR_NAME should be .praison."""
        from shadowbotagents.paths import LEGACY_DIR_NAME
        
        assert LEGACY_DIR_NAME == ".praison"


class TestGetAllPaths:
    """Tests for get_all_paths() function."""
    
    def test_returns_dict_of_all_paths(self):
        """Should return dictionary with all path locations."""
        from shadowbotagents.paths import get_all_paths
        
        result = get_all_paths()
        
        assert isinstance(result, dict)
        assert "data_dir" in result
        assert "sessions" in result
        assert "skills" in result
        assert "plugins" in result
        assert "mcp" in result
        assert "docs" in result
        assert "rules" in result
        assert "permissions" in result
        assert "storage" in result
        assert "checkpoints" in result
        assert "snapshots" in result
        assert "learn" in result
        assert "mcp_auth" in result


class TestImportPerformance:
    """Tests for import performance."""
    
    def test_import_time_under_10ms(self):
        """Module import should be fast (no heavy deps)."""
        import time as time_module
        import sys as sys_module
        
        # Remove from cache if present
        if "shadowbotagents.paths" in sys_module.modules:
            del sys_module.modules["shadowbotagents.paths"]
        
        start = time_module.perf_counter()
        import shadowbotagents.paths as paths_module  # noqa: F401
        elapsed = time_module.perf_counter() - start
        
        # Should import in under 10ms (no heavy deps)
        assert elapsed < 0.01, f"Import took {elapsed*1000:.2f}ms, expected < 10ms"


class TestProjectLocalHelpers:
    """Tests for project-local path helpers (get_project_*_dir)."""

    def test_project_sessions_dir(self):
        """get_project_sessions_dir returns .shadowbot/sessions/ in cwd."""
        from shadowbotagents.paths import get_project_sessions_dir

        result = get_project_sessions_dir()
        assert result == Path.cwd() / ".shadowbot" / "sessions"

    def test_project_sessions_dir_custom_path(self, tmp_path):
        """get_project_sessions_dir accepts custom project path."""
        from shadowbotagents.paths import get_project_sessions_dir

        result = get_project_sessions_dir(tmp_path)
        assert result == tmp_path / ".shadowbot" / "sessions"

    def test_project_knowledge_dir(self):
        """get_project_knowledge_dir returns .shadowbot/knowledge/ in cwd."""
        from shadowbotagents.paths import get_project_knowledge_dir

        result = get_project_knowledge_dir()
        assert result == Path.cwd() / ".shadowbot" / "knowledge"

    def test_project_knowledge_dir_custom_path(self, tmp_path):
        """get_project_knowledge_dir accepts custom project path."""
        from shadowbotagents.paths import get_project_knowledge_dir

        result = get_project_knowledge_dir(tmp_path)
        assert result == tmp_path / ".shadowbot" / "knowledge"

    def test_project_summaries_dir(self):
        """get_project_summaries_dir returns .shadowbot/summaries/ in cwd."""
        from shadowbotagents.paths import get_project_summaries_dir

        result = get_project_summaries_dir()
        assert result == Path.cwd() / ".shadowbot" / "summaries"

    def test_project_prp_dir(self):
        """get_project_prp_dir returns .shadowbot/prp/ in cwd."""
        from shadowbotagents.paths import get_project_prp_dir

        result = get_project_prp_dir()
        assert result == Path.cwd() / ".shadowbot" / "prp"


class TestGetSchedulesDir:
    """Tests for get_schedules_dir() function."""

    def test_returns_schedules_subdir(self):
        """Should return schedules subdirectory of data dir."""
        from shadowbotagents.paths import get_schedules_dir

        result = get_schedules_dir()
        assert result == Path.home() / ".shadowbot" / "schedules"

    def test_respects_env_override(self):
        """Should respect PRAISONAI_HOME override."""
        from shadowbotagents.paths import get_schedules_dir

        with patch.dict(os.environ, {"PRAISONAI_HOME": "/custom"}):
            result = get_schedules_dir()
            assert result == Path("/custom/schedules")


class TestGetStoragePath:
    """Tests for get_storage_path() function."""

    def test_returns_storage_db(self):
        """Should return storage.db in data dir."""
        from shadowbotagents.paths import get_storage_path

        result = get_storage_path()
        assert result == Path.home() / ".shadowbot" / "storage.db"

    def test_respects_env_override(self):
        """Should respect PRAISONAI_HOME override."""
        from shadowbotagents.paths import get_storage_path

        with patch.dict(os.environ, {"PRAISONAI_HOME": "/custom"}):
            result = get_storage_path()
            assert result == Path("/custom/storage.db")


class TestModuleWiring:
    """Tests verifying that modules use paths.py instead of hardcoded paths."""

    def test_policy_config_uses_paths(self):
        """policy/config.py should resolve rules dir via paths.py."""
        from shadowbotagents.policy.config import DEFAULT_RULES_DIR
        from shadowbotagents.paths import get_rules_dir

        assert DEFAULT_RULES_DIR == str(get_rules_dir())

    def test_policy_config_no_hardcoded_expanduser(self):
        """policy/config.py should not have hardcoded expanduser for rules."""
        import inspect
        from shadowbotagents.policy import config

        source = inspect.getsource(config)
        # The module should not contain expanduser + .shadowbot for rules
        assert 'expanduser("~"), ".shadowbot", "rules"' not in source

    def test_autonomy_snapshot_dir_defaults_via_paths(self):
        """autonomy.py AutonomyConfig should default snapshot_dir via paths.py."""
        from shadowbotagents.agent.autonomy import AutonomyConfig
        from shadowbotagents.paths import get_snapshots_dir

        config = AutonomyConfig()
        assert config.snapshot_dir == str(get_snapshots_dir())

    def test_autonomy_snapshot_dir_respects_env(self):
        """AutonomyConfig snapshot_dir should respect PRAISONAI_HOME."""
        from shadowbotagents.paths import _clear_cache

        _clear_cache()
        with patch.dict(os.environ, {"PRAISONAI_HOME": "/custom"}):
            from shadowbotagents.agent.autonomy import AutonomyConfig

            config = AutonomyConfig()
            assert config.snapshot_dir == str(Path("/custom/snapshots"))
        _clear_cache()

    def test_scheduler_store_uses_paths(self):
        """scheduler/store.py should resolve default dir via paths.py."""
        from shadowbotagents.scheduler.store import _DEFAULT_DIR
        from shadowbotagents.paths import get_schedules_dir

        assert _DEFAULT_DIR == str(get_schedules_dir())

    def test_sqlite_backend_default_uses_paths(self):
        """SQLiteBackend default db_path should use paths.py."""
        from shadowbotagents.storage.backends import SQLiteBackend
        from shadowbotagents.paths import get_storage_path

        # We can't construct SQLiteBackend without it trying to create the DB,
        # so we verify the import is present
        import inspect
        source = inspect.getsource(SQLiteBackend.__init__)
        assert "get_storage_path" in source

