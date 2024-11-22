from flask import Flask, render_template, request

app = Flask(__name__)

def assess_symptoms(symptoms):
    if "fever" in symptoms.lower():
        return "You may have a fever. Please rest and stay hydrated."
    elif "cough" in symptoms.lower():
        return "You may have a cough. Drink warm fluids and consider seeing a doctor if it persists."
    else:
        return "It's hard to diagnose based on these symptoms. Please see a healthcare provider."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    symptoms = request.form['symptoms']
    assessment = assess_symptoms(symptoms)
    return f"<h1>{assessment}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
