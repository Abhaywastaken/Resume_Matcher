#FILE: build_project.py

import os
import sys
import zipfile
import textwrap
import pandas as pd

project_root = "Resume_Matcher_project"

job_txt = textwrap.dedent("""
Software Developer Intern – Turku AMK (MyE.Way Project)

We are seeking a motivated Software Developer Intern to join the MyE.Way team.
The intern will assist in implementing and maintaining CI/CD pipelines using GitLab CI,
automate testing and deployment processes, and contribute to development of the
MyE.Way electronic sports coaching support system. Familiarity with Python, web development,
and DevOps principles is a plus.
""")

resume1 = textwrap.dedent("""
Alice A.
Aspiring software developer with hands-on experience in Python and web development.
Worked on small projects involving automated testing, CI pipelines, and REST APIs.
Familiar with Git, Docker, and basic DevOps concepts.
""")

resume2 = textwrap.dedent("""
Bob B.
Data scientist background with experience in NLP and machine learning.
Skilled in Python, scikit-learn, pandas, and building models for text classification.
Interested in recommendation systems and data-driven products.
""")

resume3 = textwrap.dedent("""
Carlos C.
Student of sports science with interest in e-sports coaching.
Experience in project coordination and data collection. Limited programming experience,
but eager to learn software development and DevOps tools.
""")

os.makedirs(os.path.join(project_root, "data", "resumes"), exist_ok=True)

with open(os.path.join(project_root, "data", "job_description.txt"), "w", encoding="utf-8") as f:
    f.write(job_txt)

with open(os.path.join(project_root, "data", "resumes", "resume_alice.txt"), "w", encoding="utf-8") as f:
    f.write(resume1)

with open(os.path.join(project_root, "data", "resumes", "resume_bob.txt"), "w", encoding="utf-8") as f:
    f.write(resume2)

with open(os.path.join(project_root, "data", "resumes", "resume_carlos.txt"), "w", encoding="utf-8") as f:
    f.write(resume3)

cwd = os.getcwd()
os.chdir(project_root)
run_output = os.popen(f"{sys.executable} run_demo.py").read()
print(run_output)
os.chdir(cwd)

results_csv = os.path.join(project_root, "data", "results.csv")
df = pd.read_csv(results_csv)
print(df.to_string(index=False))

zip_path = "resume_matcher_project.zip"
if os.path.exists(zip_path):
    os.remove(zip_path)

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(project_root):
        for file in files:
            full = os.path.join(root, file)
            arcname = os.path.relpath(full, project_root)
            zf.write(full, arcname)

print(zip_path)
