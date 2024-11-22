from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

def classify_prompt():

    return
def inference_engine(prompt):

    """i will first classify the prompt based on what it is and then make it respond
    it maybe be info based, medical, symptoms, or general chat, query etc."""



    return
# Load the model and vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
with open('vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

def assess_symptoms(symptoms):
    X = vectorizer.transform([symptoms])
    prediction = model.predict(X)[0]
    return f"You may have {prediction}. Please consult a healthcare provider for a thorough diagnosis."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    symptoms = request.form['symptoms']
    assessment = assess_symptoms(symptoms)
    return f"<div class='bubble response'>{assessment}</div>"

if __name__ == '__main__':
    app.run(debug=True)
