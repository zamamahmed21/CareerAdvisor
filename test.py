# imports
import io
import spacy
from spacy.matcher import PhraseMatcher
from recommendation import Career_Recommendation
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor

# init params of skill extractor
nlp = spacy.load("en_core_web_lg")
# init skill extractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)


# extract skills from job_description
job_description = """
Develop, test, and deploy software applications using programming languages such as Python, Java, or C++
Collaborate with product managers and stakeholders to gather and analyze requirements
Design and implement software solutions that meet business needs and adhere to best practices
Write clean, efficient, and maintainable code
Perform code reviews and provide constructive feedback to ensure code quality
Debug and resolve software defects and issues
Collaborate with cross-functional teams, including UX/UI designers and QA engineers, to deliver high-quality software
Stay updated with the latest trends and technologies in software development and implement them when applicable

"""
from recommendation import Career_Recommendation
career_rec = Career_Recommendation()
resume_text = career_rec.read_resume_text("resume\zamamahmed21@gmail.com.pdf")

annotations = skill_extractor.annotate((resume_text))
print(annotations)