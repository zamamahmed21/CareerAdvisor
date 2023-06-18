
career= {'data':{
    'Physician Assistant':['68000','131000', '201000', 'PAs, or physician assistants, work collaboratively with physicians, surgeons, and other healthcare professionals in delivering medical care. Their responsibilities involve assessing patients, making diagnoses, and providing treatment.'],
    'Pediatrician': ['94000','197000', '310000', 'A pediatrician is a medical professional who has received specialized training in the prevention, diagnosis, and treatment of diseases and injuries in children. Additionally, pediatricians assist with the management of other issues that impact children, including developmental disorders as well as behavioral, emotional, and social problems.']
}}

for key,value in career['data'].items():
   
       print(key)
       print(value[0],value[1],value[2])
       print(value[3] )


import sqlite3
import os

conn = sqlite3.connect('CareerAdDB.db')
cursor = conn.cursor()

email = 'sameermoin@gmail.com'  

cursor.execute("SELECT resume_data FROM users WHERE email = ?;", (email,))
blob_data = cursor.fetchone()[0]

file_path = os.path.join('test_data', 'output.pdf')
with open(file_path, 'wb') as file:
    file.write(blob_data)

cursor.close()
conn.close()

print(f"PDF file saved to: {file_path}")





# import sqlite3
# import tempfile
# import os
# import pdfkit

# import pdfkit




# def check_resume_for_email(email):
#     db_name = 'CareerAdDB.db'  # 
#     save_location = 'test_data/'  
#     pdf_options = {
#         'page-size': 'Letter',
#         'margin-top': '0',
#         'margin-right': '0',
#         'margin-bottom': '0',
#         'margin-left': '0',
#     }

#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()

#     cursor.execute("SELECT resume_data FROM users WHERE email=?", (email,))
#     result = cursor.fetchone()

#     conn.close()

#     if result:
#         resume_data = result[0]
#         # Save the resume data to a temporary file
#         with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_file:
#             temp_file.write(resume_data)
#             temp_filename = temp_file.name

#         # Extract the filename from the temporary file path
#         resume_filename = os.path.basename(temp_filename)

#         # Create the save location directory if it doesn't exist
#         os.makedirs(save_location, exist_ok=True)

#         # Convert the HTML file to PDF
#         pdf_filename = os.path.splitext(resume_filename)[0] + '.pdf'
#         pdf_path = os.path.join(save_location, pdf_filename)
#         pdfkit.from_file(temp_filename, pdf_path, options=pdf_options)

#         # Remove the temporary HTML file
#         os.remove(temp_filename)

#         print(f"Resume found for email '{email}'. Saved as PDF: {pdf_path}")
#     else:
#         print(f"No resume found for email '{email}'")


# if __name__ == '__main__':
#     email = 'zamamahmed21@gmail.com'  # Specify the email to check the resume for
#     check_resume_for_email(email)

