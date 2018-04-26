import nltk
from Corpora import Corpora
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class Topic_Engine:

    def __init__(self, corpora: Corpora):
        self.corpora = corpora

    def get_keywords_from_text(self, name: str, amount: int) -> list:
        """
        This function searches for most relevant words in given corpus.
        :param name: Name of the algorithm to get keywords from.
        :return: list of relevant words
        """

        # TODO TD-IDF and GitHub to get the relevant words in corpus
        # TODO Use Corpora and take algorithm name as input

        words = self.corpora.get_corpus(name)
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
