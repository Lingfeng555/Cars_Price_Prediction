import cuml.ensemble
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from cuml.ensemble import RandomForestClassifier, DecisionTreeClassifier