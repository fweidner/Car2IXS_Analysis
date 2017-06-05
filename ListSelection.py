# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 11:13:50 2017

@author: fweidner
"""

import csv

strListStart = 'NewActiveList'
strResetStage = 'ResetStage'
strSelectText = 'SelectText'
strNewActiveList = 'NewActiveList'

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

def WriteAreaResults():
    with open('LS_AreaStats.csv', 'w', newline='') as csvfile:
        filewriterAreaStats = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        res = ''
        first = True
        for key in areas:
            if (first):
                res = key
                first = False
            else:
                res = res + ';' + key
            
        print (res)
        filewriterAreaStats.writerow([res])

    
def PrintAreaResults():
    for item in areas:
       print (item)
       for valueList in areas[item]:
           res =''
           for valueListItem in valueList:
               res+= str(valueListItem) + ';'
           print (res)
        

def CalcTime(t1, t2):
    return int(t2)-int(t1)
    
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
        

def LS_CalcCountErrorAndCorrect(spamreader_var, filewriter_LS_Counts):

    CountNewActiveListStr =0
    tripellistitem =0
    tripels = {}
    CreateTriples(tripels)
    
    t1_ListStart = 0
    t2_ListEnd = 0
    SelectTextCount = 0
       
    CountCorrect =0
    CountErrorWrongItem = 0
    CountErrorListNotFinished = 0
    CountTimeError =0 #wrong items selected, after 10s
    CountTimeCorrect=0 #correct items selected but after 10s
    
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
     
        
    ###############################################
    ###############################################
    
    TotalErrorWithTimouts = CountErrorWrongItem + CountErrorListNotFinished + CountTimeCorrect
    TotalErrorWithoutTimeouts = CountErrorWrongItem + CountErrorListNotFinished 

    TotalCorrectWithTimeouts = CountCorrect
    TotalCorrectWithoutTimeouts = CountCorrect - CountTimeCorrect
    
    if (True):
        print ('Total Error w/ Timeouts    :' + str(TotalErrorWithTimouts))
        print ('Total Error w/o Timeouts   :' + str(TotalErrorWithoutTimeouts))
        print ('Total Correct w/ Timeouts  : '+ str(TotalCorrectWithTimeouts))
        print ('Total Correct w/o Timeouts : '+ str(TotalCorrectWithoutTimeouts))
        print ('Timeout but correct        : '+str(CountTimeCorrect))
        print ('Timeouts and incorrect     : '+str(CountTimeError))
        #print (completiontimes_ls) 

    


    if (TotalCorrectWithoutTimeouts+TotalErrorWithTimouts != 24):
        print ('nay! not 24 but ' + str(CountNewActiveListStr))
    if (TotalCorrectWithoutTimeouts+TotalErrorWithTimouts != CountNewActiveListStr):
        print ('nay! not CountNewActiveListStr')
    
    rowtowrite = []
    rowtowrite.append(str(TotalErrorWithTimouts))
    rowtowrite.append(str(TotalErrorWithoutTimeouts))
    rowtowrite.append(str(TotalCorrectWithTimeouts))
    rowtowrite.append(str(TotalCorrectWithoutTimeouts))
    rowtowrite.append(str(CountTimeCorrect))
    rowtowrite.append(str(CountTimeError))
    
    filewriter_LS_Counts.writerow(rowtowrite)       
    
    
    PrintAreaResults()
    WriteAreaResults()
    
