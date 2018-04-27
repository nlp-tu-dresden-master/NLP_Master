from models import Corpora

corpus = Corpora(paths=["01_data/01_Clustering_definitions"], names=["Clustering"])

# How i would access the attributes
print(corpus.token_corpora)
print(corpus.raw_corpora)
print(corpus.document_corpora)

# Prove that class attributes are empty
print(Corpora.document_corpora)
print(Corpora.token_corpora)
print(Corpora.raw_corpora)

