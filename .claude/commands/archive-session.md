# Archive Session

Archive the current conversation to a markdown file in `C:\Users\noamw\Desktop\ims\Automated Daily Forecast\.claude\session_archive\v2`.

## Pre-processing

!TRANSCRIPT=$(ls -t ~/.claude/projects/c--Users-noamw-Desktop-ims-Automated-Daily-Forecast/*.jsonl 2>/dev/null | grep -v agent | head -1) && python scripts/convert_transcript.py "$TRANSCRIPT" > .claude/.temp_conversation.md 2>/dev/null || echo "Error converting transcript"

## Instructions

1. **Determine sequence number**: Scan `C:\Users\noamw\Desktop\ims\Automated Daily Forecast\.claude\session_archive\v2` for existing files named `claude session #XX.md` and use the next number in sequence.

2. **Generate session name**: Create a concise, descriptive name (3-5 words) based on the main topics discussed.

3. **Estimate token usage**: Provide a rough estimate based on conversation length (e.g., ~5,000 for short, ~15,000 for medium, ~30,000+ for long sessions).

4. **Read converted conversation**: Read the file `.claude/.temp_conversation.md` which contains the conversation in markdown format.

5. **Create the complete archive file** with this structure:

```markdown
# #{sequence} - {Session Name}

### {Friendly date: Month Day, Year at H:MM AM/PM}

### Tokens used: ~{estimated count}

---

## Summary

{2-4 bullet points covering:}
- Main topics discussed
- Key achievements/completions
- Issues encountered (if any)
- Actionable conclusions

## Next Time

{A ready-to-use prompt suggestion for continuing work in the next session, based on what was accomplished and what remains}

---

## Conversation

{Paste content from .claude/.temp_conversation.md here}

---

**Archived:** {ISO timestamp: YYYY-MM-DDTHH:MM:SS}
```

6. **Clean up**: Delete `.claude/.temp_conversation.md` after creating the archive.

## File Location

Save to: `.claude/session_archive/v2/claude session #{sequence}.md`

## Important Notes

- Use two-digit sequence numbers (#00, #01, #02...)
- The conversation is pre-converted by the Python script - just read and paste it
- The summary should be actionable and help future-me understand the session quickly
- The "Next Time" prompt should be specific enough to immediately continue work
- This approach is token-efficient: the conversation is read from file, not regenerated
