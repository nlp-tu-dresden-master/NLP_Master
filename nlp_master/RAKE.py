from nlp_master.Operation import Operation
from nlp_master.Corpora import Corpora
from nlp_master.TopicSet import TopicSet


class RAKE(Operation):

    def __init__(self, corp: Corpora):
        if not isinstance(corp, Corpora):
            raise ValueError("Parameter 'corp' needs to be instance of class Corpora!")
        super().__init__(corp)
        self.keywords = dict()

    def extract_keywords(self):
        topic_sets: dict = dict()
        for algorithm_class in self.corpora.raw_corpora:
            keyword_candidates = self.__determine_candidates(self.corpora.raw_corpora[algorithm_class])
            word_scores_dict = self.__calculate_word_scores(keyword_candidates)
            candidate_scores = self.__calculate_candidate_scores(candidate_list=keyword_candidates,
                                                                 scores=word_scores_dict)
            sorted_candidates = sorted(candidate_scores.items(), key=lambda entry: entry[1], reverse=True)
            # print(sorted_candidates)
            topic_set = TopicSet(class_name=algorithm_class)
            for candidate in sorted_candidates:
                topic_set.add_keyword(keyword=candidate[0], rank=candidate[1], algorithm="RAKE")
            topic_sets.update({algorithm_class: topic_set})
        return topic_sets

    def __determine_candidates(self, sentences: list) -> list:
        joined_sentences = [word for sublist in sentences for word in sublist]
        candidate_list: list = list()
        temp_candidate: list = list()
        for i, token in enumerate(joined_sentences):
            if token != "0":  # Zeros point to stopwords and punctuation
                temp_candidate.append(token)
            if token == "0" and len(temp_candidate) > 0:
                candidate_list.append(" ".join(temp_candidate))
                temp_candidate = list()
            if i == len(joined_sentences)-1:  # If the sentences ended without a stopsign
                candidate_list.append(" ".join(temp_candidate))
        return candidate_list

    def __calculate_word_scores(self, candidate_list: list):
        word_frequency: dict = dict()
        word_degree: dict = dict()
        for candidate in candidate_list:
            if len(candidate.split(" ")) > 1:
                word_list = candidate.split(" ")
            else:
                word_list = [candidate]
            word_list_length = len(word_list)
            word_list_degree = word_list_length - 1
            # if word_list_degree > 3: word_list_degree = 3 #exp.
            for word in word_list:
                word_frequency.setdefault(word, 0)
                word_frequency[word] += 1
                word_degree.setdefault(word, 0)
                word_degree[word] += word_list_degree
        for item in word_frequency:
            # The overall degree of a word!
            word_degree[item] = word_degree[item] + word_frequency[item]

        # Calculate Word scores = deg(w)/frew(w)
        word_score = {}
        for item in word_frequency:
            word_score.setdefault(item, 0)
            word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)
        return word_score

    def __calculate_candidate_scores(self, candidate_list: list, scores: dict):
        keyword_candidates = {}
        for candidate in candidate_list:
            keyword_candidates.setdefault(candidate, 0)
            if len(candidate.split(" ")) > 1:
                word_list = candidate.split(" ")
            else:
                word_list = [candidate]
            candidate_score = 0
            for word in word_list:
                candidate_score += scores[word]
            keyword_candidates[candidate] = candidate_score
        return keyword_candidates

    def visualize(self, **kwargs):
        pass
