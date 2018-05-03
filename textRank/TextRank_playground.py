from pytextrank import *
import networkx as nx
import matplotlib.pyplot as plt
from models.Corpora import Corpora
import json
import pandas as pd
import seaborn as sns

if __name__ == "__main__":

    # TODO Convert Corpora to JSON
    corpus = Corpora(paths=["../01_data/01_Clustering_definitions"], names=["Clustering"])
    raw_corpus = {"id": 777, "text": corpus.raw_corpora["clustering"]}

    with open("data.json", "w") as f_json:
        json.dump(raw_corpus, f_json)

    path_stage0 = "data.json"
    path_stage1 = "out_1.json"
    path_stage2 = "out_2.json"

    # TODO What is happening here?
    with open(path_stage1, 'w') as f:
        for graf in parse_doc(json_iter(path_stage0)):
            f.write("%s\n" % pretty_print(graf._asdict()))

    # TODO - Stage 2
    graph, ranks = pytextrank.text_rank(path_stage1)
    pytextrank.render_ranks(graph, ranks)


    # TODO find most important nodes --> The nodes with the most neighboors
    def thin_out_graph(graph: nx.DiGraph, threshold: float) -> nx.DiGraph:
        """
        Functions thins out the graph. Nodes with low incomming and outcomming connections will be removed.
        :param graph:
        :param threshold:
        :return:
        """

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


    # nodes = nx.all_neighbors(graph)

    # print(nodes)

    # TODO - Drawing the Graph
    # Unfiltered
    graph_to_visualize = thin_out_graph(graph, 6)
    pos = nx.spring_layout(graph_to_visualize, k=1)  # Key is the factor which defines the space between nodes
    nx.draw_networkx_nodes(graph_to_visualize,
                           pos=pos,
                           node_size=30,
                           cmap="cividis")

    nx.draw_networkx_edges(graph_to_visualize,
                           pos=pos,
                           width=0.5,
                           arrowstyle="-",
                           cmap="inferno")

    nx.draw_networkx_labels(graph_to_visualize, pos=pos, font_size=8, font_family='sans-serif')
    plt.show()
    # Adjaceny matrix

    df_am = nx.to_pandas_adjacency(graph)
    sns.heatmap(data=df_am, center=0)
    plt.show()


    with open(path_stage2, 'w') as f:
        # RL is euqal to an ranked lexeme
        # TODO What is an ranked lexeme?
        for rl in pytextrank.normalize_key_phrases(path_stage1, ranks):
            f.write("%s\n" % pytextrank.pretty_print(rl._asdict()))  # TODO JSON is not well formed..
            # to view output in this notebook
            if rl is not None:
                print(rl)
