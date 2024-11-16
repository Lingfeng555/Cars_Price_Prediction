from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


class Evaluator():

    regression_register = {"Algorithm": [], "mae": [], "mse": [], "mape": [] ,"r2": [], "error_mean": [], "error_std_dev": [], "adjuste_r2": []}
    classification_register = {"Algorithm": [], "accuracy": [], "precision": [], "recall": [] ,"f1": [], "roc_auc": []}

    @staticmethod
    def mean_absolute_percentage_error(y_true, y_pred):
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    @staticmethod
    def mean_squared_error(y_true, y_pred, squared=True):
        mse = np.mean((y_true - y_pred) ** 2)
        if not squared:
            return np.sqrt(mse)
        return mse

    @staticmethod
    def calculate_statistics(arr):
        mean = np.mean(arr)
        variance = np.var(arr)
        std_dev = np.std(arr)
        return mean, variance, std_dev
    
    @staticmethod
    def equal_depth_binning(arr: np.array):
        values, counts = np.unique(arr, return_counts=True)
        counts_dict = dict(zip(values, counts))
        return counts_dict
    
    @staticmethod
    def adjustedr2(y_true, y_pred, n_features):
        n = len(y_true)
        r2 = r2_score(y_true, y_pred)
        adjusted_r2 = 1 - ((1 - r2) * (n - 1) / (n - n_features - 1))
        return adjusted_r2
    
    @staticmethod
    def regression_error_distribution(y_pred: np.array, y_true: np.array,  bins: int, plot:bool):
        lower_limit = min(y_true)
        upper_limit = max(y_pred)

        data = pd.DataFrame({"pred": y_pred, "true": y_true, "diff": np.abs(y_pred-y_true)})

        bin_depth = (upper_limit - lower_limit)/bins

        result = {"bin_label":[] ,"mean": [], "variance": [], "std_dev": [], "max_error": [], "min_error": [], "n_sample":[]}

        for i in range(1, bins):
            errors = data["diff"][(data["true"] <= bin_depth * i) & (data["true"] > bin_depth * (i - 1))].to_numpy()

            mean, variance, std_dev = Evaluator.calculate_statistics(errors)
            result["mean"].append(mean)
            result["variance"].append(variance)
            result["std_dev"].append(std_dev)
            
            result["max_error"].append(np.max(errors))
            result["min_error"].append(np.min(errors))
            result["bin_label"].append(f"({bin_depth*i}, {bin_depth*(i-1)}]")
            result["n_sample"].append(np.size(errors))

        result = pd.DataFrame(result)
        
        if plot : 
            colnames = result.columns.to_list()
            colnames.remove("bin_label")

            for col in colnames:
                Evaluator.plot_bar_chart_key_value(keys = result["bin_label"], values=result[col], title=col, xlabel=col, ylabel="bin_label")

        return result

    @staticmethod
    def plot_bar_chart_key_value(keys: list, values: list, title="Bar Chart", xlabel="Keys", ylabel="Values"):
        plt.figure(figsize=(10, 5))  # Set the figure size
        plt.bar(keys, values, color='black')  # Create a bar chart
        plt.xlabel(xlabel)  # Set the label for the x-axis
        plt.ylabel(ylabel)  # Set the label for the y-axis
        plt.title(title)  # Set the title of the chart
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability if needed
        plt.tight_layout()  # Adjust layout to not cut off elements
        plt.show()


    @staticmethod
    def plot_bar_chart(data: dict, title="Bar Chart", xlabel="Keys", ylabel="Values"):
        keys = list(data.keys())
        values = list(data.values())

        plt.figure(figsize=(10, 5))  # Set the figure size
        plt.bar(keys, values, color='blue')  # Create a bar chart
        plt.xlabel(xlabel)  # Set the label for the x-axis
        plt.ylabel(ylabel)  # Set the label for the y-axis
        plt.title(title)  # Set the title of the chart
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability if needed
        plt.tight_layout()  # Adjust layout to not cut off elements
        plt.show()

    @staticmethod
    def eval_regression(y_pred, y_true, plot: bool = True, bins = 5, n_features = None, regressor_name = None):
        mae = mean_absolute_error(y_true, y_pred)
        mse = Evaluator.mean_squared_error(y_true, y_pred)
        rmse = Evaluator.mean_squared_error(y_true, y_pred, squared=False)
        r2 = r2_score(y_true, y_pred)
        mape = Evaluator.mean_absolute_percentage_error(y_true, y_pred)
        print("MAE:", mae, "\n", "MSE:", mse, "\n",  "RMSE:", rmse, "\n", "R2:", r2, "\n", "MAPE:", mape)

        diff = np.abs( y_pred - y_true )
        mean, variance, std_dev = Evaluator.calculate_statistics(diff)
        print("Mean:", mean)
        print("Variance:", variance)
        print("Standard Deviation:", std_dev)

        r2_adjusted = None
        if (n_features != None): 
            r2_adjusted = Evaluator.adjustedr2(y_pred=y_pred, y_true=y_true, n_features=n_features)
            print("r2_adjusted:", r2_adjusted)

        if (regressor_name != None):
            Evaluator.register_regression(regressor_name, mae, mse, r2, mape, mean, std_dev, r2_adjusted)
        
        return Evaluator.regression_error_distribution(y_pred, y_true,  bins = bins, plot = plot)

    @staticmethod
    def register_regression(regressor_name, mae, mse, r2, mape, mean, std_dev, r2_adjusted):
        Evaluator.regression_register["Algorithm"].append(regressor_name)
        Evaluator.regression_register["mae"].append(round(mae, 4))
        Evaluator.regression_register["mse"].append(round(mse, 4))
        Evaluator.regression_register["mape"].append(round(mape, 4))
        Evaluator.regression_register["r2"].append(round(r2, 4))
        Evaluator.regression_register["error_mean"].append(round(mean, 4))
        Evaluator.regression_register["error_std_dev"].append(round(std_dev, 4))
        Evaluator.regression_register["adjuste_r2"].append(round(r2_adjusted, 4) if r2_adjusted is not None else None)

            

    @staticmethod
    def eval_classfication(y_pred, y_true, binary_classification, average='weighted', classifier_name = None):
        """
        Evaluates classification model performance and prints key metrics.
        """
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average=average)
        recall = recall_score(y_true, y_pred, average=average)
        f1 = f1_score(y_true, y_pred, average=average)
        conf_matrix = confusion_matrix(y_true, y_pred)
    
        print("Accuracy:", accuracy, "\n", "Precision:", precision, "\n", "Recall:", recall, "\n", "F1 Score:", f1)
        print("Confusion Matrix:\n", conf_matrix)

        roc_auc = None
        if binary_classification : 
            roc_auc = roc_auc_score(y_true, y_pred)
            print("ROC AUC:", roc_auc)

        if classifier_name != None:
            Evaluator.register_classification(classifier_name, accuracy, precision, recall, f1, roc_auc)

    @staticmethod
    def register_classification(classifier_name, accuracy, precision, recall, f1, roc_auc):
        Evaluator.classification_register["Algorithm"].append(classifier_name)
        Evaluator.classification_register["accuracy"].append(round(accuracy, 4))
        Evaluator.classification_register["precision"].append(round(precision, 4))
        Evaluator.classification_register["recall"].append(round(recall, 4))
        Evaluator.classification_register["f1"].append(round(f1, 4))
        Evaluator.classification_register["roc_auc"].append(round(roc_auc, 4) if roc_auc is not None else None)


    @staticmethod
    def eval_ordinal_classification(diff, plot = True):
        '''
        This function receives a numerical array of the absolute difference between the prediction and the actual value
        '''
        errors = Evaluator.equal_depth_binning(diff[diff > 0])

        if plot : Evaluator.plot_bar_chart(data=errors, title="Error frequeancies", xlabel="Range", ylabel="Frequency")
        print(errors)
        print("Error mean:", np.mean(diff[diff > 0]))
        print("Error rate:", len(diff[diff > 0])/len(diff)*100, "%")
        print("Overall mean:", np.mean(diff))
    
    @staticmethod
    def save(name):
        """
        Saves the regression_register and classification_register as CSV files.

        Parameters:
        - file_path: str - Base file path for saving the results (default is "evaluation_results").
        """
        directory_path = "evaluation"
        file_path = f"{directory_path}/{name}"

        # Create the 'evaluation' directory if it doesn't exist
        os.makedirs(directory_path, exist_ok=True)

        # Save the regression register
        regression_df = pd.DataFrame(Evaluator.regression_register)
        regression_csv_path = f"{file_path}_regression.csv"
        regression_df.to_csv(regression_csv_path, index=False)
        print(f"Regression results saved to: {regression_csv_path}")

        # Save the classification register
        classification_df = pd.DataFrame(Evaluator.classification_register)
        classification_csv_path = f"{file_path}_classification.csv"
        classification_df.to_csv(classification_csv_path, index=False)
        print(f"Classification results saved to: {classification_csv_path}")