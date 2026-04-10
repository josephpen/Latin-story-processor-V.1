# main.py
import sys
import os

# Build paths relative to wherever this script lives — works on any machine
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

from MasterKeyLoader import load_vocab_dict
from StoryCleaner import load_story
from VocabLookUp import lookup_lemmas
from ResultsWriter import write_results
from MasterKeyUpdater import update_master_key

# ── Configuration ──────────────────────────────────────────────────────────────
DB_PATH          = os.path.join(BASE_DIR, "master_key.db")
STORY_INPUT_PATH = os.path.join(BASE_DIR, "Latin stories in", "input.txt")
OUTPUT_FOLDER    = os.path.join(BASE_DIR, "Latin Stories Out")

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    vocab_dict = load_vocab_dict(DB_PATH, verbose=True)
    lemma_pairs = load_story(STORY_INPUT_PATH)
    print("\nLooking up lemmas...\n")
    results = lookup_lemmas(lemma_pairs, vocab_dict)
    write_results(results, OUTPUT_FOLDER, filename="output.txt")
    update_master_key(results, vocab_dict, DB_PATH)
    print("\nDone.")

if __name__ == "__main__":
    main()