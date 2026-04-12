"""Session logging with Rich console output and file persistence."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.logging import RichHandler
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class SessionLogger:
    """Logger for curation sessions with stdout and file output.

    Provides structured logging in the format:
    [timestamp] ACTION key=value key=value ...
    """

    def __init__(
        self,
        log_dir: Optional[Path] = None,
        session_id: Optional[str] = None,
    ):
        """Initialize the logger.

        Args:
            log_dir: Directory for log files
            session_id: Current session ID
        """
        self.log_dir = log_dir
        self.session_id = session_id
        self._file_handler: Optional[logging.FileHandler] = None

        # Set up logging
        self.logger = logging.getLogger("file_curator")
        self.logger.setLevel(logging.INFO)

        # Clear existing handlers
        self.logger.handlers.clear()

        # Console handler with Rich if available
        if RICH_AVAILABLE:
            console = Console(force_terminal=True)
            handler = RichHandler(
                console=console,
                show_time=True,
                show_path=False,
                markup=True,
                rich_tracebacks=True,
            )
        else:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )

        self.logger.addHandler(handler)

    def set_session(self, session_id: str) -> None:
        """Set the current session and configure file logging.

        Args:
            session_id: Session ID
        """
        self.session_id = session_id

        # Remove old file handler
        if self._file_handler:
            self.logger.removeHandler(self._file_handler)
            self._file_handler.close()

        # Add new file handler
        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)
            log_file = self.log_dir / f"session_{session_id}.log"
            self._file_handler = logging.FileHandler(log_file, encoding="utf-8")
            self._file_handler.setFormatter(
                logging.Formatter("[%(asctime)s] %(message)s")
            )
            self.logger.addHandler(self._file_handler)

    def _format_params(self, **kwargs) -> str:
        """Format parameters as key=value pairs.

        Args:
            **kwargs: Parameters to format

        Returns:
            Formatted string
        """
        parts = []
        for key, value in kwargs.items():
            if value is not None:
                # Quote strings with spaces
                if isinstance(value, str) and " " in value:
                    value = f'"{value}"'
                parts.append(f"{key}={value}")
        return " ".join(parts)

    def log_session_start(self, session_id: str, name: str) -> None:
        """Log session start.

        Args:
            session_id: Session ID
            name: Session name
        """
        self.set_session(session_id)
        params = self._format_params(id=session_id, name=name)
        self.logger.info(f"SESSION_START {params}")

    def log_session_resume(self, session_id: str, name: str) -> None:
        """Log session resume.

        Args:
            session_id: Session ID
            name: Session name
        """
        self.set_session(session_id)
        params = self._format_params(id=session_id, name=name)
        self.logger.info(f"SESSION_RESUME {params}")

    def log_session_end(self, session_id: str) -> None:
        """Log session end.

        Args:
            session_id: Session ID
        """
        params = self._format_params(id=session_id)
        self.logger.info(f"SESSION_END {params}")

    def log_session_complete(self, session_id: str) -> None:
        """Log session completion.

        Args:
            session_id: Session ID
        """
        params = self._format_params(id=session_id)
        self.logger.info(f"SESSION_COMPLETE {params}")

    def log_file_presented(self, path: str, index: int, total: int) -> None:
        """Log file presentation.

        Args:
            path: File path
            index: Current index
            total: Total files
        """
        params = self._format_params(path=path, index=f"{index}/{total}")
        self.logger.info(f"FILE_PRESENTED {params}")

    def log_decision(
        self,
        decision: str,
        path: str,
        observations: Optional[str] = None,
    ) -> None:
        """Log a review decision.

        Args:
            decision: Decision made (APPROVED, REJECTED, SKIPPED)
            path: File path
            observations: Optional observations
        """
        params = self._format_params(
            decision=decision,
            path=path,
            observations=observations if observations else None,
        )
        self.logger.info(f"DECISION {params}")

    def log_script_suggested(self, script: str, target: str) -> None:
        """Log script suggestion.

        Args:
            script: Script name
            target: Target file
        """
        params = self._format_params(script=script, target=target)
        self.logger.info(f"SCRIPT_SUGGESTED {params}")

    def log_script_approved(self, script: str, command: str) -> None:
        """Log script approval.

        Args:
            script: Script name
            command: Full command
        """
        params = self._format_params(script=script, command=command)
        self.logger.info(f"SCRIPT_APPROVED {params}")

    def log_script_completed(
        self,
        script: str,
        exit_code: int,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Log script completion.

        Args:
            script: Script name
            exit_code: Process exit code
            duration_ms: Execution duration
        """
        params = self._format_params(
            script=script,
            exit_code=exit_code,
            duration_ms=f"{duration_ms:.0f}" if duration_ms else None,
        )
        self.logger.info(f"SCRIPT_COMPLETED {params}")

    def log_error(self, message: str, **kwargs) -> None:
        """Log an error.

        Args:
            message: Error message
            **kwargs: Additional parameters
        """
        params = self._format_params(**kwargs) if kwargs else ""
        if params:
            self.logger.error(f"ERROR {message} {params}")
        else:
            self.logger.error(f"ERROR {message}")

    def log_warning(self, message: str, **kwargs) -> None:
        """Log a warning.

        Args:
            message: Warning message
            **kwargs: Additional parameters
        """
        params = self._format_params(**kwargs) if kwargs else ""
        if params:
            self.logger.warning(f"WARNING {message} {params}")
        else:
            self.logger.warning(f"WARNING {message}")

    def log_info(self, message: str, **kwargs) -> None:
        """Log an info message.

        Args:
            message: Info message
            **kwargs: Additional parameters
        """
        params = self._format_params(**kwargs) if kwargs else ""
        if params:
            self.logger.info(f"INFO {message} {params}")
        else:
            self.logger.info(f"INFO {message}")
