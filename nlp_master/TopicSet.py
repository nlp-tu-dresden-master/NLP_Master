from typing import List


class KeyWord:
    def __init__(self, keyword: str, rank: float, algorithm: str = None):
        self.keyword = keyword
        self.rank = rank
        self.algorithm = algorithm

    def __str__(self):
        return str(self.keyword) + " | " + str(self.rank) + " | " + str(self.algorithm)

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

    # TODO Change that class name is only added when it is different to the existing one
    # TODO Implement that only new keywords are added and existing ones are boosted in rank.
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

    def sort_by_rank(self):
        self.keyword_set.sort(key=lambda x: x.rank, reverse=True)

    def norm_ranks(self):
        maximum = max([x.rank for x in self.keyword_set])
        minimum = min([x.rank for x in self.keyword_set])
        normed_keyword_set = []
        for keyword in self.keyword_set:
            keyword.rank = (keyword.rank-minimum) / (maximum-minimum)
            normed_keyword_set.append(keyword)
        self.keyword_set = normed_keyword_set

    def add_keyword(self, keyword, rank: float, algorithm: str = None) -> None:
        if algorithm is not None:
            self.keyword_set.append(KeyWord(keyword, rank, algorithm))
        else:
            self.keyword_set.append(KeyWord(keyword, rank, algorithm))

    def get_keywords(self, duplicates=True) -> List:
        if duplicates:
            return self.keyword_set
        else:
            return list(set(self.keyword_set))

    def pretty_print(self, duplicates=True):
        print("________TopicSet - {}________".format(self.class_name))
        if duplicates:
            for keyword in self.keyword_set:
                print(keyword.__str__())
        else:
            for keyword in set(self.keyword_set):
                print(keyword.__str__())

    # print(topic_set.get_keywords(duplicates=True))
