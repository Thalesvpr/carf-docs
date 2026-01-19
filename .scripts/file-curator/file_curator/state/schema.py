"""SQLite database schema definitions."""

SCHEMA_VERSION = 1

CREATE_SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    root_path TEXT NOT NULL,
    config_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT,
    total_files INTEGER DEFAULT 0,
    approved_count INTEGER DEFAULT 0,
    rejected_count INTEGER DEFAULT 0,
    skipped_count INTEGER DEFAULT 0,
    pending_count INTEGER DEFAULT 0
);
"""

CREATE_FILES_TABLE = """
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    path TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    file_hash TEXT NOT NULL,
    title TEXT,
    doc_type TEXT,
    frontmatter_modules TEXT DEFAULT '[]',
    frontmatter_epic TEXT,
    word_count INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'pending',
    review_count INTEGER DEFAULT 0,
    skip_count INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    last_reviewed_at TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    UNIQUE (session_id, relative_path)
);
"""

CREATE_REVIEWS_TABLE = """
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    session_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    decided_at TEXT NOT NULL,
    observations TEXT DEFAULT '',
    justification TEXT DEFAULT '',
    tags TEXT DEFAULT '[]',
    rendered_markdown TEXT DEFAULT '',
    metadata_json TEXT DEFAULT '{}',
    FOREIGN KEY (file_id) REFERENCES files(id),
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
"""

CREATE_ACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    file_path TEXT,
    performed_at TEXT NOT NULL,
    details_json TEXT DEFAULT '{}',
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
"""

CREATE_SCRIPT_EXECUTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS script_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    script_name TEXT NOT NULL,
    command TEXT NOT NULL,
    args TEXT DEFAULT '[]',
    working_dir TEXT,
    is_dry_run INTEGER DEFAULT 0,
    executed_at TEXT,
    exit_code INTEGER,
    stdout TEXT DEFAULT '',
    stderr TEXT DEFAULT '',
    approved INTEGER DEFAULT 0,
    approved_at TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
"""

CREATE_METADATA_TABLE = """
CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

# Indexes for common queries
CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_files_session_status ON files(session_id, status);",
    "CREATE INDEX IF NOT EXISTS idx_files_session_path ON files(session_id, relative_path);",
    "CREATE INDEX IF NOT EXISTS idx_reviews_session ON reviews(session_id);",
    "CREATE INDEX IF NOT EXISTS idx_reviews_file ON reviews(file_id);",
    "CREATE INDEX IF NOT EXISTS idx_actions_session ON actions(session_id);",
]


def create_schema(connection) -> None:
    """Create all database tables and indexes.

    Args:
        connection: SQLite database connection
    """
    cursor = connection.cursor()

    # Create tables
    cursor.execute(CREATE_SESSIONS_TABLE)
    cursor.execute(CREATE_FILES_TABLE)
    cursor.execute(CREATE_REVIEWS_TABLE)
    cursor.execute(CREATE_ACTIONS_TABLE)
    cursor.execute(CREATE_SCRIPT_EXECUTIONS_TABLE)
    cursor.execute(CREATE_METADATA_TABLE)

    # Create indexes
    for index_sql in CREATE_INDEXES:
        cursor.execute(index_sql)

    # Set schema version
    cursor.execute(
        "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
        ("schema_version", str(SCHEMA_VERSION)),
    )

    connection.commit()


def get_schema_version(connection) -> int:
    """Get the current schema version.

    Args:
        connection: SQLite database connection

    Returns:
        Schema version number or 0 if not set
    """
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT value FROM metadata WHERE key = ?", ("schema_version",))
        row = cursor.fetchone()
        return int(row[0]) if row else 0
    except Exception:
        return 0
