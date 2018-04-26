import os
from Corpora import Corpora
from Topic_Engine import Topic_Engine


corp = Corpora(["Clustering"], ["../01_data/01_Clustering_definitions/"])

print(corp.get_all_algorithms())

engine = Topic_Engine(corp)
engine.get_most_common_tokens("Clustering", 15)
# engine.tf_idf()