import os
from nltk.tokenize import RegexpTokenizer
from nlp_master.SynsetVocab import SynsetVocab

"""
Notes encoding added --> Windows Laptops
"""


class Corpora:
    """
    This class creates and contains all corpora of the different algorithms.
    Right now these are stored in a dict with the following form:
    {name_of_algorithm: list_of_words}
    """
    """
    Think about it if a class attribute is useful. Imagine the case if we would initialize another corpus object. 
    That would mean that Corpus.token_corpora would hold both tokenized words from corpus object 1 and corpus object 2. 
    
    Issue: in my opinion this is quite dangerous because we would generate behavior that we maybe don't want. 
    Solution: using a magic method (__add__, __iadd__) to concatenate two corpus. 
    Notes: BTW the class attributes token_corpora, raw_corpora and document_corpora will always be empty.  
    """
    def __init__(self, names: list = list(), paths: list = list(), encoded: dict = None):
        """
        Builds the complete corpora dictionary.
        Lists 'paths' and 'names' needs to have same sorting.
        :param paths: List of all dict_paths, where the required.txt files are stored.
        :param names: List of all names of the algorithms.
        """
        if not isinstance(names, list):
            raise ValueError('Invalid argument! Parameter "names" must be of instance list!')
        if not isinstance(paths, list):
            raise ValueError('Invalid argument! Parameter "paths" must be of instance list!')

        # Required for document corpora
        self.__algorithm_names = names
        self.__paths = paths
        # Case difference if already encoded or raw
        if encoded is None:
            self.raw_corpora = dict()
            for i, path in enumerate(paths):
                self.build_raw_corpus(names[i], path)
        else:
            # Simply save the supplied corpora
            if isinstance(encoded, dict):
                self.raw_corpora = encoded
            else:
                raise ValueError("If a already encoded corpora should be created, please supply the complete dict.")

    def build_raw_corpus(self, name: str, directory: str):
        all_text = ""
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and file.split(".")[1] == "txt":
                text = open(os.path.join(directory, file), "r", encoding="utf-8").read()
                all_text = all_text + " " + text

        self.raw_corpora.update({name.lower(): all_text})

    def build_tokenized_corpora(self) -> dict:
        """
        This function builds a dict with all algorithms and lists of words of the corresponding raw corpus. The corpora
        will be created based on the raw corpora that is stored in instance variable.
        :return: dict
        """
        tokenizer = RegexpTokenizer(r'\w+')
        tokenzied_corpora: dict = dict()
        for algorithm in self.raw_corpora:
            tokenzied_corpora.update({algorithm.lower(): tokenizer.tokenize(self.raw_corpora[algorithm])})
        return tokenzied_corpora

    def build_document_corpora(self) -> dict:
        """
        This method builds a dictionary containing all corpora of the different algorithms in form of lists with
        the corresponding documents as strings.
        :return: dict
        """
        document_corpora = dict()
        for i, directory in enumerate(self.__paths):
            documents = []
            for file in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, file)) and file.split(".")[1] == "txt":
                    text = open(os.path.join(directory, file), "r", encoding="utf-8").read()
                    documents.append(text)
            document_corpora.update({self.__algorithm_names[i].lower(): documents})
        return document_corpora

    @property
    def algorithm_names(self):
        return [x.lower() for x in self.__algorithm_names]
