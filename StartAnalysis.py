# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 11:09:40 2017

@author: fweidner
"""

import csv
import ChangeDetection
import ListSelection
import DistanceKeeping
import os

import FinalStatistics


#Lists for Statistics of CD Response Time
List_2D_OverallResponseTime = []
List_3D_OverallResponseTime = []

List_2D_ul_ResponseTime = []
List_2D_uc_ResponseTime = []
List_2D_ur_ResponseTime = []
List_2D_dr_ResponseTime = []


List_3D_ul_ResponseTime = []
List_3D_uc_ResponseTime = []
List_3D_ur_ResponseTime = []
List_3D_dr_ResponseTime = []

#List for Statistics of CD Count:
List_2D_OverallCount_correct = []
List_2D_OverallCount_incorrect = []
List_2D_OverallCount_missed = []

List_3D_OverallCount_correct = []
List_3D_OverallCount_incorrect = []
List_3D_OverallCount_missed = []
    
List_2D_AreaCount_UL = [[],[],[]]
List_2D_AreaCount_UC = [[],[],[]]
List_2D_AreaCount_UR = [[],[],[]]
List_2D_AreaCount_DR = [[],[],[]]

List_3D_AreaCount_UL = [[],[],[]]
List_3D_AreaCount_UC = [[],[],[]]
List_3D_AreaCount_UR = [[],[],[]]
List_3D_AreaCount_DR = [[],[],[]]


List_2D_InTargetZone_CD = []
List_2D_OutOfTargetZone_CD = []
List_2D_Distance_CD = []
List_2D_Distance_LS = []

List_3D_InTargetZone_CD = []
List_3D_OutOfTargetZone_CD = []
List_3D_Distance_CD = []
List_3D_Distance_LS = []

List_2D_Times_CD = [[],[]]
List_3D_Times_CD = [[],[]]

List_2D_Times_LS = [[],[]]
List_3D_Times_LS = [[],[]]

List_2D_ResponseTime_Global_LS = [[],[],[]]
List_2D_ResponseTime_Area_LS_ul = [[],[],[]]
List_2D_ResponseTime_Area_LS_uc = [[],[],[]]
List_2D_ResponseTime_Area_LS_ur = [[],[],[]]
List_2D_ResponseTime_Area_LS_dr = [[],[],[]]

List_3D_ResponseTime_Global_LS = [[],[],[]]
List_3D_ResponseTime_Area_LS_ul = [[],[],[]]
List_3D_ResponseTime_Area_LS_uc = [[],[],[]]
List_3D_ResponseTime_Area_LS_ur = [[],[],[]]
List_3D_ResponseTime_Area_LS_dr = [[],[],[]]

AreaResponseTimeLists_2D = {}
AreaResponseTimeLists_3D = {}

GlobalCountStats_3D = {}
GlobalCountStats_2D = {}

AreaCountStats_2D = {}
AreaCountStats_3D = {}

def SkipHeader(spamreader): 
    next(spamreader)
    next(spamreader)
    next(spamreader)
    #print(str(next(spamreader)))
    next(spamreader)
    next(spamreader)
    next(spamreader)
    next(spamreader)
    next(spamreader)
    next(spamreader)

def CalcListStats(file, name, con):
    #with open ('CD_2017.06.01-13.06.39.csv', 'r') as csvfile:
    with open (file, 'r') as csvfile:
        #print (file)
        fieldnames = ["timestamp", "A", "B", "C"]
        spamreader = csv.DictReader(csvfile, fieldnames, delimiter=';')

        SkipHeader(spamreader)
        #ResponseTimesFunctions.GetResponseTimesForCorrectValues(spamreader)
        ListSelection.CalcListStats(spamreader, con, name)

#calculates mean values, stdev for distance and times in and out of target distance zone
def Calculate_DistanceKeeping_C2S_Stats(file, name = 'defaultname', condition_var = '', task=''):
     with open (file, 'r') as csvfile:
        fieldnames = ["timestamp", "A", "B", "C"]
        spamreader = csv.DictReader(csvfile, fieldnames, delimiter=';')
        SkipHeader(spamreader)
        DistanceKeeping.CalcDistanceStats(spamreader, name, condition_var, task)
      
        #                   CalcCDStats(file, name, con)

def CalcCDStats(file, name ='', condition_var=''):
    with open (file, 'r') as csvfile:
        fieldnames = ["timestamp", "A", "B", "C"]
        spamreader = csv.DictReader(csvfile, fieldnames, delimiter=';')
        SkipHeader(spamreader)
        ChangeDetection.GetResponseTimesForCorrectValues(spamreader,name,condition_var)
    
        
        
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################

#path = r'C:\Users\flarion\CloudStation\Study\Car2IXS_Analysis'

def CalcDistance(path, con, strTask):
    global List_2D_InTargetZone
    global List_2D_OutOfTargetZone_CD
    global List_2D_Distance_CD
    global List_2D_Distance_LS
    
    global List_3D_InTargetZone_CD
    global List_3D_OutOfTargetZone_CD
    global List_3D_Distance_CD
    global List_3D_Distance_LS

        
    global List_2D_Times_CD
    global List_3D_Times_CD
    global List_2D_Times_LS
    global List_3D_Times_LS
    
    DistanceKeeping.Reset()
    
    print()
    print('Calculating Distance!')
    CountExecution =0
    for (path, dirs, files) in os.walk(path):
        #print ('Path:', path)
        splits = path.split(sep='\\')
        splits_len = len(splits)
        name = splits[splits_len-1]
        con = splits[splits_len-2]
        #print (name + ' : ' + con)
        
        for f in files:
            file = path+'\\'+f
            b = os.path.getsize(file)
            if (b>20000):
                if (strTask in f):
                    Calculate_DistanceKeeping_C2S_Stats(file, name, con, strTask)
                    CountExecution+=1    
    
        #print ('----')
    
    DistanceKeeping.CalcDistancesStatPerParticipant()
    #DistanceKeeping.PrintTimes()
    #DistanceKeeping.PrintMeanDistances()
    DistanceKeeping.CalcOverallDistanceStats()
    DistanceKeeping.PrintOverallDistanceStats(con, strTask)
    DistanceKeeping.CalcAndPrintOverallTimeStats()
    
    if ('3D' in con):
        if ('LS' in strTask):
            List_3D_Distance_LS= DistanceKeeping.GetList_DistanceOverall()
            List_3D_Times_LS[0], List_3D_Times_LS[1] = DistanceKeeping.GetList_TimesOverall()
            
        elif ('CD' in strTask):
            List_3D_Distance_CD = DistanceKeeping.GetList_DistanceOverall()
            List_3D_Times_CD[0], List_3D_Times_CD[1] = DistanceKeeping.GetList_TimesOverall()
    elif ('2D' in con):
        if ('LS' in strTask):
            List_2D_Distance_LS = DistanceKeeping.GetList_DistanceOverall()
            List_2D_Times_LS[0], List_2D_Times_LS[1] = DistanceKeeping.GetList_TimesOverall()
        elif ('CD' in strTask):
            List_2D_Distance_CD = DistanceKeeping.GetList_DistanceOverall()
            List_2D_Times_CD[0], List_2D_Times_CD[1] = DistanceKeeping.GetList_TimesOverall()


            
    print()
    
def CalcListSelection(path, con):
    print()
    print('Calculating List Selection Performance!')
    
    global List_2D_ResponseTime_Global_LS
    global List_2D_ResponseTime_Area_LS_ul
    global List_2D_ResponseTime_Area_LS_uc
    global List_2D_ResponseTime_Area_LS_ur
    global List_2D_ResponseTime_Area_LS_dr
    
    global List_3D_ResponseTime_Global_LS
    global List_3D_ResponseTime_Area_LS_ul
    global List_3D_ResponseTime_Area_LS_uc
    global List_3D_ResponseTime_Area_LS_ur
    global List_3D_ResponseTime_Area_LS_dr
    
    global AreaResponseTimeLists_2D
    global AreaResponseTimeLists_3D
    global GlobalCountStats_2D
    global GlobalCountStats_3D
    
    global AreaCountStats_2D
    global AreaCountStats_3D
    
    CountExecution =0
    con = ''
    for (path, dirs, files) in os.walk(path):
        #print ('Path:', path)
        splits = path.split(sep='\\')
        splits_len = len(splits)
        name = splits[splits_len-1]
        con = splits[splits_len-2]
        #print (name + ' : ' + con)
        
        for f in files:
            file = path+'\\'+f
            b = os.path.getsize(file)
            if (b<20000):
                if ('LS' in f):
                    CalcListStats(file, name, con)
                    CountExecution+=1    
    
        #print ('----')

    ListSelection.PrepareForAreaCalculation()
    
    ListSelection.CalcAreaStats(con)
    ListSelection.PrintAreaStats(con)
    
    ListSelection.CalcGlobalStats()
    ListSelection.PrintGlobalStats()
    
    ListSelection.CalcGlobalMeanCountValues()
    ListSelection.PrintGlobalMeanCountValues()
    
    ListSelection.CalcGlobalAreaCountStats()
    
    if ('2D' in con):   
        print()
        List_2D_ResponseTime_Global_LS = ListSelection.GetGlobalResponseTimeList()
        AreaResponseTimeLists_2D = ListSelection.GetAreaResponseTimeList()
        GlobalCountStats_2D = ListSelection.GetGlobalCountLists()
        AreaCountStats_2D = ListSelection.GetAreaCountLists()
        
    elif ('3D' in con): 
        print()
        List_3D_ResponseTime_Global_LS = ListSelection.GetGlobalResponseTimeList()
        AreaResponseTimeLists_3D = ListSelection.GetAreaResponseTimeList()
        GlobalCountStats_3D = ListSelection.GetGlobalCountLists()
        AreaCountStats_3D = ListSelection.GetAreaCountLists()
    
    ListSelection.Reset()
    
def CalcChangeDetection(path, con):
    print()
    print('Calculating Change Detection Performance!')
    
    global List_2D_OverallResponseTime
    global List_2D_ul_ResponseTime
    global List_2D_uc_ResponseTime
    global List_2D_ur_ResponseTime
    global List_2D_dr_ResponseTime
    
    global List_3D_OverallResponseTime
    global List_3D_ul_ResponseTime
    global List_3D_uc_ResponseTime
    global List_3D_ur_ResponseTime
    global List_3D_dr_ResponseTime
    
    global List_2D_OverallCount_correct
    global List_2D_OverallCount_incorrect
    global List_2D_OverallCount_missed

    global List_3D_OverallCount_correct
    global List_3D_OverallCount_incorrect
    global List_3D_OverallCount_missed
    
    global List_2D_AreaCount_UL 
    global List_2D_AreaCount_UC 
    global List_2D_AreaCount_UR 
    global List_2D_AreaCount_DR 

    global List_3D_AreaCount_UL 
    global List_3D_AreaCount_UC 
    global List_3D_AreaCount_UR 
    global List_3D_AreaCount_DR 
    
    global List_2D_Distance
    global List_3D_Distance

    
    
    CountExecution =0
    
    ChangeDetection.Reset()
    
    for (path, dirs, files) in os.walk(path):
       #print ('Path:', path)
       splits = path.split(sep='\\')
       splits_len = len(splits)
       name = splits[splits_len-1]
       con = splits[splits_len-2]
       #print (name + ' : ' + con)
       
       for f in files:
           file = path+'\\'+f
           b = os.path.getsize(file)
           if (b<20000):
               if ('CD' in f):
                   CalcCDStats(file, name, con)
                   CountExecution+=1    
    
       #print ('----')

    #ChangeDetection.PrintGlobalResponseTimes()
    ChangeDetection.CalcGlobalResponseTimeStats()
    ChangeDetection.PrintGlobalResponseTimeStats()
    ChangeDetection.CalcGlobalCountStats()
    ChangeDetection.PrintGlobalCountStats()
    
    if ('2D' in con):
        List_2D_OverallResponseTime = ChangeDetection.GetList_OverallResponseTime()

        List_2D_ul_ResponseTime, List_2D_uc_ResponseTime, List_2D_ur_ResponseTime, List_2D_dr_ResponseTime= ChangeDetection.GetList_AreaResponseTime()
        List_2D_OverallCount_correct, List_2D_OverallCount_incorrect, List_2D_OverallCount_missed = ChangeDetection.GetList_OverallCount()
        List_2D_AreaCount_UL = ChangeDetection.GetList_AreaCount('UL')
        List_2D_AreaCount_UC = ChangeDetection.GetList_AreaCount('UC')
        List_2D_AreaCount_UR = ChangeDetection.GetList_AreaCount('UR')
        List_2D_AreaCount_DR = ChangeDetection.GetList_AreaCount('DR')

    
    if ('3D' in con):
        List_3D_OverallResponseTime = ChangeDetection.GetList_OverallResponseTime()
        List_3D_ul_ResponseTime, List_3D_uc_ResponseTime, List_3D_ur_ResponseTime, List_3D_dr_ResponseTime= ChangeDetection.GetList_AreaResponseTime()
        List_3D_OverallCount_correct, List_3D_OverallCount_incorrect, List_3D_OverallCount_missed = ChangeDetection.GetList_OverallCount()
        List_3D_AreaCount_UL = ChangeDetection.GetList_AreaCount('UL')
        List_3D_AreaCount_UC = ChangeDetection.GetList_AreaCount('UC')
        List_3D_AreaCount_UR = ChangeDetection.GetList_AreaCount('UR')
        List_3D_AreaCount_DR = ChangeDetection.GetList_AreaCount('DR')
        

    
##################################################
##################################################
##################################################
##################################################

Do_Distance_LS = True
Do_Distance_CD = True
Do_Performance_LS = True
Do_Performance_CD = True



print ('########### 3D List #############')
#path = r'C:\Users\flarion\CloudStation\Study\Logs\3D' 
path = r'D:\CloudStation\Study\Logs\3D'
#path = r'I:\CloudStation\Study\Logs\3D'

if (Do_Distance_LS):
    CalcDistance(path, '3D', 'LS')
if (Do_Performance_LS):
    CalcListSelection(path, '3D')

print ('########### 2D List #############')
#path = r'C:\Users\flarion\CloudStation\Study\Logs\2D' 
path = r'D:\CloudStation\Study\Logs\2D'
#path = r'I:\CloudStation\Study\Logs\2D'
if (Do_Distance_LS):
    CalcDistance(path, '2D', 'LS')
if (Do_Performance_LS):
    CalcListSelection(path,'2D')

print ('########### 3D Change #############')
#path = r'C:\Users\flarion\CloudStation\Study\LogsWD\3D' 
#path = r'I:\CloudStation\Study\Logs\3D'
path = r'D:\CloudStation\Study\Logs\3D'
if (Do_Distance_CD):
    CalcDistance(path, '2D', 'CD')
if (Do_Performance_CD):
    CalcChangeDetection(path, '3D')

print ('########### 2D Change #############')
#path = r'C:\Users\flarion\CloudStation\Study\LogsWD\2D' 
#path = r'I:\CloudStation\Study\Logs\2D'
path = r'D:\CloudStation\Study\Logs\2D'
if (Do_Distance_CD):
    CalcDistance(path, '2D', 'CD')
if (Do_Performance_CD):
    CalcChangeDetection(path, '2D')


means3D, means2D, stdev2D, stdev3D = [], [], [],[]

print ('######################################################')
print ('######################################################')
print ('############# Statistic Change Detection #############')
print ('######################################################')
print ('######################################################')
print()
print ('######################################################')
if (Do_Performance_CD):
    print ("Statistics for Overall Response Time: ")
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_OverallResponseTime, List_3D_OverallResponseTime, 'two-sided', True)
    print()
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    
    print ('######################################################')
    print ("Statistics for Area Response Time (ul): ")
    mean2d, stdev2d, mean3d, stdev3d =FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ul_ResponseTime, List_3D_ul_ResponseTime, 'two-sided', False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ("Statistics for Area Response Time (uc): ")
    mean2d, stdev2d, mean3d, stdev3d =FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_uc_ResponseTime, List_3D_uc_ResponseTime, 'two-sided', False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ("Statistics for Area Response Time (ur): ")
    mean2d, stdev2d, mean3d, stdev3d =FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ur_ResponseTime, List_3D_ur_ResponseTime, 'two-sided', False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ("Statistics for Area Response Time (dr): ")
    mean2d, stdev2d, mean3d, stdev3d =FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_dr_ResponseTime, List_3D_dr_ResponseTime, 'two-sided', False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    
    FinalStatistics.plotBarChartWithStdDevDouble(5,means2D, means3D, stdev2D, stdev3D,  ['ul', 'uc','ur','dr','t'],'Mean Response Time and StDev in [ms]')
    means3D, means2D, stdev2D, stdev3D = [], [], [],[]

    print()
   
    print ('######################################################')
    print ("Statistics for Area Count (Correct, Incorrect, Missed):")
    print ('\tUL:')
    print ('\tCorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UL[0], List_3D_AreaCount_UL[0], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tIncorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UL[1], List_3D_AreaCount_UL[1], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tMissed:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UL[2], List_3D_AreaCount_UL[2], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tUC:')
    print ('\tCorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UC[0], List_3D_AreaCount_UC[0], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tIncorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UC[1], List_3D_AreaCount_UC[1], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tMissed:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UC[2], List_3D_AreaCount_UC[2], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tUR:')
    print ('\tCorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UR[0], List_3D_AreaCount_UR[0], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tIncorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UR[1], List_3D_AreaCount_UR[1], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tMissed:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UR[2], List_3D_AreaCount_UR[2], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tDR:')
    print ('\tCorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_DR[0], List_3D_AreaCount_DR[0], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tIncorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_DR[1], List_3D_AreaCount_DR[1], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tMissed:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_DR[2], List_3D_AreaCount_DR[2], 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)

    FinalStatistics.plotBarChartWithStdDevDouble(12, means2D, means3D, stdev2D, stdev3D,  ['ul_c', 'ul_i', 'ul_t',   'uc_c', 'uc_i','uc_t',  'ur_c', 'ur_i', 'ur_t',  'dr_c', 'dr_i','dr_t'],'Mean Count of Items')
    means3D, means2D, stdev2D, stdev3D = [], [], [],[]

     
    print ('######################################################')
    print ("Statistics for Overall Count (Correct, Incorrect, Missed):")
    print ('\tCorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_OverallCount_correct, List_3D_OverallCount_correct, 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tIncorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_OverallCount_incorrect, List_3D_OverallCount_incorrect, 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tMissed:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_OverallCount_missed, List_3D_OverallCount_missed, 'two-sided')
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print()
 
    
   
    FinalStatistics.plotBarChartWithStdDevDouble(3, means2D, means3D, stdev2D, stdev3D,  ['c', 'i','m'],'Mean Count of Items')
    means3D, means2D, stdev2D, stdev3D = [], [], [],[]

     
if (Do_Distance_CD):
    print()
    print ('######################################################')
    print ('Statistics for Overall Distance:')
    print ('\tin [m]:')
    FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_Distance_CD, List_3D_Distance_CD, 'two-sided')
    print()
    print ('\tin [ms]:')
    print ('\t\tIn Target Zone:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(List_2D_Times_CD[0], List_3D_Times_CD[0])
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\t\tOutside Target Zone:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(List_2D_Times_CD[1], List_3D_Times_CD[1])
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print()
    
    FinalStatistics.plotBarChartWithStdDevDouble(2, means2D, means3D, stdev2D, stdev3D,  ['In Target Zone', 'Outside Target Zone'],'Mean Times in [s]')
    means3D, means2D, stdev2D, stdev3D = [], [], [], []


print ('######################################################')
print ('######################################################')
print ('#############  Statistic List Selection  #############')
print ('######################################################')
print ('######################################################')
print()

if (Do_Performance_LS):
    print ('######################################################')
    print ("Statistics for Global Task Completion Time: ")
    print('\tCorrect')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ResponseTime_Global_LS[0], List_3D_ResponseTime_Global_LS[0], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print('\tIncorrect')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ResponseTime_Global_LS[1], List_3D_ResponseTime_Global_LS[1], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print('\tTimeout')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ResponseTime_Global_LS[2], List_3D_ResponseTime_Global_LS[2], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print()
    FinalStatistics.plotBarChartWithStdDevDouble(3,means2D, means3D, stdev2D, stdev3D,  ['Correct', 'Incorrect','Timeout'],'Mean Task Completion Time in [s]',.27,1.5)
    means3D, means2D, stdev2D, stdev3D = [], [], [],[]


    print ('######################################################')
    print ("Statistics for Area Task Completion Time: ")
    print ('\tUL:')
    print ('\t\tCorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(AreaResponseTimeLists_2D.get('ul')[0], AreaResponseTimeLists_3D.get('ul')[0], False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\t\tIncorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('ul')[1], AreaResponseTimeLists_3D.get('ul')[1], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\t\tMissed:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('ul')[2], AreaResponseTimeLists_3D.get('ul')[2], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\tUC:')
    print ('\t\tCorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('uc')[0], AreaResponseTimeLists_3D.get('uc')[0], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\t\tIncorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('uc')[1], AreaResponseTimeLists_3D.get('uc')[1], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\t\tMissed:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('uc')[2], AreaResponseTimeLists_3D.get('uc')[2], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\tUR:')
    print ('\t\tCorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(AreaResponseTimeLists_2D.get('ur')[0], AreaResponseTimeLists_3D.get('ur')[0], False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\t\tIncorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('ur')[1], AreaResponseTimeLists_3D.get('ur')[1], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\t\tMissed:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('ur')[2], AreaResponseTimeLists_3D.get('ur')[2], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\tDR:')
    print ('\t\tCorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(AreaResponseTimeLists_2D.get('dr')[0], AreaResponseTimeLists_3D.get('dr')[0], False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\t\tIncorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(AreaResponseTimeLists_2D.get('dr')[1], AreaResponseTimeLists_3D.get('dr')[1], False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print ('\t\tMissed:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('dr')[2], AreaResponseTimeLists_3D.get('dr')[2], 'two-sided', False)
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)
    print()
    
    FinalStatistics.plotBarChartWithStdDevDouble(12, means2D, means3D, stdev2D, stdev3D,  ['ul_c', 'ul_i', 'ul_t',   'uc_c', 'uc_i','uc_t',  'ur_c', 'ur_i', 'ur_t',  'dr_c', 'dr_i','dr_t'],'Mean Task Completion Time in [s]', 0.27,1.5)
    means3D, means2D, stdev2D, stdev3D = [], [], [],[]
    
    print ('######################################################')
    print ("Statistics for Global Count: ")
    print ('\tCorrect without timeout:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(GlobalCountStats_2D.get('CWOT'), GlobalCountStats_3D.get('CWOT'), 'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tCorrect with timeout:')
    #mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(GlobalCountStats_2D.get('CWT'), GlobalCountStats_3D.get('CWT'), 'two-sided', False, False)
    #means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tError without timeout:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(GlobalCountStats_2D.get('EWOT'), GlobalCountStats_3D.get('EWOT'), 'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print ('\tError with timeout:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(GlobalCountStats_2D.get('T'), GlobalCountStats_3D.get('T'), False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print()
    
    FinalStatistics.plotBarChartWithStdDevDouble(3, means2D, means3D, stdev2D, stdev3D,  ['c', 'i', 't'],'Mean Count of Items', 0.27,1.5)
    means3D, means2D, stdev2D, stdev3D = [], [], [],[]
  
    
    print ('######################################################')
    print ("Statistics for Area Count: ")
    print('\tul ')
    print('\t\tcorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('ul')[0], AreaCountStats_3D.get('ul')[0],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print('\t\ttimeout:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('ul')[1], AreaCountStats_3D.get('ul')[1],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print('\t\tincorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('ul')[2], AreaCountStats_3D.get('ul')[2],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print()
    print('\tuc ')
    print('\t\tcorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('uc')[0], AreaCountStats_3D.get('uc')[0],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print('\t\ttimeout:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('uc')[1], AreaCountStats_3D.get('uc')[1],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print('\t\tincorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('uc')[2], AreaCountStats_3D.get('uc')[2],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print()
    print('\tur ')
    print('\t\tcorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('ur')[0], AreaCountStats_3D.get('ur')[0],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print('\t\ttimeout:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('ur')[1], AreaCountStats_3D.get('ur')[1],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print('\t\tincorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('ur')[2], AreaCountStats_3D.get('ur')[2],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print()
    print('\tdr ')
    print('\t\tcorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('dr')[0], AreaCountStats_3D.get('dr')[0],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print('\t\ttimeout:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('dr')[1], AreaCountStats_3D.get('dr')[1],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print('\t\tincorrect:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaCountStats_2D.get('dr')[2], AreaCountStats_3D.get('dr')[2],'two-sided', False, False)
    means2D.append(mean2d), means3D.append(mean3d), stdev2D.append(stdev2d), stdev3D.append(stdev3d)
    print()
    
    FinalStatistics.plotBarChartWithStdDevDouble(12, means2D, means3D, stdev2D, stdev3D,  ['ul_c', 'ul_i', 'ul_t',   'uc_c', 'uc_i','uc_t',  'ur_c', 'ur_i', 'ur_t',  'dr_c', 'dr_i','dr_t'],'Mean Count of Items', 0.27,1.5)
    means3D, means2D, stdev2D, stdev3D = [], [], [],[]
 

if (Do_Distance_LS):
    print ('######################################################')
    print ('Statistics for Overall Distance:')
    print ('\tin [m]:')
    FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_Distance_LS, List_3D_Distance_LS, 'two-sided')
    print()
    print ('\tin [ms]:')
    print ('\t\tIn Target Zone:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_Times_LS[0], List_3D_Times_LS[0])
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)

    print ('\t\tOutside Target Zone:')
    mean2d, stdev2d, mean3d, stdev3d = FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_Times_LS[1], List_3D_Times_LS[1])
    means2D.append(mean2d/1000), means3D.append(mean3d/1000), stdev2D.append(stdev2d/1000), stdev3D.append(stdev3d/1000)

    FinalStatistics.plotBarChartWithStdDevDouble(2, means2D, means3D, stdev2D, stdev3D,  ['In Target Zone', 'Outside Target Zone'],'Mean Times in [s]')
    means3D, means2D, stdev2D, stdev3D = [], [], [], []
