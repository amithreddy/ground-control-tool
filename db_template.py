from sqlqueries import *
from main import sqldb
import shutil
name = 'generateddb'
dbac = sqldb(name)

#populate the headertable 
keys= ['mine', 'orebody','level','stopename']
for x in range(0,20):
    dbac.query_db(insert_header,
        bindings={key:key+str(x) for key in keys
                        })
shutil.move('generateddb','tests/')
