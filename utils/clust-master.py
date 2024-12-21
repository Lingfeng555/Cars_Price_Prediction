import pandas
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, Birch, OPTICS
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, homogeneity_score, completeness_score, v_measure_score
import numpy as np
import optuna

class ClusterGenerator:
    def __init__(self, dataset):
        self.dataset = dataset

    def _objective(self, trial, method):
        """
        Objective function for hyperparameter optimization with Optuna.

        Parameters:
        trial (optuna.trial.Trial): The trial object for Optuna.
        method (str): The clustering method to optimize.

        Returns:
        float: The silhouette score for the trial.
        """
        if method == "kmeans":
            n_clusters = trial.suggest_int("n_clusters", 2, 15)
            model = KMeans(n_clusters=n_clusters, random_state=42)

        elif method == "agglomerative":
            n_clusters = trial.suggest_int("n_clusters", 2, 15)
            linkage = trial.suggest_categorical("linkage", ["ward", "complete", "average", "single"])
            model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)

        elif method == "dbscan":
            eps = trial.suggest_float("eps", 0.1, 5.0, log=True)
            min_samples = trial.suggest_int("min_samples", 3, 20)
            model = DBSCAN(eps=eps, min_samples=min_samples)

        elif method == "birch":
            threshold = trial.suggest_float("threshold", 0.1, 1.0)
            n_clusters = trial.suggest_int("n_clusters", 2, 15)
            model = Birch(threshold=threshold, n_clusters=n_clusters)

        elif method == "optics":
            min_samples = trial.suggest_int("min_samples", 3, 20)
            max_eps = trial.suggest_float("max_eps", 0.1, 5.0, log=True)
            model = OPTICS(min_samples=min_samples, max_eps=max_eps)

        elif method == "gmm":
            n_components = trial.suggest_int("n_components", 2, 15)
            covariance_type = trial.suggest_categorical("covariance_type", ["full", "tied", "diag", "spherical"])
            model = GaussianMixture(n_components=n_components, covariance_type=covariance_type, random_state=42)

        else:
            raise ValueError(f"Unsupported clustering method: {method}")

        labels = model.fit_predict(self.dataset) if hasattr(model, 'fit_predict') else model.fit(self.dataset).predict(self.dataset)

        if len(set(labels)) > 1:  # Ensure there is more than one cluster
            return silhouette_score(self.dataset, labels)
        else:
            return -1.0  # Penalize single-cluster solutions

    def find_best_clustering(self, method, n_trials=50):

        study = optuna.create_study(direction="maximize")
        study.optimize(lambda trial: self._objective(trial, method), n_trials=n_trials)

        best_params = study.best_params

        # Train the final model with the best parameters
        if method == "kmeans":
            model = KMeans(**best_params, random_state=42)

        elif method == "agglomerative":
            model = AgglomerativeClustering(**best_params)

        elif method == "dbscan":
            model = DBSCAN(**best_params)

        elif method == "birch":
            model = Birch(**best_params)

        elif method == "optics":
            model = OPTICS(**best_params)

        elif method == "gmm":
            model = GaussianMixture(**best_params, random_state=42)

        else:
            raise ValueError(f"Unsupported clustering method: {method}")

        labels = model.fit_predict(self.dataset) if hasattr(model, 'fit_predict') else model.fit(self.dataset).predict(self.dataset)

        # Calculate clustering metrics
        metrics = {
            "silhouette_score": silhouette_score(self.dataset, labels) if len(set(labels)) > 1 else -1.0,
            "calinski_harabasz_score": calinski_harabasz_score(self.dataset, labels) if len(set(labels)) > 1 else -1.0,
            "davies_bouldin_score": davies_bouldin_score(self.dataset, labels) if len(set(labels)) > 1 else float("inf"),
        }

        return {"best_params": best_params, "metrics": metrics, "labels": labels}
    
    def external_evaluation(self, labels, ground_truth):
        """
        Evaluate clustering performance using external metrics.

        Parameters:
        labels (array-like): Cluster labels assigned by the algorithm.
        ground_truth (array-like): Ground truth labels.

        Returns:
        dict: External evaluation metrics.
        """
        return {
            "adjusted_rand_score": adjusted_rand_score(ground_truth, labels),
            "normalized_mutual_info_score": normalized_mutual_info_score(ground_truth, labels),
            "homogeneity_score": homogeneity_score(ground_truth, labels),
            "completeness_score": completeness_score(ground_truth, labels),
            "v_measure_score": v_measure_score(ground_truth, labels)
        }
    
    def generate(self, ground_truth=None, n_trials=50):
        """
        Generate clustering results for a list of methods.

        Parameters:
        ground_truth (array-like): Ground truth labels for external evaluation (optional).
        n_trials (int): Number of optimization trials for each method.

        Returns:
        dict: A dictionary with methods as keys and their results as values.
        """
        methods = ["kmeans", "agglomerative", "dbscan", "birch", "optics", "gmm"]
        results = {}
        for method in methods:
            try:
                print(f"Optimizing method: {method}")
                clustering_result = self.find_best_clustering(method, n_trials=n_trials)
                results[method] = clustering_result
                if ground_truth is not None:
                    external_metrics = self.external_evaluation(clustering_result["labels"], ground_truth)
                    results[method]["external_metrics"] = external_metrics
            except Exception as e:
                print(f"Error with method {method}: {e}")
        return results
