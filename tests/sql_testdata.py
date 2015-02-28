import sqlqueries 
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
raw = []
for x in range(0,2):
    values= {key:key+str(x) for key in shape_keys}
    raw.append(values)
shape_1, shape_2 =raw

shape_pull_data = [param(1,shape_1,shape_1),
                   param(2,shape_2,shape_2)
        ]
#shape_push_data =[ param([value],bindings=values
#        ]
