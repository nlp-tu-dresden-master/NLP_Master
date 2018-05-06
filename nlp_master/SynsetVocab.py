import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn
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
                raw_sentence = " ".join([w for w, t in clean_sent])

                for (word, tag) in clean_sent:
                    wsd = lesk(raw_sentence, word, self.get_wordnet_pos(tag))
                    # Took list to have full index range afterwards
                    all_wsds.append(wsd)

        none_counter = 0
        for i, synset in enumerate(all_wsds):
            if synset is not None:
                # if "None" not in synset_vocab.values():  # Not working because class WordnetObject redefines __eq__
                # method and tries to call attribute __name from string. -> Not possible
                if str(synset) not in [str(x) for x in synset_vocab.values()]:
                    # Push in synset_vocab and word_vocab
                    synset_vocab.update({i: synset})
                    if synset not in word_vocab.keys():
                        word_vocab.update({synset: [all_cleaned_tokens[i]]})
                    else:
                        current_list_of_words = word_vocab[synset]
                        current_list_of_words.append(all_cleaned_tokens[i])
            else:
                synset_vocab.update({i: "None_{}".format(none_counter)})
                # Still value needs to be list for consistency
                word_vocab.update({"None_{}".format(none_counter): [all_cleaned_tokens[i]]})
                none_counter += 1
        # print(synset_vocab)
        # print(word_vocab)
        print("Vocabulary created!")
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
            tokens: list = tokenizer.tokenize(sent)
            tagged_tokens = nltk.pos_tag(tokens)
            # Double cleaning necessary
            # Pos Tagging increases precision of lemmatizer significantly!
            cleaned_tokens = [(lemmatizer.lemmatize(w.lower(), self.get_wordnet_pos(i)), i)
                              for w, i in tagged_tokens if w not in stop_words]
            cleaned_tokens = [(word, pos) for word, pos in cleaned_tokens if word not in stop_words]
            result.append(cleaned_tokens)
        return result

    def encode(self, text: str) -> list:
        all_words_as_numbers: list = list()
        clean_text = self._preprocess_text(text)
        none_counter = 0
        for sentence in clean_text:
            sentence_together = " ".join([word for word, tag in sentence])
            for word, pos_tag in sentence:
                wsd = lesk(sentence_together, word, self.get_wordnet_pos(pos_tag))
                if wsd is None:
                    wsd = "None_{}".format(none_counter)
                    none_counter += 1
                number = [key for key, value in self.synset_vocab.items() if str(value) == str(wsd)][0]
                # print("original: {}".format(wsd))
                # print("found: {}".format(number))
                all_words_as_numbers.append(str(number))
        return all_words_as_numbers

    def decode(self, text: str) -> str:
        numbers = text.split(" ")
        synsets = [self.synset_vocab[int(number)] for number in numbers]
        words = [self.word_vocab[synset] for synset in synsets]
        return " ".join([word for [(word, pos)] in words])

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
