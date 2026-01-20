# CARF Toolkit

Unified documentation toolkit integrating `carf_validator` and `carf_tree_sync` with a professional GUI.

## Features

- **Tree View Navigation**: Hierarchical folder/file view with status icons
- **Full Markdown Preview**: Complete file content with syntax highlighting
- **Integrated Validation**: Run carf_validator on files with inline results
- **Tree Sync**: Sync README index sections with carf_tree_sync
- **Export Data**: Export aggregated data to JSON, CSV, or Markdown
- **Status Management**: Approve/Reject/Skip workflow with file metadata updates

## Layout

```
+--------------+------------------------+------------------+
| Tree View    | Preview (Full Content) | File Info        |
| ------------ | ====================== | ---------------- |
| [Search...]  |                        | Status: [Review] |
|              | # Document Title       | Updated: ...     |
| > CENTRAL    |                        | Description: ... |
|   > API      | Document content...    |------------------|
|     o login  |                        | Validation       |
|     v logout | ## Section             | ---------------- |
|              |                        | [Validate]       |
|              | Content...             |                  |
|              |                        | x errors (2)     |
|              |                        | ! warnings (1)   |
+--------------+------------------------+------------------+
| [Reject] [Skip] [Approve]    [Edit] [Sync] [Tools]      |
+----------------------------------------------------------+
```

## Installation

```bash
cd .scripts/carf_toolkit
pip install -e .
```

## Usage

```bash
# Start GUI application
carf-toolkit

# Start with specific directory
carf-toolkit --root ./CENTRAL

# Or use as Python module
python -m carf_toolkit --root ./CENTRAL
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| A | Approve current file |
| R | Reject current file |
| S | Skip to next file |
| E | Toggle editor mode |
| V | Validate current file |
| J/K | Navigate files (vim-like) |
| F5 | Rescan directory |
| Esc | Exit editor mode |

## Dependencies

- PySide6 >= 6.6.0
- markdown >= 3.5.0
- pyyaml >= 6.0
- rich >= 13.0

Optional (for full functionality):
- carf_validator (in .scripts directory)
- carf_tree_sync (in .scripts directory)

## Project Structure

```
carf_toolkit/
├── __init__.py
├── __main__.py
├── models/
│   ├── __init__.py
│   └── file_item.py
├── scanner/
│   ├── __init__.py
│   ├── discovery.py
│   └── parser.py
├── integration/
│   ├── __init__.py
│   ├── validator_bridge.py
│   └── tree_sync_bridge.py
├── export/
│   ├── __init__.py
│   └── aggregator.py
└── gui/
    ├── __init__.py
    ├── app.py
    ├── main_window.py
    ├── theme.py
    ├── settings_store.py
    ├── widgets/
    │   ├── __init__.py
    │   ├── tree_view.py
    │   ├── markdown_viewer.py
    │   ├── markdown_editor.py
    │   ├── info_panel.py
    │   ├── validation_panel.py
    │   ├── combined_right_panel.py
    │   ├── action_bar.py
    │   └── progress_header.py
    └── dialogs/
        ├── __init__.py
        ├── export_dialog.py
        ├── rejection_dialog.py
        └── sync_preview_dialog.py
```
