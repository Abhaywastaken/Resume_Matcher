# FILE: run_demo.py

import os
import csv
from matcher import ResumeMatcher
from skills import extract_skills, missing_skills

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
JOB_FILE = os.path.join(DATA_DIR, "job_description.txt")
RESUME_DIR = os.path.join(DATA_DIR, "resumes")
OUT_CSV = os.path.join(DATA_DIR, "results_with_skills.csv")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    job = read_file(JOB_FILE)
    resume_files = []
    resumes = []
    for file in sorted(os.listdir(RESUME_DIR)):
        if file.endswith(".txt"):
            resume_files.append(file)
            resumes.append(read_file(os.path.join(RESUME_DIR, file)))

    matcher = ResumeMatcher()
    scores = matcher.score_job_vs_resumes(job, resumes)

    job_skills = extract_skills(job)

    rows = []
    for fname, resume_text, score in zip(resume_files, resumes, scores):
        candidate_skills = extract_skills(resume_text)
        missing = missing_skills(job_skills, candidate_skills)
        rows.append({
            "resume_file": fname,
            "score": round(float(score), 4),
            "matched_skills_count": len(job_skills) - len(missing),
            "required_skills_count": len(job_skills),
            "missing_skills": "; ".join(sorted(missing))
        })

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["resume_file","score","matched_skills_count","required_skills_count","missing_skills"])
        writer.writeheader()
        for r in sorted(rows, key=lambda x: x["score"], reverse=True):
            writer.writerow(r)

    for r in sorted(rows, key=lambda x: x["score"], reverse=True):
        print(f"{r['resume_file']}: score={r['score']:.4f} matched={r['matched_skills_count']}/{r['required_skills_count']} missing=[{r['missing_skills']}]")
    print()
    print("Results saved to", OUT_CSV)

if __name__ == "__main__":
    main()

