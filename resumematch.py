import io
from pyresparser import ResumeParser
import nltk
import io
import spacy
from spacy.matcher import PhraseMatcher
from recommendation import Career_Recommendation
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor


def extract_skills(resume_text):
    
    nlp = spacy.load("en_core_web_lg")
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    annotations = skill_extractor.annotate((resume_text))
    
    doc_node_values = []
    for match in annotations['results']['full_matches']:
        doc_node_values.append(match['doc_node_value'])

    for ngram in annotations['results']['ngram_scored']:
        doc_node_values.append(ngram['doc_node_value'])
        

        return doc_node_values



if __name__=='__main__':
    
    career_rec = Career_Recommendation()
    resume_text = career_rec.read_resume_text("resume\zamamahmed21@gmail.com.pdf")
    print(extract_skills(resume_text))
    # career_rec = Career_Recommendation()
    # resume_data = career_rec.fetch_user_resume_data('roshaan@gmail.com')
    # skills = extract_skills(resume_data)
    
    # print(skills)
    # job_description= career_rec.fetch_user_job_data('esaanjum@gmail.com')
    # job_description_skills=extract_job_skills(job_description)
    # print(job_description_skills)