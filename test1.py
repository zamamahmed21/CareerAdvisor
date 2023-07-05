import spacy
from spacy.matcher import Matcher
from PyPDF2 import PdfReader

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define the skill patterns
skill_patterns = [
    [{"LOWER": "Email Marketing"}],
    [{"LOWER": "python"}],
    [{"LOWER": "java"}],
    [{"LOWER": "sql"}],
    [{"LOWER": "machine"}, {"LOWER": "learning"}],
    [{"LOWER": "data"}, {"LOWER": "analysis"}],
    [{"LOWER": "project"}, {"LOWER": "management"}]
]

# Create the matcher
matcher = Matcher(nlp.vocab)
for pattern in skill_patterns:
    matcher.add("Skill", [pattern])

# Function to extract skills from text
def extract_skills(text):
    doc = nlp(text)
    matches = matcher(doc)
    skills = set()
    for match_id, start, end in matches:
        skills.add(doc[start:end].text)
    return skills

# Function to extract skills from a PDF resume
def extract_resume_skills(file_path):
    with open(file_path, "rb") as file:
        pdf = PdfReader(file)
        resume_text = ""
        for page in pdf.pages:
            resume_text += page.extract_text()
    skills = extract_skills(resume_text)
    return skills

# Function to extract skills from a job description
def extract_job_description_skills(job_description):
    skills = extract_skills(job_description)
    return skills

# Example usage
resume_file = "D:/Zamam/FYP_Project/CareerAdvisor/resume/roshaan@gmail.com.pdf"
job_description = '''I am passionate about using technology to drive innovation and
solve complex problems. I have interest in software development
and data analysis to make informed decisions. I am eager to learn 
and take on new challenges to further develop my skills. If you 
are looking for a dedicated and results-driven team member for 
your technology-focused organization, let's connect and work 
together towards success'''

resume_skills = extract_resume_skills(resume_file)
job_description_skills = extract_job_description_skills(job_description)

print("Resume Skills:")
print(resume_skills)
print()
print("Job Description Skills:")
print(job_description_skills)
