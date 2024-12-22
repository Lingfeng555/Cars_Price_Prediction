import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, Birch, OPTICS
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, homogeneity_score, completeness_score, v_measure_score
import numpy as np
import optuna

try:
    import cuml
    from cuml.cluster import KMeans as cuKMeans, DBSCAN as cuDBSCAN
    CUML_AVAILABLE = True
except ImportError:
    CUML_AVAILABLE = False

class ClusterGenerator:
    def __init__(self, dataset, use_cuml=False):
        """
        Initialize the ClusterGenerator class with a dataset.

        Parameters:
        dataset (pd.DataFrame): The input dataset for clustering.
        use_cuml (bool): Whether to use cuML for acceleration if available.
        """
        self.dataset = dataset
        self.use_cuml = use_cuml and CUML_AVAILABLE

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
            init = trial.suggest_categorical("init", ["k-means++", "random"])
            n_init = trial.suggest_int("n_init", 10, 50)
            max_iter = trial.suggest_int("max_iter", 100, 500)
            model = cuKMeans(n_clusters=n_clusters, init=init, n_init=n_init, max_iter=max_iter, random_state=42) if self.use_cuml else KMeans(n_clusters=n_clusters, init=init, n_init=n_init, max_iter=max_iter, random_state=42)

        elif method == "agglomerative":
            n_clusters = trial.suggest_int("n_clusters", 2, 15)
            linkage = trial.suggest_categorical("linkage", ["ward", "complete", "average", "single"])
            model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)

        elif method == "dbscan":
            eps = trial.suggest_float("eps", 0.1, 5.0, log=True)
            min_samples = trial.suggest_int("min_samples", 3, 20)
            algorithm = trial.suggest_categorical("algorithm", ["auto", "ball_tree", "brute"])
            model = cuDBSCAN(eps=eps, min_samples=min_samples) if self.use_cuml else DBSCAN(eps=eps, min_samples=min_samples, algorithm=algorithm)

        elif method == "birch":
            threshold = trial.suggest_float("threshold", 0.1, 1.0)
            n_clusters = trial.suggest_int("n_clusters", 2, 15)
            branching_factor = trial.suggest_int("branching_factor", 10, 100)
            model = Birch(threshold=threshold, n_clusters=n_clusters, branching_factor=branching_factor)

        elif method == "optics":
            min_samples = trial.suggest_int("min_samples", 3, 20)
            max_eps = trial.suggest_float("max_eps", 0.1, 5.0, log=True)
            metric = trial.suggest_categorical("metric", ["minkowski", "euclidean", "manhattan", "cosine"])
            cluster_method = trial.suggest_categorical("cluster_method", ["xi", "dbscan"])
            model = OPTICS(min_samples=min_samples, max_eps=max_eps, metric=metric, cluster_method=cluster_method)

        elif method == "gmm":
            n_components = trial.suggest_int("n_components", 2, 15)
            covariance_type = trial.suggest_categorical("covariance_type", ["full", "tied", "diag", "spherical"])
            tol = trial.suggest_float("tol", 1e-4, 1e-2, log=True)
            reg_covar = trial.suggest_float("reg_covar", 1e-6, 1e-2, log=True)
            max_iter = trial.suggest_int("max_iter", 100, 200)
            model = GaussianMixture(n_components=n_components, covariance_type=covariance_type, tol=tol, reg_covar=reg_covar, max_iter=max_iter, random_state=42)
        else:
            raise ValueError(f"Unsupported clustering method: {method}")

        labels = model.fit_predict(self.dataset) if hasattr(model, 'fit_predict') else model.fit(self.dataset).predict(self.dataset)

        if len(set(labels)) > 1:  # Ensure there is more than one cluster
            return silhouette_score(self.dataset, labels)
        else:
            return -1.0  # Penalize single-cluster solutions

    def find_best_clustering(self, method, n_trials=50):
        """
        Optimize the clustering algorithm and find the best parameters.

        Parameters:
        method (str): The clustering method to optimize (e.g., 'kmeans', 'agglomerative').
        n_trials (int): The number of optimization trials.

        Returns:
        dict: The best parameters and corresponding metrics.
        """
        study = optuna.create_study(direction="maximize")
        n_jobs=-1
        with ThreadPoolExecutor(max_workers=n_jobs if n_jobs > 0 else None) as executor:
            study.optimize(lambda trial: self._objective(trial, method), n_trials=n_trials, n_jobs=n_jobs)
        best_params = study.best_params

        # Train the final model with the best parameters
        if method == "kmeans":
            model = cuKMeans(**best_params, random_state=42) if self.use_cuml else KMeans(**best_params, random_state=42)

        elif method == "agglomerative":
            model = AgglomerativeClustering(**best_params)

        elif method == "dbscan":
            model = cuDBSCAN(**best_params) if self.use_cuml else DBSCAN(**best_params)

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

        return {"best_params": best_params, "metrics": metrics, "labels": labels, "model": model}
    
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

        self.externalEvalation = {"Algorithm":[], "adjusted_rand_score": [], "normalized_mutual_info_score": [], "completeness_score": [], "v_measure_score":[]}
        self.internalEvaluation = {"Algorithm":[], "silhouette_score": [], "calinski_harabasz_score": [], "davies_bouldin_score": []}
        self.best_params = {}
        
        for method in methods:
            try:
                self.externalEvalation["Algorithm"].append(method)
                self.internalEvaluation["Algorithm"].append(method)

                print(f"Optimizing method: {method}")
                clustering_result = self.find_best_clustering(method, n_trials=n_trials)

                # Record best parameters
                self.best_params[method] = clustering_result["best_params"]

                # Record internal metrics
                self.internalEvaluation["silhouette_score"].append(clustering_result["metrics"]["silhouette_score"])
                self.internalEvaluation["calinski_harabasz_score"].append(clustering_result["metrics"]["calinski_harabasz_score"])
                self.internalEvaluation["davies_bouldin_score"].append(clustering_result["metrics"]["davies_bouldin_score"])

                if ground_truth is not None:
                    # Compute external metrics
                    external_metrics = self.external_evaluation(clustering_result["labels"], ground_truth)
                    self.externalEvalation["adjusted_rand_score"].append(external_metrics["adjusted_rand_score"])
                    self.externalEvalation["normalized_mutual_info_score"].append(external_metrics["normalized_mutual_info_score"])
                    self.externalEvalation["completeness_score"].append(external_metrics["completeness_score"])
                    self.externalEvalation["v_measure_score"].append(external_metrics["v_measure_score"])
                else:
                    # Fill with None if ground_truth is not provided
                    self.externalEvalation["adjusted_rand_score"].append(None)
                    self.externalEvalation["normalized_mutual_info_score"].append(None)
                    self.externalEvalation["completeness_score"].append(None)
                    self.externalEvalation["v_measure_score"].append(None)

            except Exception as e:
                print(f"Error with method {method}: {e}")
                # Fill with None in case of error
                self.internalEvaluation["silhouette_score"].append(None)
                self.internalEvaluation["calinski_harabasz_score"].append(None)
                self.internalEvaluation["davies_bouldin_score"].append(None)
                self.externalEvalation["adjusted_rand_score"].append(None)
                self.externalEvalation["normalized_mutual_info_score"].append(None)
                self.externalEvalation["completeness_score"].append(None)
                self.externalEvalation["v_measure_score"].append(None)

        return {"internalEvaluation": self.internalEvaluation, "externalEvaluation": self.externalEvalation, "best_params": self.best_params}

    def save(self, name: str):
        """
        Save internal and external evaluations, as well as best parameters, to .tex files.

        Parameters:
        name (str): Name of the directory to save the .tex files.
        """
        directory_path = "evaluation"
        dir = f"{directory_path}/{name}"

        # Create directory if it doesn't exist
        if not os.path.exists(dir):
            os.makedirs(dir)

        # Save internal evaluations
        if hasattr(self, 'internalEvaluation'):
            internal_eval_df = pd.DataFrame(self.internalEvaluation)
            internal_eval_df.to_latex(f"{dir}/internal_evaluation.tex", index=False)

        # Save external evaluations
        if hasattr(self, 'externalEvalation'):
            external_eval_df = pd.DataFrame(self.externalEvalation)
            external_eval_df.to_latex(f"{dir}/external_evaluation.tex", index=False)

        # Save best parameters for each method
        if hasattr(self, 'best_params'):
            for method, params in self.best_params.items():
                params_df = pd.DataFrame([params])
                params_df.to_latex(f"{dir}/best_param_{method}.tex", index=False)
