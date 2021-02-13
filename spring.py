# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:34:07 2021

@author: kazuya
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

Th = 30000 #Threshold to detect segments. Should be adjusted upon input data.
d_min = np.inf #Min distance of current calc.
t_s=0 #Starting point of detected segment
t_e=0 #End point of detected segment
seg=[] #List of segments [t_s, T,e]
filename="handgesture.csv"
#Load data
with open(filename) as f:
    X=np.loadtxt(f, delimiter=",")
    X=X[:,3] #time-series data
    Y_s,Y_e=4551,4800
    Y=X[Y_s:Y_e] # query sub-sequence

#Initialize warping matrix
d=np.zeros((len(X)+1,len(Y)+1)) #distance
s=np.zeros((len(X)+1,len(Y)+1), dtype=np.int32) #starting point of current distance calc.
for j in range(1,len(Y)+1):
    d[0,j]=np.inf
for i in range(1,len(X)+1):
    s[i,0]=i-1

#SPRING main calc.
for i in range(len(X)):
    for j in range(len(Y)):
        #Update warping matrix with newly comming input X(i)
        if d[i+1,j]<=d[i,j] and d[i+1,j]<=d[i,j+1]:
            d_best = d[i+1,j]
            s[i+1,j+1]=s[i+1,j]
        elif d[i,j+1]<=d[i,j]:
            d_best = d[i,j+1]
            s[i+1,j+1]=s[i,j+1]
        else:
            d_best = d[i,j]
            s[i+1,j+1]=s[i,j]
        d[i+1,j+1] = np.abs(X[i]-Y[j]) + d_best
    #Judge if current segment should be reported
#    print(i,d[i+1,-1])
    if d_min<=Th:
        flag=1
        for j in range(len(Y)):
            if d[i+1,j+1]>=d_min or s[i+1,j+1]>t_e:
                flag*=1
            else:
                flag*=0
        if flag==1:
            print("****")
            seg.append([i,d_min,t_s,t_e])
            d_min=np.inf
            for j in range(len(Y)):
                if s[i+1,j+1]<=t_e:
                    d[i+1,j+1]=np.inf
    #Update d_min, t_s, t_e if input data still matches (distance is improving).
    if d[i+1,-1]<=Th and d[i+1,-1]<d_min:
        d_min=d[i+1,-1]
        t_s=s[i+1,-1]
        t_e = i

#Visualize time-series with detected segments and query subsequence
plt.plot(X) #time-series
for i in seg:
    plt.axvspan(i[2],i[3], color="gray", alpha=0.3) #detected segments in gray
plt.axvspan(Y_s,Y_e,color="red",alpha=0.3) #query subsequence in red
