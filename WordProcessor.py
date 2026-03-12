from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.lexicon.lat import LatinLewisLexicon

lemmatizer = LatinBackoffLemmatizer()
lexicon = LatinLewisLexicon()

word = input("Word: ")

lemma = lemmatizer.lemmatize([word])[0][1]

print("Lemma:", lemma)

meaning = lexicon.lookup(lemma)

if meaning:
    print("Meaning:", meaning[:200])  # print first 200 characters
else:
    print("Meaning not found.")