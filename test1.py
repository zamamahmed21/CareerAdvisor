# # imports
# import io
# import spacy
# from spacy.matcher import PhraseMatcher
# from recommendation import Career_Recommendation
# # load default skills data base
# from skillNer.general_params import SKILL_DB
# # import skill extractor
# from skillNer.skill_extractor_class import SkillExtractor

# # init params of skill extractor
# nlp = spacy.load("en_core_web_lg")
# # init skill extractor
# skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# a="zamam ahmed zamamahmed21@gmail com about \
# i am passionate about using technology to drive innovation and solve complex problems\
# i have interest in software development and data analysis to make in formed decisions i am eager to learn and take on\
# new challenges to further develop my skills if you are looking for a dedicated and results driven team member for your technology focused organization let s connect and work together towards success education matriculation muhammadi public school karachi | 2016 2017 comp uter intermediate aisha bawany gov college karachi | 2017 2019 pre engineering bachelor szabist karachi \
# | 2019 present computer science experience fresh projects employee management system szabist project 2021 basic java project to manage employee s details •\
# jdbc java database connectivity to connect to databases • oracle database • sql used to communicate with the database detect toxic content szabist project 2022 • deep learning project in python • regular expression and nltk libraries were used to data cleaning • glove i s used to to transform text features in to vector form skills programming c python sql marketing email marketing personal information father name anwar ahmed gender male nationality pakistani date of birth 21 oct 2000 language urdu english marital status un married cnic 42201 1792886 3 contact house no # 3 61 big plot shah faisal colony karachi pakistan +92 312 0257971 zamamahmed21@gmail com'"
# # extract skills from job_description

# from recommendation import Career_Recommendation
# career_rec = Career_Recommendation()
# resume_text = career_rec.read_resume_text("resume\zamamahmed21@gmail.com.pdf")

# annotations = skill_extractor.annotate((resume_text))
# doc_node_values = []
# for match in annotations['results']['full_matches']:
#     doc_node_values.append(match['doc_node_value'])

# for ngram in annotations['results']['ngram_scored']:
#     doc_node_values.append(ngram['doc_node_value'])

# print(doc_node_values)
import json
with open("output.json", "r") as file:
    data = json.load(file)
for i in range (0,len(data["results"]["full_matches"])):
    print(data["results"]["full_matches"][i]["doc_node_value"])
    

