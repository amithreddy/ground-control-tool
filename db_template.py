import sqlqueries 
from main import sqldb
import shutil,os
import nose.tools
#populate the headertable 
def gen_header_row(x):
    header_keys= sqlqueries.header_keys
    return iterKeys(x,sqlqueries.header_keys)

def iterKeys(x,keys):
    return {key:key+str(x) for key in keys}

#populate the shapetable
def gen_shape_row(x):
    shape_keys= ['b1','b2','b3','b4','t1','t2','t3','t4']
    return iterKeys(x,shape_keys)

#populate the critical js table
def gen_criticaljs_row(x):
    criticaljs_keys= sqlqueries.criticaljs_keys
    return iterKeys(x,criticaljs_keys)

#populate the Q table
def gen_Q_row(x): 
    Q_keys=sqlqueries.Q_keys
    return iterKeys(x,Q_keys)

def populate(db,query,gen,rang):
    for x in range(0,rang):
        values = gen(x)
        values['id']=str(x)
        success=db.query_db(query,bindings=values)

#populate the FactorAtable
def gen_FactorA_row(x):
    FactorA_keys= sqlqueries.FactorA_keys
    return iterKeys(x,FactorA_keys)

def main():
    name = 'generateddb'
    try:
        os.remove(name)
    except OSError:
        pass
    db = sqldb(name)
    rang =10
    populate(db,sqlqueries.header_insert,gen_header_row,15)
    populate(db,sqlqueries.shape_insert,gen_shape_row,rang)
    populate(db,sqlqueries.criticalJS_insert,gen_criticaljs_row,rang)
    populate(db,sqlqueries.Q_insert,gen_Q_row,rang)
    populate(db,sqlqueries.FactorA_insert, gen_FactorA_row,rang)
    try:
        shutil.move('generateddb','tests/')
    except shutil.Error:
        os.remove('tests/generateddb')
        shutil.move('generateddb','tests/')
if __name__ =="__main__":
    main()
