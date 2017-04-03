# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 08:50:30 2016

@author: Ziqing Zhu
Gworldid: G20525987

Programming for Analytics Assignment 01: Linear regression
"""

import numpy as np
from pandas import DataFrame

def fileInput(filename):
    """ 
    Input = name of = text file with comma separated numbers 
    Output = numpy array 
    """ 
    df = np.loadtxt(filename,delimiter=',')
    myData = DataFrame(data = df,columns=['y','x1','x2'])
    return myData


def regression(myDataSet):
    """ 
Input = numpy array with three columns 
Column 1 is the dependent variable 
Columns 2 and 3 are the independent variables 
Returns = a column vector with the b coefficients 
   """ 
    from sklearn import linear_model
    
    x = myDataSet[['x1','x2']]
    xarr = x.as_matrix()
    X = np.array([np.concatenate((v,[1])) for v in xarr])   
    model = linear_model.LinearRegression(fit_intercept = True)
    y = myDataSet[['y']]
    yarr = y.as_matrix()
    fit = model.fit(X,yarr)#use matrix to conduct linar regression
    intercept = fit.intercept_
    coef = fit.coef_
    bcoef = np.append(intercept,coef)
    
    return bcoef

def rscore(myDataSet):
    """
Input = numpy array with three columns
Return = R square
    """
    from sklearn.metrics import r2_score
    from sklearn import linear_model
    
    x = myDataSet[['x1','x2']]
    xarr = x.as_matrix()
    X = np.array([np.concatenate((v,[1])) for v in xarr])
    model = linear_model.LinearRegression(fit_intercept = True)
    y = myDataSet[['y']]
    yarr = y.as_matrix()
    fit = model.fit(X,yarr)
    intercept = fit.intercept_
    coef = fit.coef_
    bcoef = np.append(intercept,coef) #all coefficients including b0
    Xplus= np.array([np.concatenate(([1],v)) for v in xarr])
    coefplus = bcoef[0:3]#delete 0 in columns
    y_pred = np.dot(Xplus,coefplus.T) #use dot product to predict y
    r2= r2_score(y,y_pred) 
    return r2

from mpl_toolkits.mplot3d import *
def myPlot(myData, b):
    """
    Input = numpy array with three columns
            Column 1 is the dependent variable
            Columns 2 and 3 are the independent variables
            and
            a column vector with the b coefficients
    Returns = Noting
    Output = 3D plot of the actual data and 
             the surface plot of the linear model
    """        
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import cm

    fig = plt.figure()
    ax = fig.gca(projection='3d')               # to work in 3d
    plt.hold(True)
    
    x_max = max(myData[:,1])    
    y_max = max(myData[:,2])   
    
    b0 = float(b[0])
    b1 = float(b[1])
    b2 = float(b[2])   
    
    x_surf=np.linspace(0, x_max, 100)                # generate a mesh
    y_surf=np.linspace(0, y_max, 100)
    x_surf, y_surf = np.meshgrid(x_surf, y_surf)
    z_surf = b0 + b1*x_surf +b2*y_surf         # ex. function, which depends on x and y
    ax.plot_surface(x_surf, y_surf, z_surf, cmap=cm.hot, alpha=0.2);    # plot a 3d surface plot
    
    x=myData[:,1]
    y=myData[:,2]
    z=myData[:,0]
    ax.scatter(x, y, z);                        # plot a 3d scatter plot
    
    ax.set_xlabel('x1')
    ax.set_ylabel('y2')
    ax.set_zlabel('y')

    return plt.show()


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



