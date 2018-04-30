import os
from nltk.tokenize import RegexpTokenizer


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
    # token_corpora = dict()
    # raw_corpora = dict()
    # document_corpora = dict()

    def __init__(self, names: list, paths: list):
        """
        Builds the complete corpora dictionary.
        Lists 'paths' and 'names' needs to have same sorting.
        :param paths: List of all dict_paths, where the required.txt files are stored.
        :param names: List of all names of the algorithms.
        """

        self.token_corpora = dict()
        self.raw_corpora = dict()
        self.document_corpora = dict()

        for i, path in enumerate(paths):
            # print(path)
            # print(names[i])
            self.build_tokenized_corpus(names[i], path)
            self.build_raw_corpus(names[i], path)
            self.build_document_corpus(names[i], path)

    def build_tokenized_corpus(self, name: str, directory: str) -> None:
        """
        This function builds a list with all words of the resulting corpus. The corpus will be created
        based on all .txt files that are stored in the supplied directory.
        :param directory: path (string) to directory
        :param name: Name of the algorithm
        :return: void
        """
        list_of_all_words = []
        for file in os.listdir(directory):
            # print(file)
            if os.path.isfile(os.path.join(directory, file)) and file.split(".")[1] == "txt":
                text = open(os.path.join(directory, file), "r", encoding="utf-8").read()
                tokenizer = RegexpTokenizer(r'\w+')
                words = tokenizer.tokenize(text)
                list_of_all_words = list_of_all_words + words
        self.token_corpora.update({name: list_of_all_words}) # Why using the set_XX method and not this?

    def build_raw_corpus(self, name: str, directory: str):
        all_text = ""
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and file.split(".")[1] == "txt":
                text = open(os.path.join(directory, file), "r", encoding="utf-8").read()
                all_text = all_text + " " + text

        self.raw_corpora.update({name.lower(): all_text})

    def build_document_corpus(self, name: str, directory: str):
        documents = []
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and file.split(".")[1] == "txt":
                text = open(os.path.join(directory, file), "r", encoding="utf-8").read()
                documents.append(text)
        self.document_corpora.update({name.lower(): documents})

    # Useful when adding a new corpus to the class and want to have all corpora types at once
    def build_all_corpora_for_new_algorithm_type(self, name: str, path: str):
        """
        This function creates all available corpora types for a new algorithm type.
        :param name: Name of the algorithm to be created. If already exists - it will be updated
        :param path: Path to the documents
        :return: void
        """
        self.build_document_corpus(name, path)
        self.build_raw_corpus(name, path)
        self.build_tokenized_corpus(name, path)

    # We can discuss about the method name. Firstly I tought about the purpose of this function
    def get_corpus_by_class(self, name: str, type: str = "raw") -> list:
        """
        Returns the corpus of the desired algorithm. Available types: raw, document, token
        :param name: Name of the algorithm to be returned
        :param type: Algorithm type to be returned
        :return: list
        """
        if type == "raw":
            return self.raw_corpora[name.lower()]
        elif type == "document":
            return self.document_corpora[name.lower()]
        else:
            return self.token_corpora[name.lower()]

    # Look at the playground. Its easier to use corpora.attribute_name
    def get_all_algorithms(self, type: str = "raw"):
        if type == "raw":
            return self.raw_corpora.keys()
        elif type == "document":
            return self.document_corpora.keys()
        else:
            return self.token_corpora.keys()