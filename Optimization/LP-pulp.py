# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 20:16:27 2016

@author: zzq
"""

def readLPData(fname):
    """
    Input = name of JSON file
    Returns = JSON object
    """
    
    import json
    try:
        with open(fname,'r') as f:
            LPdata = json.load(f)
        return LPdata
    except:
        return None

import pulp as plp
def createandSolveLP(LPData):
    """
    Input = JSON object
    Returns = a dictionary with 2 elements
    The first element is the key value pair of the objective function and the value of
    the
    objective function and the second element is a dictionary whose key value pair is
    the
    decision variables and their values
    """
    #import contents of json file into pulp problem
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
    
    # Solve the problem using pulp

    my_model.solve()                
    
    index = []
    result = []
    index.append('objective')
    result.append(plp.value(my_model.objective))
    for v in my_model.variables():
        index.append(v.name)
        result.append(v.varValue)
        model = dict(zip(index, result))
 
    return model


def writeFile(filename, data) :
    """
    Input = name of output file
    Output = text file with the detailed output or error message if the write
    operation was unsuccessful
    """
    
    a = data['objective']
    try:
        with open(filename,'a') as f:  #Use 'a'(append mode) to conduct loop
            f.write("The optimal value is %.2f"%a+'\n'+"The decision variables and their values are:"+"\n")
            for each in data:
                if each != 'objective':
                    f.write("%s:%s\n"%(each,data[each]))
        print("Output being sent to file: %s"%filename)
        print("Ouput written to file: %s"%filename)

    except:
        print('Errir when writing output to the file.')
    
    
