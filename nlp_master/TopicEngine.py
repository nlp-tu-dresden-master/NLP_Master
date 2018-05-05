import nltk
from nlp_master import Corpora
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk.wsd import lesk


class TopicEngine:

    def __init__(self, corpora: Corpora):
        if not isinstance(corpora, Corpora):
            raise ValueError("Invalid argument! Instance of Corpora excepted as parameter!")
        self.corpora = corpora

    def generate_topics(self):
        """
        This function should create all Topics!
        For each topic there should be one TopicSet that will be created!
        :return:
        """
        pass
