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

strName = ''

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

def Calculate_LS_UI_Stats(file, filewriter):
    #with open ('CD_2017.06.01-13.06.39.csv', 'r') as csvfile:
    with open (file, 'r') as csvfile:
        fieldnames = ["timestamp", "A", "B", "C"]
        spamreader = csv.DictReader(csvfile, fieldnames, delimiter=';')

        SkipHeader(spamreader)
        #ResponseTimesFunctions.GetResponseTimesForCorrectValues(spamreader)
        ListSelection.LS_CalcCountErrorAndCorrect(spamreader, filewriter_LS_Counts)

def Calculate_DistanceKeeping_C2S_Stats(file, name = 'defaultname'):
     with open (file, 'r') as csvfile:
        fieldnames = ["timestamp", "A", "B", "C"]
        spamreader = csv.DictReader(csvfile, fieldnames, delimiter=';')
        SkipHeader(spamreader)
        DistanceKeeping.CalcDistanceStats(spamreader, name)
      
##################################################


#path = r'C:\Users\flarion\CloudStation\Study\Car2IXS_Analysis'

def CalcDistance(path):
    CountExecution =0
    for (path, dirs, files) in os.walk(path):
        #print ('Path:', path)
        splits = path.split(sep='\\')
        splits_len = len(splits)
        name = splits[splits_len-1]
        #print (name)
        for f in files:
         
            if ('LS' in f):
                file = path+'\\'+f
                b = os.path.getsize(file)
                if (b<20000):
         
                    #Calculate_LS_UI_Stats(file, filewriter_LS_Counts)
                    CountExecution +=1
                else:
                    Calculate_DistanceKeeping_C2S_Stats(file, name)
                    break
            
    
        print ('----')
    
    DistanceKeeping.ReduceDistanceStats()


#with open('LS_CalcCounts.csv', 'w', newline='') as csvfile:
#    filewriter_LS_Counts = csv.writer(csvfile, delimiter=';')
#    file = r'C:\Users\flarion\CloudStation\Study\Car2IXS_Analysis\LS_2017.06.06-17.27.21.csv'
#    with open (file, 'r') as csvfile:
#        fieldnames = ["timestamp", "A", "B", "C"]
#        spamreader = csv.DictReader(csvfile, fieldnames, delimiter=';')
#        SkipHeader(spamreader)
#    
#        Calculate_LS_UI_Stats(file, filewriter_LS_Counts)

#file = r'C:\Users\flarion\CloudStation\Study\Car2IXS_Analysis\CD_2017.06.06-17.03.38.csv'
#with open (file, 'r') as csvfile:
#    fieldnames = ["timestamp", "A", "B", "C"]
#    spamreader = csv.DictReader(csvfile, fieldnames, delimiter=';')
#    SkipHeader(spamreader)
#
#    ChangeDetection.GetResponseTimesForCorrectValues(spamreader)

##################################################
path = r'C:\Users\flarion\CloudStation\Study\Logs' 
CalcDistance(path)
        
        

        
        
        
        

