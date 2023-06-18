import io
from pyresparser import ResumeParser
import nltk

# nltk.download('stopwords')


# Function to extract skills
def extract_skills(resume_data):
    resume_text = ResumeParser(io.BytesIO(resume_data), ext='pdf').get_extracted_data()
    skills = resume_text.get('skills', [])
    return skills


if __name__=='__main__':
    from recommendation import Career_Recommendation
    career_rec = Career_Recommendation()
    resume_data = career_rec.fetch_user_resume_data('roshaan@gmail.com')
    skills = extract_skills(resume_data)
    print(skills)