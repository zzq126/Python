# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 12:15:25 2016

@author: Ziqing Zhu
Gworld Id: G20525987

Programming for Analytics Assignment 01: Usage of Pandas and database
"""

import pandas as pd

def getData():
  """
  Reads multiple files and returns contents in a pandas dataframe.
  
    Args: None: Requests for the name of the path for the files in the program
    
    Returns: a list with the file contents
    """
import time
start_time = time.time()

# Create empty dataframe    
dfAll = pd.DataFrame({'Name':[],'Sex':[],'Count':[],'Year':[]})

print('Started')
# Read a new file into a dataframe
for year in range(1880,2016):
    filename = 'yob'+str(year)+'.txt'
    filepath = '/home/zzq/Downloads/Programming for analytics/names/'+filename
    
    df = pd.read_csv(filepath,header=None)
    df.columns = ['Name','Sex','Count']
    df['Year'] = str(year)    
    dfAll = pd.concat([dfAll,df])
    
print('Done...')
print('It took', round(time.time()-start_time,4), 'seconds to read all the data into a dataframe.')


# Part 1
def q1(myDF):
    """Compute total number of births for each year and provide a formatted printout of that
 
    Args: filename: the pandas dataframe with all data
 
    Returns: Nothing 
    """

    dfCount = dfAll['Count'].groupby(dfAll['Year']).sum()
    s = '{:>5}'.format('Year')
    s = s + '{:>10}'.format('Births')
    print(s)
    for myIndex, myValue in dfCount.iteritems():
        s = '{:>5}'.format(myIndex)
        s = s + '{:>10}'.format(str(int(myValue)))
        print (s)

# Part 2
def q2(myDf):
    """Compute the total births each year (from 1990 to 2014, inclusive of both) for males and females,
    
    and provide a plot for that
    
    Args: Dataframe
    
    Returns: Dataframe
    """
import matplotlib.pyplot as plt  # import the libraries to plot              
plt.style.use('ggplot')          # set the plot style to ggplot type      

dfSubset = dfAll[ (dfAll['Year'] >= '1990') & (dfAll['Year'] <= '2014') ]
dfCountBySex = dfSubset.groupby(['Year','Sex']).sum()
print (dfCountBySex)              
dfCountBySex['Count'].plot.bar()  



#Part 3
def q3(myDF):
    """Print the top 5 names for each year starting in 1950. 
    
    Args:Dataframe
    
    Returns:Nothing
    """
 # Prepare header
s = ''
s = '{:>5}'.format('Year')
s = s + '{:>10}'.format('Name 1')
s = s + '{:>10}'.format('Name 2')
s = s + '{:>10}'.format('Name 3')
s = s + '{:>10}'.format('Name 4')
s = s + '{:>10}'.format('Name 5')
print (s)  # Print header

# Now go through all the years for the report
for i in range(1950,2015):
    fn = dfAll[(dfAll['Year'] == str(i))]                  
    fn = fn.sort_values('Count', ascending=False).head(5)  
    s = ''
    s = s = s + '{:>5}'.format(str(i))
    for idx, row in fn.iterrows():
        s = s + '{:>10}'.format(row["Name"])
    print(s)



#Part 4
def q4(myDF):
    """Find the top 3 female and top 3 male names for years 2010 and up and and 
    
    plot the frequency by gender.  
    
    Args:Dataframe
    
    Returns:Series
    """
import matplotlib.pyplot as plt             
plt.style.use('ggplot')

#create Pandas Series of Male and from 2010 
dfSubsetM = dfAll[ (dfAll['Year'] >= '2010') & (dfAll['Sex'] == 'M')]
dfMale = dfSubsetM.groupby(['Name','Sex']).sum().sort_values(by = 'Count').tail(3)
print (dfMale)

#create Pandas Series of Male and from 2010 
dfSubsetF = dfAll[ (dfAll['Year'] >= '2010') & (dfAll['Sex'] == 'F')]
dfFemale = dfSubsetF.groupby(['Name','Sex']).sum().sort_values(by = 'Count').tail(3)
print (dfFemale)

#plot its frequency 
dfMale['Count'].plot()  
dfFemale['Count'].plot()



#Part 5
def q5(myDF):
    """Plot the trend of the names 'John', 'Harry', 'Mary' and 'Marilyn' over all of the years of the data set. 

a. Stack 4 plots one over the other 

b. Plot all four trends in one plot.  

    Args:Dataframe
    
    Returns:Series
    
    """
#(a) stack one over the other
import matplotlib.pyplot as plt               
plt.style.use('ggplot')  

#create PandasSeries with each name of all years
dfJohn = dfAll.query("'John' in Name").groupby(['Year']).sum()
dfHarry = dfAll.query("'Harry' in Name").groupby(['Year']).sum()
dfMary = dfAll.query("'Mary' in Name").groupby(['Year']).sum()
dfMarilyn = dfAll.query("'Marilyn' in Name").groupby(['Year']).sum()

#merge 4 Series
frames = [dfJohn, dfHarry, dfMary, dfMarilyn]
dfCombine = pd.concat(frames,axis = 1)
dfCombine.columns = ['John', 'Harry', 'Mary', 'Marilyn']
print (dfCombine)

#stack four plots
dfCombine.plot.bar(stacked = True)
   
   
#(b) put all 4 trends in one plot
import matplotlib.pyplot as plt               
plt.style.use('ggplot')   

dfJohn = dfAll.query("'John' in Name").groupby(['Year']).sum()
dfHarry = dfAll.query("'Harry' in Name").groupby(['Year']).sum()
dfMary = dfAll.query("'Mary' in Name").groupby(['Year']).sum()
dfMarilyn = dfAll.query("'Marilyn' in Name").groupby(['Year']).sum()

frames = [dfJohn, dfHarry, dfMary, dfMarilyn]
dfCombine = pd.concat(frames,axis = 1)
dfCombine.columns = ['John', 'Harry', 'Mary', 'Marilyn']

#put all trends in one plot
plt.figure(); dfCombine.plot()



#Part 6
def q6(myDF):
    """
    Find the ten names that have shown the greatest variation over the years. Plot this. 
    
    Args:Dataframe
    
    Returns:Series
    """
#apply functions
import numpy as np
dfStd = dfAll.groupby(['Name']).agg({'Count': [np.std, np.mean]})#calculate its standard deviation

dfStdByName = dfStd.sort_values([('Count', 'std')], ascending=False).head(10)
print (dfStdByName)

dfStdByName['Count','std'].plot()

