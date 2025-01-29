# 🚗 Car Price Prediction using Machine Learning

## 📌 Overview
This repository contains the implementation of a **machine learning pipeline** for analyzing and predicting second-hand car prices based on various features such as mileage, engine capacity, brand, and fuel type. The project includes **regression, classification, and clustering tasks**, as well as deep learning techniques for **natural language processing (NLP) and computer vision**.

## 📊 Dataset
- **Name**: Cars Specifications Dataset
- **Source**: Web scraping
- **Size**: 146 features including technical, environmental, and performance specifications.

## 🔍 Tasks Implemented
✔️ **Regression**: Predicting car prices based on vehicle attributes.  
✔️ **Classification**: Categorizing cars into environmental labels (ECO, C, D).  
✔️ **Clustering**: Grouping cars based on technical features.  
✔️ **Algorithm Comparison**: Evaluating traditional ML vs deep learning models.  
✔️ **NLP Task**: Predicting car price based on textual descriptions.  
✔️ **Computer Vision**: Classifying car brands using images.  

## 🏆 Best Performing Models
| Task | Best Model |
|------|-----------|
| **Regression** | Random Forest (lowest MAE & MSE) |
| **Classification** | Random Forest (highest accuracy & F1-score) |
| **Clustering** | Agglomerative Clustering (highest silhouette score) |
| **NLP** | LSTM-based model using BETO embeddings |
| **Computer Vision** | Convolutional Neural Network (CNN) |

## ⚙️ Data Processing
- **Feature Engineering**: Extracted structured features using regex.
- **Handling Missing Data**: Used regression-based imputation and categorical mode assignment.
- **Dimensionality Reduction**: PCA and Truncated SVD applied.
- **Data Standardization**: Normalization and one-hot encoding.

## 📂 Repository Structure
```
📂 data/                     # Processed datasets
📂 preprocessing/            # Data cleaning & feature extraction
📂 models/                   # Trained ML & DL models
📂 scripts/                  # Training and evaluation scripts
📂 notebooks/                # Jupyter Notebooks with analysis
📂 utils/                    # Helper functions for preprocessing & visualization
```

## 📈 Results & Insights
- **Price trends**: Car price is strongly influenced by engine power, mileage, and brand.
- **Brand value**: Some brands retain value better in the second-hand market.
- **Model performance**: Random Forest consistently outperforms simpler linear models.
- **Feature importance**: Power, mileage, and environmental labels are key indicators of price.

## 🔗 References
- 📑 [Project Report](https://github.com/Lingfeng555/Cars_Price_Prediction/blob/main/Machine_Learning_Final-2-1.pdf)
- 📊 [Data Preprocessing](https://github.com/Lingfeng555/Cars_Price_Prediction/blob/main/Preprocessing/)
