import sqlqueries 
from nose_parameterized import param

# for test_pull
pull_keys = ["mine", "orebody","level","stopename"]
values={"mine":'hello',"orebody":'eating',
"level":'arste', "stopename":"tasrt"}
values2={"mine":'hello2',"orebody":'eating',
"level":'arste', "stopename":"tasrt2"}

                # param(quer, expected,bindings=None)
push_data= [ param(sqlqueries.insert_header,True, bindings=values),
             param(sqlqueries.insert_header,True, bindings=values2)
                    ]
                # param(query,keys,expected,bindings=None)
pull_data= [ param(sqlqueries.select_header, [values], bindings=values, pull_keys=pull_keys),
                  param(sqlqueries.select_header, [values2], bindings=values2,pull_keys =pull_keys),
                  ]
