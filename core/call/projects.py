from http import server
import sqlite3
from sqlite3 import IntegrityError
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv
from core.db import *
from smtplib import SMTP
import email.message as message

load_dotenv
imageEnds = [".jpg",".png",".jpeg",".gif"]

def sendEmail(projectName:str,messageId:str,username:str):
    """
    :return: NULL
    description !
    Sending a Joining request through email
    """
    
    server = SMTP(os.getenv("SMTPSERVER"),os.getenv("SMTPPORT"))
    server.ehlo()
    _username = os.getenv("SMTPUSERNAME")
    _sender = os.getenv("SMTPSENDERNAME")
    if __convertToBoolean(os.getenv("SMTPTSL")):
        server.starttls()
    rapport = open("database/reportsample.txt")
    rapport = rapport.replace("{messageId}",messageId)
    rapport = rapport.replace("{projectName}",projectName)
    rapport = rapport.replace("{username}",username)
    if bool(_sender): _sender = f"OMC Telegram Bot <{_sender}>"
    else: _sender = f"OMC Telegram Bot <{_username}>"

    #setting MIME
    msg = message()
    msg["From"] = _sender
    msg["To"] = os.getenv("EMAILRECEIVER")
    msg["Subject"] = "Request to Join a Project"
    msg.add_alternative(rapport,"text")

    # logging in to smtp
    server.login(_username,os.getenv("SMTPPASSWORD"))
    server.sendmail(msg["From"],msg["To"],msg.as_string())

def __convertToBoolean(prop:int):
    if prop == 0: return False
    elif prop == 1: return True

def __convertToInteger(prop:bool):
    if prop: return 1
    else: return 0

def addProject(name:str,path:str,projectManager:str,members:int,requirement:bool,stage:int,lastestStage:int):
    with sqlite3.connect("database/database.db") as database:
        cursor = database.cursor()
        try:
            cursor.execute(f"INSERT INTO project VALUES ('{name}','{path}','{projectManager}',{members},{__convertToInteger(requirement)},{stage},{lastestStage}")
        except Exception as e:
            print(e)
            # ps if u reading my code, aint doing this shit

def __getPicture(path= "/"):
    
    "get pictures path and name"
    
    images = []
    files = os.listdir(path)
    for file in files:
        for _format in imageEnds:
            if _format in file:
                images.append(f'{path}/{file}')
    
    return images

def __getDescription(path = "/"):
    "get README.md (shall contain description)"

    return open(f"{path}/README.md").read()

def getProjectInformations(projectName:str):
    with sqlite3.connect("database/database.db") as database:
        cursor = database.cursor()
        try:
            cursor.execute(f"SELECT * FROM projects WHERE project='{projectName}'")
            projectData = cursor.fetchone()
            project = {
                "name": projectData[0],
                "pics": __getPicture(projectData[1]),
                "description": __getDescription(projectData[1]),
                "projectManager": projectData[2],
                "members": projectData[3],
                "requirement": __convertToBoolean(projectData[4]),
                "stage":projectData[5],
                "latestStage":projectData[6]
            }

            return project
        except IntegrityError:
            return "couldn't export data !"
def setNewProjectFromTelegram(project:list):
    with sqlite3.connect("database/database.db") as database:
        cursor = database.cursor()
        try:
            cursor.execute("INSERT INTO projects VALUES ('{0}','{1}','{2}',{3},{4},{5},{6})".format(project[0],project[1],project[2],project[3],project[4],project[5],project[6]))
            database.commit()
            return 1
        except Exception as e:
            return 0
def genProjectMarkup(message:object,projects:list):
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    for project in projects:
        markup.add(InlineKeyboardButton(project, callback_data=project))

    return markup
def genMarkup(message:object,projectName):
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("Join Now !", callback_data="Join projectName"))

    return markup

def sendProjectInformations(message:object,bot:object,project:dict):
    messageId = message.from_user.id
    """
    todo: send pictures
    todo: send email if someone wanna join
    """

    description = f"""name: {project["name"]}
managed by: {project["projectManager"]}
members: {project["name"]}
state : {project["stage"]}/{project["latestStage"]} !

{project["description"]}
    """

    for pic in project["pics"]:
        bot.send_photo(messageId,open(pic,"rb").read())
    
    bot.send_message(messageId,description)
    
    if project["requirement"]:
        print("here requirement")
        bot.send_message(messageId,"Requirement is open",reply_markup=genMarkup(message,project["name"]))
