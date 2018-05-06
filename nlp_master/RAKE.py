from nlp_master.Operation import Operation
from nlp_master.Corpora import Corpora


class RAKE(Operation):

    def __init__(self, corp: Corpora):
        if not isinstance(corp, Corpora):
            raise ValueError("Parameter 'corp' needs to be instance of class Corpora!")
        super().__init__(corp)
        self.keywords = dict()

    def extract_keywords(self):
        pass

    def visualize(self, **kwargs):
        pass
