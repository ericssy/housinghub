import server
import requests
from flask import send_file, request, jsonify
import mysql.connector

def get_navigator(id):
    """finds and returns a navigator in the DB"""
    #id = request.get_json(force = True).get("id")
    print("test")
    cursor = server.cnx.cursor()
    query = ("SELECT * FROM navigator WHERE navigator_id = %s")
    data_id = (id,)
    cursor.execute(query, data_id)
    rows = cursor.fetchall()
    return str(rows)


def post_navigator():
    """adds a new navigator to the database and returns response"""
     
    lastName = request.get_json().get("lastName")
    firstName = request.get_json().get("firstName")
    cursor = server.cnx.cursor()
    add_navigator = ("Insert INTO navigator"
                    "(lastName, firstName)"
                    " VALUES (%s, %s)")
    data_navigator = (lastName, firstName)
    cursor.execute(add_navigator, data_navigator)
    server.cnx.commit()
    server.cnx.close()
    return 'success'



def put_navigator():
    """updates a navigator in the DB and returns the updated object"""
    return server.err_out(500, "not implemented")


def delete_navigator():
    """deletes a navigator in the DB and returns the deleted object"""
    return server.err_out(500, "not implemented")
