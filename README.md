![OptiFeed Logo](https://fishfeed.retool.com/api/file/0800ef5b-2dd5-4e45-85de-4c79042814d6)

# OptiFeed - Fish Feed Prediction API

## Project Overview

**OptiFeed** is a Flask-based API designed to predict the optimal amount of feed required for fish farming based on various environmental and fish-specific sensor data. The project supports model training and utilisation using IBM Machine Learning or Watson Studio, offering flexibility. Additionally, the API includes functionality to periodically retrain the model with updated sensor data, ensuring predictions remain accurate over time.

This MVP uses **Retool** to handle the API front-end interface, making it easy to visualize, monitor, and interact with the model predictions and sensor data.

## Key Features
- **Prediction Endpoint**: Predicts the optimal fish feed amount based on sensor data.
- **Model Retraining**: Automatically retrains the model after a configurable number of data points or when triggered manually.
- **Health Check**: Basic endpoint to check if the API is running.
- **IBM Cloud Object Storage Integration**: Upload functionality to IBM COS for additional data management capabilities (e.g., storing sensor data or models).

## API Endpoints
- `GET /health`: Health check to ensure the API is running.
- `POST /predict`: Submit sensor data in JSON format to get a feed amount prediction.
- `POST /retrain`: Manually retrain the machine learning model using stored data.

## Usage Instructions

### 1. Set up Environment
Before running the application, ensure you have a `.env` file with the following configurations:

```bash
FLASK_ENV=development
SECRET_KEY=
IBM_API_KEY_ID=
IBM_SERVICE_INSTANCE_ID=
IBM_ENDPOINT_URL=
COS_BUCKET_NAME=
RETRAIN_THRESHOLD=50
PORT=5000
```

### 2. Running the App Locally
Install the required dependencies and run the app:

```bash
pip install -r requirements.txt
source .venv/bin/activate
cd backend
python -m app.main
```

The application will be available at `http://localhost:5000`.

### 3. Using Retool for the MVP
For the MVP version, **Retool** is used as the front-end for interacting with the API. To run the application with Retool:

1. **Import the Project**:
   - Clone this repository and import the necessary code into your Retool workspace.

2. **Connect API to Retool**:
   - Set up a Retool app that connects to the API endpoints (e.g., `/predict`, `/retrain`) to visualize predictions and retrain the model from the front-end.

3. **Visualize and Trigger Predictions**:
   - Use Retool to send sensor data to the API, view the predictions, and trigger model retraining as needed.

### 4. Sensor Data Example
Here's an example of the sensor data format to be sent in JSON format to the `/predict` endpoint:

```json
{
“fish_size_kg”: 1.5,
“fish_length_cm”: 35.0,
“water_temperature_C”: 22.5,
“phosphorus_mg_L”: 0.8,
“nitrogen_mg_L”: 1.2,
“oxygen_mg_L”: 8.0,
“light_LUX”: 500.0,
“fish_speed_m_s”: 0.05,
“fish_health”: 9
}
```

## Future Improvements
- Integrating a persistent database for sensor data storage (e.g., Cloudant or PostgreSQL).
- Enhanced security with authentication and rate limiting.
- Improve integration to IBM Watson Machine Learning for cloud-based model management.
- Scale up using IBM Functions or IBM Cloud Kubernetes Service.


## License
This project is open-source under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
