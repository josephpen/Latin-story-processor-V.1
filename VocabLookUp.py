# VocabLookup.py
# Module: checks each lemma against the vocab dictionary.
# Found entries are pulled from the dict.
# Missing entries prompt the user for manual input.
 
def lookup_lemmas(lemma_pairs: list, vocab_dict: dict) -> list:
    """
    For each (lemma, original_word) pair from the story, look up the lemma
    in the vocabulary dictionary. Displays the original story form alongside
    the lemma so you can see how the word appeared in the text.
 
    Args:
        lemma_pairs: List of (lemma, original_word) tuples from the story.
        vocab_dict:  Dict mapping lemma -> entry.
 
    Returns:
        A list of (lemma, entry) tuples.
    """
    results = []
    missing = []
 
    for lemma, original in lemma_pairs:
        # Show original story form alongside lemma (if different)
        if original != lemma:
            display = f"'{lemma}'  (from story: '{original}')"
        else:
            display = f"'{lemma}'"
 
        if lemma in vocab_dict:
            results.append((lemma, vocab_dict[lemma]))
        else:
            missing.append(lemma)
            print(f"⚠️  {display} not found in dictionary.")
            entry = input(f"   Enter entry for {display}: ").strip()
            results.append((lemma, entry))
 
    print(f"\nLookup complete. {len(lemma_pairs) - len(missing)} found, {len(missing)} entered manually.")
    return results

