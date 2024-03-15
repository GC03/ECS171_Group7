from flask import Flask, request, jsonify
import kmeans
import randomforest
import regression

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get the JSON data from the request body
    model = data['model']
    inputs = data['inputs']
    
    # Perform prediction using the selected model and inputs
    if model == "kmeans":
        prediction = kmeans_model.predict(inputs)
    elif model == "random_forest":
        prediction = rf_model.predict(inputs)
    elif model == "regression":
        prediction = regression_model.predict(inputs)

    prediction = f"Predicted result using {model}: {inputs}, estimated house value is {prediction}"
    # Return the prediction as JSON response
    return jsonify({'prediction': prediction})



if __name__ == '__main__':
    kmeans_model = kmeans.model
    rf_model = randomforest.model
    regression_model = regression.model
    app.run(port=3000)
    