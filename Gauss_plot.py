# -*- coding: utf-8 -*-
'''

 Copyright (c)  2015  Thomas E. West.
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the section entitled "GNU
    Free Documentation License".
'''

"""
Created on Fri Apr 24 23:57:53 2015
@author: tewest
"""
# import modules to use.
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

''' definitions for value retrieval from files '''

# gaussian file reader, gibbs free energy. 

def gibbs(z):
    # assign .log to indicated file name should be an int.
    #z = str(z) + '.log'
    text_file = open(z,"r")
    lines = text_file.read().split(' ') 
    lines.reverse() # <- Reverse file
    lined = lines[0:lines.index('Free')] # <- put file into a list.
    strings = [x for x in lined if x] # <- remove all empty elements in list.
    
    # Algorithm for finding energy in file, cutting the list then print energy.
    c = len(strings)
    x = c - 2
    y = x + 1
    gibbs = strings[x:y]
    for i in gibbs:
        value = float(i)
        return value
              
    text_file.close()

# Still working on the enthalpy portion, to calculate the deltaH of reaction.
   
'''
def enthalpy(z):
    text_file = open(z,"r")
    lines = text_file.read().split(' ')
    lines.reverse()
    lined = lines[0:lines.index('Enthalpies=')]
    strings = [x for x in lined if x]
    c = len(strings)
    x = c - 1
    y = x + 1
    enthalpy = strings[x:y]
    for i in enthalpy:
        value = float(i)
        return value
        
        
    text_file.close()
'''
# Plot formatting and definition.

def graph(x,y,z):
    plt.suptitle('Free Energy Diagram ', fontsize=20)
    plt.xlabel('Reaction Choordinate', fontsize=18)
    plt.ylabel("Free Energy\nKcal/mol", fontsize=18)
    line = plt.plot(x,z)
    plt.setp(line, linewidth=2,color='k', linestyle='-')
    plt.xticks(x,fontsize = 18)
    plt.yticks(y, fontsize = 18)
    line1 = plt.plot(x,y)
    plt.setp(line1, linewidth=4, color='b')
    plt.grid(b=True, which='major', color='k', linestyle='--')
    ax1 = plt.axes()
    plt.axis([min(x)-2, max(x)+2, min(y)-2, max(y)+3])
    ax1.axes.get_xaxis().set_visible(False)
    plt.show()



def main():
    
    num_ts = int(input ('How many steps in the reaction?: '))
    num = num_ts
    num *= 2
    
    num_files = []
    lst = []
    
    while num > -1:
        files = int(input('Enter the number of files at this point: '))
        num_files.append(files)
        while files != 0:
            root = Tk()
            root.withdraw()
            ftypes = [('Gaussian Output File',"*.out")]
            ttl  = "MATERIAL"
            dir1 = 'C:\\'
            root.fileName = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
            lst.append(root.fileName)
            root.destroy()
            files -= 1
            
        num -= 1
    
    num_length = len(num_files)
    
    length = len(lst)
    
    values = []
    
    for i in range (1,length+1):
        for n in lst[i-1:i]:
            values.append(gibbs(n))
    
    new_values = []
    fc = 0   
    dc = 0
    for i in range (1,num_length+1):
        for n in num_files[i-1:i]:
            fc += int(n)
            dc += int(-n)
            dc = fc + dc
            add_to = values[dc:fc]
            adder = 0
            for c in add_to:
                adder += round(float(c),4) # remove noise from gaussian calculation.
            dc = 0
            new_values.append(adder)
            
    # Calculate free energy change at each step.
    
    # zero-point is always the first item in the list.
    
    zero = new_values[0:1]
    
    zero_value = 0
    
    for x in zero:
        zero_value += float(x)
    
    plot_x = []
    plot_y = []
    plot_x.append(0)
    plot_y.append(0)
    
    for i in range (1,num_length):
        for n in new_values[i:i+1]:
             numba = n - zero_value
             numba = numba*627.503 # convert to a.u.
             numba = round(numba,1) # round to 1 decimal place. 
             plot_x.append(numba)
             plot_y.append(0)
    
    
    # formatting chart.
          
    final_y = []
    
    for i in plot_x:
        final_y.append(i)
        final_y.append(i)
    
    final_x = []
    
    for i in range(1,len(final_y)+1):
        final_x.append(i)
    
     
    final_z = []
    
    for i in plot_y:
        final_z.append(i)
        final_z.append(i)
        
    # use our graph function to graph the results!
    graph(final_x,final_y,final_z)


main()
