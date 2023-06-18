import json
from flask import Flask , render_template, redirect, url_for, session
from flask import request, send_from_directory
import sqlite3
import subprocess

from resumematch import extract_skills
from recommendation import Career_Recommendation

app = Flask (__name__,template_folder='template',static_folder='static')

app.secret_key = 'CA'
career_rec = Career_Recommendation()

# resume_matcher=ResumeMatcher()


@app.route('/')
def hello_world():
    
    return render_template('new_index.html')
    

@app.route('/PersonalityTest')
def personality_test():
     '''take personality test'''
        
     return render_template('personalitytest.html') 


@app.route('/PersonalityTypeResult',methods=["POST"])
def calc_personality_test_results():
    '''calculate personality test results & send them'''
    
    if request.method == 'POST':
        data = request.get_json()
        
        # assign scores to personality letters
        results = {'E':0,'I':0,'S':0,'N':0,'F':0,'T':0,'P':0,'J':0}
        for key,values in data.items():
            for letter in results:
                for value in values:
                    if letter==value:
                        results[letter]= results[letter] + 1
        print(results)
        
        
        # get personality type
        p_type = ''
        p_type = p_type + ('E' if results['E'] > results['I'] else 'I')
        p_type = p_type + ('S' if results['S'] > results['N'] else 'N')
        p_type = p_type + ('F' if results['F'] > results['T'] else 'T')
        p_type = p_type + ('P' if results['P'] > results['J'] else 'J')
        print(p_type)
     
    return p_type    


@app.route('/PersonalityType/Results')
def show_personality_test_results():
    '''show personality test results'''
    
    return render_template("personalitytestresults.html")




@app.route('/TemperamentTest')
def temperament_test():
    '''take temperament test'''

    return render_template("temperamenttest.html")

@app.route('/TemperamentTypeResult',methods=["POST"])
def calc_temperament_type_result():
    
    if request.method == 'POST':
        data = request.get_json()
        
        # assign scores to temperament letters
        results = {'S':0,'M':0,'C':0,'P':0}
        for key,values in data.items():
            for letter in results:
                for value in values:
                    if letter==value:
                        results[letter]= results[letter] + 2
                    if letter.lower()==value:
                        results[letter]=results[letter]+ 1
        print(results)
        
        # find dominant temperament type by finding the temperament with the highest score
        t_type=''
        greatest_no = 0
        for letter in results:
            if results[letter]>greatest_no:
                greatest_no=results[letter]
                t_type = letter
                print(t_type)
        
        if t_type=='C':
            t_type = 'Choleric'
        elif t_type=='P':
            t_type = 'Phlegmatic'
        elif t_type=='S':
            t_type = 'Sanguine'
        elif t_type=='M':
            t_type = 'Melancholic'

    return t_type
   


    

        

@app.route('/TemperamentType/Results')
def show_temperament_test_results():

    return render_template("temperamenttestresults.html")



@app.route('/CareerRecommendation')
def career_recommendation():    
    '''display career recommendation'''

    return render_template("careerrecommendation.html")


@app.route('/CareerRecommendationResult',methods=["POST"])
def calc_career_recommendation():    
    '''create & return career recommendations'''

    data = request.get_json()
    p_type = data['personality_type']
    t_type = data['temperament_type']
    goal = data['goal']

    print("Careers for Personality Type ",p_type)
    print(career_rec.careers_for_mbti(p_type))
    print("Careers for Temperament Type ",t_type)
    print(career_rec.careers_for_temperament(t_type))
    print(career_rec.recommend_careers_for_mbti_and_temperament())
    print(goal)
    print(career_rec.careers_for_goals(goal))
    

    # return json containing career recommendations
    return json.dumps({"data":json.dumps(career_rec.career_recommendations_for_goals)})


@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/register')
def register():
    
     return render_template('register.html')    



@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['fullName']
        email = request.form['email']
        password = request.form['password']
        dob = request.form['dob']
        user_type = request.form['userType']

        career_rec.register(full_name,email,password,dob,user_type)

        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def log():
    error_message = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = career_rec.verify_login(email, password)
        if user:
            session['user'] = user
            return redirect('/dashboard')
        else:
            error_message = 'Invalid email or password'

    return render_template('login.html', error=error_message)







@app.route('/goal',methods=['GET','POST'])
def goal():
    goals = career_rec.get_goals()
    
    return render_template('goal.html',goals=goals) 
 
@app.route('/goal_return',methods=['POST'])
def goal_return():
    goal = request.form['goal']
    
    return "" +goal


@app.route('/about')
def about():
    return render_template('about.html')  


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        user = session['user']
        full_name = user['full_name']
        if user['user_type']=='candidate':
            return render_template('job_dashboard.html', full_name=full_name)
        elif user['user_type']=='recruiter':
            return render_template('recruiter_dashboard.html',full_name=full_name)
    else:
        return redirect(url_for('log'))

    

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('log'))


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
  

    if 'resume' not in request.files:
        return "No resume file found"

    resume_file = request.files['resume']

    if resume_file.filename == '':
        return "No selected resume file"

    resume_data = resume_file.read()
    career_rec.insert_resume(resume_data)

    subprocess.run(['python', 'resume_match.py'])
    
    resume_data=career_rec.fetch_user_resume_data(session.get('email'))
    
    
    skills = extract_skills(resume_data)
    
    email = session.get('email') 
    print(email)
    print(skills)
    career_rec.update_user_resume_data(skills, email)
    
    
    return render_template('job_dashboard.html', resume_saved=True, full_name=session['user']['full_name'])

# @app.route('/upload_resume', methods=['POST'])
# def upload_resume():
#     if 'resume' not in request.files:
#         return "No resume file found"

#     resume_file = request.files['resume']

#     if resume_file.filename == '':
#         return "No selected resume file"

#     resume_data = resume_file.read()
#     career_rec.insert_resume(resume_data)

#     return render_template('job_dashboard.html', resume_saved=True, full_name=session['user']['full_name'])

 
 
 
 
 
 
 
@app.route('/json/<path>')
def send_report(path):
    return send_from_directory('static', path)

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True) 