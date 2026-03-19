from cltk import NLP

latin_nlp = NLP(language="lat", suppress_banner=True)

# -------- File Paths --------
input_path = r"C:\Users\User\Desktop\Latin Stories in\master_key.txt"
output_path = r"C:\Users\User\Desktop\Latin Stories out\master_key_clean.txt"


# -------- Read Entries --------
with open(input_path, "r", encoding="utf-8") as f:
    entries = [line.strip() for line in f if line.strip()]


seen_lemmas = set()
clean_entries = []


for entry in entries:

    # get first word
    headword = entry.split()[0].rstrip(",;:")

    # lemmatize
    doc = latin_nlp.analyze(text=headword)

    lemma = headword.lower()
    if doc.words and doc.words[0].lemma:
        lemma = doc.words[0].lemma.lower()

    # check duplicates by lemma
    if lemma not in seen_lemmas:
        clean_entries.append(entry)
        seen_lemmas.add(lemma)


# -------- Write Clean File --------
with open(output_path, "w", encoding="utf-8") as f:
    for entry in clean_entries:
        f.write(entry + "\n")


print("Lemma-based clean master key created.")