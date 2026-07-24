"""Lightweight, additive schema patches applied on startup.

Base.metadata.create_all() creates missing *tables* but never alters existing
ones. When we add a column to a model whose table already exists on a deployed
database (e.g. Postgres), the column must be added explicitly. This module does
that idempotently and additively — it only ever ADDs missing columns, never
drops, renames, or rewrites data. Safe to run on every startup.

Registered in main.py's lifespan, right after create_all().
"""

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

# table -> { column_name: "<column type + constraints DDL>" }
_ADDITIVE_COLUMNS = {
    "card_readings": {
        # Guided-session support added after the table first shipped.
        "session_mode": "VARCHAR(12) NOT NULL DEFAULT 'quick'",
        "session_json": "TEXT",
    },
}


def apply_additive_columns(engine: Engine) -> None:
    """Add any missing columns declared in _ADDITIVE_COLUMNS. No-ops when the
    table doesn't exist yet (create_all will have made it with all columns) or
    when every column is already present."""
    insp = inspect(engine)
    existing_tables = set(insp.get_table_names())

    for table, columns in _ADDITIVE_COLUMNS.items():
        if table not in existing_tables:
            continue
        have = {c["name"] for c in insp.get_columns(table)}
        missing = {name: ddl for name, ddl in columns.items() if name not in have}
        if not missing:
            continue
        # The check above is check-then-act: if two instances boot at once
        # (a deploy overlap, or multiple workers) both can see the column as
        # missing and both issue the ALTER. Run each in its own transaction and
        # treat "already exists" as success, so the loser of the race still
        # starts cleanly instead of crashing the app on startup.
        for name, ddl in missing.items():
            try:
                with engine.begin() as conn:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"))
            except Exception as exc:  # noqa: BLE001 — narrow check below
                if "already exists" in str(exc).lower() or "duplicate column" in str(exc).lower():
                    continue
                raise
