from nlp_master.Corpora import Corpora
from nlp_master.SynsetVocab import SynsetVocab
from nlp_master.TFIDF import TFIDF
from nlp_master.FrequencyDistribution import FrequencyDistribution
from nlp_master.RAKE import RAKE
from nlp_master.TextRank import TextRank
import time


class TopicEngine:

    def __init__(self, corpora: Corpora, vocab: SynsetVocab):
        if not isinstance(corpora, Corpora):
            raise ValueError("Invalid argument! Instance of Corpora excepted as parameter!")
        self.corpora = corpora
        self.vocab = vocab

    def generate_topics(self, do_textRank: bool = True, do_rake: bool = True, do_FreqDist: bool = True, do_tfidf: bool = True):
        """
        This function should create all Topics!
        For each topic there should be one TopicSet that will be created!
        :return:
        """
        # TODO Decode all Keywords when TopicSets are returned of all functions
        encoded_corpora: Corpora = self.convert_corpora()

        if do_textRank:
            text_rank: TextRank = TextRank(encoded_corpora)
            text_rank_topics = text_rank.extract_keywords()
        if do_rake:
            rake_time_0 = time.time()
            rake: RAKE = RAKE(encoded_corpora)
            rake_topics = rake.extract_keywords()
            rake_time_total = time.time() - rake_time_0
            with open("rake_execution_time.txt", "w+") as file:
                file.write("Time for execution of RAKE algorithm: {} seconds".format(rake_time_total))
        if do_tfidf:
            tfidf_time_0 = time.time()
            tfidf: TFIDF = TFIDF(corp=encoded_corpora)
            tfidf_topics = tfidf.extract_keywords()
            tfidf_time_total = time.time() - tfidf_time_0
            with open("tfidf_execution_time.txt", "w+") as file:
                file.write("Time for execution of TF*IDF algorithm: {} seconds".format(tfidf_time_total))
        if do_FreqDist:
            freq_time_0 = time.time()
            freq_dist: FrequencyDistribution = FrequencyDistribution(corp=encoded_corpora)
            freq_topics = freq_dist.extract_keywords()
            freq_time_total = time.time() - freq_time_0
            with open("freq_execution_time.txt", "w+") as file:
                file.write("Time for execution of FrequencyDistribution algorithm: {} seconds".format(freq_time_total))
        if do_rake:
            pass
            # for rake_topic in rake_topics:
            #     rake_topics[rake_topic].pretty_print()

        # if do_tfidf:
        #     for tfidf_top in tfidf_topics:
        #         tfidf_topics[tfidf_top].pretty_print()

        if do_FreqDist:
            freq_dist.visualize(20)
        # TODO Combine Topics!
        return 2

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
