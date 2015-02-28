from sqlqueries import *
from main import sqldb
import shutil,os
name = 'generateddb'
try:
    os.remove(name)
except OSError:
    pass
db = sqldb(name)

#populate the headertable 
header_keys= ['mine', 'orebody','level','stopename']
for x in range(0,20):
    db.query_db(insert_header,
        bindings={key:key+str(x) for key in header_keys
                        })
shape_keys= ['b1','b2','b3','b4','t1','t2','t3','t4']
for x in range(0,20):
    values= {key:key+str(x) for key in shape_keys}
    values['id']=str(x)
    db.query_db(shape_insert,
            bindings=values)
try:
    shutil.move('generateddb','tests/')
except shutil.Error:
    os.remove('tests/generateddb')
    shutil.move('generateddb','tests/')
