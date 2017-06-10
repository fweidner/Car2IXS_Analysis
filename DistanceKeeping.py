# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:22:20 2017

@author: fweidner
"""

import statistics
import scipy
from scipy import stats

strDistance = 'Distance'
meanOverallInM = 0
stdevOverallInM = 0
distance_normality = []

######################Results:
distances = {}
distances_mean={} 
distances_stdev={}
times = {}

sum_correct=0 #ms
sum_incorrect =0 #ms

leftgoodzone = 0
enteredgoodzone = 0

timestamp_init = 0

execount =0

def setBIsCorrect(bIisInZone, timestamp, bWasInZone):
    global leftgoodzone
    global enteredgoodzone
    
    global execount
    result = False
    
    execount+=1
    if (bWasInZone and bIisInZone): #was in interval and is still in it
        result = True
        #print ('was in : is in')
    elif (bWasInZone and not bIisInZone): #was in interval and left it
        result = False
        leftgoodzone = timestamp
        CalcTimeCorrect(enteredgoodzone, leftgoodzone)
        #print ('was in : left it')
        #print (str(int(enteredgoodzone)))
        #print (str(int(leftgoodzone)))
        
    elif (not bWasInZone and bIisInZone): #was not in interval and entered it
        #print ('was not in : entered it')
        enteredgoodzone = timestamp
        #print (str(int(enteredgoodzone)))
        #print (str(int(leftgoodzone)))
        CalcTimeIncorrect(enteredgoodzone, leftgoodzone)

        result = True
    elif (not bWasInZone and not bIisInZone):
        #print ('was not in it : is not in it')
        result = False
    else:
        print ('wat')
    return result

def CalcTimeCorrect(t1, t2):
    global sum_correct
    res = int(t2)-int(t1)
    res = abs(res)
    sum_correct+=res
    #print ('diff ' + str(res)) 

def CalcTimeIncorrect(t1, t2):
    global sum_incorrect
    res = int(t2)-int(t1)
    res = abs(res)
    sum_incorrect+=res
    #print ('diff ' + str(res))
    
def CalcDistancesStatPerParticipant():
    for item in distances:
        tmpList = distances[item]
        #print(item)
        tmpList = list(map(int, tmpList))
        meanval = statistics.mean(tmpList)
        stdevval = statistics.stdev(tmpList)
        
        distances_stdev.update({item : stdevval})
        distances_mean.update({item: meanval})
    
def PrintMeanDistances():
    print ('Mean Distances and StDev of P:')
    for item in distances_mean:
        print ('\t' + item +'\t' + str(distances_mean[item]) +'\t' + str(distances_stdev[item]))
        
def PrintTimes():
#    print (name_var)
#    #print (str(len(distances)))
#    res_c = sum_correct/1000/60
#    res_ic = sum_incorrect/1000/60
#    print ('sum_correct:\t' + str(res_c))
#    print ('sum_incorrect:\t' + str(res_ic)) #no mean because that are atomar values
#    val = (sum_correct + sum_incorrect)/1000/60
#    #print ('sum_total: \t'+ str(val))
#   
    print ('Times P spend in or out of target distance zone:')
    print ('(Name : [sum_correct in ms, sum_incorrect in ms])')
    for item in times:
        print ('\t' + str(item) + '\t' + str(times[item]))
        
            
            
def CalcTimesPerParticipant(name_var, condition_var, task_var):
    times.update({name_var : [condition_var, task_var, sum_correct, sum_incorrect]})
    
def CalcAndPrintOverallTimeStats():
    tmpSumCorrect = []
    tmpSumIncorrect = []
                    
    for item in times:
        tmpSumCorrect.append(times.get(item)[2])
        tmpSumIncorrect.append(times.get(item)[3])

    tmpSumCorrect = list(map(int, tmpSumCorrect))
    tmpSumIncorrect = list(map(int, tmpSumIncorrect))
    normalitytimecorrect = scipy.stats.shapiro(tmpSumIncorrect)
    
    meantimecorrect = statistics.mean(tmpSumCorrect)
    stdevcorrect = statistics.stdev(tmpSumCorrect)
    normalitytimecorrect = scipy.stats.shapiro(tmpSumCorrect)
    
    meantimeincorrect = statistics.mean(tmpSumIncorrect)
    stdevincorrect = statistics.stdev(tmpSumIncorrect)
    normalitytimeincorrect = scipy.stats.shapiro(tmpSumIncorrect)

    
    print('Time in target zone [ms]:')
    print ('\t'+str(meantimecorrect) + ' [' + str(stdevcorrect) + ']')
    print ('\tnormality = ' + str(normalitytimecorrect))
    print('Time out of target zone [ms]:')
    print ('\t'+str(meantimeincorrect)+ ' [' + str(stdevincorrect) + ']')
    print ('\tnormality = ' + str(normalitytimeincorrect))
    
def CalcOverallDistanceStats():
    global meanOverallInM
    global stdevOverallInM
    global distance_normality
    
    tmpDistanceList = []
    for item in distances:
        tmpDistanceList += distances[item]
        #print (len(tmpDistanceList))
    tmpDistanceList = list(map(int, tmpDistanceList))
    meanOverallInM = statistics.mean(tmpDistanceList)
    stdevOverallInM = statistics.stdev(tmpDistanceList)
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.anderson.html
    distance_normality = scipy.stats.anderson(tmpDistanceList, dist='norm')

def PrintOverallDistanceStats(condition = '', task = ''):
    print ('Overall distance (mean and stdev) in [m] for ' + condition + ' and ' + task + ':')
    print ('\t' + str(meanOverallInM) + ' [' + str(stdevOverallInM)+']')
    print ('\tnormality = ' + str(distance_normality))
    print()
    

def CalcDistanceStats(spamreader_var, name_var, condition_var, task_var):
    
    global leftgoodzone
    global enteredgoodzone
    global sum_correct
    global sum_incorrect 
    global timestamp_init
    
    bWasCorrect = False
    sum_correct = 0
    sum_incorrect = 0
    isFirst = True
    distances.update({name_var : []})
    
    timestamp = 0
    distance = 0
    
    execution = 0
    
    for row in spamreader_var:
        
        ####count trigger
        if (row.get('A') == 'Trigger' or row.get('B') == 'Trigger'):
            execution+=1
        
        ####init everything
        if (isFirst):
            leftgoodzone = row.get('timestamp')
            enteredgoodzone = row.get('timestamp')
            timestamp_init = row.get('timestamp')
            #print (str(timestamp_init))
    
            isFirst = False
        
        #print (row)
        timestamp = row.get('timestamp')

        if strDistance in row.get('B'):
            distance = row.get('A')
            if (int(distance) >= 120 or int(distance) <= 40):
                bWasCorrect = setBIsCorrect(False, timestamp, bWasCorrect)
            else:
                bWasCorrect = setBIsCorrect(True, timestamp, bWasCorrect)
                
            distances.get(name_var).append(distance)
           
        elif strDistance in row.get('A'):
            distance = row.get('B')
            if (int(distance) >= 120 or int(distance) <= 40):
                bWasCorrect = setBIsCorrect(False, timestamp,bWasCorrect)
            else:
                bWasCorrect = setBIsCorrect(True, timestamp, bWasCorrect)
                
            distances.get(name_var).append(distance)
        
        else:
            continue
    
    #finish it:
    if ((int(distance) >= 120 or int(distance) <= 40)):
        CalcTimeIncorrect(timestamp, leftgoodzone)
    else:
        CalcTimeCorrect(timestamp, enteredgoodzone)
    
    #print (str(distance))
    #print (str(execution))
        
    CalcDistancesStatPerParticipant()
    CalcTimesPerParticipant(name_var, condition_var, task_var)
    
    
    #PrintTimes()