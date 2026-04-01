# StoryCleaner.py
import os
os.environ["STANZA_RESOURCES_DIR"] = r"C:\Users\joeyp\stanza_resources"

from cltk import NLP
import re
import unicodedata

latin_nlp = NLP(language="lat", suppress_banner=True)

ACCENT_TO_MACRON = {
    # acute
    'á': 'ā', 'é': 'ē', 'í': 'ī', 'ó': 'ō', 'ú': 'ū',
    'Á': 'Ā', 'É': 'Ē', 'Í': 'Ī', 'Ó': 'Ō', 'Ú': 'Ū',
    # grave
    'à': 'ā', 'è': 'ē', 'ì': 'ī', 'ò': 'ō', 'ù': 'ū',
    'À': 'Ā', 'È': 'Ē', 'Ì': 'Ī', 'Ò': 'Ō', 'Ù': 'Ū',
    # circumflex
    'â': 'ā', 'ê': 'ē', 'î': 'ī', 'ô': 'ō', 'û': 'ū',
    'Â': 'Ā', 'Ê': 'Ē', 'Î': 'Ī', 'Ô': 'Ō', 'Û': 'Ū',
    # umlaut / diaeresis
    'ä': 'ā', 'ë': 'ē', 'ï': 'ī', 'ö': 'ō', 'ü': 'ū',
    'Ä': 'Ā', 'Ë': 'Ē', 'Ï': 'Ī', 'Ö': 'Ō', 'Ü': 'Ū',
    # TODO: add tilde (ã ẽ ĩ õ ũ) and breve (ă ĕ ĭ ŏ ŭ) if needed
}

def normalize_accents(text: str) -> str:
    """
    Converts accented vowels (acute, grave, circumflex, umlaut) to their
    macron equivalents, so CLTK receives properly macronized Latin.
    """
    return ''.join(ACCENT_TO_MACRON.get(c, c) for c in text)

def strip_macrons(text):
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )

def load_story(input_path: str) -> list:
    """
    Reads a Latin story from a text file, extracts and lemmatizes all unique words.

    Args:
        input_path: Path to the story .txt file.

    Returns:
        A sorted list of (lemma, original_word) tuples.
    """
    print("\nLoading story...\n")
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Word count stats — use same tokenization as get_lemmas so counts are consistent
    text_for_stats = re.sub(r"-\n", "", text)
    text_for_stats = re.sub(r"[^\w\s]", " ", text_for_stats)
    raw_words = [w.lower().strip() for w in text_for_stats.split() if w.isalpha()]
    total_words = len(raw_words)
    unique_words = len(set(raw_words))
    print(f"Total words in story:    {total_words}")
    print(f"Unique words in story:   {unique_words}")

    lemma_pairs = get_lemmas(text)
    print(f"Unique lemmas extracted: {len(lemma_pairs)}")
    return lemma_pairs

def get_lemmas(text: str) -> list:
    """
    Takes a raw Latin text string and returns a sorted list of (lemma, original_word) tuples.
    The original_word is the first story form that produced this lemma.

    Analyzes the whole text in one CLTK call so the model has full sentence
    context when lemmatizing — more stable than word-by-word analysis.

    Args:
        text: Raw Latin text.

    Returns:
        A sorted list of (lemma, original_word) tuples.
    """
    # Convert accent variants (acute, grave, circumflex, umlaut) to macrons
    # so CLTK receives the standard macronized forms it was trained on
    text = normalize_accents(text)

    # Rejoin words hyphenated across line breaks (e.g. "ma-\ngister" → "magister")
    # Punctuation is kept so CLTK can use sentence boundaries for better accuracy
    text = re.sub(r"-\n", "", text)

    print("Analyzing text with CLTK (this may take a moment for longer stories)...")
    doc = latin_nlp.analyze(text=text)

    seen = set()
    lemma_pairs = []

    for word in doc.words:
        if not word.string or not word.string.isalpha():
            continue
        original = strip_macrons(word.string.lower().strip())
        lemma = strip_macrons((word.lemma or original).lower().strip())
        if not lemma:
            continue
        if lemma not in seen:
            seen.add(lemma)
            lemma_pairs.append((lemma, original))

    return sorted(lemma_pairs, key=lambda x: x[0])