from nlp_master.Corpora import Corpora
from nlp_master.SynsetVocab import SynsetVocab
from nlp_master.TFIDF import TFIDF
from nlp_master.FrequencyDistribution import FrequencyDistribution


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
        # print(encoded_corpora.raw_corpora)
        # freq_dist = FrequencyDistribution(corp=encoded_corpora)
        # freq_keywords = freq_dist.extract_keywords()
        # tfidf = TFIDF(corp=encoded_corpora)
        # tfidf_keywords = tfidf.extract_keywords()

    def convert_corpora(self, with_stopwords: bool = False):
        encoded_dict: dict = dict()
        for algorithm_class in self.corpora.raw_corpora:
            if with_stopwords:
                encoded_sentences = self.vocab.encode_for_rake(self.corpora.raw_corpora[algorithm_class])
            else:
                encoded_sentences = self.vocab.encode(self.corpora.raw_corpora[algorithm_class])
            encoded_dict.update({algorithm_class: encoded_sentences})
        encoded_corpora = Corpora(encoded=encoded_dict)
        return encoded_corpora
