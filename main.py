from flask import Flask, render_template, request, jsonify, redirect, Response
import pandas as pd
from sqlalchemy import create_engine
import openai
# from flask_mysqldb import MySQL
import mysql.connector
from flask_cors import CORS
import json

app = Flask(__name__)

CORS(app)



@app.route("/")
def dashboard():
    return render_template("chatGPT.html")

@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/dashboard")
def register():
    return render_template("index.html")
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='reportdesk'
    )
    return connection


@app.route("/anser",methods=['POST'])
def answer():
    ques = request.form.get('question')
    email= request.form.get('email')
    print(email)
    # data = json.loads(json_string)
    print(ques)
    healthcare_words = ["medications","drugs", "pills", "tablets", "prescriptions", "dosages","diabetes", "cancer", "heart disease","covid-19" "asthma", "arthritis", "Alzheimer's disease", "Parkinson's disease", "mental health conditions", "infectious diseases","doctors", "nurses", "pharmacists", "surgeons", 'therapists', 'chiropractors', "acupuncturists", 'midwives',"hospitals", "clinics", "urgent care centers", "rehabilitation centers", "nursing homes", "hospices", "home health agencies", "policies", "premiums", "deductibles", "copays", "coverage", "claims", "network", "providers","fitness", "nutrition", "weight loss", "smoking cessation", "stress management", "sleep", "mental health", "addiction treatment","blood pressure monitors", "glucose meters", "prosthetics", "hearing aids", "wheelchairs", "crutches", "braces", "inhalers","surgeries", "diagnostic tests", "imaging studies", "biopsies", "vaccinations", "screenings", "check-ups","disease prevention", "vaccination campaigns", "epidemiology", "health promotion", "health policy", "disaster preparedness","electronic health records", "telemedicine", "health apps", "wearable devices", "AI in healthcare","double helix", "nucleotide", "gene", "chromosome", "base pair", "genome sequence", "mutation", "genetic code", "genetic variation","gene expression", "genetic mapping", "epigenetics", "transcriptomics", "proteomics", "metabolomics","cystic fibrosis", "sickle cell anemia", "Huntington's disease", "muscular dystrophy", "Down syndrome", "hemophilia", "thalassemia","CRISPR", "gene therapy", "genome engineering", "targeted gene editing","pharmacogenomics", "genetic testing", "genetic counseling", "precision medicine", "gene-based diagnosis", "gene-based therapy","population genetics", "evolutionary genetics", "molecular genetics", "comparative genomics", "functional genomics","genetic engineering", "synthetic biology", "gene synthesis", "gene cloning", "genetic modification", "recombinant DNA technology","genetic discrimination", "privacy concerns", "informed consent", "gene patenting", "intellectual property rights", "genetically modified organisms","whole genome sequencing", "targeted sequencing", "high-throughput sequencing", "next-generation sequencing", "nanopore sequencing","agriculture and livestock breeding", "forensic science", "paleogenomics", "conservation biology", "ancestry testing", "evolutionary biology", "Tay-Sachs disease", "bioinformatics", "side effects", "interactions" "diseases", "providers", "facilities", "insurance", "wellness", "equipment", "procedures", "public health", "technology"]

    def is_healthcare_question(question):
        for word in healthcare_words:
            if word in question.lower():
                return True
        return False
        
    
    user_input = ques
    if is_healthcare_question(user_input):
            # Process the question with the chatbot
        connection = create_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT answer FROM questions where question = '" + ques +"'")
        result = cursor.fetchall()
        print("Result: ", result) 
        
        if result:
            ## If a match is found, return the answer 
            
            print(result[0][0])
            # response = Response(result)
            # response.headers.add('Access-Control-Allow-Origin', '*')
            # response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            # response.headers.add('Access-Control-Allow-Methods', 'POST')
            # return response
            return result[0][0]
            
        else:
            ## If no match is found, ask chatGPT and return the answers1 = 'Hello'
            s2 = ''
            s1 = ques
            print(ques)
            s3 = "{} {}".format(s2, s1)
            response = openai.Completion.create(
                engine = "text-davinci-003",
                prompt = s3,
            
                max_tokens = 1500,
                n = 1,
                stop = None,
                temperature=0.5,
                timeout = 15,
            )
        
            answer = response.choices[0].text.strip()
            
            ## Store the new question and their answer in the database
            
            
            cursor.execute("INSERT INTO questions (question, answer,useremail) VALUES (%s, %s, %s)", (ques, answer, email))
            ## Returning new answer as response
            connection.commit()
    
            #Closing the cursor
            cursor.close()
            print(answer)
            # response = Response(answer)
            # response.headers.add('Access-Control-Allow-Origin', '*')
            # response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            # response.headers.add('Access-Control-Allow-Methods', 'POST')
            # return response
            return answer

    else:
        return "Sorry, only healthcare-related questions are allowed."
    


## Configure OpenAI API Key
openai.api_key = "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"



@app.route('/saveCustomer', methods=['POST'])
def saveCustomer():
   
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone')
    Orgnization = request.form.get('Orgnization')
    
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users where email = '" + email +"'")
    result = cursor.fetchall()
    print("Result: ", result) 
       
    if result:
        ## If a match is found, return the answer 
        print("Result: ", result)
       
        return "User Already Exits"
    else:
     
        
        ## Store the new question and their answer in the database
        
        
        cursor.execute("INSERT INTO users (name, password,email,phone,organisation) VALUES (%s, %s,%s, %s, %s)", (name, password,email,phone,Orgnization))
        ## Returning new answer as response
        connection.commit()
 
        #Closing the cursor
        cursor.close()
    
        
       
        return "Data added sucessfully"


#SignIn Form

@app.route('/signin', methods=['POST'])
def signIn():
   
    
    email = request.form.get('email')
    password = request.form.get('password')
  
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users where email = '" + email +"'")
    result = cursor.fetchall()
    print("Result: ", result) 

    
    if result[0][2] ==password:
        ## If a match is found, return the answer 
        print("Result: ", result)
        cursor.execute("SELECT * FROM questions where useremail = '" + email +"'")
        result = cursor.fetchall()
        return jsonify(result)
    else:
     
    
        return "No User Find"
    
@app.route('/fetchhistory', methods=['POST'])
def fetchhistory():
   
    
    email = request.form.get('email')
    
  
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM questions where useremail = '" + email +"'")
    result = cursor.fetchall()
    print("Result: ", result) 

    
    if result:
        ## If a match is found, return the answer 
        print("Result: ", result)
        cursor.execute("SELECT * FROM questions where useremail = '" + email +"'")
        result = cursor.fetchall()
        return jsonify(result)
    else:
        return "No Search History"
# Load questions from the Excel file


## Configure database connection
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'flask'
# mysql = MySQL(app)

# cursor = mysql.connection.cursor()

# db_engine = create_engine('postgresql://postgres:imgpt@localhost/imgpt')
#db_engine = create_engine('db-instance-url-goes-here-with-database-name')



## Function to match the incoming question 

@app.route('/getAnswer', methods=['POST','GET'])
def match_question():
    
    json_string = request.get_json()
    # data = json.loads(json_string)
    
    print("Kuchh ni aya")
    ques = json_string['question']
    ## Matching the question in the database
    print("request.data")
    
    
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT question, answer FROM questions where question = '" + ques +"'")
    result = cursor.fetchall()
    print("Result: ", result) 
       
    if result:
        ## If a match is found, return the answer 
        print("Result: ", result)
        print("Result: ", result)
        # response = Response(result)
        # response.headers.add('Access-Control-Allow-Origin', '*')
        # response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        # response.headers.add('Access-Control-Allow-Methods', 'POST')
        # return response
        return answer
        
    else:
        ## If no match is found, ask chatGPT and return the answers1 = 'Hello'
        s2 = ''
        s1 = ques
        print(ques)
        s3 = "{} {} {}".format(s2, s1, "?")
        response = openai.Completion.create(
            engine = "text-davinci-002",
            prompt = s3,
           
            max_tokens = 50,
            n = 1,
            stop = None,
            temperature=0.5,
            timeout = 10,
        )
       
        answer = response.choices[0].text.strip()
        
        ## Store the new question and their answer in the database
        
        
        cursor.execute("INSERT INTO questions (question, answer) VALUES (%s, %s)", (ques, answer))
        ## Returning new answer as response
        connection.commit()
 
        #Closing the cursor
        cursor.close()
        # response = Response(answer)
        # response.headers.add('Access-Control-Allow-Origin', '*')
        # response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        # response.headers.add('Access-Control-Allow-Methods', 'POST')
        # return response
        return answer


@app.route('/train_model', methods=['POST'])

def train_model():
    
    print("Kuchh ni aya")
    json_string = request.get_json()
    #data = json.loads(json_string)
    print(json_string)
    ques = json_string['subject']
    print(ques)
    answer = json_string['request_message']
   
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT question, answer FROM questions where question = '" + ques +"'")
    result = cursor.fetchall()
    print("Result: ", result) 
       
    if result:
        ## If a match is found, return the answer 
        print("Result: ", result)
        response = Response(json.dumps({'success':True}))
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    else:

        ## Store the new question and their answer in the database
        
        cursor.execute("INSERT INTO questions (question, answer) VALUES (%s, %s)", (ques, answer))
        ## Returning new answer as response
        connection.commit()
 
        #Closing the cursor
        cursor.close()
        response = Response({'sucess':True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    


#Send All Customer

@app.route('/alluser', methods=['GET'])

def alluser():
    
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print("Result: ", result) 
    
       
    if result:
        ## If a match is found, return the answer 
        print("Result: ", result)
        resp=jsonify(result)
        
        response = Response(resp)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    else:
        resp=jsonify({'sucess':False})
        
        response = Response({'sucess':True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

@app.route('/allquestion', methods=['GET'])

def allquestion():
    
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM questions")
    result = cursor.fetchall()
    
    
       
    if result:
        ## If a match is found, return the answer 
        #print("Result: ", result)
        resp=jsonify(result)
        
        # response = Response(resp)
        # response.headers['Access-Control-Allow-Origin'] = '*'
       
        return resp
    else:
        
        response = Response({'sucess':True})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
app.run(debug=True)