# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 17:22:20 2017

@author: fweidner
"""
strDistance = 'Distance'

distances = {}
distances_mean={}
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
    
def ReduceDistanceStats():
    for item in distances:
        tmpList = distances[item]
        meanval = 0
        for val in tmpList:
            meanval+=int(val)
        listlen = len(tmpList)
        #print (item + ' : ' + str(listlen))
        meanval/= listlen
        distances_mean.update({item: meanval})
    
    for item in distances_mean:
        print (item +'\t ' + str(int(distances_mean[item])) + '\t(mean)')
        
def CalcDistanceStats(spamreader_var, name_var):
    
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
            print (str(timestamp_init))
    
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
        
    #ReduceDistanceStats()
    print (name_var)
    #print (str(len(distances)))
    res_c = sum_correct/1000/60
    res_ic = sum_incorrect/1000/60
    print ('sum_correct:\t' + str(res_c))
    print ('sum_incorrect:\t' + str(res_ic))
    val = (sum_correct + sum_incorrect)/1000/60
    print ('sum_total: \t'+ str(val))