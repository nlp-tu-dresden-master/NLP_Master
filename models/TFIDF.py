import math
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import bigrams, trigrams
from models.Corpora import Corpora


class TFIDF:  # Should be TFIDF(Operations)

    def __init__(self):
        pass

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

    def extract_keywords(self, corpora: Corpora):  # Should return TopicSet!
        """
        This method uses the tf-idf algorithm to determine the most relevant words in Corpus
        """
        """
        Defining all helper functions for tf*idf algorithm
        """
        stopwords = nltk.corpus.stopwords.words('english')
        lemmatizer = WordNetLemmatizer()

        result_dict: dict = {}
        vocabulary: list = []
        tokenized_corpora = corpora.build_tokenized_corpora()  # Already tokenized with RegExp Tokenizer
        algorithms = tokenized_corpora.keys()

        documents: list = [tokenized_corpora[i.lower()] for i in algorithms]

        for i, tokens in enumerate(documents):
            doc_id = "{}".format(algorithms[i].lower())
            # Double cleaning ugly but necessary because there are lemmatized words, lemmatized to "the"
            cleaned_tokens: list = [lemmatizer.lemmatize(token.lower()) for token in tokens if
                                    token not in stopwords]
            cleaned_tokens = [t for t in cleaned_tokens if t not in stopwords]

            bigram_tokens = bigrams(cleaned_tokens)  # Returns list of tupels
            bigram_tokens = [' '.join(token) for token in bigram_tokens]

            trigram_tokens: list = trigrams(cleaned_tokens)  # Returns list of tupels
            trigram_tokens: list = [' '.join(token) for token in trigram_tokens]

            all_tokens: list = []
            all_tokens.extend(cleaned_tokens)
            all_tokens.extend(bigram_tokens)
            all_tokens.extend(trigram_tokens)

            vocabulary.append(all_tokens)

            result_dict.update({doc_id: {}})
            for i, token in enumerate(all_tokens):
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
        return words

    def visualize(self) -> None:
        pass
