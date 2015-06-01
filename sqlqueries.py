#I dislike how this is set up because any change requries me too do
#three different changes at three different places
criticalJS_schema= """
                CREATE TABLE IF NOT EXISTS criticaljs(
                    id INTEGER PRIMARY KEY, 
                    onedip CHAR NOT NULL, onedirection CHAR NOT NULL, 
                            oneworstcase CHAR NOT NULL, oneexamineface CHAR NOT NULL,
                    twodip CHAR NOT NULL, twodirection CHAR NOT NULL,
                            twoworstcase CHAR NOT NULL, twoexamineface CHAR NOT NULL,
                    threedip CHAR NOT NULL, threedirection CHAR NOT NULL,
                            threeworstcase CHAR NOT NULL, threeexamineface CHAR NOT NULL,
                    fourdip CHAR NOT NULL, fourdirection CHAR NOT NULL,
                            fourworstcase CHAR NOT NULL, fourexamineface CHAR NOT NULL,
                    fivedip CHAR NOT NULL, fivedirection CHAR NOT NULL,
                            fiveworstcase CHAR NOT NULL, fiveexamineface CHAR NOT NULL,
                    FOREIGN KEY(id) REFERENCES header(id)
                    )
                """
criticalJS_keys=[
                    "onedip", "onedirection", "oneworstcase", "oneexamineface",
                    "twodip", "twodirection", "twoworstcase", "twoexamineface",
                    "threedip", "threedirection","threeworstcase", "threeexamineface",
                    "fourdip", "fourdirection", "fourworstcase", "fourexamineface",
                    "fivedip", "fivedirection", "fiveworstcase", "fiveexamineface"]
#accessing critical table
criticalJS_select = "Select * FROM criticaljs WHERE id =:id"
criticalJS_insert =  """
                INSERT OR REPLACE INTO criticaljs(
                    id,onedip, onedirection, oneworstcase, oneexamineface,
                    twodip, twodirection,twoworstcase, twoexamineface,
                    threedip, threedirection, threeworstcase, threeexamineface,
                    fourdip, fourdirection, fourworstcase, fourexamineface,
                    fivedip, fivedirection, fiveworstcase, fiveexamineface
                    )
                VALUES(
                    :id,:onedip, :onedirection, :oneworstcase, :oneexamineface,
                    :twodip, :twodirection,:twoworstcase, :twoexamineface,
                    :threedip, :threedirection, :threeworstcase, :threeexamineface,
                    :fourdip, :fourdirection, :fourworstcase, :fourexamineface,
                    :fivedip, :fivedirection, :fiveworstcase, :fiveexamineface
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
StabilityNumber_select="SELECT * FROM stabilitynumber where id = :id"
StabilityNumber_insert ="INSERT OR REPLACE into stabilitynumber(id,back,north,south,east,west)\
                 VALUES(:id,:back,:north,:south,:east,:west)"

#accessing header table
header_schema="""
            CREATE TABLE IF NOT EXISTS header(
                id INTEGER PRIMARY KEY,
                mine CHAR NOT NULL,
                orebody CHAR NOT NULL,
                level CHAR NOT NULL,
                stopename CHAR NOT NULL UNIQUE
                )
            """

header_insert= "INSERT INTO HEADER (mine, orebody, level, stopename) \
                            VALUES (:mine, :orebody, :level, :stopename)"
header_insert_update = "REPLACE INTO HEADER (mine, orebody, level, stopename) \
                            VALUES(:mine, :orebody, :level, :stopename)" #this has an error I think
header_select= """SELECT * FROM HEADER 
                    WHERE mine=coalesce(:mine,mine)
                    AND orebody=coalesce(:orebody,orebody)
                    AND stopename=coalesce(:stopename,stopename)
                    AND level=coalesce(:level,level)
                    """
header_keys=['mine', 'orebody','level','stopename']
#accessing shape table
shape_schema = """
            CREATE TABLE IF NOT EXISTS shape(
                id INTEGER PRIMARY KEY,
                b1x CHAR NOT NULL, b1y CHAR NOT NULL, b1z CHAR NOT NULL,
                b2x CHAR NOT NULL, b2y CHAR NOT NULL, b2z CHAR NOT NULL,
                b3x CHAR NOT NULL, b3y CHAR NOT NULL, b3z CHAR NOT NULL,
                b4x CHAR NOT NULL, b4y CHAR NOT NULL, b4z CHAR NOT NULL,
                t1x CHAR NOT NULL, t1y CHAR NOT NULL, t1z CHAR NOT NULL,
                t2x CHAR NOT NULL, t2y CHAR NOT NULL, t2z CHAR NOT NULL,
                t3x CHAR NOT NULL, t3y CHAR NOT NULL, t3z CHAR NOT NULL,
                t4x CHAR NOT NULL, t4y CHAR NOT NULL, t4z CHAR NOT NULL,
                FOREIGN KEY(id) REFERENCES header(id)
                    )
            """
shape_select = "SELECT * FROM shape where id = :id"
shape_insert= """INSERT OR REPLACE INTO shape
                (id,
                b1x, b1y, b1z,
                b2x, b2y, b2z,
                b3x, b3y, b3z,
                b4x, b4y, b4z,
                t1x, t1y, t1z,
                t2x, t2y, t2z,
                t3x, t3y, t3z,
                t4x, t4y, t4z)
                VALUES(:id,
                :b1x, :b1y, :b1z,
                :b2x, :b2y, :b2z,
                :b3x, :b3y, :b3z,
                :b4x, :b4y, :b4z,
                :t1x, :t1y, :t1z,
                :t2x, :t2y, :t2z,
                :t3x, :t3y, :t3z,
                :t4x, :t4y, :t4z)"""
shape_keys = [
            "b1x", "b1y", "b1z",
            "b2x", "b2y", "b2z",
            "b3x", "b3y", "b3z",
            "b4x", "b4y", "b4z",
            "t1x", "t1y", "t1z",
            "t2x", "t2y", "t2z",
            "t3x", "t3y", "t3z",
            "t4x", "t4y", "t4z"]

Q_schema = """
        CREATE TABLE IF NOT EXISTS Q(
            /* walls are identified by their direction*/
            id INTEGER PRIMARY KEY, 
            rockback CHAR NOT NULL, rocknorth CHAR NOT NULL,
            rocksouth CHAR NOT NULL,rockeast CHAR NOT NULL, rockwest CHAR NOT NULL,
            FOREIGN KEY(id) REFERENCES header(id)
            )
        """
Q_select = "Select * FROM Q WHERE id =:id"
Q_insert = """
        INSERT OR REPLACE INTO Q(
            id, rockback, rocknorth, rocksouth, rockeast, rockwest)
        VALUES(
            :id, :rockback, :rocknorth, :rocksouth,:rockeast, :rockwest)
        """
Q_keys=["rockback", "rocknorth","rocksouth","rockeast", "rockwest"]

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

FactorA_keys= [
                "backmpa","backucs","backfactorA", 
                "northmpa","northucs","northfactorA", 
                "southmpa","southucs","southfactorA", 
                "eastmpa","eastucs","eastfactorA", 
                "westmpa","westucs","westfactorA", 
            ]





