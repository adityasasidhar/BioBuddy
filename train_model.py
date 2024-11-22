import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

# Load the dataset
data = pd.read_csv('DiseaseAndSymptoms.csv')

# Combine symptom columns into a single string for each row
data['combined_symptoms'] = data.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

# Feature extraction using TfidfVectorizer (NLP)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['combined_symptoms'])

# Labels
y = data['Disease']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model (machine learning)
model = LogisticRegression()
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print(score)
# Save the model and vectorizer
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
with open('vectorizer.pkl', 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)

print("Model and vectorizer saved successfully.")
