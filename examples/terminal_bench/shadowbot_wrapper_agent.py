"""
ShadowBot Wrapper Agent for Terminal-Bench 2.0 (Harbor)

An external agent that uses the ShadowBot CLI wrapper instead of
direct Agent class instantiation. This provides a higher-level interface
that matches the standard `shadowbot "TASK"` CLI usage pattern.

Usage:
    harbor run -d terminal-bench/terminal-bench-2 \
        --agent-import-path examples.terminal_bench.shadowbot_wrapper_agent:ShadowBotWrapperAgent \
        --model openai/gpt-4o \
        --ae OPENAI_API_KEY=$OPENAI_API_KEY \
        -n 4

Architecture:
    Harbor Container ←→ BaseEnvironment.exec() ←→ shadowbot CLI subprocess

Dependencies:
    pip install harbor shadowbot
"""

import asyncio
import shlex
import json
import os
from typing import Any, Dict, Optional

# These imports require Harbor to be installed
try:
    from harbor.agents.base import BaseAgent
    from harbor.environments.base import BaseEnvironment
    from harbor.models.agent.context import AgentContext
except ImportError as e:
    raise ImportError(
        f"Harbor framework not installed: {e}\n"
        "Install with: pip install harbor"
    ) from e


class ShadowBotWrapperAgent(BaseAgent):
    """
    ShadowBot wrapper agent that uses the CLI/subprocess approach.
    
    This agent installs ShadowBot inside the Harbor container and runs
    tasks using the `shadowbot "TASK"` pattern, matching standard CLI usage.
    """

    @staticmethod
    def name() -> str:
        return "shadowbot-wrapper"

    def version(self) -> str | None:
        """Get ShadowBot version from container."""
        try:
            import shadowbot
            return getattr(shadowbot, "__version__", None)
        except ImportError:
            return None

    async def setup(self, environment: BaseEnvironment) -> None:
        """
        Setup phase - install ShadowBot wrapper inside the container.
        """
        print("🔧 Installing ShadowBot wrapper inside container...")
        
        # Install system dependencies
        await self._exec_as_root(
            environment,
            command="apt-get update && apt-get install -y python3 python3-pip curl git",
            env={"DEBIAN_FRONTEND": "noninteractive"},
        )
        
        # Install ShadowBot wrapper
        version_spec = f"=={self._version}" if getattr(self, '_version', None) else ""
        install_cmd = f"pip install shadowbot{version_spec} --quiet"
        
        await self._exec_as_agent(
            environment,
            command=(
                f"{install_cmd} && "
                "python3 -c 'import shadowbot; print(\"✅ shadowbot installed:\", shadowbot.__version__)'"
            ),
        )
        
        print("✅ ShadowBot wrapper setup completed")

    async def run(
        self,
        instruction: str,
        environment: BaseEnvironment,
        context: AgentContext,
    ) -> None:
        """
        Run the ShadowBot wrapper agent on the given instruction.
        
        Uses the `shadowbot "TASK"` CLI pattern inside the Harbor container.
        """
        model = self.model_name or "openai/gpt-4o"
        
        # Build the shadowbot CLI command
        # Format: shadowbot "TASK" --model MODEL
        cmd_parts = [
            "shadowbot",
            shlex.quote(instruction),
            "--model", shlex.quote(model),
        ]
        
        # Add API key to environment
        env_vars = self._get_environment_vars()
        
        command = " ".join(cmd_parts)
        
        try:
            print(f"🚀 ShadowBot wrapper starting task: {instruction[:100]}...")
            
            # Execute shadowbot CLI inside the container
            result = await environment.exec(
                command=command,
                timeout_sec=600,  # 10 minute timeout for complex tasks
                env=env_vars,
            )
            
            print(f"✅ ShadowBot wrapper completed task")
            
            # Populate Harbor context with results
            self._populate_context(result, context, instruction)
            
        except Exception as e:
            print(f"❌ ShadowBot wrapper failed: {str(e)}")
            context.metadata = {"error": str(e)}
            raise

    def _populate_context(
        self,
        result: Any,
        context: AgentContext,
        instruction: str
    ) -> None:
        """
        Populate Harbor's AgentContext with execution results.
        """
        try:
            # Extract output from result
            stdout = getattr(result, 'stdout', '') or ''
            stderr = getattr(result, 'stderr', '') or ''
            return_code = getattr(result, 'return_code', 0)
            
            # Store result summary
            context.metadata = {
                "agent_name": "shadowbot-wrapper",
                "model": self.model_name or "openai/gpt-4o",
                "framework": "shadowbot",
                "wrapper_type": "cli",
                "instruction_preview": instruction[:200],
                "return_code": return_code,
                "stderr_preview": stderr[:500] if stderr else None,
            }
            
            # Try to parse any JSON output for metrics
            try:
                # Look for JSON in the output
                lines = stdout.strip().split('\n')
                for line in reversed(lines):
                    if line.strip().startswith('{'):
                        metrics = json.loads(line.strip())
                        if isinstance(metrics, dict):
                            context.n_input_tokens = metrics.get('input_tokens')
                            context.n_output_tokens = metrics.get('output_tokens')
                            context.cost_usd = metrics.get('cost_usd')
                            context.metadata['parsed_metrics'] = metrics
                            break
            except (json.JSONDecodeError, ValueError):
                pass  # No JSON metrics found
            
            # Store final response (last non-empty line or full stdout)
            final_lines = [l for l in stdout.split('\n') if l.strip()]
            context.metadata['final_response'] = final_lines[-1][:500] if final_lines else stdout[:500]
            
        except Exception as e:
            context.metadata = {"context_error": str(e)}

    def _get_environment_vars(self) -> Dict[str, str]:
        """Get environment variables to pass to the agent execution."""
        env_vars = {}
        
        # Forward API keys
        api_keys = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GEMINI_API_KEY",
            "GOOGLE_API_KEY",
            "AZURE_OPENAI_API_KEY",
            "GROQ_API_KEY",
        ]
        
        for key in api_keys:
            value = os.environ.get(key)
            if value:
                env_vars[key] = value
        
        # Set LOGLEVEL to reduce noise
        env_vars["LOGLEVEL"] = "WARNING"
        
        return env_vars

    async def _exec_as_root(self, environment: BaseEnvironment, command: str, env: Optional[Dict] = None) -> Any:
        """Execute command as root in the container."""
        if hasattr(environment, 'exec_as_root'):
            return await environment.exec_as_root(command=command, env=env or {})
        else:
            # Fallback: use sudo
            return await environment.exec(command=f"sudo {command}", env=env or {})

    async def _exec_as_agent(self, environment: BaseEnvironment, command: str) -> Any:
        """Execute command as the agent user in the container."""
        return await environment.exec(command=command)


# Example usage for testing
if __name__ == "__main__":
    print("ShadowBot Wrapper Agent for Terminal-Bench 2.0")
    print("=" * 50)
    print()
    print("This agent uses the ShadowBot CLI wrapper approach:")
    print('  shadowbot "TASK" --model MODEL')
    print()
    print("Usage with Harbor:")
    print("  harbor run -d terminal-bench/terminal-bench-2 \\")
    print("    --agent-import-path examples.terminal_bench.shadowbot_wrapper_agent:ShadowBotWrapperAgent \\")
    print("    --model openai/gpt-4o")
    print()
    print("Dependencies:")
    print("  pip install harbor shadowbot")
