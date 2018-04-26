import os
from nltk.tokenize import RegexpTokenizer


class Corpora:
    """
    This class creates and contains all corpora of the different algorithms.
    Right now these are stored in a dict with the following form:
    {name_of_algorithm: list_of_words}
    """
    corpora = dict()

    # TODO Maybe use dictionary as well. Would be clear and needs no identical sorting.
    def __init__(self, names: list, paths: list):
        """
        Builds the complete corpora dictionary.
        Lists 'paths' and 'names' needs to have same sorting.
        :param paths: List of all paths, where the required .txt files are stored.
        :param names: List of all names of the algorithms.
        """
        for i, path in enumerate(paths):
            self.build_corpus(names[i], path)

    def build_corpus(self, name: str, directory: str):
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

        self.set_corpus(name, list_of_all_words)

    def get_corpus(self, name: str):
        """
        Returns the corpus of the desired algorithm
        :param name: Name of the algorithm to be returned
        :return: list
        """
        return self.corpora[name.lower()]

    def set_corpus(self, name: str, corpus: list):
        """
        Sets the supplied corpus in class dictionary corpora
        :param name: Name of the algorithm
        :param corpus: List of all words in the corpus
        :return: void
        """
        self.corpora.update({name.lower(): corpus})

    def get_all_corpora(self):
        return self.corpora

    def get_all_algorithms(self):
        return self.corpora.keys()