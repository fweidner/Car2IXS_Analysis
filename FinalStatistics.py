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

def CalcNonParametric_MannWhitneyWithShapiro(list1, list2, my_alternative='two-sided', printHint=False, printNorm=False):
    if (printNorm):
        print ('\t\tnormality list1 (Shapiro) = ' + str(scipy.stats.shapiro(list1)))
        print ('\t\tnormality list2 (Shapiro) = ' + str(scipy.stats.shapiro(list2)))
    print('\t\t' + str(scipy.stats.mannwhitneyu(list1, list2, alternative=my_alternative)))
    print ('\t\tMean l1 : ' + str(statistics.mean(list1)) + '\tStDev l1: ' + str(statistics.stdev(list1)))
    print ('\t\tMean l2 : ' + str(statistics.mean(list2))+ '\tStDev l2: ' + str(statistics.stdev(list2)))
    
    #print (str(len(list1)))
    #print (str(len(list2)))
        

    if(printHint):
        print('\t\tMann-Whitney:' + 'If P <= 0.05, we are confident that the distributions significantly differ')
        print('\t\tShapiro     :' + 'If P > 0.05, it may be assumed that the data have a normal distribution.')
    #http://www.randalolson.com/2012/08/06/statistical-analysis-made-easy-in-python/

def CalcParametric_WelshWithShapiroAndLevene(list1, list2, printHint=False, printNorm=False):
    if (printNorm):
        print ('\t\tnormality list1 (Shapiro) = ' + str(scipy.stats.shapiro(list1)))
        print ('\t\tnormality list2 (Shapiro) = ' + str(scipy.stats.shapiro(list2)))
 
    #print (str(len(list1)))
    #print (str(len(list2)))
     
    equalvar = scipy.stats.levene(list1, list2, center='mean')
      
    if (equalvar[1] < 0.05):
        print ('\t\t' + str(scipy.stats.ttest_ind(list1, list2, equal_var=False)) + '; Welch: '+ str(equalvar[1])) #Welch
    else: 
        print ('\t\t' + str(scipy.stats.ttest_ind(list1, list2, equal_var=True))+ '; t-test: '+str(equalvar[1]))
        # a negative sign implies tahat the sample mean is less than the hypothesized mean
    
    print ('\t\tMean l1 : ' + str(statistics.mean(list1)) + '\tStDev l1: ' + str(statistics.stdev(list1)))
    print ('\t\tMean l2 : ' + str(statistics.mean(list2))+ '\tStDev l2: ' + str(statistics.stdev(list2)))
    
    if (printHint):
        print ('\t\tLevene  : If p < 0.05 indicates a violation of the assumption that variance is equal across groups. ')    
        print ('\t\tT-Test  : If p < 0.05, then we can reject the null hypothesis of identical average scores. (they differ)')    
        print ('\t\tShapiro : If P > 0.05, it may be assumed that the data have a normal distribution.')
    

def PrintQQPlot(list1):    
    res = np.array(list1)
    fig = sm.qqplot(res)
    plt.show()