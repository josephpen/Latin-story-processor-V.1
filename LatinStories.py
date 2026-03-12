import os
os.environ["STANZA_RESOURCES_DIR"] = r"C:\Users\User\AppData\Local\StanfordNLP\stanza\Cache\1.11.0\resources"
from cltk import NLP
latin_nlp = NLP(language="lat")


import re
import unicodedata
from cltk import NLP

# Initialize Latin NLP pipeline
latin_nlp = NLP(language="lat")

# Map common acute accents to macrons
ACCENT_TO_MACRON = {
    "á": "ā", "é": "ē", "í": "ī", "ó": "ō", "ú": "ū",
    "Á": "Ā", "É": "Ē", "Í": "Ī", "Ó": "Ō", "Ú": "Ū"
}

def normalize_accents(text):
    for accented, macron in ACCENT_TO_MACRON.items():
        text = text.replace(accented, macron)
    return text

def lemmatize_paragraph(paragraph):
    # Step 1: Normalize accents
    paragraph = normalize_accents(paragraph)

    # Step 2: Remove punctuation (optional but useful)
    paragraph = re.sub(r"[^\w\sāēīōūĀĒĪŌŪ]", "", paragraph)

    # Step 3: Process with CLTK
    doc = latin_nlp.analyze(text=paragraph)

    # Step 4: Extract lemmas
    lemmas = []
    for word in doc.words:
        if word.lemma:  # Ignore None values
            lemmas.append(word.lemma.lower())

    return lemmas


# Example usage
paragraph = "Puella amat agricolám et boná fábulá narrat."

lemma_list = lemmatize_paragraph(paragraph)

print(lemma_list)