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

#path = r'C:\Users\flarion\CloudStation\Study\Car2IXS_Analysis'

def CalcDistance(path, con, strTask):
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
    print()
    
def CalcListSelection(path):
    print()
    print('Calculating List Selection Performance!')
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
    ListSelection.Reset()

    
def CalcChangeDetection(path):
    print()
    print('Calculating Change Detection Performance!')
    
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
    
##################################################

print ('########### 3D List #############')
path = r'C:\Users\flarion\CloudStation\Study\Logs\3D' 
#CalcDistance(path, '3D', 'LS')
CalcListSelection(path)

print ('########### 2D List #############')
path = r'C:\Users\flarion\CloudStation\Study\Logs\2D' 
#CalcDistance(path, '2D', 'LS')
#CalcListSelection(path)

print ('########### 3D Change #############')
path = r'C:\Users\flarion\CloudStation\Study\Logs\3D' 
#CalcDistance(path, '2D', 'CD')
#CalcChangeDetection(path)

print ('########### 2D Change #############')
path = r'C:\Users\flarion\CloudStation\Study\Logs\2D' 
#CalcDistance(path, '2D', 'CD')
#CalcChangeDetection(path)


