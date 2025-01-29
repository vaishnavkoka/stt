import nltk
from nltk import word_tokenize, TweetTokenizer
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
text="I'm eating food and drinking milk."
tokens=word_tokenize(text)
tokens=[word.lower() for word in tokens if word.isalpha()]
print("before stop words removal-->",tokens)
# tokens=[word for word in tokens if not word in stopwords.words("english")]
# print("after stop words removal-->",tokens)
print(stopwords.words("english"))