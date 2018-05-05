import nltk
from nlp_master import Operation
from nlp_master import Corpora
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from multiset import Multiset
from nlp_master import TopicSet


class FrequencyDistribution(Operation):

    def __init__(self, corp: Corpora):
        Operation.__init__(self, corp)
        self.keywords = dict()

    def extract_keywords(self, corp: Corpora) -> None:
        """
        This function searches for most often occurring words in given corpus.
        :param corp: The corpora object
        :return: list of relevant words
        """
        result:dict = dict()
        stop_words = list(stopwords.words("english"))
        all_words: dict = corp.build_tokenized_corpora()
        lemmatizer = WordNetLemmatizer()

        for alg_class in all_words:
            words = all_words[alg_class]

            # remove stopwords
            relevant_words = [lemmatizer.lemmatize(w.lower()) for w in words if w.lower() not in stop_words]
            relevant_words = [x for x in relevant_words if x not in stopwords]

            freq_distribution = nltk.FreqDist(relevant_words)
            # add that shit to dict and save in instance variable!
            result.update({alg_class: freq_distribution})

        topic_set = TopicSet()
        for alg in result:
            # add this to the new topicSet
            pass


    def visualize(self, **kwargs):
        pass
