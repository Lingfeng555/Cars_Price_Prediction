from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, log_loss
import numpy as np

class evaluator():

    @staticmethod
    def mean_squared_error(y_true, y_pred, squared=True):
        mse = np.mean((y_true - y_pred) ** 2)
        if not squared:
            return np.sqrt(mse)
        return mse

    @staticmethod
    def eval_regression(y_pred, y_true):
        mae = mean_absolute_error(y_true, y_pred)
        mse = evaluator.mean_squared_error(y_true, y_pred)
        rmse = evaluator.mean_squared_error(y_true, y_pred, squared=False)
        r2 = r2_score(y_true, y_pred)
        print("MAE:", mae, "MSE:", mse, "RMSE:", rmse, "R2:", r2)

    @staticmethod
    def eval_classfication(y_pred, y_true, binary_classification, average='weighted'):
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average=average)
        recall = recall_score(y_true, y_pred, average=average)
        f1 = f1_score(y_true, y_pred, average=average)
        conf_matrix = confusion_matrix(y_true, y_pred)
    
        print("Accuracy:", accuracy, "Precision:", precision, "Recall:", recall, "F1 Score:", f1)
        print("Confusion Matrix:\n", conf_matrix)

        if binary_classification : 
            roc_auc = roc_auc_score(y_true, y_pred)
            print("ROC AUC:", roc_auc)