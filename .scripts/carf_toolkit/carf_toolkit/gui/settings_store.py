"""Persistent settings storage for remembering user preferences."""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime


class SettingsStore:
    """Store and retrieve persistent application settings."""

    def __init__(self, settings_file: Optional[Path] = None):
        """Initialize the settings store.

        Args:
            settings_file: Path to settings file
        """
        if settings_file is None:
            # Store in the package data directory
            module_dir = Path(__file__).parent.parent.parent
            self.settings_file = module_dir / "data" / "settings.json"
        else:
            self.settings_file = settings_file

        self._settings: dict = {}
        self._load()

    def _load(self) -> None:
        """Load settings from file."""
        if self.settings_file.exists():
            try:
                self._settings = json.loads(
                    self.settings_file.read_text(encoding="utf-8")
                )
            except (json.JSONDecodeError, OSError):
                self._settings = {}
        else:
            self._settings = {}

    def _save(self) -> None:
        """Save settings to file."""
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        self.settings_file.write_text(
            json.dumps(self._settings, indent=2),
            encoding="utf-8",
        )

    # Last directory
    def get_last_directory(self) -> Optional[str]:
        """Get the last used directory."""
        return self._settings.get("last_directory")

    def set_last_directory(self, path: str) -> None:
        """Set the last used directory."""
        self._settings["last_directory"] = path
        self._save()

    # Window geometry
    def get_window_geometry(self) -> Optional[dict]:
        """Get saved window geometry."""
        return self._settings.get("window_geometry")

    def set_window_geometry(
        self, x: int, y: int, width: int, height: int
    ) -> None:
        """Save window geometry."""
        self._settings["window_geometry"] = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
        }
        self._save()

    # Generic get/set
    def get(self, key: str, default=None):
        """Get a setting value."""
        return self._settings.get(key, default)

    def set(self, key: str, value) -> None:
        """Set a setting value."""
        self._settings[key] = value
        self._save()
