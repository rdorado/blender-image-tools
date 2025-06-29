from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

connection_string = "mysql+mysqlconnector://root:secret@localhost:3306/store"
engine = create_engine(connection_string, echo = True)
#meta = MetaData(engine)
Session = sessionmaker(bind=engine)
#db = declarative_base()
#Base = declarative_base()

class Base(DeclarativeBase):
    pass

class BlenderAsset(Base):
    __tablename__ = "asset"

    id = Column(Integer, primary_key = True)
    name = Column(String(255))
    filename = Column(String(255))

    def __str__(self):
        return str(self.id)+" "+self.name+" "+self.filename




#Base.metadata.create_all(engine)
#Base.metadata.drop_all(engine)



with Session() as session:
    obj = BlenderAsset(name="test", filename="filename.blend")
    session.add(obj)
    session.commit()
    session.refresh(obj)




with Session() as session:

   todos_query = session.query(BlenderAsset)
   #done_todos_query = todos_query.filter(Student.is_done==True)
   result = todos_query.all()

   for row in result:
      print (row)












'''
students = Table(
   'students', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String(255)), 
   Column('lastname', String(255)),
)
'''

#connection = engine.connect()
# Inserts one
#ins = students.insert().values(name = 'Ravi', lastname = 'Kapoor')
#result = connection.execute(ins)

#stmt = students.insert().values(name = 'Ravi', lastname = 'Kapoor')
#with engine.connect() as conn:
#    result = conn.execute(stmt)
#    conn.commit()

# Inserts several
"""
connection.execute(students.insert(), [
   {'name':'Rajiv', 'lastname' : 'Khanna'},
   {'name':'Komal','lastname' : 'Bhandari'},
   {'name':'Abdul','lastname' : 'Sattar'},
   {'name':'Priya','lastname' : 'Rajhans'},
])
"""

#engine = create_engine(url)

'''
# Selects:
#sql = "SELECT * FROM students"
s = students.select()
connection = engine.connect()
result = connection.execute(s)
#result = connection.execute(sql) 

#print(result.count())
for row in result:
   print (row)
'''