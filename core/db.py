import sqlite3
from sqlite3 import IntegrityError

def getProviderFromDb(carrier):
    with sqlite3.connect("database/database.db",check_same_thread=False) as DB:
        CURSOR = DB.cursor()
        CURSOR.execute(f"SELECT * FROM CARRIERS WHERE areacode={carrier[0:3]} AND carrier={carrier[3:6]}")
        data = CURSOR.fetchone()
        DB.commit()
        if type(data) is tuple:return data[2]
        else:return None

def addAdmin(id,name) -> bool:
    DB = sqlite3.connect("database/database.db",check_same_thread=False)
    CURSOR = DB.cursor()
    try:
        CURSOR.execute(f"INSERT INTO ADMINS VALUES ('{id}','{name}')")
        DB.commit()
        return True
    except IntegrityError:
        return False
    DB.close()

def addMember(id,name) -> bool:
    DB = sqlite3.connect("database/database.db",check_same_thread=False)
    CURSOR = DB.cursor()
    try:
        CURSOR.execute(f"INSERT INTO Members VALUES ('{id}','{name}',0)")
        DB.commit()
        return True
    except IntegrityError:
        return False
    DB.close()

def deleteAdmin(id) -> bool:
    DB = sqlite3.connect("database/database.db",check_same_thread=False)
    CURSOR = DB.cursor()
    try:
        CURSOR.execute(f"DELETE FROM ADMINS WHERE id={id}")
        DB.commit()
        return True
    except IntegrityError:
        return False


def deleteMember(id) -> bool:
    DB = sqlite3.connect("database/database.db",check_same_thread=False)
    CURSOR = DB.cursor()
    try:
        CURSOR.execute(f"DELETE FROM Members WHERE id={id}")
        DB.commit()
        return True
    except IntegrityError:
        return False

def checkIfAdmin(id)-> bool:
    with sqlite3.connect("database/database.db",check_same_thread=False) as DB:
        CURSOR = DB.cursor()
        CURSOR.execute(f"SELECT * FROM ADMINS WHERE id={id}")
        data = CURSOR.fetchone()
        DB.commit()
        if type(data) is tuple:return True
        else:return False

def checkIfMember(id)->  bool:
    with sqlite3.connect("database/database.db",check_same_thread=False) as DB:
        CURSOR = DB.cursor()
        CURSOR.execute(f"SELECT * FROM Members WHERE id={id}")
        data = CURSOR.fetchone()
        DB.commit()
        if type(data) is tuple:return True
        else:return False

def checkIfMemberAintUsingTool(id)->  bool:
    with sqlite3.connect("database/database.db",check_same_thread=False) as DB:
        CURSOR = DB.cursor()
        CURSOR.execute(f"SELECT * FROM Members WHERE id={id}")
        data = CURSOR.fetchone()
        DB.commit()
        if data[2] == 0:return True
        else:return False

def updateMemberStatus(id,status:int)->None:
    DB = sqlite3.connect("database/database.db",check_same_thread=False)
    CURSOR = DB.cursor()
    try:
        CURSOR.execute(f"UPDATE Members SET status={status} WHERE id='{id}'")
        DB.commit()
        return True
    except:
        return False
    DB.close()


class postProviderIntoDb:
    def __init__(self):
        pass
    def post(self,carrier,provider="ATT"):
        DB = sqlite3.connect("database/database.db",check_same_thread=False)
        CURSOR = DB.cursor()
        try:
            CURSOR.execute(f"INSERT INTO CARRIERS VALUES ({int(carrier[0:3])},{int(carrier[3:6])},'{provider}')")
            DB.commit()
        except IntegrityError:
            print("Unique Code Error")
        DB.close()