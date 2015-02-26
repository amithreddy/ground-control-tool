#create tables
header_schema="""
            CREATE TABLE IF NOT EXISTS header(
                id INTEGER PRIMARY KEY,
                mine CHAR NOT NULL,
                orebody CHAR NOT NULL,
                level CHAR NOT NULL,
                stopename CHAR NOT NULL UNIQUE
                )
            """
shape_schema = """
            CREATE TABLE IF NOT EXISTS shape(
                id INTEGER PRIMARY KEY,
                b1 CHAR NOT NULL,b2 CHAR NOT NULL,b3 CHAR NOT NULL, b4 CHAR NOT NULL,
                t1 CHAR NOT NULL,t2 CHAR NOT NULL,t3 CHAR NOT NULL, t4 CHAR NOT NULL,
                FOREIGN KEY(id) REFERENCES header(id)
                    )
            """
#accessing header table
insert_header= "INSERT INTO HEADER ( mine, orebody, level, stopename) \
                VALUES(:mine, :orebody, :level, :stopename)"
insert_header_update = "REPLACE INTO HEADER (mine, orebody, level, stopename) \
                            VALUES(:mine, :orebody, :level, :stopename)"
select_header= """SELECT * FROM HEADER 
                    WHERE mine=coalesce(:mine,mine)
                    AND orebody=coalesce(:orebody,orebody)
                    AND stopename=coalesce(:stopename,stopename) 
                    AND level=coalesce(:level,level)"""

#accessing shape table
shape_pull = "SELECT * FROM shape where id = :id"
shape_insert= """INSERT or REPLACE INTO shape (ID,b1,b2,b3,b4,t1,t2,t3,t4)
                            WHERE values (  
                            (SELECT ID from Book WHERE ID = :id), :b1,:b2,:b3,:b4, :t1,:t2,:t3,:t4)"""
