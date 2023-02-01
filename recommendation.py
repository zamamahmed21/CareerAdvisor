import sqlite3


class Career_Recommendation():
    '''Recommend Careers w.r.t personality type & temperament type'''

    def __init__(self, db_name='CareerAdDB.db'):

        self.db_name = db_name
        self.mbti_careers = []
        self.temperament_careers = []
        self.career_recommendations = []


    def careers_for_mbti(self, mbti_type) -> list:
        '''get careers for mbti personality type from database'''
        
        # connection object
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        
        cursor.execute(f"SELECT career_name \
        FROM ((mbti_career\
        INNER JOIN mbti_type ON mbti_career.mbti_id_fk = mbti_type.mbti_id)\
        INNER JOIN career ON mbti_career.career_id_fk = career.career_id)\
        WHERE personality_type like '%{mbti_type}%'")

        mbti_careers = cursor.fetchall()
        # convert tuples in the output to strings
        mbti_careers = [career[0] for career in mbti_careers]

        self.mbti_careers = mbti_careers

        # Close the connection
        self.conn.close()

        return self.mbti_careers        


    def careers_for_temperament(self, temperament_type):
        '''get careers for temperament type from database'''

        # connection object
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        
        cursor.execute(f"SELECT career_name\
        FROM ((temperament_career\
        INNER JOIN temperament_type ON temperament_career.temperament_id_fk = temperament_type.temperament_id)\
        INNER JOIN career ON temperament_career.career_id_fk = career.career_id)\
        WHERE t_type like '%{temperament_type}%';")

        temperament_careers = cursor.fetchall()
        # convert tuples in the output to strings
        temperament_careers = [career[0] for career in temperament_careers]

        self.temperament_careers = temperament_careers

        # Close the connection
        self.conn.close()

        return self.temperament_careers


    def recommend_careers_for_mbti_and_temperament(self):
        '''recommend careers found similar in careers for mbti & temperament'''

        career_recommendations = []

        for temperament_career in self.temperament_careers:
            for mbti_career in self.mbti_careers:
                if mbti_career == temperament_career:
                    career_recommendations.append(mbti_career)
        
        self.career_recommendations = career_recommendations

        return self.career_recommendations


if __name__ == '__main__':

    career_rec = Career_Recommendation()
    print(career_rec.careers_for_mbti('ESTJ'))
    print(career_rec.careers_for_temperament('Phlegmatic'))
    print(career_rec.recommend_careers_for_mbti_and_temperament())


