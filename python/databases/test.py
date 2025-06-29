import sqlite3

con = sqlite3.connect("tutorial.db")

cur = con.cursor()

#cur.execute("CREATE TABLE movie(title, year, score)")

cur.execute("CREATE TABLE asset(id, name, json)")
cur.execute("CREATE TABLE layout(id, name)")
cur.execute("CREATE TABLE printable_object(id, name)")

cur.execute("CREATE TABLE asset_layout(id, name)")


res = cur.execute("SELECT name FROM sqlite_master")
resp = res.fetchone()

print(resp)



"face":
   "tblr": "0, 100, 0, 60",
   "subcomponents":
      "eye": "20, 25, 20, 30",
         "mirror-vertical": "20, 70"
      "nose":
      "mouth": "30, "
      
"person":
   "face"
   "body"

asset_layout


assets:

"picture":
    "tblr":"0,0, "
    "sq"