import sqlite3
import sys
import json

DBNAME = "assets.db"
OBJECT_TABLE_NAME = "object"
ASSET_TABLE_NAME = "asset"

def create_database():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE {OBJECT_TABLE_NAME}(name, json)")
    cur.execute(f"CREATE TABLE {ASSET_TABLE_NAME}(name, json)")

def insert_object(name, json):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(f"INSERT INTO {OBJECT_TABLE_NAME}(name, json) VALUES(?,?)", [name, json])
    con.commit()

def select_objects():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {OBJECT_TABLE_NAME}")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def select_objects_names():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(f"SELECT rowid, name FROM {OBJECT_TABLE_NAME}")
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append({"id":row[0], "name":row[1]})
    return result

def select_object_by_id(objid):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(f"SELECT rowid, * FROM {OBJECT_TABLE_NAME} WHERE rowid = ?", str(objid))
    row = cur.fetchone()
    if row:
        return {"rowid": row[0], "name": row[1], "content": json.loads(row[2])}
    return None

def insert_asset(name, json):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    print(name, json)
    print(f"INSERT INTO {ASSET_TABLE_NAME}(name, json) VALUES(?,?)")
    cur.execute(f"INSERT INTO {ASSET_TABLE_NAME}(name, json) VALUES(?,?)", [name, json])
    con.commit()

def select_assets_names():
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(f"SELECT rowid, name FROM {ASSET_TABLE_NAME}")
    rows = cur.fetchall()
    result = []
    for row in rows:
        result.append({"id":row[0], "name":row[1]})
    return result
    
def select_asset_by_id(assetid):
    con = sqlite3.connect(DBNAME)
    cur = con.cursor()
    cur.execute(f"SELECT rowid, * FROM {ASSET_TABLE_NAME} WHERE rowid = ?", str(assetid))
    row = cur.fetchone()
    if row:
        return {"rowid": row[0], "name": row[1], "content": json.loads(row[2])}
    return None

def main() -> int:
    """Echo the input arguments to standard output"""
    create_database()
    insert_object('triangle1', '[{"name": "s1", "outer": [[40,40],[50,55],[30,55]], "holes":[]}]')
    insert_object('triangle2', '[{"name": "s1", "outer": [[50,10],[90,50],[10,50]], "holes":[[[50,20],[75,45],[25,45]]]}]')
    insert_object('triangle3', '[{"name": "s1", "outer": [[50,10],[90,50],[10,50]], "holes":[[[50,20],[75,45],[25,45]]]},{"name": "s1", "outer": [[50,30],[60,40],[40,40]], "holes":[]}]')
    #select_pobjects()
    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit