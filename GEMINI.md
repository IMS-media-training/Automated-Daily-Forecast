# Gemini Agent Context

**Primary Directive:**
For all project-specific context, architecture, commands, and code style conventions, **YOU MUST READ AND FOLLOW `CLAUDE.md`**.

`CLAUDE.md` is the single source of truth for this project.

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
