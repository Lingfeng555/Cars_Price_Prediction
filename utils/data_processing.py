import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import chi2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import prince
import numpy as np

'''
This is an global encoder
'''
label_encoder = LabelEncoder()

def fill_na_with_mode(df, column_name, inplace=False):
    if column_name in df.columns:
        mode_value = df[column_name].mode().iloc[0]
        df[column_name] = df[column_name].fillna(mode_value, inplace=inplace)
    else:
        print(f"La columna '{column_name}' no existe en el DataFrame.")
    return df

def impute_with_linear_regression(data, x_columns, y_column):
    df_with_target = data.dropna(subset=[y_column])
    df_without_target = data[data[y_column].isna()]
    
    X_train = df_with_target[x_columns]
    y_train = df_with_target[y_column]
    X_test = df_without_target[x_columns]
    
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_train)
    epsilon = np.finfo(np.float64).eps
    mape = np.mean(np.abs((y_train - y_pred) / (y_train + epsilon))) * 100
    print(f"Regression mape {x_columns} -> {y_column}: {mape}%")
    if not X_test.empty:
        predicted_values = model.predict(X_test)
        data.loc[data[y_column].isna(), y_column] = predicted_values
    return data

def remove_redundand_columns(df:pd.DataFrame )->pd.DataFrame:
    for column in df.columns: #Remove redundant columns
        unique_values = df[column].dropna().unique() 
        if len(unique_values) == 1:
            df = df.drop(column, axis=1)
    return df

def __impute_categorical_mode(df, X, Y):
    # Agrupar por las columnas X y calcular el valor más común (moda) en la columna Y para cada grupo
    modes = df.groupby(X,observed=False)[Y].agg(lambda x: x.dropna().mode()[0] if not x.dropna().empty else None, ).reset_index()
    modes.rename(columns={Y: 'Mode'}, inplace=True)
    
    # Unir el DataFrame original con los modos encontrados para facilitar la imputación
    df = df.merge(modes, on=X, how='left')
    
    # Imputar los valores NaN en Y usando el valor más común de su grupo
    df[Y] = df.apply(lambda row: row['Mode'] if pd.isna(row[Y]) else row[Y], axis=1)

    # Eliminar la columna auxiliar 'Mode' añadida para la imputación
    df.drop('Mode', axis=1, inplace=True)
    
    return df

def impute_categorical_mode(df, X, Y):
    for i in range(len(X)):
        df = __impute_categorical_mode(df, X, Y)
        X.pop(len(X)-1)
    df[Y] = df[Y].fillna("unkown") #If is a unique car
    return df

def CA (categorical_columns, col_x, col_y):
    contingency_table = pd.crosstab(categorical_columns[col_x], categorical_columns[col_y])

    P = contingency_table / contingency_table.values.sum()

    # Calcular los perfiles de fila y columna (matrices D_r y D_c)
    D_r = np.diag(1 / P.sum(axis=1))
    D_c = np.diag(1 / P.sum(axis=0))

    # Calcular la matriz S (correspondencia ajustada)
    S = np.sqrt(D_r).dot(P).dot(np.sqrt(D_c))

    # Aplicar SVD
    svd = TruncatedSVD(n_components=2)
    svd.fit(S)
    row_coordinates = svd.transform(S)  # Coordenadas de las filas
    col_coordinates = svd.components_.T  # Coordenadas de las columnas

    # Visualización
    plt.figure(figsize=(8, 8))
    for i, label in enumerate(contingency_table.index):
        plt.scatter(row_coordinates[i, 0], row_coordinates[i, 1], color='blue')
        plt.text(row_coordinates[i, 0], row_coordinates[i, 1], f'{label}', color='blue', ha='right', va='bottom')
    for i, label in enumerate(contingency_table.columns):
        plt.scatter(col_coordinates[i, 0], col_coordinates[i, 1], color='red', marker='^')
        plt.text(col_coordinates[i, 0], col_coordinates[i, 1], f'{label}', color='red', ha='left', va='top')

    plt.xlabel('Componente 1')
    plt.ylabel('Componente 2')
    plt.title('Gráfico de Análisis de Correspondencias')
    plt.grid(True)
    plt.show()

def chi_square_test(categorical_columns: pd.DataFrame, column_y: str):
    encoded_df = categorical_columns.copy()
    for col in categorical_columns.columns:
        encoded_df[col] = label_encoder.fit_transform(encoded_df[col])

    X = encoded_df.drop(columns=[column_y])
    y = encoded_df[column_y]

    # Realizar la prueba de chi-cuadrado
    chi2_stat, p_values = chi2(X, y)

    # Crear un DataFrame para mostrar los resultados
    results = pd.DataFrame({
        'Feature': X.columns,
        'Chi2 Stat': chi2_stat,
        'p-value': p_values
    })

    # Ordenar los resultados por el valor p
    results.sort_values('p-value', inplace=True)

    plt.figure(figsize=(10, 6))
    plt.barh(results['Feature'], results['p-value'], color='skyblue')
    plt.xlabel('p-value')
    plt.ylabel('Features')
    plt.title('Chi-Square Test Results')
    plt.gca().invert_yaxis()  # Invertir el eje y para que la característica con menor p-value esté arriba
    plt.show()

    # Mostrar el DataFrame de resultados
    return results

def chi_square_filter(categorical_columns: pd.DataFrame, column_y: str, p_value_filter: float) -> pd.DataFrame:
    result = chi_square_test(categorical_columns=categorical_columns, column_y=column_y)
    columns = list(result[ result["p-value"] <= p_value_filter ]["Feature"])
    columns.append("price_categ")
    return categorical_columns[ columns ]