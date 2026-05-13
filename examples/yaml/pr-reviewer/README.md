# ShadowBot PR Reviewer Integration Guide

This guide provides step-by-step instructions for integrating ShadowBot as an automated PR reviewer in your GitHub CI/CD pipeline.

## Overview

ShadowBot PR Reviewer implements a **Zero-Code, Multi-Agent PR Review System** that deploys specialized agents to analyze pull requests from multiple perspectives:

- 🔐 **Security Reviewer**: Identifies vulnerabilities and security issues
- ⚡ **Performance Reviewer**: Analyzes for bottlenecks and inefficiencies  
- 📋 **Maintainability Reviewer**: Evaluates code quality and best practices
- 👨‍💼 **Lead Reviewer**: Synthesizes feedback and posts comprehensive reviews

## Architecture

This integration follows ShadowBot's **Agent-Centric** and **Protocol-Driven Core** design principles:

```
GitHub PR → @shadowbot trigger → Multi-Agent Workflow → Comprehensive Review
```

The solution leverages:
- **GitHub Actions** for CI/CD orchestration
- **ShadowBot CLI** for agent execution
- **YAML Configuration** for agent team definition
- **GitHub CLI** for PR interaction

## Prerequisites

1. **Repository Setup**:
   - GitHub repository with Actions enabled
   - Required secrets configured (see [Secrets Configuration](#secrets-configuration))

2. **ShadowBot Installation**:
   - The workflow automatically installs ShadowBot via `pip install shadowbot`
   - No additional dependencies required

3. **GitHub App/Token**:
   - GitHub App with required permissions OR
   - Personal Access Token with `repo` and `pull_requests` permissions

## Installation Steps

### Step 1: Copy Agent Configuration

The agent configuration is already provided at:
```
.github/shadowbot-reviewer.yaml
```

This file defines the multi-agent team and their specific responsibilities.

### Step 2: Create GitHub Workflow

**IMPORTANT**: Due to GitHub App permissions, the workflow file must be manually created.

1. Copy the template from:
   ```
   examples/yaml/shadowbot-pr-review.yml.template
   ```

2. Save it as:
   ```
   .github/workflows/shadowbot-pr-review.yml
   ```

### Step 3: Configure Secrets

Add the following secrets to your repository (`Settings > Secrets and variables > Actions`):

| Secret | Description | Required |
|--------|-------------|----------|
| `PRAISONAI_APP_ID` | GitHub App ID | Yes (if using GitHub App) |
| `PRAISONAI_APP_PRIVATE_KEY` | GitHub App private key | Yes (if using GitHub App) |
| `OPENAI_API_KEY` | OpenAI API key for LLM access | Yes |

**Alternative**: Use `GH_TOKEN` instead of GitHub App if you prefer PAT authentication.

### Step 4: Update Review Chain (Optional)

The review chain documentation has been updated to include ShadowBot:
```
CodeRabbit/Qodo → Gemini/ShadowBot (parallel) → Copilot → Claude (final)
```

This ensures ShadowBot integrates seamlessly with existing review workflows.

## Usage

### Manual Trigger

1. **Workflow Dispatch**: 
   - Go to `Actions > ShadowBot PR Review > Run workflow`
   - Enter the PR number to review

### Automatic Trigger

1. **Comment Trigger**:
   - Comment `@shadowbot` on any pull request
   - Only repository owners, members, and collaborators can trigger

2. **With Instructions**:
   - `@shadowbot focus on security vulnerabilities`
   - `@shadowbot check performance and memory usage`
   - `@shadowbot review for maintainability issues`

## Expected Output

When triggered, ShadowBot will post a comprehensive review with this structure:

```markdown
## 📋 Review Summary
[Brief overview and assessment]

## 🔍 General Feedback  
[Overall patterns and observations]

## 🎯 Specific Feedback
### 🔴 Critical
[Security vulnerabilities, breaking changes, major bugs]

### 🟡 High 
[Performance issues, design flaws, significant bugs]

### 🟢 Medium
[Code quality improvements, minor optimizations]

### 🔵 Low
[Documentation, naming suggestions, minor refactoring]

## ✅ Highlights
[Positive aspects worth mentioning]

---
*Review completed by ShadowBot Multi-Agent Team*
```

## Integration with Existing Workflows

ShadowBot integrates seamlessly with the existing review chain:

1. **Parallel Execution**: Runs alongside Gemini for faster reviews
2. **No Conflicts**: Uses unique trigger (`@shadowbot`) to avoid interference
3. **Complementary Analysis**: Provides different perspectives from other tools
4. **Chain Continuation**: Claude final review incorporates ShadowBot feedback

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify `PRAISONAI_APP_ID` and `PRAISONAI_APP_PRIVATE_KEY` secrets are correctly set
   - Ensure GitHub App has required permissions

2. **ShadowBot Installation Fails**:
   - Check if Python setup step completed successfully
   - Verify internet connectivity for pip installation

3. **Agent Execution Fails**:
   - Check `OPENAI_API_KEY` secret is valid
   - Verify agent configuration YAML syntax

4. **Permission Denied**:
   - Ensure triggering user has required repository permissions
   - Check workflow file permissions configuration

### Debug Steps

1. **Check Workflow Logs**:
   - Go to `Actions > ShadowBot PR Review`
   - Click on failed run to see detailed logs

2. **Validate Configuration**:
   - Ensure `.github/shadowbot-reviewer.yaml` syntax is valid
   - Test agent configuration locally if possible

3. **Test Manual Trigger**:
   - Use workflow dispatch to isolate comment trigger issues

## Advanced Configuration

### Custom Agent Teams

Modify `.github/shadowbot-reviewer.yaml` to:
- Add specialized agents (e.g., Architecture Reviewer)
- Adjust agent responsibilities
- Customize review output format

### Integration with External Tools

Extend agents to integrate with:
- Code quality tools (SonarQube, CodeClimate)
- Security scanners (Snyk, SAST tools)  
- Performance profilers

### Environment-Specific Reviews

Configure different agent teams for:
- Backend vs Frontend changes
- Different programming languages
- Specific project domains

## Performance Considerations

- **Execution Time**: Typically 3-5 minutes for comprehensive review
- **Rate Limits**: Respects GitHub API and OpenAI rate limits
- **Cost**: Uses OpenAI API - monitor usage for cost control
- **Parallel Execution**: Agents run concurrently for efficiency

## Security

- **Secret Handling**: All credentials stored securely in GitHub Secrets
- **Permissions**: Minimal required permissions for workflow execution
- **Code Access**: Review-only access, no code modification capabilities
- **Audit Trail**: All reviews logged in GitHub Actions logs

## Contributing

To improve the ShadowBot PR Reviewer:

1. **Agent Enhancement**: Improve agent prompts and capabilities
2. **Workflow Optimization**: Enhance GitHub Actions workflow
3. **Documentation**: Update guides and troubleshooting info
4. **Integration**: Add support for additional tools and platforms

## Support

For issues and questions:
1. Check this guide first
2. Review GitHub Actions logs
3. Open issue in ShadowBot repository
4. Tag with `ci/cd` and `pr-review` labels

---

*Generated as part of ShadowBot CI/CD PR Reviewer Integration (Issue #1329)*