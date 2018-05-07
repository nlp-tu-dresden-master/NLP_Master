from abc import ABC, abstractmethod
from nlp_master.Corpora import Corpora
from nlp_master.TopicSet import TopicSet
from nlp_master.SynsetVocab import SynsetVocab


class Operation(ABC):

    def __init__(self, corpora: Corpora):
        if not isinstance(corpora, Corpora):
            raise ValueError("Invalid argument! Instance of Corpora excepted as parameter!")
        self.corpora = corpora

    @abstractmethod
    def extract_keywords(self) -> TopicSet:
        pass

    @abstractmethod
    def visualize(self, **kwargs):
        pass
