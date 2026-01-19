"""Template loader with fallback hierarchy."""

from pathlib import Path
from string import Template
from typing import Optional


class TemplateLoader:
    """Loads templates with a fallback hierarchy.

    Template lookup order:
    1. User-editable templates in templates/
    2. Session-specific templates in data/sessions/{id}/templates/
    3. Built-in defaults in file_curator/templates/defaults/
    """

    DEFAULT_TEMPLATES = {
        "review_card": """## ${file_title}

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
""",
        "decision_record": """---
file: ${relative_path}
decision: ${decision}
decided_at: ${decided_at}
---

# Review: ${file_title}

## Decision: ${decision_emoji} ${decision_label}

## Observations
${observations}

## Justification
${justification}

## Tags
${tags}
""",
        "summary_report": """# Curation Summary: ${session_name}

**Session ID:** ${session_id}
**Root Path:** ${root_path}
**Created:** ${created_at}
**Completed:** ${completed_at}

## Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Files | ${total_files} | 100% |
| Approved | ${approved_count} | ${approved_percent}% |
| Rejected | ${rejected_count} | ${rejected_percent}% |
| Remaining | ${remaining_count} | ${remaining_percent}% |

## Progress

${progress_bar}

## Decisions by Type

${decisions_by_type}

## Recent Activity

${recent_activity}
""",
    }

    def __init__(
        self,
        user_templates_dir: Optional[Path] = None,
        session_templates_dir: Optional[Path] = None,
        defaults_dir: Optional[Path] = None,
    ):
        """Initialize the loader.

        Args:
            user_templates_dir: Path to user-editable templates
            session_templates_dir: Path to session-specific templates
            defaults_dir: Path to built-in defaults
        """
        self.user_templates_dir = user_templates_dir
        self.session_templates_dir = session_templates_dir
        self.defaults_dir = defaults_dir

    def load(self, template_name: str) -> Template:
        """Load a template by name.

        Args:
            template_name: Name of the template (without .md extension)

        Returns:
            string.Template instance
        """
        content = self._load_content(template_name)
        return Template(content)

    def load_raw(self, template_name: str) -> str:
        """Load raw template content.

        Args:
            template_name: Name of the template

        Returns:
            Template content string
        """
        return self._load_content(template_name)

    def _load_content(self, template_name: str) -> str:
        """Load template content with fallback.

        Args:
            template_name: Name of the template

        Returns:
            Template content string
        """
        # Try user templates first
        if self.user_templates_dir:
            path = self.user_templates_dir / f"{template_name}.md"
            if path.exists():
                return path.read_text(encoding="utf-8")

        # Try session-specific templates
        if self.session_templates_dir:
            path = self.session_templates_dir / f"{template_name}.md"
            if path.exists():
                return path.read_text(encoding="utf-8")

        # Try built-in defaults directory
        if self.defaults_dir:
            path = self.defaults_dir / f"{template_name}.md"
            if path.exists():
                return path.read_text(encoding="utf-8")

        # Fall back to hardcoded defaults
        if template_name in self.DEFAULT_TEMPLATES:
            return self.DEFAULT_TEMPLATES[template_name]

        raise FileNotFoundError(f"Template not found: {template_name}")

    def list_available(self) -> list[str]:
        """List all available template names.

        Returns:
            List of template names
        """
        templates = set(self.DEFAULT_TEMPLATES.keys())

        for dir_path in [
            self.user_templates_dir,
            self.session_templates_dir,
            self.defaults_dir,
        ]:
            if dir_path and dir_path.exists():
                for path in dir_path.glob("*.md"):
                    templates.add(path.stem)

        return sorted(templates)

    def save_user_template(self, template_name: str, content: str) -> None:
        """Save a user template.

        Args:
            template_name: Name of the template
            content: Template content
        """
        if not self.user_templates_dir:
            raise ValueError("User templates directory not configured")

        self.user_templates_dir.mkdir(parents=True, exist_ok=True)
        path = self.user_templates_dir / f"{template_name}.md"
        path.write_text(content, encoding="utf-8")

    def template_exists(self, template_name: str) -> bool:
        """Check if a template exists.

        Args:
            template_name: Name of the template

        Returns:
            True if the template exists
        """
        try:
            self._load_content(template_name)
            return True
        except FileNotFoundError:
            return False
