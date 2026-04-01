# main.py
import sys
sys.path.append(r"C:\Users\User\Latin Stories")


from MasterKeyLoader import load_vocab_dict
from StoryCleaner import load_story
from VocabLookUp import lookup_lemmas
from ResultsWriter import write_results
from MasterKeyUpdater import update_master_key

# ── Configuration ──────────────────────────────────────────────────────────────
DB_PATH          = r"C:\Users\joeyp\Latin-story-processor-V.1\master_key.db"
STORY_INPUT_PATH = r"C:\Users\joeyp\Latin-story-processor-V.1\Latin stories in\input.txt"
OUTPUT_FOLDER    = r"C:\Users\joeyp\Latin-story-processor-V.1\Latin Stories Out"
# ── Main ───────────────────────────────────────────────────────────────────────
def main():

    # Load vocabulary dictionary from database
    vocab_dict = load_vocab_dict(DB_PATH, verbose=True)

    # Load and clean story — returns (lemma, original_word) tuplesy
    lemma_pairs = load_story(STORY_INPUT_PATH)

    # Look up each lemma in the dictionary
    print("\nLooking up lemmas...\n")
    results = lookup_lemmas(lemma_pairs, vocab_dict)

    # Write results to output folder
    write_results(results, OUTPUT_FOLDER, filename="output.txt")

    # Add any unknown words to the database
    update_master_key(results, vocab_dict, DB_PATH)

    print("\nDone.")

if __name__ == "__main__":
    main()