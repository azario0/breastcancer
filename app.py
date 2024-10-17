import customtkinter as ctk
import joblib
import pandas as pd
import json

class BreastCancerDetectionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Breast Cancer Detection")
        self.geometry("800x600")

        self.model = joblib.load('breast_cancer_model.joblib')
        with open('unique_values.json', 'r') as f:
            self.unique_values = json.load(f)

        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame = ctk.CTkScrollableFrame(self)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Create input fields
        self.inputs = {}
        features = ['Age', 'Race', 'Marital Status', 'T Stage ', 'N Stage', '6th Stage',
                    'differentiate', 'Grade', 'A Stage', 'Tumor Size', 'Estrogen Status',
                    'Progesterone Status', 'Regional Node Examined', 'Reginol Node Positive',
                    'Survival Months']

        for i, feature in enumerate(features):
            label = ctk.CTkLabel(frame, text=feature)
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

            if feature in ['Age', 'Tumor Size', 'Regional Node Examined', 'Reginol Node Positive', 'Survival Months']:
                entry = ctk.CTkEntry(frame)
            else:
                entry = ctk.CTkComboBox(frame, values=self.unique_values[feature])

            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.inputs[feature] = entry

        # Create predict button
        predict_button = ctk.CTkButton(frame, text="Predict", command=self.predict)
        predict_button.grid(row=len(features), column=0, columnspan=2, pady=20)

        # Create result label
        self.result_label = ctk.CTkLabel(frame, text="")
        self.result_label.grid(row=len(features)+1, column=0, columnspan=2)

    def predict(self):
        # Get input values
        input_data = {}
        for feature, entry in self.inputs.items():
            if isinstance(entry, ctk.CTkEntry):
                input_data[feature] = float(entry.get())
            else:
                input_data[feature] = entry.get()

        # Create a DataFrame from input data
        input_df = pd.DataFrame([input_data])

        # Make prediction
        prediction = self.model.predict(input_df)
        print(prediction)

        # Update result label
        result = "Alive" if prediction[0] == 'Alive' else "Dead"
        self.result_label.configure(text=f"Prediction: {result}")

if __name__ == "__main__":
    app = BreastCancerDetectionApp()
    app.mainloop()