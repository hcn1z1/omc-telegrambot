from core.db import *
from core.call.projects import addProject, setNewProjectFromTelegram

def add(message,bot):
    info = message.text.split(" ")
    if checkIfAdmin(str(message.chat.id)):
            if "admin" == info[1]:
                admin = addAdmin(info[2],info[3])
                if admin is True:
                    bot.send_message(message.chat.id,"A new Admin have been added !")
            elif "member" == info[1]:
                member = addMember(info[2],info[3])
                if member is True:
                    bot.send_message(message.chat.id,"A new Member have been added !")   
            else:
                bot.send_message(message.chat.id,"""Wrong pattern used 
Use the following syntax:
'add member 1xxxxxxxx @telegramAccount' !""") 

def delete(message,bot):
    info = message.text.split(" ")
    if checkIfAdmin(str(message.chat.id)):
        if "admin" == info[1]:
            admin = deleteAdmin(info[2])
            if admin is True:
                bot.send_message(message.chat.id,"Admin have been deleted !")
        elif "member" == info[1]:
            member = deleteMember(info[2])
            if member is True:
                bot.send_message(message.chat.id,"Member have been deleted !")   
        else:
            bot.send_message(message.chat.id,"""Wrong pattern used 
Use the following syntax:
'delete member 1xxxxxxxx' !""") 
def create(message,bot):
    info = message.text.split(" ")
    if checkIfAdmin(str(message.chat.id)):
        if "project" == info[1]:
            allValues = message.text.replace(")","").split("(")[1].split(",")
            print(allValues)
            response = setNewProjectFromTelegram(allValues)
            if response == 1:bot.send_message(message.chat.id,"project have been added successfully !")
            elif response == 0:bot.send_message(message.chat.id,"couldn't add project !")


def make(message,bot):
    info = message.text.split(" ")
    teleId = info[1]
    status = int(info[2].split("=")[1])
    updateMemberStatus(teleId,status=status)
    bot.send_message(message.chat.id,f"status have been updated for user {teleId}")