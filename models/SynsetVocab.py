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


class SynsetVocab():

    def __init__(self, raw_corp: dict):
        self.synset_vocab = dict()
        self.word_vocab = dict()
        self.build_synset_and_word_vocab(raw_corp)

    def build_synset_and_word_vocab(self, raw_corp: dict) -> None:
        """
        This method builds two dictionaries:
        The synset_vocab dictionary contains all the different synsets/wsd that are contained in the raw corpora
        The word_vocab contains all the synsets as keys and the real words as values.
        This way we can go back from numbers to words if required.
        :param raw_corp: 
        :return:
        """
        synset_vocab: dict = dict()
        word_vocab: dict = dict()
        all_wsds: list = list()
        tokenizer = RegexpTokenizer(r'\w+')
        lemmatizer = WordNetLemmatizer()
        stop_words: list = list(stopwords.words("english"))
        all_cleaned_tokens: list = list()

        for alg in raw_corp:
            sentences: list = sent_tokenize(raw_corp[alg])
            for sent in sentences:
                tokens: list = tokenizer.tokenize(sent)
                tagged_tokens = nltk.pos_tag(tokens)
                # Double cleaning necessary
                # Pos Tagging increases precision of lemmatizer significantly!
                cleaned_tokens = [(lemmatizer.lemmatize(w.lower(), self.get_wordnet_pos(i)), i)
                                        for w, i in tagged_tokens if w not in stop_words]
                cleaned_tokens = [(word, pos) for word, pos in cleaned_tokens if word not in stop_words]
                all_cleaned_tokens.extend(cleaned_tokens)

                for (word, tag) in cleaned_tokens:
                    wsd = lesk(sent, word, self.get_wordnet_pos(tag))
                    # Took list to have full index range afterwards
                    all_wsds.append(wsd)

        # print("wsd: {}  words: {}".format(len(all_wsds), len(all_cleaned_tokens)))
        index_of_syn_dict = 0
        for i, synset in enumerate(all_wsds):
            if synset is not None:
                if synset not in synset_vocab.values():
                    # TODO What to do with None types? -> Different words but no synset...
                    # FUCK IT! SynSets do not have always the real word inside!
                    synset_vocab.update({index_of_syn_dict: synset})
                    index_of_syn_dict += 1
                    if synset not in word_vocab.keys():
                        word_vocab.update({synset: [all_cleaned_tokens[i]]})
                    else:
                        current_list_of_words = word_vocab[synset]
                        current_list_of_words.append(all_cleaned_tokens[i])
            else:
                if "None" not in word_vocab.keys():
                    word_vocab.update({"None": [all_cleaned_tokens[i]]})
                else:
                    current_list_of_words = word_vocab["None"]
                    current_list_of_words.append(all_cleaned_tokens[i])

        # if "None" not in synset_vocab.values():  # Not working because class WordnetObject redefines __eq__
        # method and tries to call attribute __name from string. -> Not possible
        # Therefore, skipping None values in synsets and adding "None" as last entry in dict.
        synset_vocab.update({len(synset_vocab): "None"})
        # print(synset_vocab)
        # print(word_vocab)
        self.synset_vocab = synset_vocab
        self.word_vocab = word_vocab

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
