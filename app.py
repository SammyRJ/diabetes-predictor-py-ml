from flask import Flask, render_template, request
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
from datetime import datetime

app = Flask(__name__)

# Load the saved model
model_path = 'ML_MODEL/random_forest_model.pkl'
model = joblib.load(model_path)

# Load the saved scaler
scaler_path = 'SCALER_DATA/scaler.pkl'
scaler = joblib.load(scaler_path)

# Define the numerical columns to standardize
numerical_cols = ['Cholesterol', 'Glucose', 'HDL_Chol', 'Ratio_Chol_HDL', 'Age', 'Height', 'Weight', 'BMI', 'Systolic_BP', 'Diastolic_BP', 'Waist', 'Hip', 'Ratio_Waist_Hip']

# Extract feature names from the model if they are available
try:
    expected_columns = model.feature_names_in_
except AttributeError:
    raise ValueError("The model does not contain feature names. Please ensure the model is trained with feature names.")

# Ensure the prediction results output folder exists
output_folder = 'PATIENT_PREDICTION_RECORDS'
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, 'predicted_results.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    probability = None
    plot_url = None
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        Gender = request.form['Gender']
        Age = int(request.form['Age'])
        Glucose = int(request.form['Glucose'])
        Cholesterol = int(request.form['Cholesterol'])
        HDL_Chol = int(request.form['HDL_Chol'])
        Height = int(request.form['Height'])
        Weight = int(request.form['Weight'])
        Systolic_BP = int(request.form['Systolic_BP'])
        Diastolic_BP = int(request.form['Diastolic_BP'])
        Waist = int(request.form['Waist'])
        Hip = int(request.form['Hip'])

        # Convert categorical inputs to numerical
        Gender = {'Male': 0, 'Female': 1}.get(Gender, 0)
        
        # Prepare input data as a DataFrame with original values
        input_data_original = pd.DataFrame({
            'Date_Time': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'First_Name': [first_name],
            'Last_Name': [last_name],
            'Gender_male': [1 if Gender == 0 else 0],
            'Gender_female': [1 if Gender == 1 else 0],
            'Glucose': [Glucose],
            'Ratio_Chol_HDL': [Cholesterol / HDL_Chol],
            'Cholesterol': [Cholesterol],
            'HDL_Chol': [HDL_Chol],
            'Age': [Age],
            'BMI': [Weight / (Height * Height) * 703],
            'Weight': [Weight],
            'Height': [Height],
            'Systolic_BP': [Systolic_BP],
            'Diastolic_BP': [Diastolic_BP],
            'Ratio_Waist_Hip': [Waist / Hip],
            'Waist': [Waist],
            'Hip': [Hip]
        })

        # Prepare input data for scaling and prediction
        input_data = input_data_original[['Gender_male', 'Gender_female', 'Glucose', 'Ratio_Chol_HDL', 'Cholesterol', 'HDL_Chol', 'Age', 'BMI', 'Weight', 'Height', 'Systolic_BP', 'Diastolic_BP', 'Ratio_Waist_Hip', 'Waist', 'Hip']]

        # Ensure columns are in the same order as during model training
        input_data = input_data[list(expected_columns)]
        
        # Standardize numerical columns using the loaded scaler
        input_data[numerical_cols] = scaler.transform(input_data[numerical_cols])

        # Debug: Print the input data
        print(input_data)

        # Prediction
        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)[0][1]

        # Debug: Print the prediction and probability
        print("Prediction:", prediction)
        print("Probability:", probability)
        
        # Plotting
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))

        sns.barplot(x=['Non-Diabetic', 'Diabetic'], y=[1 - probability, probability], ax=axes[0], palette=['#00FFFF', '#DC143C'])
        axes[0].set_title('Diabetic/Non-Diabetic Probability', color='white', fontweight='bold')
        axes[0].set_ylabel('Probability', color='white', fontweight='bold')
        axes[0].tick_params(axis='x', colors='white')
        axes[0].tick_params(axis='y', colors='white')

        # Pie chart with white text and bold fonts
        wedges, texts, autotexts = axes[1].pie([1 - probability, probability], labels=['Non-Diabetic', 'Diabetic'], autopct='%1.1f%%', colors=['#00FFFF', '#DC143C'], textprops={'color': 'white', 'fontweight': 'bold'})
        axes[1].set_title('Diabetic/Non-Diabetic Pie Chart', color='white', fontweight='bold')

        # Adjust text properties for autotexts (percentage values inside pie)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        # Set background color to transparent
        fig.patch.set_alpha(0)

        # Save plot to a PNG in-memory with transparent background and white text
        png_image = io.BytesIO()
        plt.savefig(png_image, format='png', transparent=True)
        png_image.seek(0)
        plot_url = base64.b64encode(png_image.getvalue()).decode('utf8')

        # Add prediction and probability to input data with original values
        input_data_original['Prediction'] = prediction
        input_data_original['Prediction'] = input_data_original['Prediction'].map({0: 'Non-Diabetic', 1: 'Diabetic'})
        input_data_original['Probability'] = round(probability, 4)  # Round probability to 4 decimal places
        
        # Round numerical columns (you can adjust decimal places as needed)
        rounding_columns = ['Glucose', 'Ratio_Chol_HDL', 'Cholesterol', 'HDL_Chol', 'Age', 'BMI', 'Weight', 'Height', 'Systolic_BP', 'Diastolic_BP', 'Ratio_Waist_Hip', 'Waist', 'Hip']
        input_data_original[rounding_columns] = input_data_original[rounding_columns].round(2)  # Round to 2 decimal places

        # Save or append result to CSV
        if not os.path.isfile(output_file):
            input_data_original.to_csv(output_file, index=False)
        else:
            input_data_original.to_csv(output_file, mode='a', header=False, index=False)
    
    return render_template('index.html', prediction=prediction, probability=probability, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
