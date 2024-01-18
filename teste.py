from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

language = "portuguese"

for word in stopwords.words(language):
    print(word)