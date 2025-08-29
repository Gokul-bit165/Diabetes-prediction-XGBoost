import gradio as gr
import pandas as pd
import pickle

# Load saved model & scaler
with open("diabetes_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Prediction function
def predict_diabetes(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age):
    input_data = pd.DataFrame([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]],
                              columns=["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    if prediction == 1:
        return f"⚠️ High Risk of Diabetes (Probability: {probability:.2f})"
    else:
        return f"✅ Low Risk of Diabetes (Probability: {probability:.2f})"

# Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🩺 Diabetes Prediction App")
    gr.Markdown("Enter details to check risk of diabetes.")

    with gr.Row():
        with gr.Column():
            Pregnancies = gr.Slider(0, 20, step=1, label="Pregnancies")
            Glucose = gr.Slider(0, 200, step=1, label="Glucose")
            BloodPressure = gr.Slider(0, 130, step=1, label="Blood Pressure")
            SkinThickness = gr.Slider(0, 100, step=1, label="Skin Thickness")
            Insulin = gr.Slider(0, 900, step=1, label="Insulin")
            BMI = gr.Slider(10, 70, step=0.1, label="BMI")
            DiabetesPedigreeFunction = gr.Slider(0.0, 2.5, step=0.01, label="Diabetes Pedigree Function")
            Age = gr.Slider(18, 100, step=1, label="Age")
            submit_btn = gr.Button("🔍 Predict", variant="primary")
        with gr.Column():
            result = gr.Textbox(label="Prediction Result", interactive=False)

    submit_btn.click(fn=predict_diabetes,
                     inputs=[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age],
                     outputs=result)

app.launch()
