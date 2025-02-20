from flask import Flask, render_template, request
import mysql.connector
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__, template_folder='web')


# Function to fetch data from MySQL and train model
def fetch_and_train_model():
    try:
        # # Connect to the MySQL database
        conn = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='root',
            password='123456',
            database='test2',
        )



        # Write the SQL query
        query = "SELECT * FROM ColdSyndromeInsert"

        # Use pandas to execute the query and fetch the data into a DataFrame
        df = pd.read_sql(query, conn)

        # Close the connection
        conn.close()

        # Prepare features and target variable
        X = df[['Head', 'Nose', 'Neck', 'Fever']]
        y = df['CommonCold']

        # Train a new RandomForest model
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
        model.fit(X, y)

        return model

    except Exception as e:
        print(f"Error fetching and training model: {e}")
        return None

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

            # Make prediction
            # result = loaded_model.predict([[head, nose, neck, fever]])[0]

            # Fetch data from database and train the model
            model = fetch_and_train_model()
            if model is None:
                return render_template("index.html", result="Error training the model.")

            # Prepare input for prediction
            input_data = pd.DataFrame([[head, nose, neck, fever]], columns=['Head', 'Nose', 'Neck', 'Fever'])

            # Make prediction
            result = model.predict(input_data)[0]
        
        except Exception as e:
            result = f"Error: {str(e)}"

        return render_template("index.html", result=result)

# Run Flask application
if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for better error messages

