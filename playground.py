from models import Corpora
from models import TopicEngine
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
corp = Corpora(["Clustering", "classification"], ["01_data/01_Clustering_definitions", "01_data/02_Classification_definitions"])
print(corp.vocab_object.synset_vocab)

engine = TopicEngine(corpora=corp)