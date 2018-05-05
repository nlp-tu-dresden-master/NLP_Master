from abc import ABC, abstractmethod
from nlp_master import Corpora, TopicSet

class Operation(ABC):

    def __init__(self, corpora: Corpora):
        self.corpora = corpora

    @abstractmethod
    def extract_keywords(self) -> TopicSet:
        pass

    @abstractmethod
    def visualize(self, **kwargs):
        pass
