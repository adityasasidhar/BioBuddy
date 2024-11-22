from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import sqlite3

app = Flask(__name__)

# Load the BioBERT model
model_name = "dmis-lab/biobert-base-cased-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect("health_advice.db")
    conn.row_factory = sqlite3.Row
    return conn

def fetch_general_advice():
    conn = get_db_connection()
    advice = conn.execute("SELECT advice FROM general_advice").fetchall()
    conn.close()
    return [row["advice"] for row in advice]

def fetch_disease_info(disease_name):
    conn = get_db_connection()
    info = conn.execute("SELECT details FROM diseases WHERE name LIKE ?", (f"%{disease_name}%",)).fetchone()
    conn.close()
    return info["details"] if info else "No information found for this disease."

def classify_prompt(prompt):
    """
    Classifies the prompt into categories: 'symptom', 'disease inquiry', 'general advice', or 'general query'.
    """
    if "symptom" in prompt.lower() or "feel" in prompt.lower():
        return "symptom"
    elif "disease" in prompt.lower() or "problem" in prompt.lower():
        return "disease inquiry"
    elif "advice" in prompt.lower():
        return "general advice"
    else:
        return "general query"

def inference_engine(prompt):
    """
    Uses BioBERT and database to provide a response based on the classification.
    """
    classification = classify_prompt(prompt)

    if classification == "symptom":
        return qa_pipeline({
            "question": prompt,
            "context": " ".join(fetch_general_advice())
        })["answer"]
    elif classification == "disease inquiry":
        return fetch_disease_info(prompt)
    elif classification == "general advice":
        return " ".join(fetch_general_advice())
    else:
        return "Could you provide more context or specify your query?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    prompt = request.form['prompt']
    response = inference_engine(prompt)
    return f"<div class='bubble response'>{response}</div>"

if __name__ == '__main__':
    app.run(debug=True)
