from models import Corpora
from models import Topic_Engine

corp = Corpora(["Clustering"], ["01_data/01_Clustering_definitions"])
corp.build_all_corpora_for_new_algorithm_type("Classification", "01_data/02_Classification_definitions")

# How i would access the attributes
# print(corp.token_corpora)
# print(corp.raw_corpora)
# print(corp.document_corpora)

engine = Topic_Engine(corpora=corp)
# engine.get_most_common_tokens("clustering", 15)
# engine.get_most_common_tokens("Classification", 15)
engine.get_frequency_distribution_of_word_meanings("clustering", 15)