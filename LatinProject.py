from cltk import NLP
import re
import unicodedata




# -------- File Paths --------
input_path = r"C:\Users\User\Desktop\Latin Stories in\input.txt"
master_key_path = r"C:\Users\User\Desktop\Latin Stories in\master_key_clean.txt"
output_path = r"C:\Users\User\Desktop\Latin Stories out\vocab_output.txt"

def normalize_word(word):
    # remove punctuation
    word = word.lower().rstrip(",;:.")

    # remove macrons
    word = unicodedata.normalize("NFD", word)
    word = "".join(c for c in word if unicodedata.category(c) != "Mn")
    word = unicodedata.normalize("NFC", word)

    return word


# Initialize Latin NLP
latin_nlp = NLP(language="lat", suppress_banner=True)

# -------- Accent Normalization --------
def normalize_accents(text):
    text = unicodedata.normalize("NFD", text)

    text = "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
    )

    text = unicodedata.normalize("NFC", text)

    return text
# -------- Macron Remover ---------
def remove_macrons(text):
    text = unicodedata.normalize("NFD", text)

    text = "".join(
        c for c in text
        if unicodedata.category(c) != "Mn"
    )

    return unicodedata.normalize("NFC", text)

# -------- Lemmatization Function --------
def lemmatize_paragraph(paragraph):
    paragraph = normalize_accents(paragraph)

    paragraph = re.sub(r"[^\w\sāēīōūĀĒĪŌŪ]", "", paragraph)

    doc = latin_nlp.analyze(text=paragraph)

    lemmas = []
    for word in doc.words:
        if word.lemma:
            lemmas.append(word.lemma.lower())

    return lemmas





# -------- Load Master Key as Dictionary --------
master_key = {}

with open(master_key_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        headword = line.split()[0]
        headword = normalize_word(headword)

        master_key[headword] = line

principal_parts = {}

with open(master_key_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        # split off definition part
        parts_section = line.split(";")[0]

        # split principal parts
        parts = [p.strip() for p in parts_section.split(",")]

        for part in parts:
            key = normalize_word(part)
            principal_parts[key] = line
            
# -------- Read Input File --------
with open(input_path, "r", encoding="utf-8") as f:
    paragraph = f.read()


# -------- Process Text --------
lemma_list = lemmatize_paragraph(paragraph)

lemma_list = sorted(set(lemma_list))


# -------- Output File --------


output_lines = []

for lemma in lemma_list:

    lookup = normalize_word(lemma)

    if lookup in master_key:
        output_lines.append(master_key[lookup])

    elif lookup in principal_parts:
        output_lines.append(principal_parts[lookup])

    else:
        print("\nUnknown word:", lemma)

        entry = input("Enter vocab entry (or press enter to skip): ")

        if entry.strip():

            output_lines.append(entry)

            master_key[lookup] = entry

            with open(master_key_path, "a", encoding="utf-8") as f:
                f.write(entry + "\n")

        else:
            output_lines.append(f"{lemma} (NOT IN MASTER KEY)")

# -------- Write Output File --------
with open(output_path, "w", encoding="utf-8") as f:
    for line in output_lines:
        f.write(line + "\n")


print("Vocabulary list written to file.")