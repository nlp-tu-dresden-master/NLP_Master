from nlp_master import TopicSet, Corpora
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer


def corpora_to_vector(corpora: Corpora):
    tokenized_corpora = corpora.build_tokenized_corpora()

    dic = {}
    for key in tokenized_corpora.keys():
        counter = Counter(tokenized_corpora[key])
        # dic.update({key, counter})
    return dic


def topic_set_to_vector(topic_set: TopicSet):
    lemmatizer = WordNetLemmatizer()
    counter = Counter(lemmatizer.lemmatize(x.keyword) for x in topic_set.tokenize())
    return counter


def text_to_vector(text: str):
    tokenizer = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()
    tokenized_text = tokenizer.tokenize(text)

    return Counter([lemmatizer.lemmatize(x.lower()) for x in tokenized_text])


def adapt_text_vector_to_topic_set(text: str, topic_set: Counter) -> Counter:
    counter_for_text = Counter({x: 0 for x in topic_set})
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized_text = tokenizer.tokenize(text)
    lemmatizer = WordNetLemmatizer()
    tokenized_text = [lemmatizer.lemmatize(x.lower()) for x in tokenized_text[:]]
    elements = list(topic_set.elements())
    for string in tokenized_text:
        if string in elements:
            counter_for_text.update({string: 1})
    return counter_for_text


def transforming_counter_to_vector(counter: Counter):
    lst = []
    for key in counter.keys():
        lst.append(counter[key])
    return lst


# TODO Ok what happens if an keywords appears multiple times it should has more weight
def hamming_distance(text: str, topic_set: TopicSet):
    topic_set = topic_set_to_vector(topic_set)
    text_vector = transforming_counter_to_vector(counter=adapt_text_vector_to_topic_set(text, topic_set))
    topic_set_vector = transforming_counter_to_vector(topic_set)
    difference = 0
    for pair in zip(text_vector, topic_set_vector):
        difference += abs(pair[0] - pair[1])
    return difference


def jaccard_index(counter_text: Counter, counter_topic_set: Counter):
    def calculate_symmetric_difference():
        # First we delete every from the counter which is equal to zero and put this shit into a set
        counter_1 = {x for x in counter_text if counter_text[x] > 0}
        counter_2 = set(counter_topic_set.elements())

        return counter_1.intersection(counter_2)

    def calculate_union():
        counter_1 = set(counter_text.elements())
        counter_2 = set(counter_topic_set.elements())

        return counter_1.union(counter_2)

    symmetric_difference = calculate_symmetric_difference()
    union = calculate_union()
    return (len(symmetric_difference) / len(union)) * 100
