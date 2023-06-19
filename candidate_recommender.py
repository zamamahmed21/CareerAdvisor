
# def compare_resume_with_description(job_description_skills: list[list], candidate_skills: list[list]):
#     [['python', 'sql'],['.NET', ]]

from recommendation import Career_Recommendation
career_rec = Career_Recommendation()

job_description_skills = career_rec.get_all_job_description_skills()
print("Job Description Skills:")
for skills in job_description_skills:
    print(skills)
    
candidate_skills = career_rec.get_all_candidate_skills()
print("Candidate Skills:")
for skills in candidate_skills:
    print(skills)
