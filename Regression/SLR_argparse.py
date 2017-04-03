# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 20:16:27 2016

@author: zzq
"""
from A02_Module_G20525987 import *

import argparse as ap
def Main():
    MLP = ap.ArgumentParser()
    MLP.add_argument("fname", help="The filename you want to read", type = str)
    MLP.add_argument("-b","--brief",action='store_true',help="the coefficients of the regression equation ")
    MLP.add_argument("-v","--verbose",action='store_true',help="the description of the equation and the R**2 value and actual data values with column titles ")
    MLP.add_argument("-p","--plot",action='store_true',help="plot the regression's actual values as an XY plot and the estimated values as a hyperplane")
    MLP.add_argument('-o', dest='outfile', action='store', help='output file') 
    
    
    myArgs = MLP.parse_args()
    
    mydata = fileInput(myArgs.fname)
    myset = regression(mydata)
    mynewdata = mydata.as_matrix() #convert array into matrix as the variable of myPlot Func
    r2= rscore(mydata)
    
    b0=myset[0]
    b1=myset[1]
    b2=myset[2]
    
    item=["The equation is: y = %.4f+%.4f*x1%.4f*x2"%(b0,b1,b2),
         'R-squared: %.4f' % (r2)]
    
    
    if myArgs.brief: #brief option                                                                 
        print ("The coefficient for the regression equation is: b0=%.4f"%(b0),"b1=%.4f"%(b1),"b2=%.4f"%(b2))       
    elif myArgs.verbose: #verbose option                                                                  
        print ("The equation is: y = %.4f+%.4f*x1%.4f*x2"%(b0,b1,b2))
        print ("The R square value is:%4f"%(r2))
        print ("The formatted input data is shown below:",mydata)
    elif myArgs.plot: #option to plot the regression                                                                              
        print (myPlot(mynewdata, myset))  
    else: #default output
        print ('b0:%.4f'%(b0))
        print ('b1:%.4f'%(b1))
        print ('b2:%.4f'%(b2))
        print ('R-squared: %.4f' % (r2))

    if myArgs.outfile:
        with open(myArgs.outfile, 'a') as f:
            f.write(str(mydata)+'\n'+str(item)+'\n')   #store mydata into outfile provided by user

if __name__ == "__main__":
    Main()



