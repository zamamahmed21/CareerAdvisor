import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from email.mime.base import MIMEBase


# Database connection
conn = sqlite3.connect('CareerAdDB.db')
cursor = conn.cursor()

# Retrieve candidates from the database
cursor.execute("SELECT * FROM users")
candidates = cursor.fetchall()

# Job description skills
cursor.execute("SELECT job_description_skills FROM users")
job_description_skills = cursor.fetchone()[0].split(",")  # Assuming skills are comma-separated

# Matching threshold
matching_threshold = 0.7

# Email configuration
sender_email = "zamamahmed21@.com"
sender_password = "sqsonomzithhbqlr"
smtp_server = "smtp.example.com"
smtp_port = 587

# Sent resumes file
sent_resumes_file = "sent_resume.txt"

# Iterate over candidates
for candidate in candidates:
    candidate_email = candidate[1]
    candidate_skills = candidate[5].split(",")  # Assuming skills are comma-separated and stored in the 5th column
    match_count = 0

    # Compare candidate skills with job description skills
    for skill in candidate_skills:
        if skill.strip().lower() in job_description_skills:
            match_count += 1

    # Calculate matching score
    matching_score = match_count / len(job_description_skills)

    # Check if matching score meets the threshold
    if matching_score >= matching_threshold:
        # Prepare email content
        subject = "Matching Resume for Job Opportunity"
        message = f"Dear Recruiter,\n\nI am pleased to share my resume for the job opportunity. My skills align with the required qualifications, and I believe I can contribute effectively to the role.\n\nPlease find my attached resume.\n\nThank you for your consideration.\n\nBest regards,\n{candidate[0]}"

        # Create a multipart message and set email details
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = candidate_email
        msg['Subject'] = subject

        # Attach the message to the multipart message
        msg.attach(MIMEText(message, 'plain'))

        # Attach the resume file
        resume_file_path = candidate[8]  # Assuming resume file path is stored in the 8th column
        with open(resume_file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            attachment.close()
        part.add_header('Content-Disposition', f"attachment; filename=resume.pdf")
        msg.attach(part)

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        # Remove candidate from the sent_resumes_file if the timestamp in the database is updated
        timestamp = candidate[9]  # Assuming timestamp is stored in the 9th column
        with open(sent_resumes_file, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if not line.startswith(candidate_email) or timestamp not in line:
                    file.write(line)
            file.truncate()

# Close the database connection
conn.close()
