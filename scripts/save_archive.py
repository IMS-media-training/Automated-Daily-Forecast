#!/usr/bin/env python3
"""
Save session archive with automatic sequencing.
Usage: python save_archive.py <content_file_path> <session_name>
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime


def get_next_sequence_path(archive_dir: Path, session_name: str) -> Path:
    """Determine the next sequence number and return the full path."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Find highest existing sequence number
    existing_files = list(archive_dir.glob("claude session #*.md"))
    max_seq = -1
    
    for file_path in existing_files:
        try:
            # Extract number between '#' and '.' or ' '
            name_parts = file_path.name.split('#')
            if len(name_parts) > 1:
                num_part = name_parts[1].split('.')[0].split(' ')[0]
                seq = int(num_part)
                if seq > max_seq:
                    max_seq = seq
        except (IndexError, ValueError):
            continue
            
    next_seq = max_seq + 1
    
    # Clean session name for filename
    clean_name = "".join(c for c in session_name if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = f"claude session #{next_seq:02d} - {clean_name}.md"
    
    return archive_dir / filename


def main():
    if len(sys.argv) < 3:
        print("Usage: python save_archive.py <content_file_path> <session_name>", file=sys.stderr)
        sys.exit(1)

    content_path = Path(sys.argv[1])
    session_name = sys.argv[2]
    
    # Use the same archive directory as Claude for consistency
    project_root = Path(__file__).parent.parent
    archive_dir = project_root / ".claude" / "session_archive" / "v2"

    if not content_path.exists():
        print(f"Error: Content file not found: {content_path}", file=sys.stderr)
        sys.exit(1)

    try:
        dest_path = get_next_sequence_path(archive_dir, session_name)
        
        # Read content and prepend header if not present
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Write to final destination
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Successfully archived session to:\n{dest_path}")
        
        # Clean up temp file
        content_path.unlink()
        
    except Exception as e:
        print(f"Error saving archive: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
