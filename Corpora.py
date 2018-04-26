import os
from nltk.tokenize import RegexpTokenizer


class Corpora:
    """
    This class creates and contains all corpora of the different algorithms.
    Right now these are stored in a dict with the following form:
    {name_of_algorithm: list_of_words}
    """
    token_corpora = dict()
    raw_corpora = dict()
    document_corpora = dict()

    # TODO Maybe use dictionary as well. Would be clear and needs no identical sorting.
    # TODO replace building methods to simple calling methods not writing them in class attribute
    def __init__(self, names: list, paths: list):
        """
        Builds the complete corpora dictionary.
        Lists 'paths' and 'names' needs to have same sorting.
        :param paths: List of all paths, where the required .txt files are stored.
        :param names: List of all names of the algorithms.
        """
        for i, path in enumerate(paths):
            self.build_tokenized_corpus(names[i], path)
            self.build_raw_corpus(names[i], path)
            self.build_document_corpus(names[i], path)

    def build_tokenized_corpus(self, name: str, directory: str):
        """
        This function builds a list with all words of the resulting corpus. The corpus will be created
        based on all .txt files that are stored in the supplied directory.
        :param directory: path (string) to directory
        :param name: Name of the algorithm
        :return: void
        """
        list_of_all_words = []
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and file.split(".")[1] == "txt":
                text = open(os.path.join(directory, file), "r").read()
                tokenizer = RegexpTokenizer(r'\w+')
                words = tokenizer.tokenize(text)
                list_of_all_words = list_of_all_words + words

        self.set_corpus(name, list_of_all_words, "tokenized")

    def build_raw_corpus(self, name: str, directory: str):
        all_text = ""
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and file.split(".")[1] == "txt":
                text = open(os.path.join(directory, file), "r").read()
                all_text = all_text + " " + text
        self.set_corpus(name, all_text, "raw")

    def build_document_corpus(self, name: str, directory: str):
        documents = []
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and file.split(".")[1] == "txt":
                text = open(os.path.join(directory, file), "r").read()
                documents.append(text)
        self.document_corpora.update({name.lower(): documents})

    def get_corpus(self, name: str, type: str = "raw") -> list:
        """
        Returns the corpus of the desired algorithm. Available types: raw, document, token
        :param name: Name of the algorithm to be returned
        :return: list
        """
        if type == "raw":
            return self.raw_corpora[name.lower()]
        elif type == "document":
            return self.document_corpora[name.lower()]
        else:
            return self.token_corpora[name.lower()]

    def set_corpus(self, name: str, corpus: list, type: str = "raw"):
        """
        Sets the supplied corpus in class dictionary corpora. Available types: raw, document, token
        :param name: Name of the algorithm
        :param corpus: List of all words in the corpus
        :return: void
        """
        if type == "raw":
            self.raw_corpora.update({name.lower(): corpus})
        elif type == "document":
            self.document_corpora.update({name.lower(): corpus})
        else:
            self.token_corpora.update({name.lower(): corpus})

    def get_all_corpora(self, type: str = "raw"):
        if type == "raw":
            return self.raw_corpora
        elif type == "document":
            return self.document_corpora
        else:
            return self.token_corpora

    def get_all_algorithms(self, type: str = "raw"):
        if type == "raw":
            return self.raw_corpora.keys()
        elif type == "document":
            return self.document_corpora.keys()
        else:
            return self.token_corpora.keys()