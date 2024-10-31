from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, log_loss
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class evaluator():

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
    def equal_depth_binning(arr: np.array, bins=5, precision=2):
        # Create 5 equal-depth bins using pd.qcut
        bins = pd.qcut(arr, q=bins, precision=precision, duplicates='drop')
        
        # Get the frequency count for each bin
        bin_counts = bins.value_counts().sort_index()
        
        # Create a dictionary with string representations of each range and frequencies
        result = {str(bin_range): count for bin_range, count in bin_counts.items()}
        
        return result

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
    def eval_regression(y_pred, y_true, plot: bool = True):
        mae = mean_absolute_error(y_true, y_pred)
        mse = evaluator.mean_squared_error(y_true, y_pred)
        rmse = evaluator.mean_squared_error(y_true, y_pred, squared=False)
        r2 = r2_score(y_true, y_pred)
        mape = evaluator.mean_absolute_percentage_error(y_true, y_pred)
        print("MAE:", mae, "MSE:", mse, "RMSE:", rmse, "R2:", r2, "MAPE:", mape)

        diff = np.abs( y_pred - y_true )
        mean, variance, std_dev = evaluator.calculate_statistics(diff)
        print("Mean:", mean)
        print("Variance:", variance)
        print("Standard Deviation:", std_dev)

        frequencies = evaluator.equal_depth_binning(diff)
        if plot:
            evaluator.plot_bar_chart(data=frequencies, title="Error frequeancies", xlabel="Range", ylabel="Frequency")
        print(frequencies)
            

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

    @staticmethod
    def eval_ordinal_classification(diff, plot = True):
        '''
        This function receives a numerical array of the absolute difference between the prediction and the actual value
        '''
        errors = evaluator.equal_depth_binning(diff[diff > 0])

        if plot : evaluator.plot_bar_chart(data=errors, title="Error frequeancies", xlabel="Range", ylabel="Frequency")

        print("Errors:",errors)
        print("Error mean:", np.mean(diff[diff > 0]))
        print("Error rate:", len(diff[diff > 0])/len(diff)*100, "%")
        print("Overall mean:", np.mean(diff))
