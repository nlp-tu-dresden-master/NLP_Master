import nltk
from nlp_master.Operation import Operation
from nlp_master.Corpora import Corpora
from nlp_master.TopicSet import TopicSet


class FrequencyDistribution(Operation):

    def __init__(self, corp: Corpora):
        super().__init__(corpora=corp)
        self.topics = dict()
        self.freq_dists: dict = dict()

    def extract_keywords(self) -> dict:
        """
        This function searches for most often occurring words in given corpus.
        :return: list of relevant words
        """
        result: dict = dict()
        all_words: dict = self.corpora.raw_corpora

        for alg_class in all_words:
            sents: list = all_words[alg_class]
            # All kinds of stopwords and punctuations are stored as 0
            words: list = [item for sublist in sents for item in sublist if item != "0"]
            # print("words without 0:")
            # print(words)
            freq_distribution = nltk.FreqDist(words)
            sorted_distribution = sorted(freq_distribution.items(), key=lambda entry: entry[1], reverse=True)
            topic_set = TopicSet(class_name=alg_class)
            for number, count in sorted_distribution:
                topic_set.add_keyword(keyword=number, rank=count, algorithm="FreqDist")
            topic_set.norm_ranks()
            result.update({alg_class: topic_set})

            self.freq_dists.update({alg_class: freq_distribution})
        self.topics = result
        return result

    def visualize(self, amount: int=15):
        if not isinstance(amount, int):
            raise ValueError("Please insert integer as parameter for visualize function!")
        for alg in self.freq_dists:
            self.freq_dists[alg].plot(amount)
