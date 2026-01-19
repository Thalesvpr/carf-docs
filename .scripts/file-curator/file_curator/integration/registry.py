"""Registry of available scripts from .scripts/."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ScriptInfo:
    """Information about an available script."""

    name: str
    description: str
    module_path: str
    supports_dry_run: bool = False
    is_destructive: bool = False
    required_args: list[str] | None = None
    optional_args: list[str] | None = None

    @property
    def help_text(self) -> str:
        """Generate help text for the script."""
        lines = [
            f"**{self.name}**",
            self.description,
        ]

        if self.required_args:
            lines.append(f"Required: {', '.join(self.required_args)}")

        if self.optional_args:
            lines.append(f"Optional: {', '.join(self.optional_args)}")

        if self.supports_dry_run:
            lines.append("Supports --dry-run")

        if self.is_destructive:
            lines.append("WARNING: This script modifies files")

        return "\n".join(lines)


class AvailableScriptsRegistry:
    """Registry of available scripts in the .scripts/ directory."""

    # Known scripts with their metadata
    KNOWN_SCRIPTS = {
        "carf_validator": ScriptInfo(
            name="carf_validator",
            description="Validate CARF documentation files",
            module_path=".scripts.carf_validator",
            supports_dry_run=False,
            is_destructive=False,
            optional_args=["--file", "--verbose", "--json"],
        ),
        "carf_tree_sync": ScriptInfo(
            name="carf_tree_sync",
            description="Synchronize README index with directory structure",
            module_path=".scripts.carf_tree_sync",
            supports_dry_run=True,
            is_destructive=True,
            optional_args=["--dry-run", "--verbose"],
        ),
        "doc_generator": ScriptInfo(
            name="doc_generator",
            description="Generate documentation from templates",
            module_path=".scripts.doc_generator",
            supports_dry_run=True,
            is_destructive=True,
            required_args=["template", "output"],
            optional_args=["--dry-run"],
        ),
    }

    def __init__(self, scripts_dir: Optional[Path] = None):
        """Initialize the registry.

        Args:
            scripts_dir: Path to .scripts directory
        """
        self.scripts_dir = scripts_dir
        self._available: dict[str, ScriptInfo] = {}
        self._scanned = False

    def scan(self) -> None:
        """Scan for available scripts."""
        self._available = {}

        # Add known scripts that exist
        for name, info in self.KNOWN_SCRIPTS.items():
            if self._script_exists(name):
                self._available[name] = info

        self._scanned = True

    def _script_exists(self, name: str) -> bool:
        """Check if a script exists.

        Args:
            name: Script name

        Returns:
            True if the script exists
        """
        if self.scripts_dir is None:
            return name in self.KNOWN_SCRIPTS

        # Check for module directory
        module_dir = self.scripts_dir / name
        if module_dir.is_dir():
            init_file = module_dir / "__init__.py"
            main_file = module_dir / "__main__.py"
            return init_file.exists() or main_file.exists()

        # Check for single file module
        module_file = self.scripts_dir / f"{name}.py"
        return module_file.exists()

    def get(self, name: str) -> Optional[ScriptInfo]:
        """Get script info by name.

        Args:
            name: Script name

        Returns:
            ScriptInfo or None
        """
        if not self._scanned:
            self.scan()
        return self._available.get(name)

    def list_all(self) -> list[ScriptInfo]:
        """List all available scripts.

        Returns:
            List of ScriptInfo objects
        """
        if not self._scanned:
            self.scan()
        return list(self._available.values())

    def list_names(self) -> list[str]:
        """List names of available scripts.

        Returns:
            List of script names
        """
        if not self._scanned:
            self.scan()
        return list(self._available.keys())

    def is_available(self, name: str) -> bool:
        """Check if a script is available.

        Args:
            name: Script name

        Returns:
            True if available
        """
        if not self._scanned:
            self.scan()
        return name in self._available

    def get_destructive_scripts(self) -> list[ScriptInfo]:
        """Get list of scripts that modify files.

        Returns:
            List of destructive scripts
        """
        if not self._scanned:
            self.scan()
        return [s for s in self._available.values() if s.is_destructive]

    def get_safe_scripts(self) -> list[ScriptInfo]:
        """Get list of read-only scripts.

        Returns:
            List of safe scripts
        """
        if not self._scanned:
            self.scan()
        return [s for s in self._available.values() if not s.is_destructive]
