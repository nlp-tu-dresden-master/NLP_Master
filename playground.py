from nlp_master import Corpora
from nlp_master import TopicEngine
from nlp_master import SynsetVocab

corp = Corpora(["Clustering", "classification"], ["01_data/01_Clustering_definitions", "01_data/02_Classification_definitions"])
# print(corp.vocab_object.synset_vocab)
vocab = SynsetVocab(corp.raw_corpora)
encoded = vocab.encode("Clustering algorithms examine data to find groups of items that are similar. "
             "The members of a cluster are more like each other than they are like members of other clusters. "
             "Clustering is the process of making a group of abstract objects into classes of similar objects.")

print(encoded)