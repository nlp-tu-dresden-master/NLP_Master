from nlp_master.Corpora import Corpora
from nlp_master.SynsetVocab import SynsetVocab
from nlp_master.TFIDF import TFIDF
from nlp_master.FrequencyDistribution import FrequencyDistribution
from nlp_master.RAKE import RAKE
from nlp_master.TextRank import TextRank
from nlp_master.TopicSet import TopicSet
import time


class TopicEngine:

    def __init__(self, corpora: Corpora, vocab: SynsetVocab):
        if not isinstance(corpora, Corpora):
            raise ValueError("Invalid argument! Instance of Corpora excepted as parameter!")
        self.corpora = corpora
        self.vocab = vocab

    def generate_topics(self, do_textRank: bool = True, do_rake: bool = True, do_FreqDist: bool = True, do_tfidf: bool = True) -> dict:
        """
        This function should create all Topics!
        For each topic there should be one TopicSet that will be created!
        :return: dict of all joined topic sets in the form of {al_class_1: topicSet_1,..., al_class_n: topicSet_n}
        """
        encoded_corpora: Corpora = self.convert_corpora()
        topic_sets_collection: list = list()
        if do_textRank:
            text_rank: TextRank = TextRank(encoded_corpora)
            text_rank_topics = text_rank.extract_keywords()
            topic_sets_collection.append(text_rank_topics)
        if do_rake:
            rake_time_0 = time.time()
            rake: RAKE = RAKE(encoded_corpora)
            rake_topics = rake.extract_keywords()
            topic_sets_collection.append(rake_topics)
            rake_time_total = time.time() - rake_time_0
            with open("rake_execution_time.txt", "w+") as file:
                file.write("Time for execution of RAKE algorithm: {} seconds".format(rake_time_total))
        if do_tfidf:
            tfidf_time_0 = time.time()
            tfidf: TFIDF = TFIDF(corp=encoded_corpora)
            tfidf_topics = tfidf.extract_keywords()
            topic_sets_collection.append(tfidf_topics)
            tfidf_time_total = time.time() - tfidf_time_0
            with open("tfidf_execution_time.txt", "w+") as file:
                file.write("Time for execution of TF*IDF algorithm: {} seconds".format(tfidf_time_total))
        if do_FreqDist:
            freq_time_0 = time.time()
            freq_dist: FrequencyDistribution = FrequencyDistribution(corp=encoded_corpora)
            freq_topics = freq_dist.extract_keywords()
            topic_sets_collection.append(freq_topics)
            freq_time_total = time.time() - freq_time_0
            with open("freq_execution_time.txt", "w+") as file:
                file.write("Time for execution of FrequencyDistribution algorithm: {} seconds".format(freq_time_total))

        # Combine the Topic Sets and decode them
        joined_topic_sets: dict = dict()
        if len(topic_sets_collection) > 0:
            for al_class in topic_sets_collection[0]:
                temp_topic = TopicSet(al_class)
                for i, dictionary in enumerate(topic_sets_collection):
                    temp_topic += dictionary[al_class]
                joined_topic_sets.update({al_class: temp_topic})

        joined_topic_sets = self.decode_topic_set(joined_topic_sets)
        return joined_topic_sets

    def decode_topic_set(self, topic_sets: dict) -> dict:
        decoded_result_dict: dict = dict()
        for key in topic_sets:
            decoded_topic = TopicSet(class_name=key)
            keywords = topic_sets[key].get_keywords(duplicates=True)
            for i, keyword in enumerate(keywords):
                number = keyword.keyword
                if number != "":
                    resulting_words = self.vocab.decode(str(number))
                    word = " ".join(resulting_words) if len(resulting_words) > 1 else resulting_words[0]
                    decoded_topic.add_keyword(word, keyword.rank, keyword.algorithm)
            decoded_result_dict.update({key: decoded_topic})
        for t in decoded_result_dict:
            decoded_result_dict[t].sort_by_rank()
        return decoded_result_dict

    def convert_corpora(self):
        encoded_dict: dict = dict()
        for algorithm_class in self.corpora.raw_corpora:
            encoded_sentences = self.vocab.encode(self.corpora.raw_corpora[algorithm_class])
            encoded_dict.update({algorithm_class: encoded_sentences})
        encoded_corpora = Corpora(encoded=encoded_dict)
        return encoded_corpora
