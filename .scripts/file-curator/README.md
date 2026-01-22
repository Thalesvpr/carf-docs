---
type: readme
status: draft
updated: 2026-01-22
---

# File Curator

Professional GUI for curating documentation files - "Tinder for files"

## Overview

File Curator provides a streamlined workflow for reviewing and curating documentation files one-by-one. Each file is presented with a beautiful rendered Markdown card, allowing you to make quick decisions (approve, reject, skip) with full keyboard navigation and a professional dark-themed interface.

### Key Features

- **Professional GUI**: Beautiful PySide6-based interface with dark theme
- **Beautiful Markdown Rendering**: Custom-styled markdown preview with syntax highlighting
- **Split-Pane Editor**: Edit review cards with live preview
- **100% File Coverage**: Every matching file is presented for review - no automatic filtering
- **Skip Returns to Queue**: Skipped files come back for later review
- **No Auto-Execute**: All scripts require explicit approval
- **Editable Reviews**: Add observations, justifications, and tags to each review
- **Persistent State**: Resume sessions at any time with SQLite-backed storage
- **Script Integration**: Run carf_validator from within the GUI
- **Full Audit Trail**: All actions logged to console and file

## Screenshots

```
┌─────────────────────────────────────────────────────────────────┐
│  Session Name | Progress Bar (45/120) | 37.5%                   │
├─────────────┬───────────────────────────────────┬───────────────┤
│             │                                   │               │
│  File List  │      Markdown Preview/Editor      │   Metadata    │
│  (Queue)    │                                   │   Panel       │
│             │      ┌─────────────────────┐      │               │
│  ● current  │      │  Beautiful render   │      │  Path:        │
│  ○ pending  │      │  of review card     │      │  Type:        │
│  ○ pending  │      │  with good typo     │      │  Size:        │
│  ✓ approved │      │                     │      │  Modified:    │
│  ✗ rejected │      └─────────────────────┘      │               │
│             │                                   │               │
├─────────────┴───────────────────────────────────┴───────────────┤
│  Action Bar: [✓ Approve] [✗ Reject] [→ Skip] [✎ Edit] [⚙ Tools] │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

```bash
# From the file-curator directory
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Dependencies

- **PySide6** (>=6.6.0) - Qt-based GUI framework
- **markdown** (>=3.5.0) - Markdown rendering
- **pyyaml** (>=6.0) - Configuration files
- **rich** (>=13.0) - Beautiful console logging

## Quick Start

```bash
# Start GUI application (default)
python -m file_curator

# Use TUI instead (text-based interface)
python -m file_curator --tui

# Create a new named session
python -m file_curator --new "audit-2026"

# Resume an existing session
python -m file_curator --resume <session-id>

# Specify a different root directory
python -m file_curator --root /path/to/docs
```

## CLI Reference

```
usage: file-curator [-h] [--root ROOT] [--config CONFIG] [--tui]
                    [--new NAME | --resume ID | --list]
                    [--stats ID] [--export ID] [-o OUTPUT]
                    [--version] [--dry-run]

Professional GUI for curating documentation files

options:
  -h, --help            show this help message and exit
  --root ROOT           Root directory to curate (default: current directory)
  --config CONFIG       Path to config file (YAML or JSON)
  --tui                 Use text-based TUI instead of GUI
  --new NAME            Create a new session with the given name
  --resume ID           Resume an existing session by ID
  --list                List all sessions
  --stats ID            Show statistics for a session
  --export ID           Export session to JSON
  -o, --output OUTPUT   Output file for export (default: stdout)
  --version             show program's version number and exit
  --dry-run             Show what would be done without making changes
```

## Keyboard Shortcuts

### Main Window

| Key | Action | Description |
|-----|--------|-------------|
| `A` | Approve | Mark file as approved |
| `R` | Reject | Mark file as rejected (requires justification) |
| `S` | Skip | Skip file (returns to queue) |
| `E` | Edit | Toggle Markdown editor |
| `J` | Next | Navigate to next file in list |
| `K` | Previous | Navigate to previous file in list |
| `Escape` | Exit Editor | Close editor pane |
| `Ctrl+,` | Settings | Open settings dialog |
| `Ctrl+Q` | Quit | Save and quit |

### Editor

| Key | Action |
|-----|--------|
| `Ctrl+S` | Save changes |
| `Escape` | Cancel and close |

## Visual Design

### Color Palette (Dark Theme)

| Element | Color |
|---------|-------|
| Background | `#1a1a2e` (deep navy) |
| Surface | `#16213e` (card background) |
| Primary | `#0f3460` (buttons, accents) |
| Approve | `#4ecca3` (green) |
| Reject | `#e94560` (red) |
| Skip | `#f0a500` (amber) |
| Text | `#eaeaea` (primary) |
| Border | `#2a2a4a` |

### Typography

- **UI Font**: Inter or system sans-serif
- **Code Font**: JetBrains Mono or Consolas
- **Base Size**: 14px body, 24px headings
- **Line Height**: 1.6 for readability

## Configuration

Create a `file_curator_config.yaml` in your project root:

```yaml
scan:
  include_patterns:
    - "**/*.md"
  exclude_dirs:
    - ".git"
    - ".obsidian"
    - ".scripts"
    - "SRC-CODE"
    - "node_modules"
    - "file-curator"

paths:
  data_dir: "data"
  templates_dir: "templates"
  reviews_dir: "data/reviews"

review:
  require_observations: false
  require_justification_on_reject: true
  skip_returns_to_queue: true

scripts:
  enabled: true
  require_approval: true
  default_to_dry_run: true
```

## Templates

Customize the review card and decision record templates by creating files in the `templates/` directory:

### templates/review_card.md

```markdown
## ${file_title}

**Path:** `${relative_path}`
**Type:** ${doc_type} | **Modules:** ${modules} | **Epic:** ${epic}

### Metadata
| Field | Value |
|-------|-------|
| Status | ${status} |
| Last Update | ${last_update} |
| Words | ${word_count} |

### Content Preview
${content_preview}

### Validation Issues
${validation_issues}
```

## Logging

All actions are logged to both stdout (with Rich formatting) and session log files:

```
[2026-01-19 14:32:15] SESSION_START id=abc123 name="audit-2026"
[2026-01-19 14:32:16] FILE_PRESENTED path="docs/README.md" index=1/120
[2026-01-19 14:32:45] DECISION decision=APPROVED path="docs/README.md" observations="Good structure"
[2026-01-19 14:32:46] FILE_PRESENTED path="docs/API.md" index=2/120
[2026-01-19 14:33:10] DECISION decision=SKIPPED path="docs/API.md"
[2026-01-19 14:33:11] SCRIPT_SUGGESTED script="carf_validator" target="docs/API.md"
[2026-01-19 14:33:15] SCRIPT_APPROVED script="carf_validator" command="python -m carf_validator docs/API.md"
[2026-01-19 14:33:20] SCRIPT_COMPLETED script="carf_validator" exit_code=0
```

Log files are stored in `data/logs/session_<id>.log`.

## Data Storage

All session data is stored in SQLite at `data/curator.db`. This includes:

- Session metadata
- File inventory with status
- Review records with observations
- Script execution history

### Exported Reports

Use `--export <session-id>` to generate a JSON report containing:

```json
{
  "session": { ... },
  "files": [ ... ],
  "reviews": [ ... ],
  "exported_at": "2026-01-19T..."
}
```

## Script Integration

File Curator integrates with existing `.scripts/` tools:

### carf_validator
- Validates documentation files against CARF standards
- Read-only operation (safe to run)
- Available via Tools menu

All script executions require explicit approval and show a preview dialog before running.

## Architecture

```
file-curator/
├── file_curator/           # Main package
│   ├── models/             # Data models (FileItem, Session, Review)
│   ├── scanner/            # File discovery and parsing
│   ├── state/              # SQLite persistence
│   ├── templates/          # Template rendering
│   ├── actions/            # Review actions
│   ├── integration/        # Script integration
│   ├── config/             # Configuration
│   ├── logging/            # Session logging with Rich
│   ├── gui/                # PySide6 GUI
│   │   ├── widgets/        # Reusable widgets
│   │   ├── dialogs/        # Dialog windows
│   │   └── resources/      # Stylesheets, icons
│   └── tui/                # Textual TUI (legacy)
├── templates/              # User-editable templates
└── data/                   # Runtime data (gitignored)
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_scanner.py
```

## Requirements

- Python 3.10+
- PySide6 >= 6.6.0
- markdown >= 3.5.0
- pyyaml >= 6.0
- rich >= 13.0

### Optional (for TUI mode)
- textual >= 0.47.0

## License

MIT
