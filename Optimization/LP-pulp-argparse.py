# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 09:11:22 2016

@author: zzq
"""

from A06_Module_G20525987_Q1 import *

import argparse as ap
def Main():
    
    MLP = ap.ArgumentParser()
    MLP.add_argument("fname", help="The filename you want to read", type = str)
    MLP.add_argument("-b","--brief",action='store_true',help="The optimal value ")
    MLP.add_argument("-d","--detailed",action='store_true',help=" The optimal value and the decision variables and their values")
    MLP.add_argument('-o', dest='outfile', action='store', help='output file') 
    
    
    myArgs = MLP.parse_args()
    
    mylp = readLPData(myArgs.fname)
    model = createandSolveLP(mylp)

    a = mylp['objective']
    b0 = model['objective']  
    
    if (myArgs.outfile and myArgs.detailed):
        print ("The %s value is %.3f"%(a,b0))
        print ("The decision variables and their values are:")
        for ad in model:  
            if ad != 'objective':
                print(ad,":",model[ad])
  
        writeFile(myArgs.outfile,model)  
    elif myArgs.brief: #brief option                                                                 
        print (b0)       

    elif myArgs.detailed: #detailed option                                                                  
        print ("The %s value is %.3f"%(a,b0))
        print ("The decision variables and their values are:")
        for ad in model:  
            if ad != 'objective':
                print(ad,":",model[ad])

    elif myArgs.outfile:
        writeFile(myArgs.outfile,model)   
  
    else: #default output
        print('The optimal value is %.3f'%(b0))

if __name__ == "__main__":
    Main()

         
