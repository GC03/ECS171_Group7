import React, { useState } from 'react';

function App() {
  const [selectedModel, setSelectedModel] = useState('');
  const [inputValues, setInputValues] = useState([
    '', // Longitude
    '', // Latitude
    '', // Housing Median Age
    '', // Total number of rooms
    '', // Total number of bedrooms
    '', // Population
    '', // Households
    '', // Median Income
    '', // Ocean Proximity
  ]);
  const [prediction, setPrediction] = useState('');

  const handleModelChange = (event) => {
    setSelectedModel(event.target.value);
  };

  const handleOceanProximityChange = (event) => {
    const newInputValues = [...inputValues];
    newInputValues[8] = event.target.value;
    setInputValues(newInputValues);
  };

  const handleInputChange = (event, index) => {
    const newInputValues = [...inputValues];
    newInputValues[index] = event.target.value;
    setInputValues(newInputValues);
  };

  const handlePrediction = async () => {
    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model: selectedModel, inputs: inputValues }),
      });

      const data = await response.json();
      setPrediction(data.prediction);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>ML Model Frontend</h1>
      <div>
        <label>Select Model:</label>
        <select value={selectedModel} onChange={handleModelChange}>
          <option value="">--Select Model--</option>
          <option value="kmeans">K-Means Clustering</option>
          <option value="random_forest">Random Forest</option>
          <option value="regression">Regression</option>
        </select>
      </div>
      <div>
        <h2>Input Fields:</h2>
        <div>
          <div>
            <label>Longitude:</label>
            <input
              type="text"
              value={inputValues[0]}
              onChange={(event) => handleInputChange(event, 0)}
            />
          </div>
          <div>
            <label>Latitude:</label>
            <input
              type="text"
              value={inputValues[1]}
              onChange={(event) => handleInputChange(event, 1)}
            />
          </div>
          <div>
            <label>Housing Median Age:</label>
            <input
              type="text"
              value={inputValues[2]}
              onChange={(event) => handleInputChange(event, 2)}
            />
          </div>
          <div>
            <label>Total number of rooms:</label>
            <input
              type="text"
              value={inputValues[3]}
              onChange={(event) => handleInputChange(event, 3)}
            />
          </div>
        </div>
        <div>
          <div>
            <label>Total number of bedrooms:</label>
            <input
              type="text"
              value={inputValues[4]}
              onChange={(event) => handleInputChange(event, 4)}
            />
          </div>
          <div>
            <label>Population:</label>
            <input
              type="text"
              value={inputValues[5]}
              onChange={(event) => handleInputChange(event, 5)}
            />
          </div>
          <div>
            <label>Households:</label>
            <input
              type="text"
              value={inputValues[6]}
              onChange={(event) => handleInputChange(event, 6)}
            />
          </div>
          <div>
            <label>Median Income:</label>
            <input
              type="text"
              value={inputValues[7]}
              onChange={(event) => handleInputChange(event, 7)}
            />
          </div>
        </div>
        <div>
          <div>
            <label>Ocean Proximity:</label>
            <select value={inputValues[8]} onChange={handleOceanProximityChange}>
              <option value="">--Select--</option>
              <option value="<1H OCEAN">Less than 1H from Ocean"</option>
              <option value="INLAND">Inland</option>
              <option value="NEAR BAY">Near Bay</option>
              <option value="NEAR OCEAN">Near Ocean</option>
        </select>
          </div>
        </div>
      </div>
      <button disabled={!selectedModel || inputValues.includes('')} onClick={handlePrediction}>
        Submit
      </button>
      {prediction && (
        <div>
          <h2>Median Housing Price Prediction:</h2>
          <p>{prediction}</p>
        </div>
      )}
    </div>
  );
}

export default App;