import nltk
from nlp_master import Corpora
from nlp_master import SynsetVocab
from nlp_master import TFIDF


class TopicEngine:

    def __init__(self, corpora: Corpora, vocab: SynsetVocab):
        if not isinstance(corpora, Corpora):
            raise ValueError("Invalid argument! Instance of Corpora excepted as parameter!")
        self.corpora = corpora
        self.vocab = vocab

    def generate_topics(self):
        """
        This function should create all Topics!
        For each topic there should be one TopicSet that will be created!
        :return:
        """
        encoded_corpora: Corpora = self.convert_corpora()

        pass

    def convert_corpora(self):
        encoded_dict: dict = dict()
        for algorithm_class in self.corpora.raw_corpora:
            encoded_text = self.vocab.encode(self.corpora.raw_corpora[algorithm_class])
            encoded_dict.update({algorithm_class: encoded_text})
        encoded_corpora = Corpora(encoded=encoded_dict)
        return encoded_corpora
