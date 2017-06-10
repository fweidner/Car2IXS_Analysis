# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 13:09:15 2017

@author: fweidner
"""

import statistics
import scipy
from scipy import stats

highlighton = 'Highlight-1'
highligtoff = 'Highlight-0'
yay = 'yay'
nay = 'nay'


countsCD = {}
globalCountStats = {}


responsetimes_total = []
responsetimes_stat_total = []

responsetimes_ul = []
responsetimes_uc = []
responsetimes_ur = []
responsetimes_dr = []

globalCount_ul = {}
globalCount_uc = {}
globalCount_ur = {}
globalCount_dr = {}

    
def Reset():
    global responsetimes_stat_total
    global responsetimes_total
    global countsCD
    global globalCountStats
    
    responsetimes_stat_total = []
    responsetimes_total = []
    countsCD = {}
    globalCountStats = {}

def CalcTime(t1, t2, responsetimes_cd):
    res = int(t2)-int(t1)
    responsetimes_cd.append(res)

def MergeResponseTimes(responsetimes_var):
    global responsetimes_total
    responsetimes_total+=responsetimes_var
    
def PrintGlobalResponseTimes():
    global responsetimes_total
    print (responsetimes_total)
    
def CalcGlobalResponseTimeStats():
    global responsetimes_total
    global responsetimes_stat_total
    responsetimes_total = list(map(int, responsetimes_total))
    responsetimes_stat_total.append(statistics.mean(responsetimes_total))
    responsetimes_stat_total.append(statistics.stdev(responsetimes_total))

def PrintGlobalResponseTimeStats():
    print('Mean Change Detection Response Time and StDev in [ms]:')
    print ('\t' + str(responsetimes_stat_total))
    print('\tnormality =', scipy.stats.shapiro(responsetimes_total))

    
def PrintGlobalCountsCD():
    global countsCD
    for item in countsCD:
        print (item + ' : ' + str(countsCD[item]))
        
def CalcAndPrintGlobalCountStats():
    global globalCountStats
    
    tmpListCorrect =[]
    tmpListWrong=[]
    tmpListMissed=[]
    
    for item in countsCD:
        tmpListCorrect.append(countsCD.get(item)[2])    
        tmpListWrong.append(countsCD.get(item)[3])    
        tmpListMissed.append(countsCD.get(item)[4])    
    
    meancorrect = statistics.mean(tmpListCorrect)
    stdevcorrect = statistics.stdev(tmpListCorrect)
    
    meanwrong = statistics.mean(tmpListWrong)
    stdevwrong = statistics.stdev(tmpListWrong)
    
    meanmissed = statistics.mean(tmpListMissed)
    stdevmissed= statistics.stdev(tmpListMissed)
    
    
    
    print ('Stats about correct, incorrent and missed values (mean + stdev):')
    print ('\tCorrect : ' + str(meancorrect) + ' [' +str(stdevcorrect) + ']')
    print('\t\t  normality =', scipy.stats.shapiro(tmpListCorrect))

    print ('\tWrong   : ' + str(meanwrong)   + ' [' +str(stdevwrong) + ']')
    print('\t\t  normality =', scipy.stats.shapiro(tmpListMissed))
 
    print ('\tMissed  : ' + str(meanmissed)  + ' [' +str(stdevmissed) + ']')
    print('\t\t  normality =', scipy.stats.shapiro(tmpListWrong))

    print()
    
    #H0: list is normal distributed
    # If P is higher than 0.05, it may be assumed that the data have a Normal distribution and the conclusion ‘accept Normality’ is displayed.
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
    # https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test
    
    
    
def GetResponseTimesForCorrectValues(spamreader_var, name ='',con=''):
    
    global countsCD
    
    bShouldPress = False
    bShouldCalcTime = True
    responsetimes_cd = []
    count_correct = 0
    count_wrong = 0
    count_highlight =0
    tmp_t1=0
    tmp_t2=0
    tmp_t_response=0
    
    for tmprow in spamreader_var:
      #print (tmprow)
      #calc response time
      if (bShouldCalcTime):  
          CalcTime(tmp_t1, tmp_t_response, responsetimes_cd)
          bShouldCalcTime = False
    #time began
      if (highlighton in tmprow.get('A')):
          bShouldPress = True
          count_highlight+=1
          tmp_t1=tmprow.get('timestamp')
          continue
    #time ended  
      if (highligtoff in tmprow.get('A')):
          bShouldPress = False
          tmp_t2 = tmprow.get('timestamp')
          continue
      
    #correct button press
      if ((yay in tmprow.get('A')) & bShouldPress):
          count_correct+=1
          bShouldPress=False
          bShouldCalcTime = True
          tmp_t_response = tmprow.get('timestamp')
      
    #wrong button press
      if ((nay in tmprow.get('A'))):
          count_wrong+=1
          bShouldPress=False
          
      missed = int(count_highlight)-int(count_wrong)-int(count_correct)
      countsCD.update({name : [con, count_highlight, count_correct, count_wrong, missed]})    
    
#    print (responsetimes_cd)
#    print ("Triggers: " + str(count_highlight))
#    print ("yay: " + str(count_correct))
#    print ("nay: " + str(count_wrong))
#    print ("missed: " + str(int(count_highlight)-int(count_wrong)-int(count_correct)))

    MergeResponseTimes(responsetimes_cd)          
          
 
        