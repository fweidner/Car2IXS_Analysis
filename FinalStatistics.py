# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:25:16 2017

@author: flwe6397
"""

import scipy


import statsmodels.api as sm
from matplotlib import pyplot as plt
import numpy as np

import statistics

def CalcNonParametric_MannWhitneyWithShapiro(list1, list2, my_alternative, printHint=False):
    print ('\t\tnormality list1 (Shapiro) = ' + str(scipy.stats.shapiro(list1)))
    print ('\t\tnormality list2 (Shapiro) = ' + str(scipy.stats.shapiro(list2)))
    print('\t\t' + str(scipy.stats.mannwhitneyu(list1, list2, alternative=my_alternative)))
        
    if(printHint):
        print('\t\tMann-Whitney:' + 'If P <= 0.05, we are confident that the distributions significantly differ')
        print('\t\tShapiro     :' + 'If P > 0.05, it may be assumed that the data have a normal distribution.')
    #http://www.randalolson.com/2012/08/06/statistical-analysis-made-easy-in-python/

def CalcParametric_WelshWithShapiroAndLevene(list1, list2, printHint=False):
    print ('\t\tnormality list1 (Shapiro) = ' + str(scipy.stats.shapiro(list1)))
    print ('\t\tnormality list2 (Shapiro) = ' + str(scipy.stats.shapiro(list2)))
 
    equalvar = scipy.stats.levene(list1, list2, center='mean')
      
    if (equalvar[1] < 0.05):
        print ('\t\t' + str(scipy.stats.ttest_ind(list1, list2, equal_var=False)) + '; unequal variance: '+ str(equalvar[1]))
    else: 
        print ('\t\t' + str(scipy.stats.ttest_ind(list1, list2, equal_var=True))+ '; equal variance: '+str(equalvar[1]))
    
    if (printHint):
        print ('\t\tLevene  : If p < 0.05 indicates a violation of the assumption that variance is equal across groups. ')    
        print ('\t\tT-Test  : If p < 0.05, then we can reject the null hypothesis of identical average scores.')    
        print ('\t\tShapiro : If P > 0.05, it may be assumed that the data have a normal distribution.')
        
def CalcDistance(list1, list2): #large sample size        
    
    list1 = list(map(int, list1))
    list2 = list(map(int, list2))
    
    
    
    print ('\t\tnormality list1 (Shapiro) = ' + str(scipy.stats.shapiro(list1)))
    print ('\t\tnormality list2 (Shapiro) = ' + str(scipy.stats.shapiro(list2)))
      
    print ('\t\tMean l1 :' + str(statistics.mean(list1)))
    print ('\t\tStDev l1: ' + str(statistics.stdev(list1)))
 
    
    print ('\t\tMean l2 : ' + str(statistics.mean(list1)))
    print ('\t\tStDev l2: ' + str(statistics.stdev(list1)))
    
    print ('\t\t' + str(scipy.stats.mannwhitneyu(list1, list2, alternative='two-sided')))    
    

def PrintQQPlot(list1):    
    res = np.array(list1)
    fig = sm.qqplot(res)
    plt.show()