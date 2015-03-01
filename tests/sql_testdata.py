import sqlqueries 
import db_template
from nose_parameterized import param

#HEADER table
pull_keys = ["mine", "orebody","level","stopename"]
values={"mine":'mine1',"orebody":'orebody1',
"level":'level1', "stopename":"stopename1"}
values2={"mine":'mine2',"orebody":'orebody2',
"level":'level2', "stopename":"stopename2"}
partial = {'mine':'hello', 'orebody':None, 'level':None, 'stopename':None}
            # param(quer, expected,bindings=None)
push_data= [ param(sqlqueries.insert_header,False, bindings=values),
             param(sqlqueries.insert_header,False, bindings=values2)
                    ]
            # param(query,keys,expected,bindings=None)
pull_data= [ param(sqlqueries.select_header, [values], bindings=values, pull_keys=pull_keys),
             param(sqlqueries.select_header, [values2], bindings=values2,pull_keys =pull_keys),
                  ]

#SHAPE TABLE
shape_keys= ['b1','b2','b3','b4','t1','t2','t3','t4']
shape_select_data =[]
for id in range(0,2):
    values =db_template.select_shape(id)
    shape_select_data.append((id,values,values))

shape_insert_data= []
for id in range(9,11):
    values=db_template.insert_shape(id) 
    shape_insert_data.append((id,values,True))
