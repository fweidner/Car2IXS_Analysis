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

currentarea = ''

countsCD = {}
globalCountStats = {}   #1 =highlights, 2 = correct, 3 = wrong, 4 = missed, 
                        #5/6/7 = ul
                        #8/9/10 = uc
                        #11/12/13 = ur
                        #14/15/16 = dr


responsetimes_total = []
responsetimes_stat_total = []

responsetimes_ul = []
responsetimes_uc = []
responsetimes_ur = []
responsetimes_dr = []

responsetimes_areas = {}

globalCount_area = {} # aera : corr , wrong, missed
globalCount_area.update({'ul' : [0,0,0]})
globalCount_area.update({'uc' : [0,0,0]})
globalCount_area.update({'ur' : [0,0,0]})
globalCount_area.update({'dr' : [0,0,0]})

def Reset():
    global responsetimes_stat_total
    global responsetimes_total
    global countsCD
    global globalCountStats
    global responsetimes_areas
    global globalCount_area 
    
    global responsetimes_dr
    global responsetimes_uc
    global responsetimes_ul
    global responsetimes_ur
    
    responsetimes_stat_total = []
    responsetimes_total = []
    countsCD = {}
    globalCountStats = {}
    responsetimes_areas = {}
    globalCount_area = {}

    globalCount_area.update({'ul' : [0,0,0]})
    globalCount_area.update({'uc' : [0,0,0]})
    globalCount_area.update({'ur' : [0,0,0]})
    globalCount_area.update({'dr' : [0,0,0]})
    
    responsetimes_ul = []
    responsetimes_uc = []
    responsetimes_ur = []
    responsetimes_dr = []

def CalcTime(t1, t2, responsetimes_cd):
    global currentarea
    
    res = int(t2)-int(t1)
    responsetimes_cd.append(res)
    
    
    if (currentarea == 'ul'):
        responsetimes_ul.append(res)
    elif (currentarea == 'uc'):
        responsetimes_uc.append(res)
    elif (currentarea == 'ur'):
        responsetimes_ur.append(res)
    elif (currentarea == 'dr'):
        responsetimes_dr.append(res)
    else:
        print ('huh ' + str(currentarea))

def MergeResponseTimes(responsetimes_var):
    global responsetimes_total
    responsetimes_total+=responsetimes_var
    
def PrintGlobalResponseTimes():
    global responsetimes_total
    print (responsetimes_total)
    
def CalcGlobalResponseTimeStats():
    global responsetimes_total
    global responsetimes_stat_total
    
    global responsetimes_dr
    global responsetimes_uc
    global responsetimes_ul
    global responsetimes_ur
    
    responsetimes_total = list(map(int, responsetimes_total))
    responsetimes_stat_total.append(statistics.mean(responsetimes_total))
    responsetimes_stat_total.append(statistics.stdev(responsetimes_total))
        
    mean = statistics.mean(list(map(int, responsetimes_ul)))
    stdev = statistics.stdev(list(map(int, responsetimes_ul)))
    norm = scipy.stats.shapiro(list(map(int, responsetimes_ul)))
    responsetimes_areas.update({'ul' : [mean, stdev, norm]})
    
    mean = statistics.mean(list(map(int, responsetimes_uc)))
    stdev = statistics.stdev(list(map(int, responsetimes_uc)))
    norm = scipy.stats.shapiro(list(map(int, responsetimes_uc)))
    responsetimes_areas.update({'uc' : [mean, stdev, norm]})
    
    mean = statistics.mean(list(map(int, responsetimes_ur)))
    stdev = statistics.stdev(list(map(int, responsetimes_ur)))
    norm = scipy.stats.shapiro(list(map(int, responsetimes_ur)))
    responsetimes_areas.update({'ur' : [mean, stdev, norm]})
    
    mean = statistics.mean(list(map(int, responsetimes_dr)))
    stdev = statistics.stdev(list(map(int, responsetimes_dr)))
    norm = scipy.stats.shapiro(list(map(int, responsetimes_dr)))
    responsetimes_areas.update({'dr' : [mean, stdev, norm]})

def PrintGlobalResponseTimeStats():
    global responsetimes_stat_total
    global responsetimes_total
    global responsetimes_areas
    
    print()
    print('Overall mean Change Detection Response Time and StDev in [ms]:')
    print ('\t' + str(responsetimes_stat_total))
    print('\tnormality =', scipy.stats.shapiro(responsetimes_total))
    print('Area Mean Change Detection Response Time, StDev in [ms] and normality:')
    for item in responsetimes_areas:
        print('\t' + item + ' : ' + str(responsetimes_areas[item]))
    
def PrintGlobalCountsCD():
    global countsCD
    for item in countsCD:
        print (item + ' : ' + str(countsCD[item]))
        
def fillMissed():
    #5/6/7 = ul
    #8/9/10 = uc
    #11/12/13 = ur
    #14/15/16 = dr
    global countsCD
    
    for item in countsCD:
        #ul
        res = 13 - countsCD.get(item)[6] - countsCD.get(item)[5] 
        countsCD.get(item)[7] = res if res>=0 else 0

        res = 13 - countsCD.get(item)[9] - countsCD.get(item)[8] 
        countsCD.get(item)[10] = res if res>=0 else 0

        res = 19 - countsCD.get(item)[12] - countsCD.get(item)[11]
        countsCD.get(item)[13] = res if res>=0 else 0

        res = 13 - countsCD.get(item)[15] - countsCD.get(item)[14]
        countsCD.get(item)[16] = res if res>=0 else 0

def CalcGlobalCountStats():
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
    
    globalCountStats.update({'Correct': [meancorrect, stdevcorrect, scipy.stats.shapiro(tmpListCorrect)]})
    globalCountStats.update({'Wrong  ': [meanwrong, stdevwrong, scipy.stats.shapiro(tmpListWrong)]})
    globalCountStats.update({'Missed ': [meanmissed, stdevmissed, scipy.stats.shapiro(tmpListMissed)]})

                        #5/6/7 = ul
                        #8/9/10 = uc
                        #11/12/13 = ur
                        #14/15/16 = dr
    
    fillMissed()
    
    ####################### ul
    tmpList_c = []
    tmpList_w = []
    tmpList_m = []
    for item in countsCD:
        tmpList_c.append(countsCD.get(item)[5])
        tmpList_w.append(countsCD.get(item)[6])
        tmpList_m.append(countsCD.get(item)[7])
        
    mean_ul_c = statistics.mean(tmpList_c)
    stdev_ul_c = statistics.stdev(tmpList_c)
    norm_ul_c = scipy.stats.shapiro(tmpList_c)
    
    mean_ul_w = statistics.mean(tmpList_w)
    stdev_ul_w = statistics.stdev(tmpList_w)    
    norm_ul_w = scipy.stats.shapiro(tmpList_w)

    mean_ul_m = statistics.mean(tmpList_m)
    stdev_ul_m = statistics.stdev(tmpList_m)
    norm_ul_m = scipy.stats.shapiro(tmpList_m)
   
    ####################### uc
    tmpList_c = []
    tmpList_w = []
    tmpList_m = []
    for item in countsCD:
        tmpList_c.append(countsCD.get(item)[8])
        tmpList_w.append(countsCD.get(item)[9])
        tmpList_m.append(countsCD.get(item)[10])
    mean_uc_c = statistics.mean(tmpList_c)
    stdev_uc_c = statistics.stdev(tmpList_c)
    norm_uc_c = scipy.stats.shapiro(tmpList_c)

    mean_uc_w = statistics.mean(tmpList_w)
    stdev_uc_w = statistics.stdev(tmpList_w)    
    norm_uc_w = scipy.stats.shapiro(tmpList_w)

    mean_uc_m = statistics.mean(tmpList_m)
    stdev_uc_m = statistics.stdev(tmpList_m)
    norm_uc_m = scipy.stats.shapiro(tmpList_m)

    ####################### ur
    tmpList_c = []
    tmpList_w = []
    tmpList_m = []
    for item in countsCD:
        tmpList_c.append(countsCD.get(item)[11])
        tmpList_w.append(countsCD.get(item)[12])
        tmpList_m.append(countsCD.get(item)[13])
    mean_ur_c = statistics.mean(tmpList_c)
    stdev_ur_c = statistics.stdev(tmpList_c)
    norm_ur_c = scipy.stats.shapiro(tmpList_c)

    mean_ur_w = statistics.mean(tmpList_w)
    stdev_ur_w = statistics.stdev(tmpList_w)
    norm_ur_w = scipy.stats.shapiro(tmpList_w)
    
    mean_ur_m = statistics.mean(tmpList_m)
    stdev_ur_m = statistics.stdev(tmpList_m)
    norm_ur_m = scipy.stats.shapiro(tmpList_m)
   
    ####################### dr
    tmpList_c = []
    tmpList_w = []
    tmpList_m = []
    for item in countsCD:
        tmpList_c.append(countsCD.get(item)[14])
        tmpList_w.append(countsCD.get(item)[15])
        tmpList_m.append(countsCD.get(item)[16])
    mean_dr_c = statistics.mean(tmpList_c)
    stdev_dr_c = statistics.stdev(tmpList_c)
    norm_dr_c = scipy.stats.shapiro(tmpList_c)

    mean_dr_w = statistics.mean(tmpList_w)
    stdev_dr_w = statistics.stdev(tmpList_w)
    norm_dr_w = scipy.stats.shapiro(tmpList_w)
    
    mean_dr_m = statistics.mean(tmpList_m)
    stdev_dr_m = statistics.stdev(tmpList_m)
    norm_dr_m = scipy.stats.shapiro(tmpList_m)
   
    
    globalCountStats.update({'ul_c' : [mean_ul_c, stdev_ul_c, norm_ul_c]})
    globalCountStats.update({'ul_w' : [mean_ul_w, stdev_ul_w, norm_ul_w]})
    globalCountStats.update({'ul_m' : [mean_ul_m, stdev_ul_m, norm_ul_m]})
    
    globalCountStats.update({'uc_c' : [mean_uc_c, stdev_uc_c, norm_uc_c]})
    globalCountStats.update({'uc_w' : [mean_uc_w, stdev_uc_w, norm_uc_w]})
    globalCountStats.update({'uc_m' : [mean_uc_m, stdev_uc_m, norm_uc_m]})
    
    globalCountStats.update({'ur_c' : [mean_ur_c, stdev_ur_c, norm_ur_c]})
    globalCountStats.update({'ur_w' : [mean_ur_w, stdev_ur_w, norm_ur_w]})
    globalCountStats.update({'ur_m' : [mean_ur_m, stdev_ur_m, norm_ur_m]})
    
    globalCountStats.update({'dr_c' : [mean_dr_c, stdev_dr_c, norm_dr_c]})
    globalCountStats.update({'dr_w' : [mean_dr_w, stdev_dr_w, norm_dr_w]})
    globalCountStats.update({'dr_m' : [mean_dr_m, stdev_dr_m, norm_dr_m]})
    
    
    #H0: list is normal distributed
    # The null-hypothesis of this test is that the population is normally distributed. 
    # If P is higher than 0.05, it may be assumed that the data have a Normal distribution and the conclusion ‘accept Normality’ is displayed.
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
    # https://en.wikipedia.org/wiki/Shapiro%E2%80%93Wilk_test

def PrintGlobalCountStats():
    print()
    print ('Overall Stats about correct, incorrent and missed values (mean + stdev):')
     
    
    print ('\tCorrect : ' + str(globalCountStats.get('Correct')))
    print ('\tWrong   : ' + str(globalCountStats.get('Wrong  ')))
    print ('\tMissed  : ' + str(globalCountStats.get('Missed ')))
    
    print ('Area Stats about correct, incorrent and missed values (mean + stdev):')  
    print ('\tUpper left:')
    print ('\t\tulc     : ' + str(globalCountStats.get('ul_c')))
    print ('\t\tulw     : ' + str(globalCountStats.get('ul_w')))
    print ('\t\tulm     : ' + str(globalCountStats.get('ul_m')))
    print ('\tUpper center:')
    print ('\t\tucc     : ' + str(globalCountStats.get('uc_c')))
    print ('\t\tucw     : ' + str(globalCountStats.get('uc_w')))
    print ('\t\tucm     : ' + str(globalCountStats.get('uc_m')))
    print ('\tUpper right:')
    print ('\t\turc     : ' + str(globalCountStats.get('ur_c')))
    print ('\t\turw     : ' + str(globalCountStats.get('ur_w')))
    print ('\t\turm     : ' + str(globalCountStats.get('ur_m')))
    print ('\tLower right:')
    print ('\t\tdrc     : ' + str(globalCountStats.get('dr_c')))
    print ('\t\tdrw     : ' + str(globalCountStats.get('dr_w')))
    print ('\t\tdrm     : ' + str(globalCountStats.get('dr_m')))
    
    print()
    
def SetArea(val_x, val_z):
    #print ('(' + val_x + ' : ' + val_z + ')')
    global currentarea
    
    x = float(val_x)
    z = float(val_z)
    
    if (x > 60):
        currentarea = 'ul'
    elif (x >-23 and x < 60):

        currentarea = 'uc'
    elif (x<-23 and z>20):
        currentarea = 'ur'
    elif (x<-23 and z<20):
        currentarea = 'dr'
    else:
        print ('what')
    #print (str(currentarea))

def UpdateAreaCountCorrect(name = ''):
    global globalCount_area

    #print('correct')

    if (currentarea == 'ul'):
        globalCount_area.get('ul')[0] +=1
        countsCD.get(name)[5]+=1
        
    elif (currentarea == 'uc'):
        globalCount_area.get('uc')[0] +=1
        countsCD.get(name)[8]+=1
    elif (currentarea == 'ur'):
        globalCount_area.get('ur')[0] +=1
        countsCD.get(name)[11]+=1
    elif (currentarea == 'dr'):
        globalCount_area.get('dr')[0] +=1
        countsCD.get(name)[14]+=1
    else:
        print ('huh ' + str(currentarea))
    
    
def UpdateAreaCountWrong(name =''):
    #print ('wrong')
    
    if (currentarea == 'ul'):
        globalCount_area.get('ul')[1] +=1
        countsCD.get(name)[6]+=1

    elif (currentarea == 'uc'):
        globalCount_area.get('uc')[1] +=1
        countsCD.get(name)[9]+=1

    elif (currentarea == 'ur'):
        globalCount_area.get('ur')[1] +=1
        countsCD.get(name)[12]+=1

    elif (currentarea == 'dr'):
        globalCount_area.get('dr')[1] +=1
        countsCD.get(name)[15]+=1

    else:
        print ('huh ' + str(currentarea))
    

def UpdateAreaCountMissed(name =''):
    #print ('missed')
    
    if (currentarea == 'ul'):
        globalCount_area.get('ul')[2] +=1
        countsCD.get(name)[7]+=1

    elif (currentarea == 'uc'):
        globalCount_area.get('uc')[2] +=1
        countsCD.get(name)[10]+=1

    elif (currentarea == 'ur'):
        globalCount_area.get('ur')[2] +=1
        countsCD.get(name)[13]+=1

    elif (currentarea == 'dr'):
        globalCount_area.get('dr')[2] +=1
        countsCD.get(name)[16]+=1

    else:
        print ('huh ' + str(currentarea))
    
def GetResponseTimesForCorrectValues(spamreader_var, name ='',con=''):
    
    global countsCD
    
    bShouldPress = False
    bShouldCalcTime = False
    responsetimes_cd = []
    count_correct = 0
    count_wrong = 0
    count_highlight =0
    tmp_t1=0
    tmp_t2=0
    tmp_t_response=0
    countsCD.update({name : ['',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]})
    for tmprow in spamreader_var:
      #print (tmprow)
      #calc response time
      if (bShouldCalcTime):  
          CalcTime(tmp_t1, tmp_t_response, responsetimes_cd)
          bShouldCalcTime = False
          
    #time began
      if (highlighton in tmprow.get('A')):
          count_highlight+=1
          if (count_highlight<=4):
              continue
          #print (count_highlight)
          SetArea(tmprow.get('B'),tmprow.get('C'))
          bShouldPress = True
          
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
          UpdateAreaCountCorrect(name)
          bShouldPress=False
          bShouldCalcTime = True
          tmp_t_response = tmprow.get('timestamp')
      
    #wrong button press
      if ((nay in tmprow.get('A'))):
          UpdateAreaCountWrong(name)
          count_wrong+=1
    
   
    missed = int(count_highlight)-int(count_wrong)-int(count_correct)
    #countsCD.update({name : [con, count_highlight, count_correct, count_wrong, missed]})    
    countsCD.get(name)[0] = con
    countsCD.get(name)[1] = count_highlight
    countsCD.get(name)[2] = count_correct
    countsCD.get(name)[3] = count_wrong
    countsCD.get(name)[4] = missed
    
    
#    print (responsetimes_cd)
#    print ("Triggers: " + str(count_highlight))
#    print ("yay: " + str(count_correct))
#    print ("nay: " + str(count_wrong))
#    print ("missed: " + str(missed))
#    print ('ul_c: ' + str(countsCD.get(name)[5]) + '\t\tul_w: ' + str(countsCD.get(name)[6])+'\t\tul_m: ' + str(countsCD.get(name)[7])) 
#    print ('uc_c: ' + str(countsCD.get(name)[8]) +'\t\tuc_w: ' + str(countsCD.get(name)[9]) +'\t\tuc_m: ' + str(countsCD.get(name)[10]))  
#    print ('ur_c: ' + str(countsCD.get(name)[11])+'\t\tur_w: ' + str(countsCD.get(name)[12])+'\t\tur_m: ' + str(countsCD.get(name)[13]))   
#    print ('dr_c: ' + str(countsCD.get(name)[14])+'\t\tdr_w: ' + str(countsCD.get(name)[15])+'\t\tdr_m: ' + str(countsCD.get(name)[16]))  
#    print()
    
    #countsCD.get(name)[5]
#    print ('ul_c' + str()
 #   print ('ul_w' + str(countsCD.get(name)[6]))
  #  print ('ul_m' + str(countsCD.get(name)[7]))

    MergeResponseTimes(responsetimes_cd)          
    
def GetList_OverallResponseTime():
    global responsetimes_total
    return responsetimes_total
    
def GetList_AreaResponseTime():
    global responsetimes_dr
    global responsetimes_uc
    global responsetimes_ul
    global responsetimes_ur
    
    return responsetimes_ul, responsetimes_uc, responsetimes_ur, responsetimes_dr
 
def GetList_OverallCount():
    tmpListCorrect =[]
    tmpListWrong=[]
    tmpListMissed=[]
    
    for item in countsCD:
        tmpListCorrect.append(countsCD.get(item)[2])    
        tmpListWrong.append((countsCD.get(item)[3]+countsCD.get(item)[4])/2)    
        #tmpListWrong.append(countsCD.get(item)[4])    
        
    return tmpListCorrect, tmpListWrong, tmpListMissed
    
def GetList_AreaCount(area):

                        #5/6/7 = ul
                        #8/9/10 = uc
                        #11/12/13 = ur
                        #14/15/16 = dr
                        
    tmpListCorrect =[]
    tmpListWrong=[]
    tmpListMissed=[]
    i,j,k =0,0,0
    if ('UL' in area):
        i = 5
        j = 6
        k = 7
    elif ('UC' in area):
        i = 8
        j = 9
        k = 10
    elif ('UR' in area):
        i = 11
        j = 12
        k = 13
    elif ('DR' in area):
        i = 14
        j = 15
        k = 16
    else:
        print ('whaaat')
        
    for item in countsCD:
        tmpListCorrect.append(countsCD.get(item)[i])    
        tmpListWrong.append(statistics.mean([countsCD.get(item)[j],countsCD.get(item)[k]]))    
        #tmpListWrong.append(countsCD.get(item)[k])    
    
    #print (str(tmpListMissed))
    
    return [tmpListCorrect, tmpListWrong, tmpListMissed]
