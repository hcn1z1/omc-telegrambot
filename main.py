from json import load
from threading import Thread
from core.db import *
from core.functions import *
from telebot import TeleBot
from core.call.projects import *
from core.call.control import *
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE = postProviderIntoDb()
print(os.getenv("TELEGRAMTOKEN"))
bot = TeleBot(os.getenv("TELEGRAMTOKEN"))


             
@bot.message_handler(commands=["start","help"])
def menu(message):
    menu_ = """
/start          show menu
/member         get your id
/projects       projects list
/admins         admins id's
/credit         credit to the developer
"""
    if checkIfAdmin(message.chat.id):
        menu_ += "/commands       commands for admin"
    bot.send_message(message.chat.id,menu_)

@bot.message_handler(commands=["admins"])
def buyer(message):
    admins = getAdmins()
    bot.send_message(message.chat.id,"""
Contact one of those following sellers to buy the tool.
    """)
    for admin in admins:
        msg = "Admin : "+str(admin[1])
        bot.send_message(message.chat.id,msg)

@bot.message_handler(commands=["projects"])
def projecting(message):
    if checkIfMember(message.chat.id) or checkIfAdmin(message.chat.id):
        messageId = message.chat.id
        projects = [project[0] for project in getProjects()]
        print(projects)
        bot.send_message(messageId,"Projects list :",reply_markup=genProjectMarkup(message,projects))
    else:
        bot.send_message(messageId,"Unfortunately you ain't a member :'( eat some zlabiya and write /member")
    

@bot.message_handler(commands=["member"])
def sendHisId(message):
    bot.send_message(message.chat.id,f"If you are a member of the great Open Minds Club. Please, send this id [{message.chat.id}] to one of the admins !")

@bot.message_handler(commands=["credit"])
def creadit(message):
    bot.send_message(message.chat.id,"this bot have been developped by the great hasni @tools_designer")

@bot.message_handler(commands=["commands"])
def commands(message):
    if checkIfAdmin(message.chat.id):
        menu_ = """
for admins there is several commands to make the bot works perfectly.
this is some commands:

<i>add member </i><b>id username</b>
this command is used for adding a new members.

<i>add admin </i><b>id username</b>
this command is used for adding a new admin.

<i>delete member </i><b>id username</b>
delete an existant member.

<i>make <b>id</b> </i>status=<b>0</b>
when the bot get rebooted please use this for corrupted user (that cant use bot after rebooting)

<i>create <b>project</b> </i><b>(values)</b>
create a project, try /values for more informations

<i>get database</i>
a backup of database"""
        bot.send_message(message.chat.id,menu_,parse_mode="html")

@bot.message_handler(commands=["values"])
def values(message):
    main = """
(project name,path,project manage,members,requirement,status,final status)

project name: a simple <b>string</b>
path: path for the description and images folder
project manager: think
members: <b>integer</b> (number of project members)
requirements: <b>binary</b> (0 for false 1 for true)
status : <b>integer</b> (how much is done of the project)
final status : <b>integer</b> (how much steps do this project needs)

<b>example</b> : create project (zlabiya,projects/uwu,andrew tate TOP G, 7,1,3,5)
PS: <i>bel3ani i ruined the zlabiya joke</i>
    """
    if checkIfAdmin(message.chat.id):
        bot.send_message(message.chat.id,main,parse_mode="html")
@bot.message_handler()
def handler(message):
    info = message.text.split(" ")
    if "add" == info[0]: 
        if checkIfAdmin(str(message.chat.id)):
            add(message,bot)
    elif "delete" == info[0]:
        delete(message,bot)

    elif "get" == info[0] :
        if checkIfAdmin(str(message.chat.id)) and "database"==info[1]:
            bot.send_document(message.chat.id,getDatabase(),caption="Please send this to @tools_designer",visible_file_name="database.db")
            timeline(message.chat.id,database=True)
    elif "make" == info[0]:
        make(message,bot)
    elif "create" == info[0]:
        create(message,bot)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call.data)
    data = call.data
    id = call.id
    username = call.from_user.username
    if "Join" not in data:
        projectInfo = getProjectInformations(data)
        bot.answer_callback_query(call.id, "Wait just few seconds!")
        if type(projectInfo) is not dict:
            bot.send_message(id,"Couldn't fetch this project !")
            return 0
        else:
            sendProjectInformations(call,bot,projectInfo)
            return 1
    else:
        data = data.split(" ")
        bot.answer_callback_query(id, "Success ! Will contact you soon !")
        thread = Thread(target=sendEmail, args=(data[1],call.from_user.id,username))
        thread.start()

bot.infinity_polling()