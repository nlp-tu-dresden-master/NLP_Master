import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
import re
import string
"""
This class is used to hold a dictionary with the references from numbers to words and their meanings in our corpora
"""


class SynsetVocab:

    def __init__(self, raw_corp: dict):
        if not isinstance(raw_corp, dict):
            raise ValueError("Invalid argument! Instance of dict excepted as parameter!")
        self.synset_vocab = dict()
        self.word_vocab = dict()
        self.build_synset_and_word_vocab(raw_corp)

    def build_synset_and_word_vocab(self, raw_corp: dict) -> None:
        """
        This method builds two dictionaries:
        The synset_vocab dictionary contains all the different synsets/wsd that are contained in the raw corpora
        The word_vocab contains all the synsets as keys and the real words as values.
        This way we can go back from numbers to words if required.
        :param raw_corp: Raw Corpora of all algorithm types as dict
        :return: None
        """
        synset_vocab: dict = dict()
        word_vocab: dict = dict()
        all_wsds: list = list()
        all_cleaned_tokens: list = list()

        for alg in raw_corp:
            cleaned_sentences = self._preprocess_text(raw_corp[alg])
            # sentences: list = sent_tokenize(raw_corp[alg])
            for clean_sent in cleaned_sentences:
                all_cleaned_tokens.extend(clean_sent)
                raw_sentence = " ".join([w for w, t in clean_sent if w is not "stop"])

                for (word, tag) in clean_sent:
                    if word is not "stop":
                        wsd = lesk(raw_sentence, word, self.get_wordnet_pos(tag))
                    else:
                        wsd = "stop"
                    # Took list to have full index range afterwards
                    all_wsds.append(wsd)

        none_counter = 0
        for i, synset in enumerate(all_wsds):
            if synset is not None:
                # Word vocab
                if synset not in word_vocab.keys():
                    word_vocab.update({synset: {all_cleaned_tokens[i]}})
                else:
                    current_set_of_words = word_vocab[synset]
                    current_set_of_words.add(all_cleaned_tokens[i])

                if synset is not "stop":
                    # if "None" not in synset_vocab.values():  # Not working because class WordnetObject redefines __eq__
                    # method and tries to call attribute __name from string. -> Not possible
                    if str(synset) not in [str(x) for x in synset_vocab.values()]:
                        synset_vocab.update({i+1: synset})
                else:
                    synset_vocab.update({0: "stop"})
            else:
                synset_vocab.update({i: "None_{}".format(all_cleaned_tokens[i][0])})
                # Still value needs to be list for consistency
                word_vocab.update({"None_{}".format(all_cleaned_tokens[i][0]): [all_cleaned_tokens[i]]})
                none_counter += 1
        print(synset_vocab)
        print(word_vocab)
        # print("Vocabulary created!")
        self.synset_vocab = synset_vocab
        self.word_vocab = word_vocab

    def _preprocess_text(self, text: str) -> list:
        """
        This method preprocesses the given text with tokenizing, lemmatizing and pos tagging.
        It returns a list with every tokenized sentence as a list with values (word, pos_tag).
        :param text: Raw input text
        :return: list (sentences) of list (words) with format list(list((word, pos_tag)))
        """
        result: list = list()
        tokenizer = RegexpTokenizer(r'\w+')
        lemmatizer = WordNetLemmatizer()
        stop_words: list = list(stopwords.words("english"))

        sentences: list = sent_tokenize(text)
        for sent in sentences:
            tokens: list = word_tokenize(sent)
            symbols = set(string.punctuation)
            tagged_tokens = nltk.pos_tag(tokens)
            new_words: list = list()
            for (word, tag) in tagged_tokens:
                if word in stop_words or word in symbols:
                    new_words.append(('stop', 'stop'))
                else:
                    try:
                        c = (str(re.match(r'\w+', word)[0]), tag)
                        new_words.append(c)
                    except TypeError:
                        new_words.append(("stop", "stop"))

            # Double cleaning necessary
            # Pos Tagging increases precision of lemmatizer significantly!
            cleaned_tokens = [(lemmatizer.lemmatize(w.lower(), self.get_wordnet_pos(i)), i)
                              if w not in stop_words and w is not "stop" else ("stop", "stop")
                              for w, i in new_words]
            cleaned_tokens = [(word, pos) for word, pos in cleaned_tokens if word not in stop_words]
            result.append(cleaned_tokens)
        return result

    def encode(self, text: str) -> list:
        encoded_sentences: list = list()
        clean_text = self._preprocess_text(text)
        for sentence in clean_text:
            all_words_as_numbers: list = list()
            sentence_together = " ".join([word for word, tag in sentence if word != "stop"])
            # print(sentence_together)
            for word, pos_tag in sentence:
                if word != "stop":
                    wsd = lesk(sentence_together, word, self.get_wordnet_pos(pos_tag))
                else:
                    wsd = "stop"
                if wsd is None:
                    wsd = "None_{}".format(word)
                number = [key for key, value in self.synset_vocab.items() if str(value) == str(wsd)][0]
                # print("original: {}".format(wsd))
                # print("found: {}".format(number))
                all_words_as_numbers.append(str(number))
            encoded_sentences.append(all_words_as_numbers)
        return encoded_sentences

    def decode(self, text) -> list:
        """
        Decodes a given string or list of numbers corresponding the created SynsetVocab
        :param text: Input numbers as string or list
        :return: str
        """
        if isinstance(text, str):
            text = text.split(" ")

        synsets: list = list()
        for numbers in text:
            try:
                syn = self.synset_vocab[int(numbers)]
                synsets.append(syn)
            except ValueError:
                n_gram_nums = numbers.split(" ")
                synsets.append([self.synset_vocab[int(num)] for num in n_gram_nums])

        words: list = list()
        for synset in synsets:
            if not isinstance(synset, list):
                word = list(self.word_vocab[synset])[0][0]
                words.append(word)
            else:
                n_gram_word_tuple_sets = [self.word_vocab[s] for s in synset]
                n_gram_words = set([w for n_set in n_gram_word_tuple_sets for (w, p) in n_set])
                n_gram_words = " ".join([w for w in n_gram_words])
                words.append(n_gram_words)
        return words

    """
    def encode_for_rake(self, text: str):
        print("RAKE!!!")
        encoded_sentences: list = list()
        clean_text: list = list()
        # tokenizer = RegexpTokenizer(r'\w+')
        lemmatizer = WordNetLemmatizer()
        stop_words: list = list(stopwords.words("english"))

        sentences: list = sent_tokenize(text)
        for sent in sentences:
            tokens: list = word_tokenize(sent)
            symbols = set(string.punctuation)
            new_words: list = list()
            tagged_tokens = nltk.pos_tag(tokens)
            # TODO maybe do this in preprocessing as well...
            for (word, tag) in tagged_tokens:
                if word in stop_words or word in symbols:
                    new_words.append(('stop', 'stop'))
                else:
                    try:
                        c = (str(re.match(r'\w+', word)[0]), tag)
                        new_words.append(c)
                    except TypeError:
                        new_words.append(("stop", "stop"))

            # print(new_words)
            # Double cleaning necessary
            # Pos Tagging increases precision of lemmatizer significantly!
            cleaned_tokens = [(lemmatizer.lemmatize(w.lower(), self.get_wordnet_pos(i)), i)
                              if w not in stop_words and w is not "stop" else ("stop", "stop")
                              for index, (w, i) in enumerate(new_words)]
            cleaned_tokens = [(word, pos) if word not in stop_words
                              else ("stop", "stop")
                              for word, pos in cleaned_tokens]

            clean_text.append(cleaned_tokens)
        # print("Clean:")
        # print(clean_text)
        for sentence in clean_text:
            all_words_as_numbers: list = list()
            sentence_together = " ".join([word for word, tag in sentence if word is not "stop"])
            print(sentence_together)
            for word, pos_tag in sentence:
                if word != "stop":
                    wsd = lesk(sentence_together, word, self.get_wordnet_pos(pos_tag))
                    number = 0
                    if wsd is None:
                        wsd = "None_{}".format(word)
                    try:
                        number = [key for key, value in self.synset_vocab.items() if str(value) == str(wsd)][0]
                    except:
                        print("CAUTION!!!!: {}".format(wsd))
                    # print("original: {}".format(wsd))
                    # print("found: {}".format(number))
                    all_words_as_numbers.append(str(number))
                else:
                    all_words_as_numbers.append("stop")
            encoded_sentences.append(all_words_as_numbers)
        print(encoded_sentences)
        return encoded_sentences
    """
    @staticmethod
    def get_wordnet_pos(pos_tag: str):
        if pos_tag.startswith('J'):
            return wn.ADJ
        elif pos_tag.startswith('V'):
            return wn.VERB
        elif pos_tag.startswith('N'):
            return wn.NOUN
        elif pos_tag.startswith('R'):
            return wn.ADV
        else:
            return wn.NOUN  # Noun is default in lemmatizer
