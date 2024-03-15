import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
import os

# Get the directory path of the Flask script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative file path
csv_file_path = os.path.join(script_dir, 'housing.csv')


# importing data from csv file to dataframe using pandas library
data = pd.read_csv(csv_file_path)
original_columns = data.drop(["median_house_value"], axis=1).columns

## drop the missing vale datapoint
data.dropna(inplace=True)

oec = OneHotEncoder()
ocean_proximity_encoded = oec.fit_transform(data[['ocean_proximity']]).toarray()

columns = oec.get_feature_names_out(['ocean_proximity'])
ocean_proximity_df = pd.DataFrame(ocean_proximity_encoded, columns=columns)

ocean_proximity_df.index = data.index

## drop two columns (ocean_proximity and median_house_value)
## because we add onehotencoder for ocean_proximity
## and we need to predict median house value
X = pd.concat([data.drop(['ocean_proximity', 'median_house_value'], axis=1), ocean_proximity_df], axis=1)
y = data['median_house_value']

X.fillna(X.median(), inplace=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
rf = RandomForestRegressor(n_estimators=100, random_state=42)

## train model
rf.fit(X_train, y_train)

class rf_model:
    def __init__(self, encoder, rf):
        self.oec = encoder
        self.rf = rf
    
    def predict(self, values):
        values = pd.DataFrame([values], columns=original_columns)
        ocean_prox_encoded = oec.transform(values[["ocean_proximity"]]).toarray()
        columns = oec.get_feature_names_out(['ocean_proximity'])
        ocean_prox_df = pd.DataFrame(ocean_prox_encoded, columns=columns)

        values = pd.concat([values.drop(["ocean_proximity"], axis=1), ocean_prox_df], axis=1)
        
        return self.rf.predict(values)[0]
    
model = rf_model(oec, rf)