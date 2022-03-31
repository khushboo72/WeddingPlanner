from flask import Flask
from flask import request, jsonify,session,redirect,url_for
from flask_mail import *
from DBHelper import server_connection
from DBHelper import get_sql_connection
from DBHelper import create_table
from accounts import admin_connection
from accounts import create_tableadmin
from random import * 
from authlib.integrations.flask_client import OAuth
import bookevent
import mysql.connector
import json
import DBHelper
import venue
import mandap 
import meal 
import equipment 
import decor 
import seating
import transport 
import accounts
import emp 
from flask_bcrypt import Bcrypt

connection1=server_connection()
connection = get_sql_connection()
connection2=admin_connection()
create_table(connection)
create_tableadmin(connection2)
otp=randint(0000,9999)

app = Flask(__name__)
app.secret_key="khushboo"

# with open('config.json','r') as f:
#     parameter=json.load(f)['parameters']

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT']=465
# app.config['MAIL_USERNAME']=parameter['gmailuser']
# app.config['MAIL_PASSWORD']=parameter['gmailpassword']
# app.config['MAIL_USE_TLS']= False
# app.config['MAIL_USE_SSL']= True

mail=Mail(app)
bcrypt = Bcrypt(app)
oauth = OAuth(app)
app.config['GOOGLE_CLIENT_ID']="915087860247-kld8efr0u0bov67vhehv5j08ck0p00nq.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET']="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"

google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)

@app.route('/email') #this is just for testing purpose. It should not be included in main code 
def email():
    msg=Message('mail',sender='demo@gmail.com',recipients=['gadiakhushboo@gmail.com'])
    msg.body="this is a test mail"
    mail.send(msg)
    return"msg sent"
 
@app.route('/verify',methods=['POST']) #This function will send otp to the user  
def emailverify():
    gmail=request.form['email']
    msg=Message('OTP',sender='demo@gmail.com',recipients=[gmail])
    msg.body=str(otp)
    mail.send(msg)
    return "msg sent"

@app.route('/validate',methods=['POST']) # to check whether the otp entered by the user is correct or not
def emailvalidate():

    userotp=request.form['otp']
    if otp==int(userotp):
        return "Email Verified Successfully"
    return "Email not verified.Please try again"

# @app.route('/googlelogin') #Method 2 
# def google_login():
#     google = oauth.create_client('google')
#     redirect_uri = url_for('google_authorize', _external=True)
#     return google.authorize_redirect(redirect_uri)

# # Google authorize route. The user will bw redirected here in case of sccessful login 
# @app.route('/googleauthorize')
# def google_authorize():
#     google = oauth.create_client('google')
#     token = google.authorize_access_token()
#     resp = google.get('userinfo').json()
#     print(f"\n{resp}\n")
#     return "You are successfully signed in using google"


@app.route('/register', methods=['POST'])
def register():
    if 'usertype' in request.json and 'userfullname' in request.json and 'username' in request.json and 'userpassword' in request.json and 'email' in request.json and 'usercontact' in request.json and 'usercity' in request.json and 'userstate' in request.json and 'usercountry' in request.json:
        usertype = request.json['usertype']
        userfullname=request.json['userfullname']
        username = request.json['username']
        userpassword = request.json['userpassword']
        email = request.json['email']
        usercontact=request.json['usercontact']
        usercity=request.json['usercity']
        userstate=request.json['userstate']
        usercountry=request.json['usercountry']
        
        cursor = connection2.cursor()
        cursor.execute('SELECT * FROM account WHERE email=%s OR username=%s OR usercontact=%s', (email,username,usercontact,))
        accounts = cursor.fetchone()
        if email in accounts:
            return 'email already exists'
        elif username in accounts:
            return 'Username already taken'
        elif usercontact in accounts:
            return 'phone number already exists'
        else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
            userpassword = bcrypt.hashpw(userpassword.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO account VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,)', (usertype,userfullname,username, userpassword, email,usercontact,usercity,userstate,usercountry))
            connection2.commit() 
    return 'Please fill out the form'

@app.route('/login', methods=['POST'])
def login():
    if 'userpassword' in request.json and 'email' in request.json:
        userpassword = request.json['userpassword']
        email = request.json['email']
        
        cursor = connection2.cursor()
        cursor.execute('SELECT * FROM account WHERE email = %s ', (email, ))
        # Fetch one record and return result
        accounts = cursor.fetchone()
        if accounts:
            if bcrypt.checkpw(userpassword.encode('utf-8'), accounts.userpassword):
                return 'login successful'
            else:
                return 'User does not exists'
        return 'sg'
    return 'User does not exists'

@app.route('/logout')  
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('user_id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


@app.route('/updateaccount', methods=['PUT'])
def updateaccount():   
    user_id = accounts.update_account(connection,request.json)
    response = jsonify({
        'user_id': user_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
   
@app.route('/deleteaccount', methods=['POST'])
def deleteaccount():    
    return_id = accounts.delete_account(connection2,request.json)
    response = jsonify({
        'user_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deletebooking', methods=['POST'])
def deletebooking():
    return_id = bookevent.delete_booking(connection,request.json)
    response = jsonify({
        'cust_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getvenue')
def getvenue():
    venue1  = venue.get_venue(connection)
    response=jsonify(venue1)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertvenue',methods=['POST'])
def insertvenue():
    request_payload = request.json
     # request_payload = json.loads(request.json)
    venue_id=venue.insert_venue(connection,request_payload)
    response=jsonify({
        'venue_id': venue_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deletevenue', methods=['POST'])
def deletevenue():
    return_id = venue.delete_venue(connection,request.json)
    response = jsonify({
        'venue_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updatevenue', methods=['PUT'])
def updatevenue():
    venue_id = venue.update_venue(connection,request.json)
    response = jsonify({
        'venue_id': venue_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getmandap')
def getmandap():
    mandap1  = mandap.get_mandap(connection)
    response=jsonify(mandap1)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertmandap',methods=['POST'])
def insertmandap():
    request_payload = request.json
    mandap_id=mandap.insert_mandap(connection,request_payload)
    response=jsonify({
        'mandap_id': mandap_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletemandap', methods=['POST'])
def deletemandap():    
    return_id = mandap.delete_mandap(connection,request.json)
    response = jsonify({
        'mandap_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updatemandap', methods=['PUT'])
def updatemandap():
    mandap_id = mandap.update_mandap(connection,request.json)
    response = jsonify({
        'mandap_id': mandap_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getmeal')
def getmeal():
    meal1  = meal.get_meal(connection)
    response=jsonify(meal1)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertmeal',methods=['POST'])
def insertmeal():
    request_payload = request.json
    meal_id=meal.insert_meal(connection,request_payload)
    response=jsonify({
        'meal_id': meal_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletemeal', methods=['POST'])
def deletemeal():
    return_id = meal.delete_meal(connection,request.json)
    response = jsonify({
        'meal_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updatemeal', methods=['PUT'])
def updatemeal():
    meal_id = meal.update_meal(connection,request.json)
    response = jsonify({
        'meal_id': meal_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/getequipment')
def getequipment():
    equipment1  = equipment.get_equipment(connection)
    response=jsonify(equipment1)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertequipment',methods=['POST'])
def insertequipment():
    request_payload = request.json
    equipment_id=equipment.insert_equipment(connection,request_payload)
    response=jsonify({
        'equipment_id': equipment_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deleteequipment', methods=['POST'])
def deleteequipment():
    return_id = equipment.delete_equipment(connection,request.json)
    response = jsonify({
        'equipment_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/updateequipment', methods=['PUT'])
def updateequipment():
    equipment_id = equipment.update_equipment(connection,request.json)
    response = jsonify({
        'equipment_id': equipment_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getdecor')
def getdecor():
    decor1  = decor.get_decor(connection)
    response=jsonify(decor1)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertdecor',methods=['POST'])
def insertdecor():
    request_payload = request.json
    decor_id=decor.insert_decor(connection,request_payload)
    response=jsonify({
        'decor_id': decor_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletedecor', methods=['POST'])
def deletedecor():
    return_id = decor.delete_decor(connection,request.json)
    response = jsonify({
        'decor_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/updatedecor', methods=['PUT'])
def updatedecor():
    decor_id = decor.update_decor(connection,request.json)
    response = jsonify({
        'decor_id': decor_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getseating')
def getseating():
    seating1  = seating.get_seating(connection)
    response=jsonify(seating1)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertseating',methods=['POST'])
def insertseating():
    request_payload = request.json
    seating_id=seating.insert_seating(connection,request_payload)
    response=jsonify({
        'seating_id': seating_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deleteseating', methods=['POST'])
def deleteseating():
    return_id = seating.delete_seating(connection,request.json)
    response = jsonify({
        'seating_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/updateseating', methods=['PUT'])
def updateseating():
    seating_id = seating.update_seating(connection,request.json)
    response = jsonify({
        'seating_id': seating_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/gettransport')
def gettransport():
    transport1  = transport.get_transport(connection)
    response=jsonify(transport1)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/inserttransport',methods=['POST'])
def inserttransport():
    request_payload = request.json
    transport_id=transport.insert_transport(connection,request_payload)
    response=jsonify({
        'transport_id': transport_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletetransport', methods=['POST'])
def deletetransport():
    return_id = transport.delete_transport(connection,request.json)
    response = jsonify({
        'transport_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updatetransport', methods=['PUT'])
def updatetransport():
    transport_id = transport.update_transport(connection,request.json)
    response = jsonify({
        'transport_id': transport_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getemp')
def getemp():
    emp1 = emp.get_emp(connection)
    response=jsonify(emp1)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertemp',methods=['POST'])
def insertemp():
    request_payload = request.json
    emp_id=emp.insert_emp(connection,request_payload)
    response=jsonify({
        'emp_id': emp_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deleteemp', methods=['POST'])
def deleteemp():
    return_id = emp.delete_emp(connection,request.json)
    response = jsonify({
        'emp_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/updateemp', methods=['PUT'])
def updateemp():
    emp_id = emp.update_emp(connection,request.json)
    response = jsonify({
        'emp_id': emp_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Wedding Planner Management System")
    app.run(debug=True,port=5000)