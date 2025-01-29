# Import necessary modules
# import sys
# sys.path.append('C:/Users/Administrator/indic_nlp_library/indic_nlp_resources/indic_nlp_library/')
from indicnlp import common
common.set_resources_path('C:/Users/Administrator/indic_nlp_library/indic_nlp_resources/indic_nlp_library/indicnlp/')

from indicnlp.tokenize import sentence_tokenize, indic_tokenize


# Example text in Hindi
text = "भारत एक महान देश है। हम विविधता में एकता का अनुभव करते हैं।"

# Sentence Tokenization
sentences = sentence_tokenize.sentence_split(text, lang='hi')
print("Sentence Tokenization:")
for sentence in sentences:
    print(sentence)

# Word Tokenization
words = indic_tokenize.trivial_tokenize(text)
print("\nWord Tokenization:")
for word in words:
    print(word)
