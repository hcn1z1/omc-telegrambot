import os
import time
import sqlite3

def zipdir(path, ziph):
    """
    Zip a folder with python
    note: code copied from stackoverflow
    """
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

def timeline(message_id,database=False):
    seconds = time.time()
    local_time = time.ctime(seconds)
    local_time = " ".join(local_time.split(" ")[::-1])
    if database is False:log = f"id : {message_id} [{local_time}]\n"
    else:log = f"id : {message_id} [{local_time}] database sent ! \n"
    logs = open("logs/logs.txt","a+")
    logs.write(log)
    logs.close()

def getAdmins():
    """
    :return: list
    get Admins list from database
    """
    db = sqlite3.connect("database/database.db")
    cursor = db.cursor()
    # todo: make this function work
    # source: your ipython sheet xD
    cursor.execute("SELECT * FROM ADMINS")
    admins = cursor.fetchall()

    return admins

def getProjects():
    """
    :return: list
    get all project's names from database
    """
    db = sqlite3.connect("database/database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    
    return projects

def getDatabase():
    """
    return content of database
    """
    file = open("database/database.db","rb")
    return file.read()
