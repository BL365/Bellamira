import web
from db_creator import dbCreator

db = web.database(dbn='sqlite', db=dbCreator.dbName)

def getNextId(tableName):
    id = 1
    maxId = db.query('SELECT max(id) FROM '+tableName)[0]['max(id)']
    if maxId != None:
        id = id + maxId
    return id


def getdropValues():
    people = db.select("people", order="FIO")
    dropValue = [(-1, "Add")]
    for p in people:
        dropValue.append((p["id"], p["FIO"]))
    return dropValue