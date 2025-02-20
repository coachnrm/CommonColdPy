from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__, template_folder='web')

# Home route - renders index.html
@app.route('/')
def home():
    return render_template('index.html', result='')

# Form submission and result prediction
@app.route('/', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            head = int(request.form['head'])
            nose = int(request.form['nose'])
            neck = int(request.form['neck'])
            fever = int(request.form['fever'])

            # Load the trained model
            # loaded_model = joblib.load('common-cold.sav')
            loaded_model = pickle.load(open('common-cold.sav', 'rb'))

            # Make prediction
            result = loaded_model.predict([[head, nose, neck, fever]])[0]
        except Exception as e:
            result = f"Error: {str(e)}"

        return render_template("index.html", result=result)

# Run Flask application
if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for better error messages
