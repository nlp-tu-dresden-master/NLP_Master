from nlp_master import *
from pytextrank import *
import networkx as nx
import matplotlib.pyplot as plt
import json
import seaborn as sns
import os
from typing import List


class TextRank(Operation):

    def __init__(self, corpora: Corpora):
        super().__init__(corpora)
        self.graph = None
        self.ranks = None

        self.topic_set = None

        self.path_stage0 = "data.json"
        self.path_stage1 = "out_1.json"
        self.path_stage2 = "out_2.json"

        self.__initialize_graph()

    def __initialize_graph(self):
        corpus = self.corpora
        classes = corpus.algorithm_names
        self.topic_set = TopicSet(class_name=classes)
        for _class in classes:
            raw_corpus = {"id": 777, "text": corpus.raw_corpora[_class]}
            with open("data.json", "w") as f_json:
                json.dump(raw_corpus, f_json)

            with open(self.path_stage1, 'w') as f:
                for graf in parse_doc(json_iter(self.path_stage0)):
                    f.write("%s\n" % pretty_print(graf._asdict()))

            self.graph, self.ranks = pytextrank.text_rank(self.path_stage1)
            #self.__delete_stages([self.path_stage0, self.path_stage1])

    def thin_out_graph(self, threshold: float) -> nx.DiGraph:
        graph = self.graph.copy()
        nodes = nx.nodes(graph)

        # parsing n_amount into list
        lst_keep = []
        lst_remove = []
        for node in nodes:
            neighbors = nx.all_neighbors(graph, node)
            counter = 0
            dic = dict()
            for neighbor in neighbors:
                counter += 1
                dic.update({"node": node, "n_amount": counter})
            if counter >= threshold:
                lst_keep.append(dic)
            else:
                lst_remove.append(dic)

        # Remove Nodes from Graph
        for node in lst_remove:
            graph.remove_node(node["node"])

        return graph

    def __delete_stages(self, lst: List):
        [os.remove(x) for x in lst]

    def extract_keywords(self) -> TopicSet:
        pytextrank.render_ranks(self.graph, self.ranks)
        with open(self.path_stage2, 'w') as f:
            # RL is euqal to an ranked lexeme
            # TODO What is an ranked lexeme?
            for rl in pytextrank.normalize_key_phrases(self.path_stage1, self.ranks):
                f.write("%s\n" % pytextrank.pretty_print(rl._asdict()))  # TODO JSON is not well formed..
                # to view output in this notebook
                if rl is not None:
                    self.topic_set.add_keyword(keyword=rl.text, rank=rl.rank, algorithm="TextRank")
        #self.__delete_stages([self.path_stage2, "graph.dot"])
        return self.topic_set

    def visualize(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        graph = self.graph
        # First Check for threshold and adapt the grpah. Otherwise threshold needs to be the first given par.
        for key in kwargs.keys():
            if key == "threshold":
                print(kwargs["threshold"])
                graph = self.thin_out_graph(threshold=kwargs["threshold"])

        for key in kwargs.keys():
            if key == "heatmap":
                if kwargs["heatmap"]:
                    df_am = nx.to_pandas_adjacency(graph)
                    sns.heatmap(data=df_am, center=0)
                    plt.show()

            if key == "network":
                if kwargs["network"]:
                    pos = nx.spring_layout(graph,
                                           k=1)  # Key is the factor which defines the space between nodes
                    nx.draw_networkx_nodes(graph,
                                           pos=pos,
                                           node_size=30,
                                           cmap="cividis")

                    nx.draw_networkx_edges(graph,
                                           pos=pos,
                                           width=0.5,
                                           arrowstyle="-",
                                           cmap="inferno")

                    nx.draw_networkx_labels(graph, pos=pos, font_size=8, font_family='sans-serif')
                    plt.show()