insert_header= "INSERT INTO HEADER ( mine, orebody, level, stopename) \
        VALUES(:mine, :orebody, :level, :stopename)"

"""   
coalesce function will first return non-null value, so when a
value is provided forr a parameter it is used in the comparison
operation. When a value is not supplied for a parameter, the current column value is used. A column value always equals itself, which
causes all the rows to be returned for that operation.
"""
select_header= """
                SELECT * FROM HEADER 
                WHERE mine=coalesce(:mine,mine)
                AND orebody=coalesce(:orebody,orebody)
                AND stopename=coalesce(:stopename,stopename) 
                AND level=coalesce(:level,level)
            """
