import pandas as pd
from .classifierGenerator import ClassifierGenerator
from .cluster_generator import ClusterGenerator
from .regressor_generator import RegressionGenerator

class MasterGenerator:

    def __init__(self, X, y_categ, y_numeric, name, n_tries, CUML = False):
        self.X = X
        self.y_categ = y_categ
        self.y_numeric = y_numeric
        self.name = name
        self.n_tries = n_tries
        self.CUML = CUML

    def _regression_generate (self):
        regression_generator = RegressionGenerator(X=self.X, y=self.y_numeric, use_cuml=self.CUML)
        regression_generator.generate(n_trials=self.n_tries)
        regression_generator.save(self.name)

    def _classification_generate(self):
        classifier_generator = ClassifierGenerator(dataset=self.X, target_column=self.y_categ, use_cuml=self.CUML)
        classifier_generator.generate(n_trials=self.n_tries)
        classifier_generator.save(self.name)

    def _clustering_generate(self):
        cluster_generator = ClusterGenerator (dataset=self.X, use_cuml=self.CUML)
        cluster_generator.generate(n_trials=self.n_tries, ground_truth=self.y_categ)
        cluster_generator.save(self.name)

    def generate(self):
        self._regression_generate()

        self._classification_generate()

        self._clustering_generate()