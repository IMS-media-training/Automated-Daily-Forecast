#!/usr/bin/env python3
"""
Convert Claude Code JSONL transcript to readable markdown format.
Usage: python convert_transcript.py <transcript_path>
"""

import json
import sys
from pathlib import Path


def convert_transcript_to_markdown(transcript_path):
    """Read JSONL transcript and output formatted markdown conversation."""

    if not Path(transcript_path).exists():
        print(f"Error: Transcript file not found: {transcript_path}", file=sys.stderr)
        sys.exit(1)

    markdown_lines = []

    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            try:
                entry = json.loads(line)

                # Skip non-message entries
                if entry.get('type') not in ['user', 'assistant']:
                    continue

                # Extract message content from the nested structure
                message = entry.get('message', {})
                role = message.get('role', '')
                content = message.get('content', '')

                # Handle user messages
                if entry.get('type') == 'user' or role == 'user':
                    if isinstance(content, list):
                        # Content can be array of text/image blocks
                        text_parts = [block.get('text', '') for block in content if block.get('type') == 'text']
                        content = '\n'.join(text_parts)

                    if content:
                        markdown_lines.append("\n### User\n")
                        markdown_lines.append(content)

                # Handle assistant messages
                elif entry.get('type') == 'assistant' or role == 'assistant':
                    if isinstance(content, list):
                        # Extract text blocks, skip tool use blocks for readability
                        text_parts = []
                        for block in content:
                            if block.get('type') == 'text':
                                text_parts.append(block.get('text', ''))
                            elif block.get('type') == 'tool_use':
                                # Optionally include tool calls in a condensed format
                                tool_name = block.get('name', 'unknown')
                                text_parts.append(f"*[Used tool: {tool_name}]*")
                        content = '\n'.join(text_parts)

                    if content:
                        markdown_lines.append("\n### Assistant\n")
                        markdown_lines.append(content)

            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON line: {e}", file=sys.stderr)
                continue

    return '\n'.join(markdown_lines)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python convert_transcript.py <transcript_path>", file=sys.stderr)
        sys.exit(1)

    transcript_path = sys.argv[1]
    markdown_output = convert_transcript_to_markdown(transcript_path)

    # Force UTF-8 output to handle all characters
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(markdown_output)
