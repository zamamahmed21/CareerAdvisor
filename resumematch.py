import spacy
from spacy.matcher import Matcher
from PyPDF2 import PdfReader
import json
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define the skill patterns
with open("skill.json") as file:
    data = json.load(file)
    skill_patterns = data["skill_patterns"]

# Create the skill matcher
skill_matcher = Matcher(nlp.vocab)
for pattern in skill_patterns:
    skill_matcher.add("Skill", [pattern])

def extract_skills(text):
    doc = nlp(text)
    skill_matches = skill_matcher(doc)
    skills = set()
    for match_id, start, end in skill_matches:
        matched_tokens = doc[start:end]
        skills.add(matched_tokens.text.lower())
    return skills

def extract_resume_skills(resume_data):
    with open(resume_data, "rb") as file:
        pdf = PdfReader(file)
        resume_text = ""
        for page in pdf.pages:
            resume_text += page.extract_text()
    skills = extract_skills(resume_text)
    return skills


def extract_job_description_skills(job_description):
    skills = extract_skills(job_description)
    return skills


