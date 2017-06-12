# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 11:13:50 2017

@author: fweidner
"""
import statistics
import scipy
from scipy import stats

import ListSelection_Helper

strListStart = 'NewActiveList'
strResetStage = 'ResetStage'
strSelectText = 'SelectText'
strNewActiveList = 'NewActiveList'

areas = {}     #key: blueprint name of list; 
               #value0: reactiontime of correct items including timeouts; 
               #value1: list of 1/0. 1 = correct w/o timeout; 0 = correct w/ timeout; 2 = incorrect
               #valu23: con
               
areas_divided = {}
                #key: blueprint name of list; 
                #value0: list of reactiontimes of correct items excluding timeouts; 
                #value1: number correct
                #value2: list of reactiontimes of correct but timeout items; 
                #value3: number timeout
                #value4: list of reactiontimes of incorrect items
                #value5: number incorrect

name_performance = {}
name_performance_stats = {}


area_ul = {}
area_uc = {}
area_ur = {}
area_dr = {}

global_mean_stdev = {}
area_mean_stdev = {}

count_people = 0

def Reset():
    global name_performance
    global area_ul
    global area_uc
    global area_ur
    global area_dr
    
    global global_mean_stdev
    global area_mean_stdev
    global areas_divided
    global count_people
    global areas
    name_performance = {}
    
    area_ul = {}
    area_uc = {}
    area_ur = {}
    area_dr = {}

    global_mean_stdev = {}
    area_mean_stdev = {}
    areas_divided = {}

    count_people = 0
    areas = {} 
    
def CreateTriples(tripels):
    tripels.update({'0' : ['Juice', 'Dog', 'Flower']})
    tripels.update({'1' : ['Wine', 'Cat', 'Tree']})
    tripels.update({'2' : ['Beer', 'Horse', 'Bush']})
    tripels.update({'3' : ['Water', 'Mouse', 'Plant']})
    tripels.update({'4' : ['Juice', 'Bird', 'Flower']})
    tripels.update({'5' : ['Milk', 'Horse', 'Grass']})
    tripels.update({'6' : ['Beer', 'Dog', 'Plant']})
    tripels.update({'7' : ['Juice', 'Bird', 'Tree']})
    tripels.update({'8' : ['Water', 'Mouse', 'Flower']})
    tripels.update({'9' : ['Wine', 'Cat', 'Plant']})
    tripels.update({'10' : ['Beer', 'Bird', 'Tree']})
    tripels.update({'11' : ['Milk', 'Dog', 'Bush']})
    tripels.update({'12' : ['Water', 'Mouse', 'Flower']})
    tripels.update({'13' : ['Juice', 'Horse', 'Grass']})
    tripels.update({'14' : ['Water', 'Bird', 'Plant']})
    tripels.update({'15' : ['Beer', 'Cat', 'Tree']})
    tripels.update({'16' : ['Wine', 'Dog', 'Flower']})
    tripels.update({'17' : ['Juice', 'Horse', 'Grass']})
    tripels.update({'18' : ['Beer', 'Mouse', 'Bush']})
    tripels.update({'19' : ['Wine', 'Bird', 'Tree']})
    tripels.update({'20' : ['Juice', 'Horse', 'Bush']})
    tripels.update({'21' : ['Beer', 'Mouse', 'Tree']})
    tripels.update({'22' : ['Water', 'Cat', 'Flower']})
    tripels.update({'23' : ['Milk', 'Dog', 'Grass']})

def CreateAreas():
    area_ul.update({'List_Scaling_BP' : [[],[]]})
    area_ul.update({'List_Scaling_BP2' : [[],[]]})
    area_ul.update({'List_Scaling_BP3' : [[],[]]})
    area_ul.update({'List_Scaling_BP4' : [[],[]]})
    area_ul.update({'List_Scaling_BP5' : [[],[]]})
    area_ul.update({'List_Scaling_BP24' : [[],[]]})
    
    area_uc.update({'List_Scaling_BP6' : [[],[]]})
    area_uc.update({'List_Scaling_BP7' : [[],[]]})
    area_uc.update({'List_Scaling_BP8' : [[],[]]})
    area_uc.update({'List_Scaling_BP9' : [[],[]]})
    area_uc.update({'List_Scaling_BP10' : [[],[]]})
    area_uc.update({'List_Scaling_BP23' : [[],[]]})

    area_ur.update({'List_Scaling_BP11' : [[],[]]})
    area_ur.update({'List_Scaling_BP12' : [[],[]]})
    area_ur.update({'List_Scaling_BP13' : [[],[]]})
    area_ur.update({'List_Scaling_BP14' : [[],[]]})
    area_ur.update({'List_Scaling_BP15' : [[],[]]})
    area_ur.update({'List_Scaling_BP22' : [[],[]]})
    
    area_dr.update({'List_Scaling_BP16' : [[],[]]})
    area_dr.update({'List_Scaling_BP17' : [[],[]]})
    area_dr.update({'List_Scaling_BP18' : [[],[]]})
    area_dr.update({'List_Scaling_BP19' : [[],[]]})
    area_dr.update({'List_Scaling_BP20' : [[],[]]})
    area_dr.update({'List_Scaling_BP21' : [[],[]]})
    
def PrepareForAreaCalculation():
#    for item in areas:
#       print (item)
#       for valueList in areas[item]:
#           res =''
#           for valueListItem in valueList:
#               res+= str(valueListItem) + ';'
#           print (res)
    global area_uc
    global area_ur
    global area_ur
    global area_dr

    CreateAreas()
    
    area_ul.update({'combined_list_ul' : [[],[]]})  #rt, 0-1-2     
    area_uc.update({'combined_list_uc' : [[],[]]})
    area_ur.update({'combined_list_ur' : [[],[]]})
    area_dr.update({'combined_list_dr' : [[],[]]})

    for item in areas:
        if (str(item) in area_ul.keys()):
            #print ('yayul')     
            area_ul.get(item)[0] = area_ul.get(item)[0]+areas.get(item)[0]
            area_ul.get(item)[1] = area_ul.get(item)[1]+areas.get(item)[1]
            
            area_ul.get('combined_list_ul')[0] = area_ul.get('combined_list_ul')[0] + areas.get(item)[0]
            area_ul.get('combined_list_ul')[1] = area_ul.get('combined_list_ul')[1] + areas.get(item)[1]
        elif (str(item) in area_uc.keys()):
            #print ('yayuc')
            area_uc.get(item)[0] = area_uc.get(item)[0].append(areas.get(item)[0])
            area_uc.get(item)[1] = area_uc.get(item)[1].append(areas.get(item)[1])
            
            area_uc.get('combined_list_uc')[0] = area_uc.get('combined_list_uc')[0] + areas.get(item)[0]
            area_uc.get('combined_list_uc')[1] = area_uc.get('combined_list_uc')[1] + areas.get(item)[1]
          
        elif (str(item) in area_ur.keys()):
            #print ('yayur')
            area_ur.get(item)[0] = area_ur.get(item)[0] + areas.get(item)[0]
            area_ur.get(item)[1] = area_ur.get(item)[1] + areas.get(item)[1]
          
            area_ur.get('combined_list_ur')[0] = area_ur.get('combined_list_ur')[0] + areas.get(item)[0]
            area_ur.get('combined_list_ur')[1] = area_ur.get('combined_list_ur')[1] + areas.get(item)[1]
        elif (str(item) in area_dr.keys()):
            #print ('yaydr')
            area_dr.get(item)[0] = area_dr.get(item)[0] + areas.get(item)[0]
            area_dr.get(item)[1] = area_dr.get(item)[1] + areas.get(item)[1]
            
            area_dr.get('combined_list_dr')[0] = area_dr.get('combined_list_dr')[0] + areas.get(item)[0]
            area_dr.get('combined_list_dr')[1] = area_dr.get('combined_list_dr')[1] + areas.get(item)[1]
        else:
            print ('naaay: ' + str(item))
            
   

def CalcGlobalStats():
    global areas
    global areas_divided
    global global_mean_stdev
    #seperate entries
    for item in areas:
        areas_divided.update({item : [[],0,[],0,[],0]})
        length_entries = len(areas.get(item)[1])
        tmpList_items = areas.get(item)[1]
        tmpList_correctresponsetime = areas.get(item)[0]
        count_correct = 0
        count_timeout = 0
        count_incorrect =0
        for i in range (0,length_entries):
            if (tmpList_items[i] == 1):
                count_correct +=1
                areas_divided.get(item)[0].append(tmpList_correctresponsetime[i])
            elif (tmpList_items[i] == 0):
                count_timeout +=1
                areas_divided.get(item)[2].append(tmpList_correctresponsetime[i])
            else:
                count_incorrect +=1
                areas_divided.get(item)[4].append(tmpList_correctresponsetime[i])
        areas_divided.get(item)[1] = count_correct
        areas_divided.get(item)[3] = count_timeout
        areas_divided.get(item)[5] = count_incorrect
     
    tmpCorrect = []
    tmpTimeOut = []
    tmpIncorrect = []
    tmpcorrect = 0
    tmpincorrect =0
    tmptimeout =0

    for item in areas_divided:
        tmpCorrect +=areas_divided.get(item)[0]
        tmpcorrect += areas_divided.get(item)[1]
        
        tmpTimeOut +=areas_divided.get(item)[2]
        tmptimeout += areas_divided.get(item)[3]
        
        tmpIncorrect +=areas_divided.get(item)[4]
        tmpincorrect += areas_divided.get(item)[5]
    
    #set mean, stdev, normality for correct but correct elements
    tmpCorrect = list(map(int, tmpCorrect))
    mean = statistics.mean(tmpCorrect)
    stdev = statistics.stdev(tmpCorrect)
    normality = scipy.stats.normaltest(tmpCorrect)
    global_mean_stdev.update({'correct' : [mean, stdev, normality, tmpcorrect]})
    
    #set mean, stdev, normality for correct but timeout elements
    tmpTimeOut= list(map(int, tmpTimeOut))
    mean = statistics.mean(tmpTimeOut)
    stdev = statistics.stdev(tmpTimeOut)
    normality = scipy.stats.normaltest(tmpTimeOut)
    global_mean_stdev.update({'timeout' : [mean, stdev, normality,tmptimeout]})
    
    #calc missed and classify as incorrect
    desirednumber = count_people * 24
    missed = desirednumber - tmpcorrect - tmptimeout

    #set mean, stdev, normality for incorrect elements    
    tmpIncorrect = list(map(int, tmpIncorrect))
    mean = statistics.mean(tmpIncorrect)
    stdev = statistics.stdev(tmpIncorrect)
    normality = scipy.stats.normaltest(tmpIncorrect)
    global_mean_stdev.update({'incorrect' : [mean, stdev, normality, missed]})
    
def PrintGlobalStats():
    print ('\tGlobal response time stats:' )
    for item in global_mean_stdev:
        print ('\t\t'+item + '  \t' + str(global_mean_stdev[item]))
    
      
# Calculates cumulative statistics over all participants!
def CalcAreaStats(con = '', task = ''):
    global area_mean_stdev
    global area_ul
    global area_uc
    global area_ur
    global area_dr
    
    ListSelection_Helper.CalcStatForOneArea(area_mean_stdev, area_ul, 'combined_list_ul', 'ul_c', 'ul_t', 'ul_i')
    ListSelection_Helper.CalcStatForOneArea(area_mean_stdev, area_ur, 'combined_list_ur', 'ur_c', 'ur_t', 'ur_i')
    ListSelection_Helper.CalcStatForOneArea(area_mean_stdev, area_uc, 'combined_list_uc', 'uc_c', 'uc_t', 'uc_i')
    ListSelection_Helper.CalcStatForOneArea(area_mean_stdev, area_dr, 'combined_list_dr', 'dr_c', 'dr_t', 'dr_i')

    
def PrintAreaStats(con = ''):
    global area_mean_stdev
    
    print ('\tArea response time stats (area, mean, stdev) in [ms] for ' + con  + ':')    
    
    for item in sorted(area_mean_stdev):
         print ('\t\t' + str(item) + ' \t' + str(area_mean_stdev[item]))
    
    
def CalcTime(t1, t2):
    return int(t2)-int(t1)
    
def UpdateListForMeanValues(name, TotalErrorWithTimeouts, TotalErrorWithoutTimeouts, TotalCorrectWithTimeouts, TotalCorrectWithoutTimeouts,CountNewActiveListStr):
    global name_performance
    name_performance.update({name : [name, TotalErrorWithTimeouts, TotalErrorWithoutTimeouts, TotalCorrectWithTimeouts, TotalCorrectWithoutTimeouts,CountNewActiveListStr]})

def CalcGlobalMeanCountValues():
    global name_performance
    global name_performance_stats
    
    tmpCountCorrectWithoutTimeoutList = []
    tmpCountErrorWithTimeoutList = []
    tmpCountErrorWithoutTimeouts = []
    tmpCountCorrectWithTimeout = []
    for item in name_performance:
        tmpCountCorrectWithoutTimeoutList.append(name_performance.get(item)[4])    #correct without timeout 
        tmpCountErrorWithTimeoutList.append(name_performance.get(item)[1])    #error with timeouts
        tmpCountErrorWithoutTimeouts.append(name_performance.get(item)[2])
        tmpCountErrorWithoutTimeouts.append(name_performance.get(item)[2])
        tmpCountCorrectWithTimeout.append(name_performance.get(item)[3])

    mean_cwot = statistics.mean(tmpCountCorrectWithoutTimeoutList)
    stdev_cwot = statistics.stdev(tmpCountCorrectWithoutTimeoutList)
    normality_cwot = scipy.stats.shapiro(tmpCountCorrectWithoutTimeoutList)
    
    mean_ewt = statistics.mean(tmpCountErrorWithTimeoutList)
    stdev_ewt = statistics.stdev(tmpCountErrorWithTimeoutList)
    normality_ewt = scipy.stats.shapiro(tmpCountErrorWithTimeoutList)
    
    mean_ewot = statistics.mean(tmpCountErrorWithoutTimeouts)
    stdev_ewot = statistics.stdev(tmpCountErrorWithoutTimeouts)
    normality_ewot = scipy.stats.shapiro(tmpCountErrorWithoutTimeouts)
    
    mean_cwt = statistics.mean(tmpCountCorrectWithTimeout)
    stdev_cwt = statistics.stdev(tmpCountCorrectWithTimeout)
    normality_cwt = scipy.stats.shapiro(tmpCountCorrectWithTimeout)
    
    name_performance_stats.update({'CWOT Mean' : [mean_cwot, stdev_cwot, normality_cwot]})
    name_performance_stats.update({'EWT Mean ' : [mean_ewt, stdev_ewt, normality_ewt]})
    name_performance_stats.update({'EWOT Mean' : [mean_ewot, stdev_ewot, normality_ewot]})
    name_performance_stats.update({'CWT Mean ' : [mean_cwt, stdev_cwt, normality_cwt]})
#    print (len(tmpCountCorrectWithoutTimeoutList))
#    print (tmpCountCorrectWithoutTimeoutList)
#    print (str(meancwot) + ' : ' + str(stdevcwot) + ' : ' +str(normalitycwot))
#    
#    
#    print ()
#    print (len(tmpCountErrorWithTimeoutList))
#    print (tmpCountErrorWithTimeoutList)
#    print (str(mean_ewt) + ' : ' + str(stdev_ewt) + ' : ' +str(normality_ewt))
#    
#    print()
#    print (len(tmpCountCorrectWithoutTimeoutList))
#    print (tmpCountCorrectWithoutTimeoutList)
#    print (str(mean_ewot) + ' : ' + str(stdev_ewot) + ' : ' +str(normality_ewot))
#    
#    print ()
#    print (len(tmpCountCorrectWithTimeout))
#    print (tmpCountCorrectWithTimeout)
#    print (str(mean_cwt) + ' : ' + str(stdev_cwt) + ' : ' +str(normaliy_cwt))
#       
#    print ()
# 

def PrintGlobalMeanCountValues():
    print ('\tGlobal count stats:')
    for item in name_performance_stats:
        print ('\t\t'+item + ' : ' + str(name_performance_stats[item]))
        
def UpdateAreaStats(areas, BP_name, responsetime, isCorrect):
    #print (BP_name)
    if (BP_name not in areas.keys()):
      areas.update({BP_name : [[responsetime], [isCorrect]]})
    else:
      tmpPairOfTwoLists = areas.get(BP_name)
      
      tmpListOfResponseTimes = tmpPairOfTwoLists[0]
      tmpListOfResponseTimes.append(responsetime)
      
      tmpListOfCorrect = tmpPairOfTwoLists[1]
      tmpListOfCorrect.append(isCorrect)
  
def PrintSummary(CountErrorWrongItem,CountErrorListNotFinished,CountTimeCorrect,CountCorrect,CountTimeError,CountNewActiveListStr):
    TotalErrorWithTimouts = CountErrorWrongItem + CountErrorListNotFinished + CountTimeCorrect
    TotalErrorWithoutTimeouts = CountErrorWrongItem + CountErrorListNotFinished 

    TotalCorrectWithTimeouts = CountCorrect
    TotalCorrectWithoutTimeouts = CountCorrect - CountTimeCorrect
    
    if (True):
        print ('Summary:')
        print ('\tTotal Error w/ Timeouts    : ' + str(TotalErrorWithTimouts))
        print ('\tTotal Error w/o Timeouts   : ' + str(TotalErrorWithoutTimeouts))
        print ('\tTotal Correct w/ Timeouts  : ' + str(TotalCorrectWithTimeouts))
        print ('\tTotal Correct w/o Timeouts : ' + str(TotalCorrectWithoutTimeouts))
        print ('\tTimeout but correct        : ' + str(CountTimeCorrect))
        print ('\tTimeouts and incorrect     : ' + str(CountTimeError))
        #print (completiontimes_ls) 

    if (TotalCorrectWithoutTimeouts+TotalErrorWithTimouts != 24):
        print ('nay! not 24 but ' + str(CountNewActiveListStr))
    if (TotalCorrectWithoutTimeouts+TotalErrorWithTimouts != CountNewActiveListStr):
        print ('nay! not CountNewActiveListStr')
        
def CalcListStats(spamreader_var, con, name):
    global count_people
    global name_performance
    
    count_people +=1
    
    CountNewActiveListStr =0
    tripellistitem = 0
    tripels = {}
    CreateTriples(tripels)
    
    t1_ListStart = 0
    t2_ListEnd = 0
    SelectTextCount = 0
       
    CountCorrect = 0
    CountErrorWrongItem = 0
    CountErrorListNotFinished = 0
    CountTimeError = 0 #wrong items selected, after 10s
    CountTimeCorrect= 0 #correct items selected but after 10s
    
    completiontimes_ls = []
    tmpListName = ''
    tmpSelectedItems = []
    
    ListStart = True
    for tmprow in spamreader_var:
        #print(tmprow)
        ##### get timestamp when list appears
        if (strNewActiveList in tmprow.get('A') and ListStart): #Initiate analysis
            tmpListName = tmprow.get('B')
            ListStart = False
            t1_ListStart = tmprow.get('timestamp')
            continue
        
        if (strNewActiveList in tmprow.get('A') and not ListStart): # no call of ResetStage
            tripellistitem+=1
            CountErrorListNotFinished+=1
            SelectTextCount = 0  #reset text count (three times selected)
            tmpSelectedItems =  [] #reset selected items
            continue
        
        ##### is list finished?
        if (strResetStage in tmprow.get('A')):
            ListStart = True
            CountNewActiveListStr +=1
            t2_ListEnd = tmprow.get('timestamp')
            completiontime = CalcTime(t1_ListStart,t2_ListEnd)
            completiontimes_ls.append(completiontime)
                        
            if (SelectTextCount == 3):# did we found three selection operations?
                #print (str(tripellistitem)) 
                #print('TargetString:   ' + str(tripels.get(str(tripellistitem))))
                #print('SelectedString: ' + str(tmpSelectedItems))
                res = set(tmpSelectedItems).difference(tripels.get(str(tripellistitem)))
                #print ('Result: ' + str(res))
                if (len(res) ==0): # did P select the correct items?
                    CountCorrect +=1
                    if (completiontime>10000): #within 10sec?
                        CountTimeCorrect+=1
                        UpdateAreaStats(areas, tmpListName, completiontime, 0) #correct without timeouts

                    else:
                        UpdateAreaStats(areas, tmpListName, completiontime, 1) #correct without timeouts
                        
                else: # increase wrong item error counter
                    CountErrorWrongItem+=1               
                    UpdateAreaStats(areas, tmpListName, completiontime, 2) #correct without timeouts
                        
                    if (completiontime>10000):
                        CountTimeError+=1
               
                
            else: #increase missed error counter                
                CountErrorListNotFinished +=1
               
            tripellistitem+=1 #advance to next triple for correctness check
            SelectTextCount = 0 #reset text count (three times selected)
            tmpSelectedItems =  [] #reset selected items
            
            ##### how much time did the participant need?
               
        if (strSelectText in tmprow.get('A')):
            tmpSelectedItems.append(tmprow.get('C'))
            SelectTextCount+=1
            
            
            #####check here if selection is correct :)
            #print (tmprow.get('C'))
     
    TotalErrorWithTimeouts = CountErrorWrongItem + CountErrorListNotFinished + CountTimeCorrect
    TotalErrorWithoutTimeouts = CountErrorWrongItem + CountErrorListNotFinished 

    TotalCorrectWithTimeouts = CountCorrect
    TotalCorrectWithoutTimeouts = CountCorrect - CountTimeCorrect
 
    UpdateListForMeanValues (name, TotalErrorWithTimeouts, TotalErrorWithoutTimeouts, TotalCorrectWithTimeouts, TotalCorrectWithoutTimeouts,CountNewActiveListStr)
    ###############################################
    ###############################################
    
    #PrintSummary(CountErrorWrongItem,CountErrorListNotFinished,CountTimeCorrect,CountCorrect,CountTimeError,CountNewActiveListStr)
    