
from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
GoogleMaps(app)
app.secret_key = 'ssh...Big secret!'
#MySQL configurations

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'tekken5'
app.config['MYSQL_DATABASE_DB'] = 'safelocality'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# route to index.html
@app.route("/")
def main():
    return render_template('index.html')

# route to signup.html
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# interact with MySQL for sign up
@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _firstname = request.form['inputFirstName']
        _lastname = request.form['inputLastName']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_firstname,_lastname,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return redirect('/showSignin')
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        if len(data) > 0:
            if check_password_hash(str(data[0][5]),_password):
                session['user'] = data[0][0]
                print "here"
                return redirect('/dashboard')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()
@app.route('/dashboard')
def demo():
    newDict = {}
    with open('Places.txt','r') as lines:
        for i in lines:
            k=i.split(',')
            v=k[2].strip("\n").strip("\r")
            cord=[k[1],v]
            newDict[k[0]] = cord
    conn = mysql.connect()
    cursor = conn.cursor()
    place=[]
    lat=[]
    lon=[]
    k=0
    print newDict
    for i in newDict:
        place.append(i)
        lat.append(float(newDict[i][0])) 
        lon.append(float(newDict[i][1])) 
    #cursor.callproc('sp_addLoc',('dfsd',12.12,12.1234,))
    for i in range(0,len(place)):
        cursor.callproc('sp_addLoc',(place[i],lat[i],lon[i]))
    cursor.execute("DELETE FROM Coordinates WHERE Loc_id>140")
    cursor.execute("SELECT Loc_name FROM Coordinates")
    data = cursor.fetchall()
    print data
    conn.commit()
    cursor.close()
    conn.close()
    print "here I am"
    return render_template('dashboard.html', data = data)


@app.route('/places/<place_name>/')
def places(place_name):
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Coordinates WHERE Loc_name = %s", (place_name))
        data = cursor.fetchall()
        print data
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('demo.html',data = data)
    else:
        return render_template('error.html',error = 'Unauthorized Access')
@app.route('/userHome')
def userHome():
    if session.get('user'):
        mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        style = "height:600px;width:600px;",
        markers={'http://maps.google.com/mapfiles/ms/icons/green-dot.png':[(37.4419, -122.1419)],
                 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png':[(37.4300, -122.1400)]}
        )
        return render_template('userHome.html', mymap=mymap)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.run()
