# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Google ADK (Agent Development Kit) project that builds AI agents powered by Gemini models. The project uses the `google-adk` library to define agents with custom tools and instructions.

## Tech Stack

- Python 3.14, managed via `uv`
- Google ADK (`google-adk`) for agent framework
- Gemini 2.5 Flash as the LLM backend

## Commands

```bash
# Install dependencies
uv sync

# Run the agent locally via ADK dev server
adk web

# Run the agent in the terminal
adk run masteragent
```

## Architecture

The project follows the Google ADK agent structure convention:

- `agent.py` — Defines `root_agent`, the main ADK agent entry point. Custom tool functions (e.g., `morning_greet`, `evening_greet`) are defined here and passed to the `Agent` constructor.
- `__init__.py` — Re-exports the agent module; required by ADK for agent discovery.
- `.adk/` — Local ADK runtime data (session storage). Not committed to version control.
- `.env` — Environment variables (API keys). Not committed to version control.

The ADK framework expects the agent package directory name to match the agent project name. The `root_agent` variable in `agent.py` is the conventional entry point that ADK looks for.
