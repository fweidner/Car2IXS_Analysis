# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 11:09:40 2017

@author: fweidner
"""


responsetimes_cd = []

count_positives = 0
count_missed = 0
count_wrongpress =0



import csv
import ResponseTimesFunctions

fieldnames = ["timestamp", "A", "B", "C"]
with open ('CD_2017.06.01-13.06.39.csv', 'r') as csvfile:
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

    ResponseTimesFunctions.GetResponseTimesForCorrectValues(spamreader)
  
        
        
        

        
        
        
        

