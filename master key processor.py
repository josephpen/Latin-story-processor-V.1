from cltk import NLP
import unicodedata

latin_nlp = NLP(language="lat", suppress_banner=True)

# -------- File Paths --------
input_path = r"C:\Users\User\Desktop\Latin Stories V1\master_key_clean.V1.txt"
output_path = r"C:\Users\User\Desktop\Latin Stories out\master_key_V.2.txt"


# -------- Read Entries --------

def strip_macrons(text):
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


with open(input_path, "r", encoding="utf-8") as f:
    entries = [line.strip() for line in f if line.strip()]


seen_lemmas = set()
clean_entries = []


for entry in entries:

    # get first word
    headword = entry.split(";", 1)[0].strip()

    # lemmatize
    doc = latin_nlp.analyze(text=headword)

    lemma = headword.lower()
    if doc.words and doc.words[0].lemma:
        lemma = strip_macrons(doc.words[0].lemma.lower().strip())

    # check duplicates by lemma
    if lemma not in seen_lemmas:

        new_entry = f"{lemma} | {entry}"

        clean_entries.append(new_entry)
        seen_lemmas.add(lemma)

# -------- Write Clean File --------
with open(output_path, "w", encoding="utf-8") as f:
    for entry in clean_entries:
        f.write(entry + "\n")


print("Lemma-based clean master key created.")