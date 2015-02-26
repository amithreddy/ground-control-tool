insert_header= "INSERT INTO HEADER ( mine, orebody, level, stopename) \
                VALUES(:mine, :orebody, :level, :stopename)"
insert_header_update = "REPLACE INTO HEADER (mine, orebody, level, stopename) \
                            VALUES(:mine, :orebody, :level, :stopename)"
"""   
coalesce function will first return non-null value, so when a
value is provided forr a parameter it is used in the comparison
operation. When a value is not supplied for a parameter, the current column value is used. A column value always equals itself, which
causes all the rows to be returned for that operation.
"""
select_header= """SELECT * FROM HEADER 
                    WHERE mine=coalesce(:mine,mine)
                    AND orebody=coalesce(:orebody,orebody)
                    AND stopename=coalesce(:stopename,stopename) 
                    AND level=coalesce(:level,level)"""
# write a query for each possible case

shape_pull = "SELECT * FROM shape where id = :id"
shape_insert= """INSERT or REPLACE INTO shape (ID,b1,b2,b3,b4,t1,t2,t3,t4)
                            WHERE values (  
                            (SELECT ID from Book WHERE ID = :id), :b1,:b2,:b3,:b4, :t1,:t2,:t3,:t4)"""
