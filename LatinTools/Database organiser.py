"""
alphabetize_db.py
-----------------
Sorts the 'vocabulary' table in master_key.db alphabetically by 'lemma'
and reassigns sequential IDs starting from 0.

Usage:
    python alphabetize_db.py                    # uses default path below
    python alphabetize_db.py my_database.db     # or pass a path as argument
"""

import sqlite3
import shutil
import sys
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────
DEFAULT_DB_PATH = r"master_key.db"   # change this if needed
TABLE          = "vocabulary"
SORT_COLUMN    = "lemma"
# ──────────────────────────────────────────────────────────────────────────────


def backup_db(db_path: Path) -> Path:
    """Create a timestamped backup before modifying anything."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path.with_name(f"{db_path.stem}_backup_{stamp}{db_path.suffix}")
    shutil.copy2(db_path, backup_path)
    print(f"  Backup saved → {backup_path.name}")
    return backup_path


def alphabetize(db_path: Path) -> None:
    print(f"\nOpening: {db_path}")

    backup_db(db_path)

    with sqlite3.connect(db_path, timeout=10) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Pull all rows sorted by lemma (case-insensitive)
        cur.execute(f"""
            SELECT lemma, entry, source, date_added
            FROM {TABLE}
            ORDER BY LOWER({SORT_COLUMN})
        """)
        rows = cur.fetchall()
        print(f"  Read {len(rows)} rows.")

        # Rebuild the table with fresh sequential IDs
        cur.execute(f"DELETE FROM {TABLE}")
        cur.executemany(
            f"""
            INSERT INTO {TABLE} (lemma, entry, source, date_added)
            VALUES (?, ?, ?, ?)
            """,
            [(r["lemma"], r["entry"], r["source"], r["date_added"]) for r in rows]
        )

        # Reset the autoincrement counter to match
        cur.execute(f"""
            UPDATE sqlite_sequence SET seq = ? WHERE name = ?
        """, (len(rows) - 1, TABLE))

        conn.commit()

    print(f"  Done. {len(rows)} rows re-inserted in alphabetical order by '{SORT_COLUMN}'.\n")

    # Quick preview
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT id, lemma FROM {TABLE} ORDER BY id LIMIT 10")
        print("  First 10 entries after sort:")
        print(f"  {'ID':<5} {'Lemma'}")
        print(f"  {'-'*5} {'-'*30}")
        for row in cur.fetchall():
            print(f"  {row[0]:<5} {row[1]}")


if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB_PATH
    db_path  = Path(path_arg)

    if not db_path.exists():
        print(f"Error: file not found → {db_path}")
        sys.exit(1)

    alphabetize(db_path)
