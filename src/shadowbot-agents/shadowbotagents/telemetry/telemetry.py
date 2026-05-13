"""
Telemetry stub for ShadowBot Agents.

All telemetry and external analytics have been permanently removed.
No data is collected, tracked, or sent anywhere.
"""

import threading
from typing import Dict, Any, Optional


def _is_monitoring_disabled() -> bool:
    return True


class MinimalTelemetry:
    """No-op telemetry stub. Collects and sends nothing."""

    def __init__(self, enabled: bool = None):
        self.enabled = False
        self.session_id = None
        self._metrics = {}
        self._shutdown_complete = True
        self._shutdown_lock = threading.Lock()
        self._thread_pool = None
        self._environment = {}

    def track_agent_execution(self, agent_name: str = None, success: bool = True, async_mode: bool = False):
        pass

    def track_task_completion(self, task_name: str = None, success: bool = True):
        pass

    def track_tool_usage(self, tool_name: str, success: bool = True, execution_time: float = None):
        pass

    def track_error(self, error_type: str = None):
        pass

    def track_feature_usage(self, feature_name: str):
        pass

    def get_metrics(self) -> Dict[str, Any]:
        return {"enabled": False}

    def flush(self):
        pass

    def shutdown(self):
        pass

    def _get_framework_version(self) -> str:
        try:
            from .. import __version__
            return __version__
        except (ImportError, KeyError, AttributeError):
            return "unknown"


# Global instance
_telemetry_instance = None
_telemetry_instance_lock = threading.Lock()


def get_telemetry() -> MinimalTelemetry:
    global _telemetry_instance
    with _telemetry_instance_lock:
        if _telemetry_instance is None:
            _telemetry_instance = MinimalTelemetry()
        return _telemetry_instance


def disable_telemetry():
    pass


def enable_telemetry():
    pass


def force_shutdown_telemetry():
    global _telemetry_instance
    with _telemetry_instance_lock:
        _telemetry_instance = None


class TelemetryCollector:
    """No-op backward-compatibility stub."""

    def __init__(self, backend: str = "minimal", service_name: str = "shadowbot-agents", **kwargs):
        self.telemetry = get_telemetry()

    def start(self):
        pass

    def stop(self):
        pass

    def trace_agent_execution(self, agent_name: str, **attributes):
        from contextlib import contextmanager

        @contextmanager
        def _trace():
            yield None

        return _trace()

    def trace_task_execution(self, task_name: str, agent_name: str = None, **attributes):
        from contextlib import contextmanager

        @contextmanager
        def _trace():
            yield None

        return _trace()

    def trace_tool_call(self, tool_name: str, **attributes):
        from contextlib import contextmanager

        @contextmanager
        def _trace():
            yield None

        return _trace()

    def trace_llm_call(self, model: str = None, **attributes):
        from contextlib import contextmanager

        @contextmanager
        def _trace():
            yield None

        return _trace()

    def record_tokens(self, prompt_tokens: int, completion_tokens: int, model: str = None):
        pass

    def record_cost(self, cost: float, model: str = None):
        pass

    def get_metrics(self) -> Dict[str, Any]:
        return self.telemetry.get_metrics()
