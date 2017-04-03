
def getFileNames():
    """
    Input = name of JSON file
    Returns = JSON object
    """
    import os
    included_extenstions = [ 'json' ] ;
    file_names = [fn for fn in os.listdir(os.getcwd())
    if any([fn.endswith(ext)
    for ext in included_extenstions])];
    return file_names
    
def readAndStore(file_name):
    import pymongo
    import os
    # Connecting to MongoDB
    client = pymongo.MongoClient('localhost:27017')
    db = client['Library']
    collection = db["Json"]
    #Test if the collection exists
    if db.Json.count()!= 0:
        db.Json.drop()
        collection = db["Json"]
    
    import json
    for file in file_name:
        with open(file,'r') as f:
            a = json.load(f)
        db.Json.insert_one(a)
        
    allobj = db.Json.find()
    aobj = list(allobj)
    
    from bson import Binary, Code
    from bson.json_util import dumps
    # import the problem from MongoDB to a json file and then load the data we need
    dumps(a)
    with open('lpproblem.json','w') as f:
        f.write(dumps(aobj))
    with open('lpproblem.json','r') as f:
        mylp = json.load(f)
    # delete the json file
    os.remove('lpproblem.json')
    return mylp
    
def createandSolveLP(LPData):
    """
    Input = JSON object
    Returns = a dictionary with 3 elements
    The first element is the key value pair of the objective function and the value of
    the
    objective function and the second element is a dictionary whose key value pair is
    the
    decision variables and their values and the third element is a the key value pair of the problem name
    """
    import pulp as plp
    if LPData['objective'] == "MIN":
        my_model = plp.LpProblem(LPData['name'], plp.LpMinimize)
    elif LPData['objective'] == "MAX":
        my_model = plp.LpProblem(LPData['name'], plp.LpMaximize)
    else:
        print("error")
        exit(0)
        
    decVars = LPData['variables']
    
    x = plp.LpVariable.dict('x_%s', decVars, lowBound = 0)
    
    objCoeffList = LPData["objCoeffs"]
    objective = dict(zip(decVars, objCoeffList))
    
    my_model += sum([objective[i] * x[i] for i in decVars])
    
    constraintKeys = LPData["LHS"].keys()
    
    for key in constraintKeys:
        LHScoeffs = dict(zip(decVars, LPData["LHS"][key]))
        if LPData["conditions"][key] == '<=':
            my_model += sum([LHScoeffs[j] * x[j] for j in decVars]) <= LPData['RHS'][key]    
        elif LPData["conditions"][key] == '>=':
            my_model += sum([LHScoeffs[j] * x[j] for j in decVars]) >= LPData['RHS'][key] 
        elif LPData["conditions"][key] == '==':
            my_model += sum([LHScoeffs[j] * x[j] for j in decVars]) == LPData['RHS'][key]
        else:
            print ("Problems with constraint {} ".format(key))
            exit(0)
    
    # Solve the problem
    my_model.solve()                
    
    index = []
    result = []
    index.append('objective')
    result.append(plp.value(my_model.objective))
    for v in my_model.variables():
        index.append(v.name)
        result.append(v.varValue)
        model = dict(zip(index, result))
    model['problemName'] = LPData['name']
        
    return model

def writeFile(filename, data) :
    """
    Input = name of output file and the output we will send
    Output = text file with the detailed output or error message if the write
    operation was unsuccessful
    """
    
    a = data['objective']
    
    try:
        with open(filename,'a') as f: #Use 'a'(append mode) to conduct Loop
            f.write("The optimal value is %.2f"%a+'\n'+"The decision variables and their values are:"+"\n")
            for each in data:
                if each != 'objective':
                    f.write("%s:%s\n"%(each,data[each]))
    except:
        print('Error when writing output to the file.')

    
def writeDatabase(tablename,list):
    """
    Input = name of output table and the output we will send
    Output = SQL table in LP database with the brief output
    """
    
    import pymysql as myDB
    
    conn = myDB.connect('localhost', 'root', 'hero15ab') 
    cursor = conn.cursor()
    
    sql = ' SHOW DATABASES; '
    cursor.execute(sql)
    
    # Check if the database already exists
    sql = ' DROP DATABASE IF EXISTS LP; ' 
    cursor.execute(sql)
    
    # Check if the table already exists
    sql = ' CREATE DATABASE LP; ' 
    cursor.execute(sql)

    sql = ' USE LP; ' 
    cursor.execute(sql)

    sql = '''
            DROP TABLE if exists %s;
            CREATE TABLE %s (
            problemName CHAR (20),
            optimalValue CHAR (20)
            );
          '''%(tablename,tablename)
    cursor.execute(sql)
    for dic in list:
        sql = '''
                INSERT INTO %s (problemName,optimalValue) VALUES ("%s",%.3f);
              '''%(tablename,dic['name'],dic['optval'])
   
        cursor.execute(sql)
        conn.commit()
    
    conn.close()

