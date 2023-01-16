# library imports
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from linear_assignment_ import linear_assignment
from sklearn.cluster import KMeans, AffinityPropagation, AgglomerativeClustering
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score

# project imports


def _make_cost_m(cm):
    """
    This if the function that checks if the match between
    the cluster and classification data is optimal using a confession matrix
    """
    return np.max(cm) - cm


class ResearchTypeProfiler:
    """
    A class responsible to see if we can differ unsupervised between authors using their journal publish profile
    """

    def __init__(self,
                 cluster_n: int):
        self.kmeans = KMeans(n_clusters=cluster_n,
                             verbose=2)
        self.affinity_propagation = AffinityPropagation(verbose=2)
        self.agglomerative_clustering = AgglomerativeClustering(n_clusters=cluster_n)

    def train(self,
              x: pd.DataFrame):
        self.kmeans.fit(x)
        self.affinity_propagation.fit(x)
        self.agglomerative_clustering.fit(x)

    def test(self,
             x: pd.DataFrame,
             y: pd.Series):
        models_tests = {
            "kmeans": self.kmeans,
            "affinity_propagation": self.kmeans,
            "agglomerative_clustering": self.agglomerative_clustering,
        }
        answer = {}
        for name, model in models_tests:
            y_pred = model.predict(x)
            # find best match between two vectors
            cm = confusion_matrix(y, y_pred)
            indexes = linear_assignment(_make_cost_m(cm))
            js = [e[1] for e in sorted(indexes, key=lambda x: x[0])]
            cm = cm[:, js]
            mapper = {index: js[index] for index in range(len(js))}
            y_pred_match = [mapper[val] for val in list(y_pred)]
            answer[name] = {
                "y_pred": y_pred,
                "acc": np.trace(cm) / np.sum(cm),
                "recall": recall_score(y_pred=y_pred_match, y_true=y),
                "precision": precision_score(y_pred=y_pred_match, y_true=y),
                "f1": f1_score(y_pred=y_pred_match, y_true=y)
            }
        return answer

    def save(self,
             path: str):
        with open(path, "wb") as model_file:
            pickle.dump(self, model_file)

    @staticmethod
    def load(path: str):
        model = None
        with open(path, "rb") as model_file:
            model = pickle.load(model_file)
        return model
