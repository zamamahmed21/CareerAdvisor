
career= {'data':{
    'Physician Assistant':['68000','131000', '201000', 'PAs, or physician assistants, work collaboratively with physicians, surgeons, and other healthcare professionals in delivering medical care. Their responsibilities involve assessing patients, making diagnoses, and providing treatment.'],
    'Pediatrician': ['94000','197000', '310000', 'A pediatrician is a medical professional who has received specialized training in the prevention, diagnosis, and treatment of diseases and injuries in children. Additionally, pediatricians assist with the management of other issues that impact children, including developmental disorders as well as behavioral, emotional, and social problems.']
}}

for key,value in career['data'].items():
   
       print(key)
       print(value[0],value[1],value[2])
       print(value[3] )
   
