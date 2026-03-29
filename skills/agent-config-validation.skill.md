# Agent Configuration Validation Skill

## Overview

Validate and fix Copilot Chat agent configuration files by identifying and removing unknown tool references while preserving functionality.

## When to Use

- VS Code linter shows "Unknown tool" errors in .agent.md files
- Agent configurations reference tools that don't exist in current environment
- Need to ensure agents work properly without configuration errors

## Common Issues

### Unknown Tools

- `github.vscode-pull-request-github/issue_fetch`
- `github.vscode-pull-request-github/activePullRequest`

### Unknown Models

- `Gemini 3 Flash (Preview) (copilot)`

## Resolution Process

### 1. Identify Problems

Run `get_errors` on all .agent.md files in the copilot-chat directory.

### 2. Remove Problematic Tools

Remove unknown tool references from the `tools` array while keeping essential functionality:

**Keep these tools:**

- `'search'`, `'read'`, `'web'` - core search and reading
- `'vscode/memory'` - memory management
- `'github/issue_read'` - GitHub issue access
- `'execute/getTerminalOutput'`, `'execute/testFailure'` - terminal operations
- `'vscode/askQuestions'` - question handling
- `'agent'` - agent coordination (for plan agents)

**Remove these tools:**

- `'github.vscode-pull-request-github/*'` - unknown GitHub tools

### 3. Fix Model References

Remove unknown model references from `model` arrays, keeping valid ones like:

- `'Claude Haiku 4.5 (copilot)'`
- `'Auto (copilot)'`

### 4. Verify Fixes

Run `get_errors` again to confirm all configuration issues are resolved.

## Agent Types Fixed

### Ask Agent

- Read-only question answering
- Tools: search, read, web, memory, terminal, questions

### Explore Agent

- Codebase exploration and Q&A
- Tools: search, read, web, memory, terminal

### Plan Agent

- Research and planning with handoffs
- Tools: search, read, web, memory, terminal, agent coordination

## Benefits

- ✅ Eliminates configuration linting errors
- ✅ Ensures agents load and function properly
- ✅ Maintains agent capabilities while fixing compatibility
- ✅ Prepares agents for current VS Code/Copilot environment
