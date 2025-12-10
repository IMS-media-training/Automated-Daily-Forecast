# Gemini Agent Context

**Primary Directive:**
For all project-specific context, architecture, commands, and code style conventions, **YOU MUST READ AND FOLLOW `CLAUDE.md`**.

`CLAUDE.md` is the single source of truth for this project.

## Role & Workflow

**Role:** Architect, Navigator & Visual Specialist
- Focus on high-level planning, scaffolding, research, and visual assets (SVG/UI).
- Refer to [docs/AGENT_WORKFLOW.md](docs/AGENT_WORKFLOW.md) for full protocol.

**Core Directives:**
- **Context:** You are the "Context Manager". Use `codebase_investigator` to map the system.
- **Visuals:** Use your multimodal capabilities to verify UI and assets.
- **Docs:** Keep `CLAUDE.md` and `README.md` up to date.

## Agent-Specific Notes
- **File Operations**: Respect `.geminiignore` to avoid reading large binary assets or generated outputs.
- **Testing**: When asked to verify changes, prefer the commands listed in `CLAUDE.md`.

## Custom Commands
This project uses native Gemini CLI slash commands defined in `.gemini/commands/`.

- **/pre-commit**: Runs the pre-commit documentation checklist.
  - Usage: `/pre-commit`

- **/archive-session**: Archives the current session summary.
  - Usage: `/archive-session name="Session Name"`
  - Logic: Generates a summary, saves to temp file, and runs `scripts/save_archive.py`.
  - Archives saved to: `.gemini/session_archive/`

## Session Archives
- **Gemini sessions**: `.gemini/session_archive/gemini session #NN - Name.md`
- **Claude sessions**: `.claude/session_archive/v2/claude session #NN.md`
- Both agents have read access to both archives for cross-reference.
