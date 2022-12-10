from flask import Flask, request, render_template
import pickle
import sqlite3

# Create flask app
flask_app = Flask(__name__)

model = pickle.load(open('model.sav', 'rb'))

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    features= [str(x) for x in request.form.values()]
    print(features)
    prediction = model.predict([[features[2],features[3]]])
    print(prediction[0])
    
    # Storing in db
    conn = sqlite3.connect('customers.db')
    insert_sql = f'INSERT into customers (CustomerID, Age, Annual_Income, Spending_Score, Gender_Male, Category) VALUES ( {features[0]}, {features[1]}, {features[2]}, {features[3]}, {features[4]}, {prediction[0]} )'
    cursor = conn.cursor()
    cursor.execute(insert_sql)
    conn.commit()
    conn.close()
    return render_template("index.html", prediction_text = "This customer belongs to category: {}".format(prediction[0]))

if __name__ == "__main__":
    flask_app.run(debug=True)