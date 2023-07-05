import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def calculate_similarity(candidate_skills, recruiter_skills):
    candidate_skills_set = set(candidate_skills)
    # print(f"candidate_skills_set: {candidate_skills_set}")
    recruiter_skills_set = set(recruiter_skills)
    # print(f"recruiter_skills_set:{recruiter_skills_set}")
    common_skills = candidate_skills_set.intersection(recruiter_skills_set)
    # print(f"common_skills: {common_skills}")
    similarity = len(common_skills) / len(recruiter_skills_set)
    # print(f"len(common_skills): {len(common_skills)} \n len(candidate_skills_set): {len(recruiter_skills_set)}")
    return similarity

conn = sqlite3.connect('CareerAdDB.db')
cursor = conn.cursor()

sent_resumes = {}

with open('sent_resumes.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        email, timestamp = line.split(':', 1)
        sent_resumes[email] = timestamp


cursor.execute("SELECT email, skills, resume_data, timestamp FROM users WHERE skills IS NOT NULL")
candidates = cursor.fetchall()

cursor.execute("SELECT email, job_description_skills FROM users WHERE job_description_skills IS NOT NULL")
recruiters = cursor.fetchall()


for candidate in candidates:
    candidate_email = candidate[0]
    candidate_skills = candidate[1].split(", ")
    resume_path = candidate[2]
    timestamp = candidate[3]

    if candidate_email in sent_resumes:
        stored_timestamp = sent_resumes[candidate_email]
        if stored_timestamp == timestamp or stored_timestamp is None:
            print("This candidate's resume has already been sent:", candidate_email)
            continue

    for recruiter in recruiters:
        recruiter_email = recruiter[0]
        recruiter_skills = recruiter[1].split(", ")

        similarity = calculate_similarity(candidate_skills, recruiter_skills)
        if similarity >= 0.7:
            print("Match Found!")
            print("Candidate Email:", candidate_email)
            print("Recruiter Email:", recruiter_email)
            print("Similarity:", similarity)

            msg = MIMEMultipart()
            msg['From'] = 'zamamahmed21@gmail.com'  
            msg['To'] = recruiter_email
            msg['Subject'] = 'Matching Candidate Resume'

            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(open(resume_path, 'rb').read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename='resume.pdf')
            msg.attach(attachment)

            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  
            smtp_server.starttls()
            smtp_server.login('zamamahmed21@gmail.com', 'sqsonomzithhbqlr')  
            smtp_server.send_message(msg)
            smtp_server.quit()

            print("Resume sent to recruiter:", recruiter_email)
            

    sent_resumes[candidate_email] = timestamp

with open('sent_resumes.txt', 'w') as file:
    for email, timestamp in sent_resumes.items():
        file.write(f"{email}:{timestamp}\n")

cursor.close()
conn.close()
