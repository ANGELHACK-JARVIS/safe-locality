
from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import pygal
from pygal.style import BlueStyle, NeonStyle,DarkSolarizedStyle, LightSolarizedStyle, LightColorizedStyle, DarkColorizedStyle, TurquoiseStyle

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

    if(session.get('user')):
        return render_template('home.html',session = session)
    else:
        return render_template('home.html')
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
                return render_template('home.html')
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
    #No need to repeatedly create and delete tuples from the Coordinates table
    #place=[]
    #lat=[]
    #lon=[]
    #k=0
    #print newDict
    #for i in newDict:
    #    place.append(i)
    #    lat.append(float(newDict[i][0]))
    #    lon.append(float(newDict[i][1]))
    #cursor.callproc('sp_addLoc',('dfsd',12.12,12.1234,))
    #for i in range(0,len(place)):
    #    cursor.callproc('sp_addLoc',(place[i],lat[i],lon[i]))
    #cursor.execute("DELETE FROM Coordinates WHERE Loc_id<6 and Loc_id>8")
    cursor.execute("SELECT Loc_name FROM Coordinates ORDER BY Loc_name DESC")
    data = cursor.fetchall()
    print data
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('dashboard.html', data = data)

######################################################################################33
#This is the review form implementation

@app.route('/addStats')
def displayForm():
    return render_template('addStats.html')

@app.route('/addStats', methods=['POST'])
def takeData():
    locale=str(request.form['inputLocale'])
    water=int(request.form['inputWater'])
    electricity=int(request.form['inputElectricity'])
    network=int(request.form['inputNetworkAvailability'])
    cleanliness=int(request.form['inputCleanliness'])
    green=int(request.form['inputGreenSpace'])
    life=int(request.form['inputNightlife'])
    rmen=int(request.form['inputRepairmenAvailability'])
    edu=int(request.form['inputeducation'])
    nhood=int(request.form['inputNeighbourhood'])
    lent=int(request.form['inputLocalEntertainment'])
    rev=str(request.form['inputReview'])
    uid=int(session.get('user'))
    conn=mysql.connect()
    cur=conn.cursor()
    cur.execute("Select Loc_id from Coordinates where Loc_name=%s",(locale))
    lid=int(cur.fetchone()[0])
    cur.execute("Insert into Review (UserId,Loc_id,review_text) values(%s,%s,%s)",(uid,lid,rev))
    conn.commit()
    cur.callproc('sp_addStats',(uid,lid,water,electricity,network,cleanliness, green, lent, life, rmen, edu, nhood))
    conn.commit()
    cur.close()
    conn.close()
    return render_template('home.html')

######################################################################################

@app.route('/places/<place_name>/')
def places(place_name):
    if session.get('user'):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Coordinates WHERE Loc_name = %s", (place_name))
        data = cursor.fetchall()[0]
        name=data[1]
        conn.commit()
        cursor.close()
        conn.close()
        mymap = Map(
        identifier="view-side",
        lat=data[2],
        lng=data[3],
        markers=[(37.4419, -122.1419)]
        )

        lat = data[2]
        lon = data[3]

        #The graph is made and passed on from here onwards
        ###################################################
        title="Crime Rates"
        crime_graph=pygal.Bar(width=600, height=600, explicit_size=True, title=title, style=BlueStyle, disable_xml_declaration=True, range=(0,10))
        crime_labels=['Theft','Violence', 'Harassment']
        conn = mysql.connect()
        cursor = conn.cursor()
        #procedure not used for simpler execution
        cursor.execute("select avg(Theft), avg(Violence), avg(Harassment) from Security, Coordinates where Coordinates.Loc_id=Security.Loc_id and Coordinates.Loc_name=%s",(place_name))
        data1=cursor.fetchone()
        crime_values=[data1[0],data1[1],data1[2]]
        crime_graph.x_labels=crime_labels
        crime_graph.add('Rating', crime_values)
        lifestyle_graph=pygal.Bar(width=1200, height=600, explicit_size=True, title="Living Standards", style=BlueStyle, disable_xml_declaration=True, range=(0,10))
        cursor.close()
        conn.close()
        conn = mysql.connect()
        cursor = conn.cursor()
        #procedure not used for simpler execution
        cursor.execute("SELECT avg(Water), avg(Electricity), avg(Network_Availability), avg(Cleanliness), avg(Green_space), avg(Local_Entertainment), avg(NightLife), avg(Repairmen_avail), avg(Education), avg(Neighbourhood) from LifeStyle, Coordinates where Coordinates.Loc_id=LifeStyle.Loc_id and Coordinates.Loc_name=%s",(place_name))
        data1=cursor.fetchone()
        lifestyle_values=[data1[0], data1[1], data1[2], data1[3], data1[4], data1[5], data1[6], data1[7], data1[8], data1[9]]
        lifestyle_labels=["Water", "Electricity", "Network Availability", "Cleanliness", "Green Space", "Local Entertainment", "Night Life", "Services", "Education", "Neighbourhood"]
        lifestyle_graph.x_labels=lifestyle_labels
        lifestyle_graph.add('Rating', lifestyle_values)
        graphs=[crime_graph, lifestyle_graph]
        cursor.close()
        conn.close()
        ########################################################
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Review where Loc_id = (SELECT Loc_id from Coordinates where Loc_name=%s) ",(place_name))
        dat = cursor.fetchone()
        print dat[0]
        cursor.execute("SELECT UserName from User where UserId = %s",dat[0])
        use_fec = cursor.fetchone()
        print use_fec[0]
        return render_template('demo.html',use_fec=use_fec,rev_data=dat,name=name, mymap=mymap,data=data,lat = data[2],lon=data[3], graphs=graphs,dat=dat)

    else:
        return render_template('error.html',error = 'Unauthorized Access')
@app.route('/demo')
def userHome():
    if session.get('user'):
        mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
        return render_template('demo.html', mymap=mymap)
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return render_template('home.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
