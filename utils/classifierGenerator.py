import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
import optuna

try:
    import cuml
    from cuml.ensemble import RandomForestClassifier as cuRandomForestClassifier
    from cuml.tree import DecisionTreeClassifier as cuDecisionTreeClassifier
    CUML_AVAILABLE = True
except ImportError:
    CUML_AVAILABLE = False

class ClassifierGenerator:
    def __init__(self, dataset, target_column, use_cuml=False):
        """
        Initialize the ClassifierGenerator class with a dataset and target column.

        Parameters:
        dataset (pd.DataFrame): The input dataset for classification.
        target_column (str): The name of the target column in the dataset.
        use_cuml (bool): Whether to use cuML for acceleration if available.
        """
        self.dataset = dataset
        self.target_column = target_column
        self.X = dataset
        self.y = target_column
        self.use_cuml = use_cuml and CUML_AVAILABLE
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.results = None  # Store the results from generate()

    def _objective(self, trial, method):
        """
        Objective function for hyperparameter optimization with Optuna.

        Parameters:
        trial (optuna.trial.Trial): The trial object for Optuna.
        method (str): The classification method to optimize.

        Returns:
        float: The accuracy score for the trial.
        """

        if method == "decision_tree":
            max_depth = trial.suggest_int("max_depth", 2, 20)
            min_samples_split = trial.suggest_int("min_samples_split", 2, 10)
            min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 5)
            if self.use_cuml:
                model = cuDecisionTreeClassifier(max_depth=max_depth)
            else:
                model = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, random_state=42)

        elif method == "random_forest":
            n_estimators = trial.suggest_int("n_estimators", 50, 200)
            max_depth = trial.suggest_int("max_depth", 2, 20)
            min_samples_split = trial.suggest_int("min_samples_split", 2, 10)
            min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 5)
            if self.use_cuml:
                model = cuRandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
            else:
                model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, random_state=42)

        elif method == "svc":
            C = trial.suggest_float("C", 0.1, 100.0, log=True)
            kernel = trial.suggest_categorical("kernel", ["linear", "poly", "rbf", "sigmoid"])
            gamma = trial.suggest_categorical("gamma", ["scale", "auto"])
            model = SVC(C=C, kernel=kernel, gamma=gamma, random_state=42)

        else:
            raise ValueError(f"Unsupported classification method: {method}")

        model.fit(self.X_train, self.y_train)
        y_pred = model.predict(self.X_val)
        return accuracy_score(self.y_val, y_pred)

    def find_best_classifier(self, method, n_trials=50):
        """
        Optimize the classification algorithm and find the best parameters.

        Parameters:
        method (str): The classification method to optimize.
        n_trials (int): The number of optimization trials.

        Returns:
        dict: The best parameters and corresponding metrics.
        """
        study = optuna.create_study(direction="maximize")
        study.optimize(lambda trial: self._objective(trial, method), n_trials=n_trials)

        best_params = study.best_params

        # Train the final model with the best parameters
        if method == "decision_tree":
            if self.use_cuml:
                model = cuDecisionTreeClassifier(**best_params)
            else:
                model = DecisionTreeClassifier(**best_params, random_state=42)

        elif method == "random_forest":
            if self.use_cuml:
                model = cuRandomForestClassifier(**best_params)
            else:
                model = RandomForestClassifier(**best_params, random_state=42)

        elif method == "svc":
            model = SVC(**best_params, random_state=42)

        else:
            raise ValueError(f"Unsupported classification method: {method}")

        model.fit(self.X, self.y)
        return {"best_params": best_params, "model": model}

    def evaluate(self, model):
        """
        Evaluate the classifier on various metrics.

        Parameters:
        model: The trained classification model.

        Returns:
        dict: A dictionary of evaluation metrics.
        """
        y_pred = model.predict(self.X_val)

        metrics = {
            "accuracy": accuracy_score(self.y_val, y_pred),
            "precision": precision_score(self.y_val, y_pred, average="weighted"),
            "recall": recall_score(self.y_val, y_pred, average="weighted"),
            "f1_score": f1_score(self.y_val, y_pred, average="weighted"),
            "confusion_matrix": confusion_matrix(self.y_val, y_pred).tolist(),
        }
        return metrics

    def generate(self, n_trials=20):
        """
        Generate classification results for a list of methods.

        Parameters:
        n_trials (int): Number of optimization trials for each method.

        Returns:
        dict: A dictionary with methods as keys and their results as values.
        """
        methods = ["decision_tree", "random_forest", "svc"]
        self.results = {}

        for method in methods:
            try:
                print(f"Optimizing method: {method}")
                result = self.find_best_classifier(method, n_trials=n_trials)
                evaluation_metrics = self.evaluate(result["model"])
                self.results[method] = {
                    "best_params": result["best_params"],
                    "metrics": evaluation_metrics,
                }
            except Exception as e:
                print(f"Error with method {method}: {e}")
                self.results[method] = {"error": str(e)}

        return self.results

    def save(self, name: str):
        """
        Save evaluation results to .tex files. Uses previously generated results.

        Parameters:
        name (str): Name of the directory to save the .tex files.
        """
        if self.results is None:
            raise ValueError("No results to save. Please run generate() first.")

        directory_path = "evaluation"
        dir = f"{directory_path}/{name}"

        # Create directory if it doesn't exist
        if not os.path.exists(dir):
            os.makedirs(dir)

        # Save results for each method
        for method, result in self.results.items():
            if "metrics" in result:
                metrics_df = pd.DataFrame([result["metrics"]])
                metrics_df.to_latex(f"{dir}/{method}_evaluation.tex", index=False)
            if "best_params" in result:
                params_df = pd.DataFrame([result["best_params"]])
                params_df.to_latex(f"{dir}/{method}_best_params.tex", index=False)
