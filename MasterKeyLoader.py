# MasterKeyLoader.py
# Module: loads the vocabulary dictionary from the SQLite database.

import sqlite3

def load_vocab_dict(db_path: str, verbose: bool = True) -> dict:
    """
    Loads the full vocabulary dictionary from the SQLite database.

    Args:
        db_path:  Path to the master_key.db file.
        verbose:  If True, prints a loading summary.

    Returns:
        A dict mapping lemma (str) -> entry (str).
    """
    if verbose:
        print(f"Loading vocabulary from database...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT lemma, entry FROM vocabulary")
    rows = cursor.fetchall()
    conn.close()

    vocab_dict = {lemma: entry for lemma, entry in rows}

    if verbose:
        print(f"Dictionary loaded with {len(vocab_dict)} entries.")

    return vocab_dict