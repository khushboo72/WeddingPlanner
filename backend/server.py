from flask import Flask, request, jsonify,session,render_template,redirect,url_for
import re
from DBHelper import server_connection
from DBHelper import get_sql_connection
from DBHelper import create_table
from accounts import admin_connection
from accounts import create_tableadmin

import bookevent
import mysql.connector
import json
import DBHelper
import venue
import mandap 
import meal 
import stage
import equipment 
import decor 
import seating
import transport 
import accounts



connection1=server_connection()
connection = get_sql_connection()
connection2=admin_connection()
create_table(connection)
create_tableadmin(connection2)

app = Flask(__name__)
app.secret_key = 'khush'


@app.route('/login',methods=['GET','POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'userpassword' in request.form:
        # Create variables for easy access
        username = request.form['username']
        userpassword = request.form['userpassword']
        # Check if account exists using MySQL
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM account WHERE username = %s AND userpassword = %s', (username, userpassword,))
        # Fetch one record and return result
        accounts = cursor.fetchone()
        # If account exists in accounts table in out database
        if accounts:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_id'] = accounts['user_id']
            session['username'] = accounts['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    
    return render_template('index.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'userpassword' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        userpassword = request.form['userpassword']
        email = request.form['email']
                # Check if account exists using MySQL
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM account WHERE username = %s', (username,))
        accounts = cursor.fetchone()
        # If account exists show error and validation checks
        if accounts:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not userpassword or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO account VALUES (NULL, %s, %s, %s)', (username, userpassword, email,))
            connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
    

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
    request_payload = json.loads(request.form['data'])
    user_id = accounts.update_account(connection, request_payload)
    response = jsonify({
        'user_id': user_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
   
@app.route('/deletebooking', methods=['POST'])
def deletebooking():
    return_id = bookevent.delete_booking(connection,request.form['cust_id'])
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
    request_payload = json.loads(request.form['data'])
    venue_id=venue.insert_venue(connection,request_payload)
    response=jsonify({
        'venue_id': venue_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletevenue', methods=['POST'])
def deletevenue():
    return_id = venue.delete_venue(connection,request.form['venue_id'])
    response = jsonify({
        'venue_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/updatevenue', methods=['PUT'])
def updatevenue():
    request_payload = json.loads(request.form['data'])
    venue_id = venue.update_venue(connection, request_payload)
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
    request_payload = json.loads(request.form['data'])
    mandap_id=mandap.insert_mandap(connection,request_payload)
    response=jsonify({
        'mandap_id': mandap_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletemandap', methods=['POST'])
def deletemandap():
    return_id = mandap.delete_mandap(connection,request.form['mandap_id'])
    response = jsonify({
        'mandap_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/updatemandap', methods=['PUT'])
def updatemandap():
    request_payload = json.loads(request.form['data'])
    mandap_id = mandap.update_mandap(connection, request_payload)
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
    request_payload = json.loads(request.form['data'])
    meal_id=meal.insert_meal(connection,request_payload)
    response=jsonify({
        'meal_id': meal_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletemeal', methods=['POST'])
def deletemeal():
    return_id = meal.delete_meal(connection,request.form['meal_id'])
    response = jsonify({
        'meal_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updatemeal', methods=['PUT'])
def updatemeal():
    request_payload = json.loads(request.form['data'])
    meal_id = meal.update_meal(connection, request_payload)
    response = jsonify({
        'meal_id': meal_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getstage')
def getstage():
    stage1  = stage.get_stage(connection)
    response=jsonify(stage1)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertstage',methods=['POST'])
def insertstage():
    request_payload = json.loads(request.form['data'])
    stage_id=stage.insert_stage(connection,request_payload)
    response=jsonify({
        'stage_id': stage_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletestage', methods=['POST'])
def deletestage():
    return_id = stage.delete_stage(connection,request.form['stage_id'])
    response = jsonify({
        'stage_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updatestage', methods=['PUT'])
def updatestage():
    request_payload = json.loads(request.form['data'])
    stage_id = stage.update_stage(connection, request_payload)
    response = jsonify({
        'stage_id': stage_id
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
    request_payload = json.loads(request.form['data'])
    equipment_id=equipment.insert_equipment(connection,request_payload)
    response=jsonify({
        'equipment_id': equipment_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deleteequipment', methods=['POST'])
def deleteequipment():
    return_id = equipment.delete_equipment(connection,request.form['equipment_id'])
    response = jsonify({
        'equipment_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/updateequipment', methods=['PUT'])
def updateequipment():
    request_payload = json.loads(request.form['data'])
    equipment_id = equipment.update_equipment(connection, request_payload)
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
    request_payload = json.loads(request.form['data'])
    decor_id=decor.insert_decor(connection,request_payload)
    response=jsonify({
        'decor_id': decor_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletedecor', methods=['POST'])
def deletedecor():
    return_id = decor.delete_decor(connection,request.form['decor_id'])
    response = jsonify({
        'decor_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/updatedecor', methods=['PUT'])
def updatedecor():
    request_payload = json.loads(request.form['data'])
    decor_id = decor.update_decor(connection, request_payload)
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
    request_payload = json.loads(request.form['data'])
    seating_id=seating.insert_seating(connection,request_payload)
    response=jsonify({
        'seating_id': seating_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deleteseating', methods=['POST'])
def deleteseating():
    return_id = seating.delete_seating(connection,request.form['seating_id'])
    response = jsonify({
        'seating_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/updateseating', methods=['PUT'])
def updateseating():
    request_payload = json.loads(request.form['data'])
    seating_id = seating.update_seating(connection, request_payload)
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
    request_payload = json.loads(request.form['data'])
    transport_id=transport.insert_transport(connection,request_payload)
    response=jsonify({
        'transport_id': transport_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/deletetransport', methods=['POST'])
def deletetransport():
    return_id = transport.delete_transport(connection,request.form['transport_id'])
    response = jsonify({
        'transport_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/updatetransport', methods=['PUT'])
def updatetransport():
    request_payload = json.loads(request.form['data'])
    transport_id = transport.update_transport(connection, request_payload)
    response = jsonify({
        'transport_id': transport_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Wedding Planner Management System")
    app.run(debug=True,port=5000)
