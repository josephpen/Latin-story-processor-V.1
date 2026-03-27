# migrate_to_db.py
# Run this ONCE to convert your master_key_V.2.txt into a SQLite database.
# Your original .txt file will not be modified.
 
import sqlite3
import os
 
TXT_INPUT_PATH = r"C:\Users\User\Desktop\Latin Stories In\master_key_V.2.txt"
DB_OUTPUT_PATH = r"C:\Users\User\Desktop\Latin Stories\master_key.db"
 
def migrate():
    # ── Read the .txt file ─────────────────────────────────────────────────────
    print(f"Reading {TXT_INPUT_PATH}...\n")
    entries = []
 
    with open(TXT_INPUT_PATH, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            original_line = line
            line = line.strip()
 
            if not line:
                continue
            if "|" not in line:
                print(f"[Line {line_number}] ⚠️  No '|' found → {original_line.strip()}")
                continue
 
            parts = line.split("|", 1)
            lemma, entry = parts[0].strip(), parts[1].strip()
 
            if not lemma or not entry:
                print(f"[Line {line_number}] ⚠️  Empty lemma or entry → {original_line.strip()}")
                continue
 
            entries.append((lemma, entry))
 
    print(f"{len(entries)} entries read from .txt file.")
 
    # ── Create the database and table ──────────────────────────────────────────
    os.makedirs(os.path.dirname(DB_OUTPUT_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_OUTPUT_PATH)
    cursor = conn.cursor()
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            lemma       TEXT    NOT NULL UNIQUE,
            entry       TEXT    NOT NULL,
            source      TEXT    NOT NULL DEFAULT 'master_key',
            date_added  TEXT    NOT NULL DEFAULT (DATE('now'))
        )
    """)
 
    # ── Insert all entries ─────────────────────────────────────────────────────
    duplicates = 0
    inserted = 0
 
    for lemma, entry in entries:
        try:
            cursor.execute(
                "INSERT INTO vocabulary (lemma, entry, source) VALUES (?, ?, ?)",
                (lemma, entry, "master_key")
            )
            inserted += 1
        except sqlite3.IntegrityError:
            print(f"⚠️  Duplicate lemma skipped: '{lemma}'")
            duplicates += 1
 
    conn.commit()
    conn.close()
 
    # ── Summary ────────────────────────────────────────────────────────────────
    print(f"\nMigration complete.")
    print(f"  Inserted:  {inserted} entries")
    print(f"  Skipped:   {duplicates} duplicates")
    print(f"  Database:  {DB_OUTPUT_PATH}")
 
if __name__ == "__main__":
    migrate()
 

