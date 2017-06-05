# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 11:09:40 2017

@author: fweidner
"""

import csv
import ChangeDetection
import ListSelection
import os

def analyzeTheShitOutOfIt(file, filewriter):
    #with open ('CD_2017.06.01-13.06.39.csv', 'r') as csvfile:
    with open (file, 'r') as csvfile:
        fieldnames = ["timestamp", "A", "B", "C"]
        spamreader = csv.DictReader(csvfile, fieldnames, delimiter=';')

        #skip header
        next(spamreader)
        next(spamreader)
        next(spamreader)
        next(spamreader)
        next(spamreader)
        next(spamreader)
        next(spamreader)
        next(spamreader)
        next(spamreader)
        #ResponseTimesFunctions.GetResponseTimesForCorrectValues(spamreader)
        ListSelection.LS_CalcCountErrorAndCorrect(spamreader, filewriter_LS_Counts)

##################################################

# analyzeTheShitOutOfIt()

path = r'C:\Users\flarion\CloudStation\Study\Logs' 

with open('LS_CalcCounts.csv', 'w', newline='') as csvfile:
    filewriter_LS_Counts = csv.writer(csvfile, delimiter=';')
   
    CountExecution =0
    for (path, dirs, files) in os.walk(path):
        print ('Path:', path)
    
        #print ('\nDirs:')
        #for d in dirs:
        #    print ('\t'+d)
    
        #print ('\nFiles:')
        for f in files:
            if ('LS' in f):
                file = path+'\\'+f
                b = os.path.getsize(file)
                if (b<20000):
                    analyzeTheShitOutOfIt(file, filewriter_LS_Counts)
                    CountExecution +=1
        print ('----')

#    analyzeTheShitOutOfIt(r'C:\Users\flarion\CloudStation\Study\Car2IXS_Analysis\LS_2017.06.01-17.21.49.csv', filewriter_LS_Counts)
##################################################

  
        
        
        

        
        
        
        

