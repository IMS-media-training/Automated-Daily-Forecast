# Standardized Multi-Agent Workflow (Gemini 3.0 Pro & Claude Sonnet 4.5)

**Version:** 1.0 (Draft)
**Date:** December 10, 2025
**Context:** Leveraging the complementary strengths of Gemini 3.0 Pro and Claude Sonnet 4.5 for maximum efficiency.

---

## 1. Agent Roles & Specializations

To maximize efficiency, we assign roles based on the proven strengths of each model version.

### 🤖 Gemini 3.0 Pro (The Architect & Navigator)
**Primary Strengths:** Massive Context Window (2M+), Multimodal Understanding (UI/SVG), Web Grounding, Speed.
**Role:**
*   **Project Lead / Architect:** High-level planning, system design, and file scaffolding.
*   **Context Manager:** Reading entire codebases to answer "where is X defined?" or "how does Y fit in?".
*   **Visual Specialist:** Generating and verifying SVG assets, UI layouts, and map coordinates (leveraging multimodal vision).
*   **Researcher:** Using Google Search to find library documentation, API changes, or competitor analysis.
*   **Documentation:** maintaining `CLAUDE.md`, `README.md`, and changelogs.

### 🧠 Claude Sonnet 4.5 (The Lead Engineer)
**Primary Strengths:** Complex Reasoning, Precision Coding (0% internal benchmark error rate), Deep Debugging, Agentic Focus.
**Role:**
*   **Core Implementation:** Writing complex algorithms, business logic, and error handling.
*   **Refactoring:** Restructuring existing code for performance and readability without breaking functionality.
*   **Deep Debugging:** Solving "impossible" bugs by tracing logic paths that require extended reasoning.
*   **Security & Quality:** Final code reviews and writing comprehensive test suites.

---

## 2. The Unified Workflow Protocol

### Phase 1: Inception & Planning (Gemini)
*   **User Goal:** "I want to add a new feature X."
*   **Gemini Action:**
    1.  Uses `codebase_investigator` to map relevant files.
    2.  Drafts a high-level plan in `docs/plans/FEATURE_X.md`.
    3.  Scaffolds empty files/modules and directory structures.
    4.  Updates `CLAUDE.md` if new commands are needed.

### Phase 2: Implementation (Claude)
*   **Handoff:** User points Claude to the plan created by Gemini.
*   **Claude Action:**
    1.  Reads the plan and scaffolded files.
    2.  Implements the core logic (the "hard" coding).
    3.  Writes unit tests.
    4.  Runs the code to verify behavior (using `run_shell_command`).

### Phase 3: Visuals & Polish (Gemini)
*   **Handoff:** User asks Gemini to "review the UI" or "generate assets".
*   **Gemini Action:**
    1.  Generates/updates SVG icons, CSS gradients, or map coordinates (Multimodal check).
    2.  Updates documentation (`CHANGELOG.md`).
    3.  Runs the "Pre-commit" checklist.

---

## 3. Session Handoff Standards

Since agents cannot directly talk to each other, we use the file system as a communication bus.

### The "Session Archive" Pattern
We already use `.gemini/session_archive/` and `.claude/session_archive/`. We will standardize the summary format to make reading each other's work easier.

**Standard Summary Format (End of Session):**
```markdown
# Session Handoff: [Topic]
**Status:** [In Progress / Complete / Blocked]
**Next Agent:** [Gemini / Claude]

## Context for Next Agent
- **Goal:** What were we trying to do?
- **Changes:** Which files did we touch? (List relative paths)
- **Current State:** Does the code compile? Are tests passing?
- **Next Steps:** specific instructions for the next agent (e.g., "I implemented the logic in `utils.py`, now generate the SVGs for it").
```

---

## 4. Operational Rules

1.  **Code Style:** Both agents must strictly adhere to `CLAUDE.md`.
2.  **No Overwrite Without Read:** Never overwrite a file without reading it first (unless it's a new scaffold).
3.  **Test-Driven Handoff:** If Claude writes code, it should ideally leave a failing test or a verification script that Gemini can run to confirm the environment is set up correctly.
4.  **Single Source of Truth:** `CLAUDE.md` remains the master rulebook. This document (`AGENT_WORKFLOW.md`) describes *how* we work, `CLAUDE.md` describes *what* the project is.

---

## 5. Example Scenarios

| Task Type | Recommended Agent | Reasoning |
| :--- | :--- | :--- |
| "Fix this complex async bug" | **Claude** | superior reasoning for concurrency/logic |
| "Create a new project structure" | **Gemini** | faster scaffolding, better big-picture view |
| "Generate 15 weather icons" | **Gemini** | multimodal capabilities for visual consistency |
| "Refactor this 500-line class" | **Claude** | lower risk of breaking logic during refactor |
| "Update all docs" | **Gemini** | faster context processing of all .md files |
