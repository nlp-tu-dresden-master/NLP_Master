import nltk
from models.Corpora import Corpora
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk.wsd import lesk


class TopicEngine:

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

    def generate_topics(self):
        """
        This function should create all Topics!
        For each topic there should be one TopicSet that will be created!
        :return:
        """
        pass
