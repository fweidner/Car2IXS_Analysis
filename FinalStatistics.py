# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:25:16 2017

@author: flwe6397
"""

import scipy


import statsmodels.api as sm
from matplotlib import pyplot
import numpy as np

import statistics

def CalcNonParametric_MannWhitneyWithShapiro(list1, list2, my_alternative='two-sided', printHint=False, printNorm=False):
    if (printNorm):
        print ('\t\tnormality list1 (Shapiro) = ' + str(scipy.stats.shapiro(list1)))
        print ('\t\tnormality list2 (Shapiro) = ' + str(scipy.stats.shapiro(list2)))
    print('\t\t' + str(scipy.stats.mannwhitneyu(list1, list2, alternative=my_alternative)))
    
    meanl1 = statistics.mean(list1)
    meanl2 = statistics.mean(list2)
    
    stdevl1 = statistics.stdev(list1)
    stdevl2 = statistics.stdev(list2)
    
    print ('\t\tMean l1 : ' + str(statistics.mean(list1)) + '\tStDev l1: ' + str(statistics.stdev(list1)))
    print ('\t\tMean l2 : ' + str(statistics.mean(list2))+ '\tStDev l2: ' + str(statistics.stdev(list2)))
    
    if (printNorm):
       print (str(len(list1)))
       print (str(len(list2)))
    

    if(printHint):
        print('\t\tMann-Whitney:' + 'If P <= 0.05, we are confident that the distributions significantly differ')
        print('\t\tShapiro     :' + 'If P > 0.05, it may be assumed that the data have a normal distribution.')
    #http://www.randalolson.com/2012/08/06/statistical-analysis-made-easy-in-python/
    
    return meanl1, stdevl1, meanl2, stdevl2

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
    
    meanl1 = statistics.mean(list1)
    meanl2 = statistics.mean(list2)
    
    stdevl1 = statistics.stdev(list1)
    stdevl2 = statistics.stdev(list2)
  
        
    print ('\t\tMean l1 : ' + str(statistics.mean(list1)) + '\tStDev l1: ' + str(statistics.stdev(list1)))
    print ('\t\tMean l2 : ' + str(statistics.mean(list2))+ '\tStDev l2: ' + str(statistics.stdev(list2)))
    
    if (printHint):
        print ('\t\tLevene  : If p < 0.05 indicates a violation of the assumption that variance is equal across groups. ')    
        print ('\t\tT-Test  : If p < 0.05, then we can reject the null hypothesis of identical average scores. (they differ)')    
        print ('\t\tShapiro : If P > 0.05, it may be assumed that the data have a normal distribution.')
    
    return meanl1, stdevl1, meanl2, stdevl2
    
def PrintQQPlot(list1):    
    res = np.array(list1)
    fig = sm.qqplot(res)
    pyplot.show()
    
def plotBarChartWithStDev(means, stdev):
    ind = np.arange(len(means))
    width = 0.35
    colours = ['red','blue','green','yellow', 'orange']
    
    pyplot.figure()
    #pyplot.title('Average Age')
    for i in range(len(means)):
        pyplot.bar(ind[i],means[i],width,color=colours[i],align='center',yerr=stdev[i],ecolor='k')
    pyplot.ylabel('bla')
    pyplot.xticks(ind,('ul','uc','ur','dr','t'))

def plotBarChartWithStdDevDouble(n, means1, means2, stdev1, stdev2, axislist, axistitle = '', newwidth=0.27):
    N = n
    ind = np.arange(N)  # the x locations for the groups
    width = newwidth       # the width of the bars
    
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    
    yvals = means1#[4, 9,6,9,2]
    rects1 = ax.bar(ind+width, yvals, width, yerr=stdev1, ecolor='black', error_kw=dict(lw=1, capsize=3, capthick=1), color='#A9A9A9', hatch='//')
    
    zvals = means2#[1,2,21,1,2]
    rects2 = ax.bar(ind+width*2, zvals, width, yerr=stdev2, ecolor='black',error_kw=dict(lw=1, capsize=3, capthick=1), color='#D3D3D3', hatch='..')
    
    ax.set_ylabel(axistitle)
    ax.set_xticks(ind+width*2)
    ax.set_xticklabels( axislist )
    ax.legend( (rects1[0], rects2[0]), ('2D', '3D') )
    
    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                    ha='center', va='bottom')
