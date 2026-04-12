"""Configuration settings."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

from .defaults import DEFAULT_CONFIG


@dataclass
class ScanConfig:
    """Scan configuration."""

    include_patterns: list[str] = field(
        default_factory=lambda: DEFAULT_CONFIG["scan"]["include_patterns"]
    )
    exclude_dirs: list[str] = field(
        default_factory=lambda: DEFAULT_CONFIG["scan"]["exclude_dirs"]
    )

    @classmethod
    def from_dict(cls, data: dict) -> "ScanConfig":
        """Create from dictionary."""
        return cls(
            include_patterns=data.get(
                "include_patterns", DEFAULT_CONFIG["scan"]["include_patterns"]
            ),
            exclude_dirs=data.get(
                "exclude_dirs", DEFAULT_CONFIG["scan"]["exclude_dirs"]
            ),
        )


@dataclass
class PathsConfig:
    """Paths configuration."""

    data_dir: str = DEFAULT_CONFIG["paths"]["data_dir"]
    templates_dir: str = DEFAULT_CONFIG["paths"]["templates_dir"]
    reviews_dir: str = DEFAULT_CONFIG["paths"]["reviews_dir"]

    @classmethod
    def from_dict(cls, data: dict) -> "PathsConfig":
        """Create from dictionary."""
        return cls(
            data_dir=data.get("data_dir", DEFAULT_CONFIG["paths"]["data_dir"]),
            templates_dir=data.get(
                "templates_dir", DEFAULT_CONFIG["paths"]["templates_dir"]
            ),
            reviews_dir=data.get("reviews_dir", DEFAULT_CONFIG["paths"]["reviews_dir"]),
        )


@dataclass
class ReviewConfig:
    """Review configuration."""

    require_observations: bool = DEFAULT_CONFIG["review"]["require_observations"]
    require_justification_on_reject: bool = DEFAULT_CONFIG["review"][
        "require_justification_on_reject"
    ]
    skip_returns_to_queue: bool = DEFAULT_CONFIG["review"]["skip_returns_to_queue"]

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewConfig":
        """Create from dictionary."""
        return cls(
            require_observations=data.get(
                "require_observations",
                DEFAULT_CONFIG["review"]["require_observations"],
            ),
            require_justification_on_reject=data.get(
                "require_justification_on_reject",
                DEFAULT_CONFIG["review"]["require_justification_on_reject"],
            ),
            skip_returns_to_queue=data.get(
                "skip_returns_to_queue",
                DEFAULT_CONFIG["review"]["skip_returns_to_queue"],
            ),
        )


@dataclass
class ScriptsConfig:
    """Scripts configuration."""

    enabled: bool = DEFAULT_CONFIG["scripts"]["enabled"]
    require_approval: bool = DEFAULT_CONFIG["scripts"]["require_approval"]
    default_to_dry_run: bool = DEFAULT_CONFIG["scripts"]["default_to_dry_run"]

    @classmethod
    def from_dict(cls, data: dict) -> "ScriptsConfig":
        """Create from dictionary."""
        return cls(
            enabled=data.get("enabled", DEFAULT_CONFIG["scripts"]["enabled"]),
            require_approval=data.get(
                "require_approval", DEFAULT_CONFIG["scripts"]["require_approval"]
            ),
            default_to_dry_run=data.get(
                "default_to_dry_run", DEFAULT_CONFIG["scripts"]["default_to_dry_run"]
            ),
        )


@dataclass
class TUIConfig:
    """TUI configuration."""

    theme: str = DEFAULT_CONFIG["tui"]["theme"]
    show_preview: bool = DEFAULT_CONFIG["tui"]["show_preview"]
    preview_max_lines: int = DEFAULT_CONFIG["tui"]["preview_max_lines"]

    @classmethod
    def from_dict(cls, data: dict) -> "TUIConfig":
        """Create from dictionary."""
        return cls(
            theme=data.get("theme", DEFAULT_CONFIG["tui"]["theme"]),
            show_preview=data.get("show_preview", DEFAULT_CONFIG["tui"]["show_preview"]),
            preview_max_lines=data.get(
                "preview_max_lines", DEFAULT_CONFIG["tui"]["preview_max_lines"]
            ),
        )


@dataclass
class CuratorConfig:
    """Main configuration class."""

    scan: ScanConfig = field(default_factory=ScanConfig)
    paths: PathsConfig = field(default_factory=PathsConfig)
    review: ReviewConfig = field(default_factory=ReviewConfig)
    scripts: ScriptsConfig = field(default_factory=ScriptsConfig)
    tui: TUIConfig = field(default_factory=TUIConfig)

    @classmethod
    def from_dict(cls, data: dict) -> "CuratorConfig":
        """Create from dictionary."""
        return cls(
            scan=ScanConfig.from_dict(data.get("scan", {})),
            paths=PathsConfig.from_dict(data.get("paths", {})),
            review=ReviewConfig.from_dict(data.get("review", {})),
            scripts=ScriptsConfig.from_dict(data.get("scripts", {})),
            tui=TUIConfig.from_dict(data.get("tui", {})),
        )

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "CuratorConfig":
        """Load configuration from file.

        Args:
            config_path: Path to config file (YAML or JSON)

        Returns:
            CuratorConfig instance
        """
        if config_path is None:
            return cls()

        if not config_path.exists():
            return cls()

        try:
            content = config_path.read_text(encoding="utf-8")
            if config_path.suffix in (".yaml", ".yml"):
                data = yaml.safe_load(content) or {}
            else:
                import json
                data = json.loads(content)
            return cls.from_dict(data)
        except Exception:
            return cls()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "scan": {
                "include_patterns": self.scan.include_patterns,
                "exclude_dirs": self.scan.exclude_dirs,
            },
            "paths": {
                "data_dir": self.paths.data_dir,
                "templates_dir": self.paths.templates_dir,
                "reviews_dir": self.paths.reviews_dir,
            },
            "review": {
                "require_observations": self.review.require_observations,
                "require_justification_on_reject": self.review.require_justification_on_reject,
                "skip_returns_to_queue": self.review.skip_returns_to_queue,
            },
            "scripts": {
                "enabled": self.scripts.enabled,
                "require_approval": self.scripts.require_approval,
                "default_to_dry_run": self.scripts.default_to_dry_run,
            },
            "tui": {
                "theme": self.tui.theme,
                "show_preview": self.tui.show_preview,
                "preview_max_lines": self.tui.preview_max_lines,
            },
        }

    def save(self, config_path: Path) -> None:
        """Save configuration to file.

        Args:
            config_path: Path to save to
        """
        config_path.parent.mkdir(parents=True, exist_ok=True)
        content = yaml.dump(self.to_dict(), default_flow_style=False)
        config_path.write_text(content, encoding="utf-8")

    def get_data_path(self, root: Path) -> Path:
        """Get the data directory path.

        Args:
            root: Root directory

        Returns:
            Data directory path
        """
        return root / self.paths.data_dir

    def get_templates_path(self, root: Path) -> Path:
        """Get the templates directory path.

        Args:
            root: Root directory

        Returns:
            Templates directory path
        """
        return root / self.paths.templates_dir

    def get_reviews_path(self, root: Path) -> Path:
        """Get the reviews directory path.

        Args:
            root: Root directory

        Returns:
            Reviews directory path
        """
        return root / self.paths.reviews_dir

    def get_db_path(self, root: Path) -> Path:
        """Get the database file path.

        Args:
            root: Root directory

        Returns:
            Database file path
        """
        return self.get_data_path(root) / "curator.db"

    def get_data_dir(self, root: Path) -> Path:
        """Get the data directory path.

        Alias for get_data_path for consistency.

        Args:
            root: Root directory

        Returns:
            Data directory path
        """
        return self.get_data_path(root)
