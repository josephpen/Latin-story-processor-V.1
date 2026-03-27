# MasterKeyUpdater.py
# Module: adds newly entered unknown words into the SQLite database.
# Includes a review step before saving — approve, edit, or skip each entry.

import sqlite3
from datetime import date

def review_new_entries(new_entries: list) -> list:
    """
    Shows all new entries and lets the user approve, edit, or skip each one.

    Args:
        new_entries: List of (lemma, entry) tuples to review.

    Returns:
        A filtered/edited list of (lemma, entry) tuples approved for saving.
    """
    print("\n" + "=" * 60)
    print(f"  REVIEW — {len(new_entries)} new word(s) to add to the database")
    print("=" * 60)

    for i, (lemma, entry) in enumerate(new_entries):
        print(f"\n  [{i + 1} of {len(new_entries)}]")
        print(f"  Lemma : {lemma}")
        print(f"  Entry : {entry}")

    print("\n" + "-" * 60)
    print("Options for each entry:  [a] Approve  [e] Edit  [s] Skip")
    print("-" * 60)

    approved = []

    for i, (lemma, entry) in enumerate(new_entries):
        print(f"\n  [{i + 1}] {lemma} | {entry}")
        while True:
            choice = input("  Action [a/e/s]: ").strip().lower()
            if choice == "a":
                approved.append((lemma, entry))
                print(f"  ✔  Approved.")
                break
            elif choice == "e":
                new_entry = input(f"  New entry for '{lemma}': ").strip()
                if new_entry:
                    approved.append((lemma, new_entry))
                    print(f"  ✔  Updated and approved.")
                else:
                    print("  ⚠️  No entry given — skipping.")
                break
            elif choice == "s":
                print(f"  ✖  Skipped.")
                break
            else:
                print("  Please enter 'a', 'e', or 's'.")

    return approved


def update_master_key(results: list, vocab_dict: dict, db_path: str):
    """
    Finds any lemmas in results that were not in the original vocab_dict
    (i.e. entered manually by the user), runs a review step, then inserts
    approved entries into the database.

    Args:
        results:    List of (lemma, entry) tuples from VocabLookup.
        vocab_dict: The original loaded vocabulary dictionary.
        db_path:    Path to the master_key.db file.
    """
    # Find entries that were manually added (not in the original dict)
    new_entries = [
        (lemma, entry)
        for lemma, entry in results
        if lemma not in vocab_dict
    ]

    if not new_entries:
        print("\nNo new words to add to the database.")
        return

    # Review step — user approves, edits, or skips each entry
    approved = review_new_entries(new_entries)

    if not approved:
        print("\nNo entries approved — nothing saved to database.")
        return

    # Insert approved entries into the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    inserted = 0
    for lemma, entry in approved:
        try:
            cursor.execute(
                "INSERT INTO vocabulary (lemma, entry, source, date_added) VALUES (?, ?, ?, ?)",
                (lemma, entry, "manual", str(date.today()))
            )
            inserted += 1
        except sqlite3.IntegrityError:
            print(f"⚠️  '{lemma}' already exists in database — skipping.")

    conn.commit()
    conn.close()

    print(f"\n{inserted} new word(s) saved to the database:")
    for lemma, entry in approved:
        print(f"  + {lemma} | {entry}")