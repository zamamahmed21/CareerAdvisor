import sqlite3
from time import sleep


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



if __name__ == '__main__':

    career_rec = Career_Recommendation()

    print(career_rec.careers_for_mbti('ESFP'))
    print(career_rec.careers_for_temperament('Sanguine'))
    print(career_rec.recommend_careers_for_mbti_and_temperament())
    # print(career_rec.get_goals())
    print(career_rec.careers_for_goals('Accumulate wealth.'))
