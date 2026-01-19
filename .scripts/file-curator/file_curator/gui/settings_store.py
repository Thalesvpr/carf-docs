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
            settings_file: Path to settings file (default: data/settings.json)
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

    # Last session
    def get_last_session_id(self) -> Optional[str]:
        """Get the last used session ID."""
        return self._settings.get("last_session_id")

    def set_last_session_id(self, session_id: str) -> None:
        """Set the last used session ID."""
        self._settings["last_session_id"] = session_id
        self._settings["last_session_time"] = datetime.now().isoformat()
        self._save()

    # Recent sessions (history)
    def get_recent_sessions(self, limit: int = 10) -> list[dict]:
        """Get list of recent sessions.

        Returns:
            List of dicts with session_id, name, root_path, last_used
        """
        return self._settings.get("recent_sessions", [])[:limit]

    def add_recent_session(
        self, session_id: str, name: str, root_path: str
    ) -> None:
        """Add a session to recent history."""
        recent = self._settings.get("recent_sessions", [])

        # Remove if already exists
        recent = [s for s in recent if s.get("session_id") != session_id]

        # Add to front
        recent.insert(0, {
            "session_id": session_id,
            "name": name,
            "root_path": root_path,
            "last_used": datetime.now().isoformat(),
        })

        # Keep only last 10
        self._settings["recent_sessions"] = recent[:10]
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
