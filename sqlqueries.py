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
            rockback CHAR NOT NULL, rocknorth CHAR NOT NULL,
            rocksouth CHAR NOT NULL,rockeast CHAR NOT NULL, rockwest CHAR NOT NULL,
            q_minimum CHAR NOT NULL,
            q_most_likely CHAR NOT NULL, q_maximum CHAR NOT NULL,
            FOREIGN KEY(id) REFERENCES header(id)
            )
        """
FactorA_schema = """
        CREATE TABLE IF NOT EXISTS factorA(
            id INTEGER PRIMARY KEY,
            backmpa CHAR NOT NULL, backucs CHAR NOT NULL, backfactorA CHAR NOT NULL,  
            northmpa CHAR NOT NULL, northucs CHAR NOT NULL, northfactorA CHAR NOT NULL,  
            southmpa CHAR NOT NULL, southucs CHAR NOT NULL, southfactorA CHAR NOT NULL,  
            eastmpa CHAR NOT NULL, eastucs CHAR NOT NULL, eastfactorA CHAR NOT NULL,  
            westmpa CHAR NOT NULL, westucs CHAR NOT NULL, westfactorA CHAR NOT NULL, 
            FOREIGN KEY(id) REFERENCES header(id)
            )
        """
FactorB_schema = """
        CREATE TABLE IF NOT EXISTS factorB(
            id INTEGER PRIMARY KEY,
            back CHAR NOT NULL,
            north CHAR NOT NULL,
            south CHAR NOT NULL,
            east CHAR NOT NULL,
            west CHAR NOT NULL,
            FOREIGN KEY(id) REFERENCES header(id)
            )
        """
FactorB_insert ="INSERT OR REPLACE into factorB(id,back,north,south,east,west)\
                 VALUES(:id,:back,:north,:south,:east,:west)"
FactorB_select ="SELECT * FROM factorB where id = :id"
FactorB_keys = [
            "back",
            "north",
            "south",
            "east",
            "west"]
StabilityNumber_schema = """
        CREATE TABLE IF NOT EXISTS stabilitynumber(
        id INTEGER PRIMARY KEY,
        back CHAR NOT NULL,
        north CHAR NOT NULL,
        south CHAR NOT NULL,
        east CHAR NOT NULL,
        west CHAR NOT NULL
        )
        """
StabilityNumber_keys=['back','north','south','east','west']
StabilityNumber_select="SELECT * FROM shape where id = :id"
StabilityNumber_insert ="INSERT OR REPLACE into stabilitynumber(id,back,north,south,east,west)\
                 VALUES(:id,:back,:north,:south,:east,:west)"
#accessing header table
header_insert= "INSERT INTO HEADER ( mine, orebody, level, stopename) \
                VALUES(:mine, :orebody, :level, :stopename)"
header_insert_update = "REPLACE INTO HEADER (mine, orebody, level, stopename) \
                            VALUES(:mine, :orebody, :level, :stopename)"
header_select= """SELECT * FROM HEADER 
                    WHERE mine=coalesce(:mine,mine)
                    AND orebody=coalesce(:orebody,orebody)
                    AND stopename=coalesce(:stopename,stopename)
                    AND level=coalesce(:level,level)
                    """
header_keys=['mine', 'orebody','level','stopename']
#accessing shape table
shape_select = "SELECT * FROM shape where id = :id"
shape_insert= "INSERT OR REPLACE INTO shape (id,b1,b2,b3,b4,t1,t2,t3,t4) \
                VALUES(:id,:b1,:b2,:b3,:b4,:t1,:t2,:t3,:t4)"
shape_keys = ['b1','b2','b3','b4','t1','t2','t3','t4' ]

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
Q_insert = """
        INSERT OR REPLACE INTO Q(
            id, rockback,rocknorth, rocksouth,rockeast, rockwest, q_minimum, q_most_likely,q_maximum)
        VALUES(
            :id, :rockback, :rocknorth, :rocksouth,:rockeast, :rockwest,:q_minimum, :q_most_likely, :q_maximum)
        """
FactorA_select = "Select * FROM factorA WHERE id =:id"

FactorA_insert = """
        INSERT OR REPLACE INTO factorA(
                id, 
                backmpa,backucs,backfactorA, 
                northmpa,northucs,northfactorA, 
                southmpa,southucs,southfactorA, 
                eastmpa,eastucs,eastfactorA,
                westmpa,westucs,westfactorA)
        VALUES(
                :id, 
                :backmpa,:backucs,:backfactorA, 
                :northmpa,:northucs,:northfactorA, 
                :southmpa,:southucs,:southfactorA, 
                :eastmpa,:eastucs,:eastfactorA,
                :westmpa,:westucs,:westfactorA
                )
        """

Q_keys=["rockback", "rocknorth","rocksouth","rockeast", "rockwest",
                "q_minimum", "q_most_likely", "q_maximum"]
criticaljs_keys=[
                    "backdip", "backdirection", "backworstcase", "backexamineface",
                    "southdip", "southdirection","southworstcase", "southexamineface",
                    "northdip", "northdirection", "northworstcase", "northexamineface",
                    "eastdip", "eastdirection", "eastworstcase", "eastexamineface",
                    "westdip", "westdirection", "westworstcase", "westexamineface"]

FactorA_keys= [
                "backmpa","backucs","backfactorA", 
                "northmpa","northucs","northfactorA", 
                "southmpa","southucs","southfactorA", 
                "eastmpa","eastucs","eastfactorA", 
                "westmpa","westucs","westfactorA", 
            ]





