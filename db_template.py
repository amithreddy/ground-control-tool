import sqlqueries 
from main import sqldb
import shutil,os
import nose.tools
import itertools
#populate the headertable 
def gen_header_row(x):
    header_keys= sqlqueries.header_keys
    return iterKeys(x,sqlqueries.header_keys)

def iterKeys(x,keys,numonly=False):
    if numonly is True:
        return {key:str(x) for key in keys}
    return {key:key+str(x) for key in keys}

#populate the shapetable
def gen_shape_row(x):
    shape_keys=sqlqueries.shape_keys
    return iterKeys(x,shape_keys,numonly=True)

#populate the critical js table
def gen_criticaljs_row(x):
    criticaljs_keys= sqlqueries.criticaljs_keys
    return iterKeys(x,criticaljs_keys,numonly=True)

#populate the Q table
def gen_Q_row(x): 
    Q_keys=sqlqueries.Q_keys
    return iterKeys(x,Q_keys,numonly=True)

def populate(db,query,gen,rang,id=True):
    for x in range(0,rang):
        values = gen(x)
        if id is True:
            values['id']=str(x)
        success=db.query_db(query,bindings=values)

def gen_cube(origin,indict=True):
    x,y,z=0,1,2
    vertices = []
    vertices.append(origin) #t1
    vertices.append((origin[x],origin[y]+1,origin[z]))#t2
    vertices.append((origin[x]+1,origin[y]+1,origin[z]))#t3
    vertices.append((origin[x]+1,origin[y],origin[z]))#t4
    for vert in itertools.islice(vertices,0,4,1):
        vertices.append((vert[x],vert[y],vert[z]+1))
    if indict is True:
        verticesdict = {}
        untuplized =[]
        for point in vertices:
            for d in point:
                untuplized.append(d)
        keys = sqlqueries.shape_keys
        
        assert len(untuplized) == len(keys)
        for index, key in enumerate(keys):
            verticesdict[key] = untuplized[index]
        return verticesdict
    else:
        return vertices
#populate the FactorAtable
def gen_FactorA_row(x):
    FactorA_keys= sqlqueries.FactorA_keys
    return iterKeys(x,FactorA_keys,numonly=True)

def gen_FactorB_row(x):
    FactorB_keys= sqlqueries.FactorB_keys
    return iterKeys(x,FactorB_keys,numonly=True)

def gen_StabilityNumber_row(x):
    StabilityNumber_keys= sqlqueries.StabilityNumber_keys
    return iterKeys(x,StabilityNumber_keys,numonly=True)
def main():
    name = 'generateddb'
    try:
        os.remove(name)
    except OSError:
        pass
    db = sqldb(name)
    rang =10
    populate(db,sqlqueries.header_insert,gen_header_row,15,id=False)
    populate(db,sqlqueries.shape_insert,gen_shape_row,rang)
    populate(db,sqlqueries.criticalJS_insert,gen_criticaljs_row,rang)
    populate(db,sqlqueries.Q_insert,gen_Q_row,rang)
    populate(db,sqlqueries.FactorA_insert, gen_FactorA_row,rang)
    populate(db,sqlqueries.FactorB_insert, gen_FactorB_row,rang)
    populate(db,sqlqueries.StabilityNumber_insert, gen_StabilityNumber_row,rang)
    try:
        shutil.move('generateddb','tests/')
    except shutil.Error:
        os.remove('tests/generateddb')
        shutil.move('generateddb','tests/')
if __name__ =="__main__":
    main()
