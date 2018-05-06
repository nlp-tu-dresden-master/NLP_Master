import nltk
from nlp_master.Operation import Operation
from nlp_master.TopicSet import TopicSet
from nlp_master.Corpora import Corpora


class FrequencyDistribution(Operation):

    def __init__(self, corp: Corpora):
        super().__init__(corpora=corp)
        self.keywords = dict()

    def extract_keywords(self) -> dict:
        """
        This function searches for most often occurring words in given corpus.
        :param corp: The corpora object
        :return: list of relevant words
        """
        result: dict = dict()
        all_words: dict = self.corpora.raw_corpora

        for alg_class in all_words:
            words = all_words[alg_class]
            freq_distribution = nltk.FreqDist(words)
            # add that shit to dict and save in instance variable!
            result.update({alg_class: freq_distribution})
        self.keywords = result
        return result
        # topic_set = TopicSet()
        # for alg in result:
        #     # add this to the new topicSet
        #     pass

    def visualize(self, **kwargs):
        pass
