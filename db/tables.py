from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from db.base import metadata

repos = Table(
    "repos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String, unique=True, index=True),
    Column("last_scanned_sha", String, nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
)

commits = Table(
    "commits",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("sha", String, unique=True, index=True),
    Column("repo_id", Integer, ForeignKey("repos.id")),
    Column("date", DateTime),
    Column("scanned", Boolean, default=False),
)

findings = Table(
    "findings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("commit_id", Integer, ForeignKey("commits.id")),
    Column("type", String),
    Column("masked_value", String),
    Column("file_path", String),
    Column("line_no", Integer),
    Column("created_at", DateTime, server_default=func.now()),
)