import sqlqueries
import main
name = 'generateddb'
dbac = main.sqldb(name)

#populate the headertable 
keys= ['mine', 'orebody','level','stopename']
for x in range(0,20):
    dbac.query_db(sqlqueries.insert_header,
        bindings={key:key+str(x) for key in keys
                        })
