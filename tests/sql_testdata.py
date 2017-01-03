import sqlqueries 
import db_template
from nose_parameterized import param

#HEADER table
pull_keys = ["mine", "orebody","level","stopename"]
values=db_template.iterKeys(1,pull_keys)
values2=db_template.iterKeys(2,pull_keys)
#test partial select queries for open dialog
partial = {'mine':'hello', 'orebody':None, 'level':None, 'stopename':None}
            # param(quer, expected,bindings=None)
push_data= [ param(sqlqueries.header_insert,False, bindings=values),
             param(sqlqueries.header_insert,False, bindings=values2)
                    ]
            # param(query,keys,expected,bindings=None)
pull_data= [ param(sqlqueries.header_select, [values], bindings=values, pull_keys=pull_keys),
             param(sqlqueries.header_select, [values2], bindings=values2,pull_keys =pull_keys),
                  ]

#SHAPE TABLE
shape_select_data =[]
for id in range(0,2):
    values =db_template.gen_shape_row(id)
    values = { key:str(val) for key,val in values.iteritems()}
    shape_select_data.append((id,values,values))

shape_insert_data= []
for id in range(9,11):
    values=db_template.gen_shape_row(id) 
    values = { key:str(val) for key,val in values.iteritems()}
    shape_insert_data.append((id,values,True))

critical_JSQ_loaddata=[]
for x in range(5,6):
    JSvalues = db_template.gen_criticaljs_row(x)
    Qvalues =db_template.gen_Q_row(x)
    allvalues ={}
    allvalues.update(JSvalues)
    allvalues.update(Qvalues)
    critical_JSQ_loaddata.append((x,JSvalues,Qvalues,allvalues))

critical_JSQ_savedata=[]
for x in range(11,14):
    JSvalues = db_template.gen_criticaljs_row(x)
    Qvalues =db_template.gen_Q_row(x)
    allvalues ={}
    allvalues.update(JSvalues)
    allvalues.update(Qvalues)
    critical_JSQ_savedata.append((x,JSvalues,Qvalues,True))
