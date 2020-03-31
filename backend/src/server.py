from flask import Flask, request, jsonify, send_file, redirect, Response, render_template
from flask_restful import Resource, Api
#from flask_mysqldb import MySQL
import mysql.connector
import requests
import db
import navigatorhandlers
import landlordhandlers
import propertyhandlers
import authhandlers
import os
import logging

# flask setup
app = Flask(__name__, template_folder="../templates")
app.config.from_pyfile('../config.cfg')
'''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyDB'
mysql = MySQL(app)
'''
# db setup
db = db.DB(os.environ['DYNAMO_DB_ENDPOINT'])

cnx = mysql.connector.connect(user='ss8rs', password='ssy19981025ssy',
                                host='cs4750.cs.virginia.edu',
                                database='ss8rs')

##########
## util ##
##########



def server_docs():
    """Serves docs to browser"""
    return send_file("../api/index.html")


def err_out(code, error):
    """util function for returning non 2xx responses"""
    logging.error(error)
    return jsonify(code=code, error=error), code


#########
## api ##
#########

supportedCrudEndpoints = [{
    "name":
    "navigator",
    "path":
    "/navigator",
    "methods": [ {
        "method": "POST",
        "handler": navigatorhandlers.post_navigator
    }, {
        "method": "PUT",
        "handler": navigatorhandlers.put_navigator
    }, {
        "method": "DELETE",
        "handler": navigatorhandlers.delete_navigator
    }]
}, {
    "name":
    "landlord",
    "path":
    "/landlord",
    "methods": [{
        "method": "GET",
        "handler": landlordhandlers.get_landlord
    }, {
        "method": "POST",
        "handler": landlordhandlers.post_landlord
    }, {
        "method": "PUT",
        "handler": landlordhandlers.put_landlord
    }, {
        "method": "DELETE",
        "handler": landlordhandlers.delete_landlord
    }]
}, {
    "name":
    "property",
    "path":
    "/property",
    "methods": [{
        "method": "GET",
        "handler": propertyhandlers.get_property
    }, {
        "method": "POST",
        "handler": propertyhandlers.post_property
    }, {
        "method": "PUT",
        "handler": propertyhandlers.put_property
    }, {
        "method": "DELETE",
        "handler": propertyhandlers.delete_property
    }]
}, {
    "name":
    "register a new user",
    "path":
    "/auth/register",
    "methods": [{
        "method": "POST",
        "handler": authhandlers.register_new_user
    }]
}, {
    "name":
    "login an existing user",
    "path":
    "/auth/login",
    "methods": [{
        "method": "POST",
        "handler": authhandlers.login
    }]
}, {
    "name":
    "get the status of a user",
    "path":
    "/auth/status",
    "methods": [{
        "method": "GET",
        "handler": authhandlers.get_login_status
    }]
}, {
    "name":
    "log out a user",
    "path":
    "/auth/logout",
    "methods": [{
        "method": "GET",
        "handler": authhandlers.logout
    }]
}]

for endpt in supportedCrudEndpoints:
    for m in endpt.get("methods"):
    # add_url_rule(rule, endpoint, view_func, options )
        app.add_url_rule(endpt.get("path"),
                         "{} a {}".format(m.get("method"), endpt.get("name")),
                         m.get("handler"),
                         methods=[m.get("method")])
app.add_url_rule('/navigator/<id>', "GET a Navigator", navigatorhandlers.get_navigator, methods = ['GET'])

# docs

app.add_url_rule('/', "swagger docs", server_docs)


@app.route('/index', methods = ["GET", "POST"])
def index():
    if (request.method == "POST"):
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cursor = cnx.cursor()
        add_user = ("Insert INTO MyUsers" 
                    "(firstName, lastName)"
                    "Values (%s, %s)" )
        data_user = (firstName, lastName)
        cursor.execute(add_user, data_user)
        cnx.commit()
        cnx.close()
        return 'sucesss'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
