'AI Resume and Job Description Matcher'

This project is an AI-powered system that compares a job description with multiple resumes and calculates how well each resume matches the role. It uses sentence transformer embeddings for semantic similarity and an AI skill extractor to identify which required skills are missing from each candidate's resume. The goal of this project is to demonstrate practical use of NLP, embeddings, and machine learning to automate resume screening and provide insights into candidate fit.

'Features'

Semantic matching using sentence transformer embeddings

AI-based skill extraction using an LLM

Detection of missing skills for each resume

CSV output with match scores and skill comparison

Simple and clean project structure for learning and portfolio use

'How it works'

The program reads a job description from the data folder.

It loads all resumes stored in the resumes folder.

It generates embeddings using a transformer model for semantic comparison.

It extracts skills from both job description and resumes using an LLM or fallback method.

It identifies missing skills for each resume.

It outputs a CSV file listing match score, matched skills, and missing skills.

'Dependencies'

Install required packages using:

pip install -r requirements.txt

Set your API key if using the skill extraction feature:

Set environment variable OPENAI_API_KEY to your OpenAI key.

'Project Structure'

matcher.py - Handles semantic similarity using sentence transformer or fallback
skills.py - Extracts skills using LLM or fallback extractor
run_demo.py - Main script that compares resumes and outputs results
data/ - Contains job description, resumes, and generated results
requirements.txt - Python dependencies

'How to run'

Run the match and skill comparison:

python run_demo.py

Results will be created inside data/results_with_skills.csv.
