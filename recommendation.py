import sqlite3
from time import sleep
from flask import Flask, session
import os
import PyPDF2
import datetime
import bcrypt


app = Flask(__name__)
app.secret_key = 'AC'


class Career_Recommendation():
    '''Recommend Careers w.r.t personality type & temperament type'''

    def __init__(self, db_name='CareerAdDB.db'):

        self.db_name = db_name
        self.goal_careers = []
        self.mbti_careers = []
        self.temperament_careers = []
        self.career_recommendations = []


    def careers_for_mbti(self, mbti_type):
        '''Get careers for mbti personality type from database'''
        
        # connection object
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        
        cursor.execute(f"SELECT career_name \
        FROM ((mbti_career\
        INNER JOIN mbti_type ON mbti_career.mbti_id_fk = mbti_type.mbti_id)\
        INNER JOIN career ON mbti_career.career_id_fk = career.career_id)\
        WHERE personality_type like '%{mbti_type}%'")

        mbti_careers = cursor.fetchall()
        # convert tuples in the output to list
        self.mbti_careers = [career[0] for career in mbti_careers]

        # Close the connection
        self.conn.close()

        return self.mbti_careers        


    def careers_for_temperament(self, temperament_type):
        '''Get careers for temperament type from database'''

        # connection object
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        
        cursor.execute(f"SELECT career_name\
        FROM ((temperament_career\
        INNER JOIN temperament_type ON temperament_career.temperament_id_fk = temperament_type.temperament_id)\
        INNER JOIN career ON temperament_career.career_id_fk = career.career_id)\
        WHERE t_type like '%{temperament_type}%';")

        temperament_careers = cursor.fetchall()
        # convert tuples in the output to list
        self.temperament_careers = [career[0] for career in temperament_careers]

        # Close the connection
        self.conn.close()

        return self.temperament_careers


    def recommend_careers_for_mbti_and_temperament(self):
        '''Recommend careers found similar in careers for mbti & temperament'''

        for temperament_career in self.temperament_careers:
            for mbti_career in self.mbti_careers:
                if mbti_career == temperament_career:
                    self.career_recommendations.append(mbti_career)

        return self.career_recommendations
    

    def get_goals(self):
        '''Get dictionary of 'goal: description' from database'''
        
        # connection object
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT title, description FROM goal;")
        goals = cursor.fetchall()
        # convert tuples in the output to dictionaries
        goals = dict((goal,description) for goal, description in goals)

        # Close the connection
        self.conn.close()

        return goals


    def careers_for_goals(self, goal:str) -> dict[list]:
        '''Get careers for goal'''

        # connection object
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        
        cursor.execute(f"""
        SELECT career.career_name, career.low_avg_income, career.avg_income, career.max_avg_income, career.general_description
        FROM goal_career
        INNER JOIN career ON goal_career.career_career_id = career.career_id
        INNER JOIN goal ON goal_career.goal_goal_id = goal.goal_id
        WHERE lower(goal.title) = '{goal.lower()}'""")
        careers = cursor.fetchall()
        # convert tuples in the output to dictionaries
        self.career_recommendations_for_goals = dict((career, [low_avg_income, avg_income, max_avg_income, description]) 
                     for career, low_avg_income, avg_income, max_avg_income, description in careers)
        
        # Close the connection
        self.conn.close()
                
        # only keep the careers that are present in career recommendations from mbti & temperament
        careers = dict()
        for career_recommendation in self.career_recommendations:
            try:
                careers.update({career_recommendation:self.career_recommendations_for_goals[career_recommendation]})
            except:
                pass
        self.career_recommendations_for_goals = careers
        
        return self.career_recommendations_for_goals

    def register(self,full_name,email,password,dob,user_type):
    
        # self.conn = sqlite3.connect(self.db_name)
        # cursor = self.conn.cursor()
        # cursor.execute("INSERT INTO users (full_name, email, password, dob, user_type) VALUES (?, ?, ?, ?, ?)",
        #             (full_name, email, password, dob, user_type))
        # self.conn.commit()
        # self.conn.close()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (full_name, email, password, dob, user_type) VALUES (?, ?, ?, ?, ?)",
                    (full_name, email, hashed_password.decode('utf-8'), dob, user_type))
        self.conn.commit()
        self.conn.close()
        
    def verify_login(self, email, password):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        self.conn.close()

        if user:
            stored_password = user[3]  # Fetch the stored password from the database
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                session['email'] = email
                user_dict = {
                    'id': user[0],
                    'full_name': user[1].capitalize(),
                    'email': user[2],
                    'password': user[3],
                    'dob': user[4],
                    'user_type': user[5]
                }
                return user_dict
        return None
        
   
    def save_resume(self, resume_file):
        if resume_file.filename == '':
            return "No selected resume file"
        
        if not os.path.exists('resume'):
            os.makedirs('resume')
        
        filename = resume_file.filename
        file_ext = os.path.splitext(filename)[1]
        
        user_email = session.get('email')  

        if user_email:
            save_filename = user_email + file_ext
        else:
            save_filename = "unknown_user" + file_ext
            
        save_path = os.path.join('resume', save_filename)
        
        resume_file.save(save_path)
        # resume_data = career_rec.get_resume_pdf(save_path)

        print(save_path)
        return save_path
        
    
    def insert_resume_path(self,resume_path):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        email = session.get('email')
        
        if email:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("UPDATE users SET resume_data = ?, timestamp = ? WHERE email = ?", (resume_path, current_time, email,))
            self.conn.commit()
            self.conn.close()
            
   
        
    def fetch_user_resume_data(self,email):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute("SELECT resume_data FROM users WHERE email=?", (email,))
        row = cursor.fetchone()
        self.conn.close()
        return row[0]
    
    def update_user_resume_data(self,skills,email):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET skills = ? WHERE email = ?;", (', '.join(skills), email))
        self.conn.commit()
        self.conn.close()
        
    def update_user_job_data(self,job_description_skills,email):
        self.conn = sqlite3.connect(self.db_name)
        print(job_description_skills)  
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET job_description_skills = ? WHERE email = ?;", (', '.join(job_description_skills), email))
        self.conn.commit()
        self.conn.close()    
        # print(f'UPDATE users SET job_description_skills = {job_description_skills} WHERE email={email};')
        
             
    def get_all_job_description_skills(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = lambda cursor, row: list(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT job_description_skills FROM users WHERE user_type='recruiter'and job_description_skills is Not NUll")
        job_description_skills=cursor.fetchall()
        self.conn.close()
        return job_description_skills
    
    
    def get_all_candidate_skills(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = lambda cursor, row: list(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT skills FROM users WHERE user_type='candidate' and skills is Not Null")
        candidate_skills = cursor.fetchall()
        self.conn.close()
        return candidate_skills

    
    def fetch_user_job_data(self,email):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute("SELECT job_description FROM users WHERE email=?", (email,))
        row = cursor.fetchone()
        self.conn.close()
        return row[0]
       
    
    def save_job_description(self,job_description,email):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET job_description = ? WHERE email=?;", (job_description,email))
        self.conn.commit()
        self.conn.close()
    
        # print(f'UPDATE users SET job_description = {job_description} WHERE email={email};')
    
    
    
          
                
if __name__ == '__main__':

    career_rec = Career_Recommendation()
    # career_rec.update_user_job_data('job_description_skills','esaanjum@gmail.com')
    print(career_rec.get_all_job_description_skills())
    print(career_rec.get_all_candidate_skills())
    # print(career_rec.careers_for_mbti('ESFP'))
    # print(career_rec.careers_for_temperament('Sanguine'))
    # print(career_rec.recommend_careers_for_mbti_and_temperament())
    # # print(career_rec.get_goals())
    # print(career_rec.careers_for_goals('Accumulate wealth.'))
    
