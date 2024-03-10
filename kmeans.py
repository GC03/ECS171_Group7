import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
import os

# Get the directory path of the Flask script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative file path
csv_file_path = os.path.join(script_dir, 'housing.csv')

# Data preprocessing
data = pd.read_csv(csv_file_path)
original_columns = data.drop(["median_house_value"], axis=1).columns
data = data.dropna()
data = data[data['ocean_proximity'] != 'ISLAND']
data, median_house_value = data.drop(["median_house_value"], axis=1), data[["median_house_value"]]

oec = OneHotEncoder()
ocean_proximity_encoded = oec.fit_transform(data[['ocean_proximity']]).toarray()

columns = oec.get_feature_names_out(['ocean_proximity'])
ocean_proximity_df = pd.DataFrame(ocean_proximity_encoded, columns=columns)

ocean_proximity_df.index = data.index

normalizedData = pd.DataFrame()
scaler = MinMaxScaler()
for i in range(data.shape[1] - 1):
    normalData = scaler.fit_transform(data.iloc[:, i].values.reshape(-1, 1))
    normalizedData[data.columns[i]] = pd.Series(np.ravel(normalData))
normalizedData.index = data.index

data = pd.concat([normalizedData, ocean_proximity_df], axis=1)

# Fit the KMeans model
k = 4
trained_model = KMeans(n_clusters=k, n_init="auto").fit(np.asarray(data))
model_labels = pd.Series(trained_model.labels_, name='class')
median_house_value["Label"] = model_labels
house_value_grouped = median_house_value.groupby("Label").mean()

# The model
class kmean_model:
    def __init__(self, encoder, kmeans_model) -> None:
        self.oec = encoder
        self.kmeans = kmeans_model

    def predict(self, values):
        values = pd.DataFrame([values], columns=original_columns)
        ocean_prox_encoded = oec.transform(values[["ocean_proximity"]]).toarray()
        columns = oec.get_feature_names_out(['ocean_proximity'])
        ocean_prox_df = pd.DataFrame(ocean_prox_encoded, columns=columns)

        values = pd.concat([values.drop(["ocean_proximity"], axis=1), ocean_prox_df], axis=1)
        predicted_label = self.kmeans.predict(values).tolist()[0]
        
        predicted_median_house_value = house_value_grouped.loc[predicted_label, "median_house_value"]
        return predicted_median_house_value
        

# Create the kmean_model instance
model = kmean_model(oec, trained_model)

