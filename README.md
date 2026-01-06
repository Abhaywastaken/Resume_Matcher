# Resume_Matcher
This small project matches a job description against a folder of resumes and produces similarity scores.
Resume / CV Matcher (TF-IDF + Cosine Similarity)

  Structure
  - 'matcher.py' - core matching utilities (uses scikit-learn if available, otherwise uses a fallback).
  - 'run_demo.py' - demo script: compares 'data/job_description.txt' with all '.txt' files in 'data/resumes/'.
  - 'data/' - contains sample job description and resumes, plus 'results.csv'.
  - 'requirements.txt' - suggested packages.
    
 ## How to run
  1.  Create a virtual environment and install requirements:
   pip install -r requirements.txt
  2. Run the demo:
   python run_demo.py
  3. Check 'data/results.csv' for ranked matches.

  ## Notes
  - The project uses 'scikit-learn's 'TfidfVectorizer' when available for best performance.
  - The fallback implementation is intentionally simple for production use, install scikit-learn.
