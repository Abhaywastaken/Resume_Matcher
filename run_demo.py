# FILE: run_demo.py

import os
import csv
import matcher

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
JOB_FILE = os.path.join(DATA_DIR, "job_description.txt")
RESUME_DIR = os.path.join(DATA_DIR, "resumes")


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    job = read_file(JOB_FILE)
    resumes = []
    names = []

    for file in sorted(os.listdir(RESUME_DIR)):
        if file.endswith(".txt"):
            names.append(file)
            resumes.append(read_file(os.path.join(RESUME_DIR, file)))

    matcher = matcher()
    vectors = matcher.fit_transform([job] + resumes)

    scores = matcher.similarity(vectors[0:1], vectors[1:])[0]

    results = sorted(zip(names, scores), key=lambda x: x[1], reverse=True)

    with open(os.path.join(DATA_DIR, "results.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["resume_file", "score"])
        for name, score in results:
            writer.writerow([name, round(float(score), 4)])

    for name, score in results:
        print(f"{name}: {score:.4f}")


if __name__ == "__main__":
    main()
