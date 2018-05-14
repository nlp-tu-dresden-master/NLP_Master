from typing import List
from nltk.tokenize import RegexpTokenizer


class KeyWord:
    def __init__(self, keyword: str, rank: float, algorithm: str = None):
        self.keyword = keyword
        self.rank = rank
        self.algorithm = algorithm

    def __str__(self):
        return str(self.keyword) + "| " + str(self.rank) + "| " + str(self.algorithm)

    def __repr__(self):
        return "({}, {})".format(self.keyword, self.rank)

    def __eq__(self, other):
        if self.keyword == other.keyword:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.keyword)


class TopicSet:

    def __init__(self, class_name):
        self.class_name = class_name
        self.keyword_set = []

    def __repr__(self):
        return "class: {} \n keywords: {}".format(self.class_name, self.keyword_set)

    def __add__(self, other):
        class_names = []
        class_names.append(self.class_name)
        class_names.append(other.class_name)
        topic_set = TopicSet(class_name=class_names)
        [topic_set.add_keyword(x.keyword, x.rank, x.algorithm) for x in (self.keyword_set + other.keyword_set)]

        return topic_set

    def __len__(self):
        return len(self.keyword_set)

    def __iter__(self):
        return iter(self.keyword_set)

    def norm_ranks(self):
        maximum = max([x.rank for x in self.keyword_set])
        normed_keyword_set = []
        for keyword in self.keyword_set:
            keyword.rank = keyword.rank / maximum * maximum
            normed_keyword_set.append(keyword)
        self.keyword_set = normed_keyword_set

    def add_keyword(self, keyword, rank: float, algorithm: str = None) -> None:
        """
        if algorithm is not None:
            self.keyword_set.append(KeyWord(keyword, rank, algorithm))
        else:
            self.keyword_set.append(KeyWord(keyword, rank, algorithm))
        """
        self.keyword_set.append(KeyWord(keyword, rank, algorithm))

    def get_keywords(self, duplicates=True) -> List:
        if duplicates:
            return self.keyword_set
        else:
            return list(set(self.keyword_set))

    # TODO needs defintely some discussion
    #  --> What are we doing with tokenized n-grams does it make sense?
    # --> Do we need to tokenize the keywords? Yes because we are manly working with it
    # --> Should we substitute the TopicSet by itself or just return a new lst?
    # --> What happens if we change the tokenizer or something like that? We change in 100x times in the code?

    def tokenize(self):
        tokenizer = RegexpTokenizer(r'\w+')
        tokenized_set = [tokenizer.tokenize(x.keyword) for x in self.keyword_set]
        ranks = [x.rank for x in self.keyword_set]
        algorithms = [x.algorithm for x in self.keyword_set]
        new_topic_set = []
        for i, lst in enumerate(tokenized_set):
            keyword = KeyWord(keyword= "", rank=ranks[i], algorithm=algorithms[i])
            for string in lst:
                if keyword.keyword == "":
                    keyword.keyword += string
                else:
                    keyword.keyword += " " + string
            new_topic_set.append(keyword)
        return new_topic_set
    # self.keyword_set = [type(x) for x in self.keyword_set]


def pretty_print(self, duplicates=True):
    print("_______TopicSet - {}________".format(self.class_name))
    if duplicates:
        for keyword in self.keyword_set:
            print(keyword.__str__())
    else:
        for keyword in set(self.keyword_set):
            print(keyword.__str__())

# print(topic_set.get_keywords(duplicates=True))
