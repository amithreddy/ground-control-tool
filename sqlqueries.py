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
criticalJS_schema= """
                CREATE TABLE IF NOT EXISTS criticaljs(
                    id INTEGER PRIMARY KEY, 
                    backdip CHAR NOT NULL, backdirection CHAR NOT NULL, 
                            backworstcase CHAR NOT NULL, backexamineface CHAR NOT NULL,
                    southdip CHAR NOT NULL, southdirection CHAR NOT NULL,
                            southworstcase CHAR NOT NULL, southexamineface CHAR NOT NULL,
                    northdip CHAR NOT NULL, northdirection CHAR NOT NULL,
                            northworstcase CHAR NOT NULL, northexamineface CHAR NOT NULL,
                    eastdip CHAR NOT NULL, eastdirection CHAR NOT NULL,
                            eastworstcase CHAR NOT NULL, eastexamineface CHAR NOT NULL,
                    westdip CHAR NOT NULL, westdirection CHAR NOT NULL,
                            westworstcase CHAR NOT NULL, westexamineface CHAR NOT NULL,
                    FOREIGN KEY(id) REFERENCES header(id)
                    )
                """
Q_schema = """
        CREATE TABLE IF NOT EXISTS Q(
            /* walls are identified by their direction*/
            id INTEGER PRIMARY KEY, 
            back CHAR NOT NULL, south CHAR NOT NULL,
            east CHAR NOT NULL, west CHAR NOT NULL,
            minimum CHAR NOT NULL,
            most_likely CHAR NOT NULL, maximum CHAR NOT NULL,
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
                    AND level=coalesce(:level,level)
                    """
#accessing shape table
shape_select = "SELECT * FROM shape where id = :id"
shape_insert= "INSERT OR REPLACE INTO shape (id,b1,b2,b3,b4,t1,t2,t3,t4) \
                VALUES(:id,:b1,:b2,:b3,:b4,:t1,:t2,:t3,:t4)"

#accessing critical table
criticalJS_select = "Select * FROM criticaljs WHERE id =:id"
criticalJS_insert =  """
                INSERT OR REPLACE INTO criticaljs(
                    id,backdip, backdirection, backworstcase, backexamineface,
                    southdip, southdirection,southworstcase, southexamineface,
                    northdip, northdirection, northworstcase, northexamineface,
                    eastdip, eastdirection, eastworstcase, eastexamineface,
                    westdip, westdirection, westworstcase, westexamineface
                    )
                VALUES(
                    :id,:backdip, :backdirection, :backworstcase, :backexamineface,
                    :southdip, :southdirection,:southworstcase, :southexamineface,
                    :northdip, :northdirection, :northworstcase, :northexamineface,
                    :eastdip, :eastdirection, :eastworstcase, :eastexamineface,
                    :westdip, :westdirection, :westworstcase, :westexamineface
                    )
                """

Q_select = "Select * FROM Q WHERE id =:id"
Q_Insert = """
        CREATE TABLE IF NOT EXISTS Q(
            id, back, south,east, west,minimum, most_likely, maximum)
        VALUES(
            :id, :back, :south,:east, :west,:minimum, :most_likely, :maximum)
        """
