import pymysql
import configparser
from flask import Flask, jsonify,request
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()

config = configparser.ConfigParser()
config.read('config.ini')




app.config['MYSQL_DATABASE_USER'] = config["UserManagement"]['MYSQL_DATABASE_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = config["UserManagement"]['MYSQL_DATABASE_PASSWORD']
app.config['MYSQL_DATABASE_DB'] = config["UserManagement"]['MYSQL_DATABASE_DB']
app.config['MYSQL_DATABASE_HOST'] = config["UserManagement"]['MYSQL_DATABASE_HOST']

mysql.init_app(app)



    

@app.route('/getAll')
def getAll():

        mycursor = mysql.connect().cursor(pymysql.cursors.DictCursor)

        mycursor.execute("select * from users")
        rows=mycursor.fetchall()
        resp = jsonify(rows)
        return resp




@app.route('/get')
def get():
    try:
        mycursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
        q = "select * from users where {} = %s".format(request.args.get('col'))
        mycursor.execute(q,(request.args.get('val'),))
        rows=mycursor.fetchall()
        resp = jsonify(rows)
        return resp
    except pymysql.err.InternalError:
        print("error")
        return("Invalid column entered")


@app.route('/deleteUser')
def deleteUser():
    try:
        mycon = mysql.connect()
        mycursor = mycon.cursor(pymysql.cursors.DictCursor)
        q = "delete from users where username = %s"
    
        mycursor.execute(q,(request.args.get('username'),))
        mycon.commit()
    
        return getAll()
    except pymysql.err.InternalError:
        print("error")
        return("Username does not exist")


@app.route('/delete')
def delete():
    
    try:
        mycon = mysql.connect()
        mycursor = mycon.cursor(pymysql.cursors.DictCursor)
        q = "delete from users where {} = %s".format(request.args.get('col'))

        mycursor.execute(q,(request.args.get('val'),))
        mycon.commit()
    
        return getAll()
    
    except pymysql.err.InternalError:
        print("error")
        return("Column does not exist")
    

@app.route('/update')
def update():
    try:
        mycon = mysql.connect()
        mycursor = mycon.cursor(pymysql.cursors.DictCursor)
        q = "Update users set {} = %s where username = %s".format(request.args.get('col'))
        mycursor.execute(q,(request.args.get('val'),request.args.get('username')))
        mycon.commit()
    
        return getAll()
    except pymysql.err.InternalError:
        print("error")
        return("Enter a valid column")
    except pymysql.err.ProgrammingError:
        print("error")
        return("Enter a valid column")
    except pymysql.err.IntegrityError:
        return("Invalid username value")
    #program error


@app.route('/updateAll')
def updateAll():
    try:
        mycon = mysql.connect()
        mycursor = mycon.cursor(pymysql.cursors.DictCursor)
        q = "Update users set firstname = %s,lastname = %s,username = %s ,password = %s,email= %s, active=%s where username = %s"
        mycursor.execute(q,(request.args.get('firstname'),request.args.get('lastname'),request.args.get('newusername'),request.args.get('password'),request.args.get('email'),request.args.get('active'),request.args.get('username')))
    
        mycon.commit()
    
        return getAll()
        
    except pymysql.err.IntegrityError:
        return("Invalid value for new username") 
    


@app.route('/create')
def create():
    try:
        mycon = mysql.connect()
        mycursor = mycon.cursor(pymysql.cursors.DictCursor)
        q = "insert into users(Firstname,Lastname,Username,Password,Email,Active) values(%s,%s,%s,%s,%s,%s)"
        mycursor.execute(q,(request.args.get('firstname'),request.args.get('lastname'),request.args.get('username'),request.args.get('password'),request.args.get('email'),request.args.get('active')))
        mycon.commit()

        return getAll()
    except pymysql.err.IntegrityError:
        return("Invalid value for username")
    except pymysql.err.InternalError:
        return("Invalid value for active")

@app.route('/usernameContains')
def usernameContains():
    mycon = mysql.connect()
    mycursor = mycon.cursor(pymysql.cursors.DictCursor)
    q = "Select * from users Where Username like '%{}%' ".format(request.args.get('word'))
    mycursor.execute(q)
    rows=mycursor.fetchall()
    resp = jsonify(rows)
    return resp


@app.route('/getActiveUsers')
def getActiveUsers():
    mycon = mysql.connect()
    mycursor = mycon.cursor(pymysql.cursors.DictCursor)
    mycursor.execute("select * from users where active = true")
    rows=mycursor.fetchall()
    resp = jsonify(rows)
    return resp

@app.route('/getInactiveUsers')
def getInactiveUsers():
    mycon = mysql.connect()
    mycursor = mycon.cursor(pymysql.cursors.DictCursor)
    mycursor.execute("select * from users where active = 0")
    rows=mycursor.fetchall()
    resp = jsonify(rows)
    return resp


@app.route('/createGroup')
def createGroup():
    try:
        mycon = mysql.connect()
        mycursor = mycon.cursor(pymysql.cursors.DictCursor)
        q = "create table {} (Id int NOT NULL AUTO_INCREMENT, Username varchar(255) UNIQUE not null, permission ENUM('Admin', 'member', 'viewer', 'collaborator') default 'member', primary key(ID), foreign key(Username) references Users(Username))".format(request.args.get('name'))
        q2 = "insert into GroupsList(name) values(%s)"
        mycursor.execute(q2,request.args.get('name'),)
        mycursor.execute(q)
    
        mycon.commit()
        return getAllGroups()
    except pymysql.err.IntegrityError:
        return("Invalid value for groupname")
    except pymysql.err.InternalError:
        return("Invalid value for groupname")
    except pymysql.err.ProgrammingError:
        print("error")
        return("Invalid value for groupname")
    
@app.route('/getAllGroups')
def getAllGroups():
    mycursor = mysql.connect().cursor(pymysql.cursors.DictCursor)

    mycursor.execute("select * from GroupsList")
    rows=mycursor.fetchall()
    resp = jsonify(rows)
    return resp


@app.route('/getAllFromGroup')
def getAllFromGroup():
    mycon = mysql.connect()
    mycursor = mycon.cursor(pymysql.cursors.DictCursor)
    q = "Select * from {}".format(request.args.get('name'))
    mycursor.execute(q)
    rows=mycursor.fetchall()
    resp = jsonify(rows)
    return resp


@app.route('/getAllUserGroups')
def getAllUserGroups():
    username= format(request.args.get('username'))
    mycon = mysql.connect()
    mycursor = mycon.cursor(pymysql.cursors.DictCursor)
    mycursor.execute("Select * from GroupsList")
    rows=mycursor.fetchall()
    g = []
    f = []
    for row in rows:
        g.append(row['name'])
    for group in g:
        res = {}
        q =  "select permission from {} where username = %s".format(group)
        mycursor.execute(q,username,)
        re = mycursor.fetchall()
        
        if re:
            
            res[group] = re[0]['permission']
            f.append(res)
            
    
    
    resp = jsonify(f)
    return resp
        
def getAllFromGroup(group):
    mycon = mysql.connect()
    mycursor = mycon.cursor(pymysql.cursors.DictCursor)
    q = "Select * from {}".format(group)
    mycursor.execute(q)
    rows=mycursor.fetchall()
    resp = jsonify(rows)
    return resp
    

@app.route('/addUserToGroup')
def addUserToGroup():
    try:
        mycon = mysql.connect()
        mycursor = mycon.cursor(pymysql.cursors.DictCursor)
        q = "insert into {} (username,permission) values (%s,%s)".format(request.args.get('groupname'))
        mycursor.execute(q,(request.args.get('username'),request.args.get('permission')))
        mycon.commit()
        return getAllFromGroup(request.args.get('groupname'))
    except pymysql.err.IntegrityError:
        return("Invalid value for username")
    except pymysql.err.InternalError:
        return("Invalid values entered")
    except pymysql.err.ProgrammingError:
       
        return("Invalid values entered")



@app.route('/getPermissionInGroup')
def getPermissionsInGroup():
    try:
        mycon = mysql.connect()
        mycursor = mycon.cursor(pymysql.cursors.DictCursor)
        q = "select * from {} where permission = %s".format(request.args.get('groupname'))
        mycursor.execute(q,request.args.get('permission'),)
        rows=mycursor.fetchall()
        resp = jsonify(rows)
        return resp
    except pymysql.err.ProgrammingError:       
        return("enter valid groupname and permission")


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_error(error):

    return "Error: Invalid values entered"

    
    
    
if __name__ == '__main__':
    app.run()

