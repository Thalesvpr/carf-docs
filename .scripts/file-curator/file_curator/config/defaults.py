"""Default configuration values."""

DEFAULT_CONFIG = {
    "scan": {
        "include_patterns": ["**/*.md"],
        "exclude_dirs": [
            ".git",
            ".obsidian",
            ".scripts",
            "SRC-CODE",
            "node_modules",
            "file-curator",
            "__pycache__",
            ".venv",
            "venv",
        ],
    },
    "paths": {
        "data_dir": "data",
        "templates_dir": "templates",
        "reviews_dir": "data/reviews",
    },
    "review": {
        "require_observations": False,
        "require_justification_on_reject": True,
        "skip_returns_to_queue": True,
    },
    "scripts": {
        "enabled": True,
        "require_approval": True,
        "default_to_dry_run": True,
    },
    "tui": {
        "theme": "dark",
        "show_preview": True,
        "preview_max_lines": 20,
    },
}
