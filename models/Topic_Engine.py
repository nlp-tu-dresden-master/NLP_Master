import nltk
from models.Corpora import Corpora
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import datetime, sys
from sklearn.feature_extraction.text import TfidfVectorizer


class Topic_Engine:

    def __init__(self, corpora: Corpora):
        self.corpora = corpora

    def get_most_common_tokens(self, name: str, amount: int) -> list:
        """
        This function searches for most relevant words in given corpus.
        :param name: Name of the algorithm to get keywords from.
        :return: list of relevant words
        """
        text = self.corpora.get_corpus(name)
        # Tokenize without punctuation
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text)

        # remove stopwords
        stop_words = list(stopwords.words("english"))
        relevant_words = [w.lower() for w in words if w.lower() not in stop_words]

        # Lemmatize words
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(w) for w in relevant_words]

        freq_distribution = nltk.FreqDist(lemmatized_words)
        print("Top {} Clustering Terms:".format(amount))
        print(freq_distribution.most_common(amount))
        return freq_distribution.most_common(amount)

    # Kind of useless to use tf_idf function.
    # Finds best word to distinguish the documents in the corpus. -> Want to have words that combine these documents
    def tf_idf(self):

        def tokenize_and_stem(text):
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(text)
            stop_words = list(stopwords.words("english"))
            relevant_words = [w.lower() for w in tokens if w.lower() not in stop_words]
            lemmatizer = WordNetLemmatizer()
            lemmatized_words = [lemmatizer.lemmatize(w) for w in relevant_words]
            return lemmatized_words

        documents = self.corpora.get_corpus("Clustering", "document")

        tfidf = TfidfVectorizer(tokenizer=tokenize_and_stem, stop_words='english', decode_error='ignore')
        print('building term-document matrix... [process started: ' + str(datetime.datetime.now()) + ']')
        sys.stdout.flush()

        tdm = tfidf.fit_transform(documents)  # this can take some time (about 60 seconds on my machine)
        print('done! [process finished: ' + str(datetime.datetime.now()) + ']')
        feature_names = tfidf.get_feature_names()
        print('TDM contains ' + str(len(feature_names)) + ' terms and ' + str(tdm.shape[0]) + ' documents')
        print('first 15 terms: ' + str(feature_names[0:14]))


# NER not useful here -> Do not want to find only entities but simple words
# NER definitely useful for getting the terms which to show in the example algorithm
# chunks = nltk.ne_chunk(nltk.pos_tag(words), binary=True)
# entities = [" ".join(w for w, t in elt) for elt in chunks if isinstance(elt, nltk.Tree)]
# print(entities)