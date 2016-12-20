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

def getdropValues2():
    people = db.query('SELECT renters_group.id AS r_id, renters.name || ", " || renters_group.name as name FROM (renters_group Inner Join renters on r_id = renters.id)')
    dropValue = [(-1, "Add")]
    for p in people:
        dropValue.append((p["r_id"], p["name"]))
    return dropValue