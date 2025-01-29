from indicnlp.tokenize import indic_tokenize
from indicnlp.stopwords import stopwords

# Load the Hindi stop words
hindi_stopwords = stopwords.get_stopwords('hi')

# Example Hindi text corpus
corpus = "मुझे कंप्यूटर विज्ञान पढ़ना बहुत पसंद है और यह बहुत मजेदार है।"

# Tokenize the corpus using indic-nlp
words = list(indic_tokenize.trivial_tokenize(corpus))

# Remove stopwords
filtered_sentence = [word for word in words if word not in hindi_stopwords]

# Join the filtered words back into a sentence
filtered_corpus = ' '.join(filtered_sentence)

print("Original Sentence:", corpus)
print("Filtered Sentence (without stopwords):", filtered_corpus)

