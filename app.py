# app.py
import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB Configuration
client = MongoClient('mongodb+srv://geethanjali:geethu2304@cluster0.gm8m1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['exam_portal']
questions_collection = db['questions']

# Function to extract questions from Excel
def import_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    questions = []
    for index, row in df.iterrows():
        question = {
            'question_number': row['question_number'],
            'question': row['question'],
            'options': [row['option1'], row['option2'], row['option3'], row['option4']],
            'correct_option': row['correct_option']
        }
        questions.append(question)
    return questions

# Load questions into MongoDB
def load_questions_into_db(file_path):
    questions = import_questions_from_excel(file_path)
    questions_collection.insert_many(questions)

# For testing purposes, load questions on startup
if not questions_collection.find_one():
    load_questions_into_db('questions.xlsx')

# Routes
@app.route('/')
def home():
    return render_template('student_login.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher_login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/exam')
def exam():
    questions = list(questions_collection.find())
    return render_template('exam.html', questions=questions)

# Add your login logic and other routes here

if __name__ == '__main__':
    app.run(debug=True)

