# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 09:15:17 2016

@author: zzq
"""

from A06_Module_G20525987_Q2 import *

import argparse as ap
def Main():
    
    MLP = ap.ArgumentParser()
    MLP.add_argument("-d",dest="database",action='store', help=" The optimal value and the decision variables and their values")
    MLP.add_argument('-t', dest='outfile', action='store', help='output file') 

    
    myArgs = MLP.parse_args()
    
    file_name = getFileNames()
    mylp = readAndStore(file_name)
    list = []
    index = ['name','optval']
    
     
    if (myArgs.outfile and myArgs.database):
        for i in mylp:
            model = createandSolveLP(i)
            obj = [model['problemName'],model['objective']]
            list.append(dict(zip(index,obj)))
            writeFile(myArgs.outfile,model)
            print('The optimal value for %s is %.3f'%(model['problemName'],model['objective']))

        print('Output being sent to table: %s in the LP database'%myArgs.database)
        writeDatabase(myArgs.database,list)
        print('Output written to table: %s in the LP database'%myArgs.database)
        
        print('Output being sent to file: %s'%myArgs.outfile)
        print('Output written to file: %s'%myArgs.outfile)

    elif myArgs.database: #database option 
        for i in mylp:
            model = createandSolveLP(i)
            obj = [model['problemName'],model['objective']]
            list.append(dict(zip(index,obj)))
            print('The optimal value for %s is %.3f'%(model['problemName'],model['objective']))
        
        print('Output being sent to table: %s in the LP database'%myArgs.database)
        print('Output written to table: %s in the LP database'%myArgs.database)

    elif myArgs.outfile: #table option
        for i in mylp:
            model = createandSolveLP(i)
            writeFile(myArgs.outfile,model)
            print('The optimal value for %s is %.3f'%(model['problemName'],model['objective']))

        print('Output being sent to file: %s'%myArgs.outfile)
        print('Output written to file: %s'%myArgs.outfile)
    
    
        
    else: #default output
        file_name = getFileNames()
        mylp = readAndStore(file_name)
        list = []
        index = ['name','optval']

        for i in mylp:
            model = createandSolveLP(i)
            print('The optimal value for %s is %.3f'%(model['problemName'],model['objective']))
        
if __name__ == "__main__":
    Main()
