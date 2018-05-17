import nltk
from models.Corpora import Corpora
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk.wsd import lesk
import re
import math
from nltk import bigrams, trigrams


class Topic_Engine:

    def __init__(self, corpora: Corpora):
        self.corpora = corpora

    def get_most_common_tokens(self, name: str, amount: int) -> list:
        """
        This function searches for most relevant words in given corpus.
        :param name: Name of the algorithm to get keywords from.
        :return: list of relevant words
        """
        text = self.corpora.raw_corpora[name.lower()]
        # Tokenize without punctuation
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(text)

        # remove stopwords
        stop_words = list(stopwords.words("english"))
        relevant_words = [w.lower() for w in words if w.lower() not in stop_words]

        # Lemmatize words
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(w) for w in relevant_words]

        freq_distribution = nltk.FreqDist(lemmatized_words)
        print("Top {} {} Terms:".format(amount, name.lower()))
        print(freq_distribution.most_common(amount))
        return freq_distribution.most_common(amount)

    def get_frequency_distribution_of_word_meanings(self, name: str, amount: int):
        text = self.corpora.raw_corpora[name.lower()]
        sentences = sent_tokenize(text)
        reg_tokenizer = RegexpTokenizer(r'\w+')
        # List of Lists with tokenized words
        token_sent = [reg_tokenizer.tokenize(sentence) for sentence in sentences]
        stop_words = list(stopwords.words("english"))
        lemmatizer = WordNetLemmatizer()
        # TODO Lemmatize with pos tag!!! -> Yields way better results
        new_sent_list = []
        temp_sent_list = []
        for i, sent in enumerate(token_sent):
            temp_sent_list.append([lemmatizer.lemmatize(w.lower()) for w in sent if w.lower() not in stop_words])
            new_sent_list.append([lesk(" ".join(temp_sent_list[i]), w) for w in temp_sent_list[i]])
            # for j, w in enumerate(temp_sent_list[i]):
            #     new_sent_list[i].append(lesk(" ".join(token_sent[i]), w))
        flat_list = [item for sublist in new_sent_list for item in sublist]
        # print(flat_list)
        freq_distribution = nltk.FreqDist(flat_list)
        print("Top {} {} Terms:".format(amount, name.lower()))
        print(freq_distribution.most_common(amount))
        return freq_distribution.most_common(amount)

    # Kind of useless to use tf_idf function.
    # Finds best word to distinguish the documents in the corpus. -> Want to have words that combine these documents
    def tf_idf(self, algorithms: list) -> dict:
        """
        This method uses the tf-idf algorithm to determine the most relevant words in Corpus
        :return: list
        """
        """
        Defining all helper functions for tf*idf algorithm
        """
        def frequency(word: str, document: list) -> int:
            return document.count(word)

        def number_of_words(doc: str) -> int:
            return len(doc)

        def term_frequency(word: str, document: list) -> float:
            return float(frequency(word, document) / number_of_words(document))

        def number_of_docs_containing_word(word: str, documents: list) -> float:
            count: = 0
            for document in documents:
                if frequency(word, document) > 0:
                    count += 1
            return count

        def inverse_document_freq(word: str, documents: list) -> float:
            # log(Total number of documents / number of docs with the term)
            return math.log(len(documents) / number_of_docs_containing_word(word, documents))

        stopwords = nltk.corpus.stopwords.words('english')
        lemmatizer = WordNetLemmatizer()

        result_dict: dict = {}
        vocabulary: list = []
        documents: list = [self.corpora.token_corpora[i.lower()] for i in algorithms]  # Already tokenized with RegExp

        for i, tokens in enumerate(documents):
            doc_id = "{}".format(algorithms[i].lower())
            # Double cleaning ugly but necessary because there are lemmatized words, lemmatized to "the"
            cleaned_tokens: list = [lemmatizer.lemmatize(token.lower()) for token in tokens if token not in stopwords]
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
                term_freq: float = term_frequency(token, all_tokens)
                result_dict[doc_id][token].update({'term_frequency': term_freq})

        for doc in result_dict:
            for token in result_dict[doc]:
                # Calculating IDF
                result_dict[doc][token].update({"inverse_document_frequency": inverse_document_freq(token, vocabulary)})
                # Calculating TF-IDF
                result_dict[doc][token].update(
                    {"tf-idf": result_dict[doc][token]["term_frequency"] * result_dict[doc][token]["inverse_document_frequency"]})

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

