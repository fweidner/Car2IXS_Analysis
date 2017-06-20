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
        
    elif ('3D' in con): 
        print()
        List_3D_ResponseTime_Global_LS = ListSelection.GetGlobalResponseTimeList()
        AreaResponseTimeLists_3D = ListSelection.GetAreaResponseTimeList()
    
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


print ('########### 3D List #############')
#path = r'C:\Users\flarion\CloudStation\Study\Logs\3D' 
path = r'I:\CloudStation\Study\Logs\3D'
#CalcDistance(path, '3D', 'LS')
CalcListSelection(path, '3D')

print ('########### 2D List #############')
#path = r'C:\Users\flarion\CloudStation\Study\Logs\2D' 
path = r'I:\CloudStation\Study\Logs\2D'
#CalcDistance(path, '2D', 'LS')
CalcListSelection(path,'2D')

print ('########### 3D Change #############')
#path = r'C:\Users\flarion\CloudStation\Study\LogsWD\3D' 
#path = r'I:\CloudStation\Study\Logs\3D'
#CalcDistance(path, '2D', 'CD')
#CalcChangeDetection(path, '3D')

print ('########### 2D Change #############')
#path = r'C:\Users\flarion\CloudStation\Study\LogsWD\2D' 
#path = r'I:\CloudStation\Study\Logs\2D'
#CalcDistance(path, '2D', 'CD')
#CalcChangeDetection(path, '2D')


#print ('######################################################')
#print ('############# Statistic Change Detection ############# ')
#print ('######################################################')
#
#print ("Statistics for Overall Response Time: ")
#
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_OverallResponseTime, List_3D_OverallResponseTime, 'two-sided', True)
#print()
#
#print ("Statistics for Area Response Time (ul): ")
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ul_ResponseTime, List_3D_ul_ResponseTime, 'two-sided', False)
#print ("Statistics for Area Response Time (uc): ")
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_uc_ResponseTime, List_3D_uc_ResponseTime, 'two-sided', False)
#print ("Statistics for Area Response Time (ur): ")
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ur_ResponseTime, List_3D_ur_ResponseTime, 'two-sided', False)
#print ("Statistics for Area Response Time (dr): ")
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_dr_ResponseTime, List_3D_dr_ResponseTime, 'two-sided', False)
#
#
#print()
#
#print ("Statistics for Overall Count (Correct, Incorrect, Missed):")
#print ('\tCorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_OverallCount_correct, List_3D_OverallCount_correct, 'two-sided')
#print ('\tIncorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_OverallCount_incorrect, List_3D_OverallCount_incorrect, 'two-sided')
#print ('\tMissed:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_OverallCount_missed, List_3D_OverallCount_missed, 'two-sided')
#
#print()
#
#print ("Statistics for Area Count (Correct, Incorrect, Missed):")
#print ('\tUL:')
#print ('\tCorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UL[0], List_3D_AreaCount_UL[0], 'two-sided')
#print ('\tIncorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UL[1], List_3D_AreaCount_UL[1], 'two-sided')
#print ('\tMissed:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UL[2], List_3D_AreaCount_UL[2], 'two-sided')
#
#print ('\tUC:')
#print ('\tCorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UC[0], List_3D_AreaCount_UC[0], 'two-sided')
#print ('\tIncorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UC[1], List_3D_AreaCount_UC[1], 'two-sided')
#print ('\tMissed:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UC[2], List_3D_AreaCount_UC[2], 'two-sided')
#
#print ('\tUR:')
#print ('\tCorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UR[0], List_3D_AreaCount_UR[0], 'two-sided')
#print ('\tIncorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UR[1], List_3D_AreaCount_UR[1], 'two-sided')
#print ('\tMissed:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_UR[2], List_3D_AreaCount_UR[2], 'two-sided')
#
#print ('\tDR:')
#print ('\tCorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_DR[0], List_3D_AreaCount_DR[0], 'two-sided')
#print ('\tIncorrect:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_DR[1], List_3D_AreaCount_DR[1], 'two-sided')
#print ('\tMissed:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_AreaCount_DR[2], List_3D_AreaCount_DR[2], 'two-sided')
#
#print()
#print ('Statistics for Overall Distance:')
#print ('\tin [m]:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_Distance_CD, List_3D_Distance_CD, 'two-sided')
#
#print()
#print ('\tin [ms]:')
#print ('\t\tIn Target Zone:')
#FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(List_2D_Times_CD[0], List_3D_Times_CD[0])
#print ('\t\tOutside Target Zone:')
#FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(List_2D_Times_CD[1], List_3D_Times_CD[1])

print ('######################################################')
print ('#############  Statistic List Selection  #############')
print ('######################################################')

print ("Statistics for Global Task Completion Time: ")
print('\tCorrect')
FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ResponseTime_Global_LS[0], List_3D_ResponseTime_Global_LS[0], 'two-sided', False)
print('\tIncorrect')
FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ResponseTime_Global_LS[1], List_3D_ResponseTime_Global_LS[1], 'two-sided', False)
print('\tTimeout')
FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_ResponseTime_Global_LS[2], List_3D_ResponseTime_Global_LS[2], 'two-sided', False)

print ("Statistics for Area Task Completion Time: ")
print ('\tUL:')
print ('\tCorrect:')
FinalStatistics.CalcParametric_WelshWithShapiroAndLevene(AreaResponseTimeLists_2D.get('ul')[0], AreaResponseTimeLists_3D.get('ul')[0], False)

print ('\tIncorrect:')
FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('ul')[1], AreaResponseTimeLists_3D.get('ul')[1], 'two-sided', False)

print ('\tMissed:')
FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(AreaResponseTimeLists_2D.get('ul')[2], AreaResponseTimeLists_3D.get('ul')[2], 'two-sided', False)

print ('\tUC:')
print ('\tCorrect:')

print ('\tIncorrect:')

print ('\tMissed:')

print ('\tUR:')
print ('\tCorrect:')

print ('\tIncorrect:')

print ('\tMissed:')

print ('\tDR:')
print ('\tCorrect:')

print ('\tIncorrect:')

print ('\tMissed:')




















#print()
#print ('Statistics for Overall Distance:')
#print ('\tin [m]:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_Distance_LS, List_3D_Distance_LS, 'two-sided')
#
#print()
#print ('\tin [ms]:')
#print ('\t\tIn Target Zone:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_Times_LS[0], List_3D_Times_LS[0])
#print ('\t\tOutside Target Zone:')
#FinalStatistics.CalcNonParametric_MannWhitneyWithShapiro(List_2D_Times_LS[1], List_3D_Times_LS[1])
