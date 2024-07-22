

# Diabetes Predictor using Python and Machine Learning

This project implements a diabetes predictor using machine learning techniques in Python. It includes preprocessing steps, model training, evaluation, and prediction functionalities.

## Features

- **Data Preprocessing**: Clean and prepare the dataset for machine learning.
- **Model Training**: Train machine learning models using various algorithms.
- **Evaluation**: Evaluate model performance using metrics like accuracy, precision, and recall.
- **Prediction**: Make predictions on new data using trained models.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SammyRJ/diabetes-predictor-py-ml.git
   ```

2. Navigate to the project directory:
   ```bash
   cd diabetes-predictor-py-ml
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### The model has already been trained. Run the application script to start using the prediction model:
   ```bash
   python app.py
   ```
   After execution, open your web browser and go to `http://127.0.0.1:5000` to access the application.

### If you want to train the model on your own:

1. **Install Jupyter Notebook**: If you haven't already installed Jupyter Notebook, you can do so using pip:
   ```bash
   pip install notebook
   ```

2. **Open the Notebook**: Once Jupyter Notebook is installed, navigate to the directory where `Diabetes_Analysis.ipynb` is located using your command line or terminal.

3. **Start Jupyter Notebook**: Run the following command to start the Jupyter Notebook server:
   ```bash
   jupyter notebook
   ```
   
## Prediction History:

The prediction records are stored in the directory `PATIENT_PREDICTION_RECORDS`, in the file `predicted_results.csv`. You can access the previous predictions through this file.
