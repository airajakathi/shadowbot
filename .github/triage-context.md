# GitHub Issue #1350: Add debug log on successful branch checkout

The github_create_branch function in src/shadowbot-agents/shadowbotagents/tools/github_tools.py should call logger.debug after a successful checkout.
