# pylint: disable=unspecified-encoding

# pylint: disable=E0401,C0116,C0303,C0114,C0304
import json
from flask import Flask , render_template, redirect, url_for, session
from flask import request, send_from_directory

app = Flask (__name__,template_folder='template',static_folder='static')


@app.route('/')
def hello_world():
    return render_template('index.html')
    

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
        results = {'S':0,'M':0,'C':2,'P':0}
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






@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')    

@app.route('/goal')
def goal():
    return render_template('goal.html')  

@app.route('/about')
def about():
    return render_template('about.html')  
     
@app.route('/json/<path>')
def send_report(path):
    return send_from_directory('static', path)

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True) 