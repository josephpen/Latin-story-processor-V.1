# lemma_debug.py
# Quick tool to lemmatize any word or sentence and see the result.

from cltk import NLP
import unicodedata
import re

latin_nlp = NLP(language="lat", suppress_banner=True)

def strip_macrons(text):
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )

def lemmatize_input(text):
    text_clean = re.sub(r"[^\w\s]", " ", text)
    words = text_clean.split()

    print(f"\n{'Original':<20} {'Lemma':<20}")
    print("-" * 40)

    for word in words:
        word = word.lower().strip()
        if not word or not word.isalpha():
            continue
        doc = latin_nlp.analyze(text=word)
        lemma = word
        if doc.words and doc.words[0].lemma:
            lemma = strip_macrons(doc.words[0].lemma.lower().strip())
        print(f"{word:<20} {lemma:<20}")

print("Latin Lemmatizer Debug Tool")
print("Type a word or sentence, or 'quit' to exit.\n")

while True:
    user_input = input("Enter word(s): ").strip()
    if user_input.lower() in ("quit", "exit", "q"):
        print("Goodbye.")
        break
    if user_input:
        lemmatize_input(user_input)
