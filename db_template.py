from sqlqueries import *
from main import sqldb
import shutil,os

#populate the headertable 
def insert_header(db,id):
    values ={key:key+str(id) for key in header_keys}
    db.query_db(insert_header,
        bindings=values)
    return values
header_keys= ['mine', 'orebody','level','stopename']
def populate_header(db):
    for x in range(0,20):
        insert_header(db,x)

#populate the shapetable
def insert_shape(id):
    shape_keys= ['b1','b2','b3','b4','t1','t2','t3','t4']
    values= {key:key+str(id) for key in shape_keys}
    return values

def select_shape(x):
    shape_keys= ['b1','b2','b3','b4','t1','t2','t3','t4']
    return {key:key+str(x) for key in shape_keys}
def populate_shape(db):
    for x in range(0,10):
        values =insert_shape(x)    
        db.query_db(shape_insert,
            bindings=values)

def main():
    name = 'generateddb'
    try:
        os.remove(name)
    except OSError:
        pass
    db = sqldb(name)
    populate_header(db)
    populate_shape(db)
    try:
        shutil.move('generateddb','tests/')
    except shutil.Error:
        os.remove('tests/generateddb')
        shutil.move('generateddb','tests/')
if __name__ =="__main__":
    main()
