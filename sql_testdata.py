import sqlqueries 
from nose_parameterized import param

# for test_pull
pull_keys = ["mine", "orebody","level","stopename"]
values={"mine":'hello',"orebody":'eating',
"level":'arste', "stopename":"tasrt"}
values2={"mine":'hello2',"orebody":'eating',
"level":'arste', "stopename":"tasrt2"}

                # param(query,keys,expected,bindings=None)
test_push_data= [ param(sqlqueries.select_header, pull_keys, values, bindings=values),
                  param(sqlqueries.select_header, pull_keys, values2, bindings=values2)
                    ]
                # param(query,keys,expected,bindings=None)
test_pull_data= [ param(sqlqueries.select_header, pull_keys, [values], bindings=values),
                  param(sqlqueries.select_header, pull_keys, [values2], bindings=values2)
                  ]
