import math
from nltk import bigrams, trigrams
from nlp_master.Corpora import Corpora
from nlp_master.Operation import Operation
from nlp_master.TopicSet import TopicSet


class TFIDF(Operation):

    def __init__(self, corp: Corpora):
        if not isinstance(corp, Corpora):
            raise ValueError("Invalid argument! Instance of Corpora excepted as parameter!")
        super().__init__(corpora=corp)
        self.keywords = dict()

    def frequency(self, word: str, document: list) -> int:
        return document.count(word)

    def number_of_words(self, doc: list) -> int:
        return len(doc)

    def term_frequency(self, word: str, document: list) -> float:
        return float(self.frequency(word, document) / self.number_of_words(document))

    def number_of_docs_containing_word(self, word: str, documents: list) -> float:
        count: int = 0
        for document in documents:
            if self.frequency(word, document) > 0:
                count += 1
        return count

    def inverse_document_freq(self, word: str, documents: list) -> float:
        # log(Total number of documents / number of docs with the term)
        return math.log(len(documents) / self.number_of_docs_containing_word(word, documents))

    def extract_keywords(self) -> dict:  # Should return TopicSet!
        """
        This method uses the tf-idf algorithm to determine the most relevant words in Corpus
        """
        """
        Defining all helper functions for tf*idf algorithm
        """

        result_dict: dict = {}
        vocabulary: list = []
        algorithms = list(self.corpora.raw_corpora)

        for algorithm_class in self.corpora.raw_corpora:
            sents = self.corpora.raw_corpora[algorithm_class]
            words: list = list()
            for sent in sents:
                words.extend(sent)
            self.corpora.raw_corpora.update({algorithm_class: words})

        documents: list = [self.corpora.raw_corpora[i] for i in algorithms]

        for i, tokens in enumerate(documents):
            doc_id = "{}".format(algorithms[i].lower())

            bigram_tokens = bigrams(tokens)  # Returns list of tupels
            bigram_tokens = [' '.join(token) for token in bigram_tokens]

            trigram_tokens: list = trigrams(tokens)  # Returns list of tupels
            trigram_tokens: list = [' '.join(token) for token in trigram_tokens]

            all_tokens: list = []
            all_tokens.extend(tokens)
            all_tokens.extend(bigram_tokens)
            all_tokens.extend(trigram_tokens)

            vocabulary.append(all_tokens)
            result_dict.update({doc_id: {}})

            for j, token in enumerate(all_tokens):
                result_dict[doc_id].update({token: {}})
                term_freq: float = self.term_frequency(token, all_tokens)
                result_dict[doc_id][token].update({'term_frequency': term_freq})

        for doc in result_dict:
            for token in result_dict[doc]:
                # Calculating IDF
                result_dict[doc][token].update(
                    {"inverse_document_frequency": self.inverse_document_freq(token, vocabulary)})
                # Calculating TF-IDF
                result_dict[doc][token].update(
                    {"tf-idf": result_dict[doc][token]["term_frequency"] * result_dict[doc][token][
                        "inverse_document_frequency"]})

        # Build new dict with only "token -> tf-idf"
        # TODO Can be included in upper for loop for less code and little bit faster execution
        words = {}
        for doc in result_dict:
            words.update({doc: {}})
            for token in result_dict[doc]:
                if token not in words[doc]:
                    words[doc].update({token: result_dict[doc][token]['tf-idf']})
                else:
                    if result_dict[doc][token]['tf-idf'] > words[doc][token]:
                        words[doc].update({token: result_dict[doc][token]['tf-idf']})

        for doc in words:
            words[doc] = sorted(words[doc].items(), key=lambda entry: entry[1], reverse=True)
            print("\n###### Results for algorithm: " + doc + " ######")
            for i, token_and_score in enumerate(words[doc]):
                print(token_and_score)
                if i == 14:
                    break
        self.keywords = words
        return words

    def visualize(self, **kwargs) -> None:
        pass
