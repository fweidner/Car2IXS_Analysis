# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 11:13:50 2017

@author: fweidner
"""
import statistics
import scipy
from scipy import stats

strListStart = 'NewActiveList'
strResetStage = 'ResetStage'
strSelectText = 'SelectText'
strNewActiveList = 'NewActiveList'

areas = {}  #key: List; 
               #value1: reactiontime of correct items including timeouts; 
               #value2: list of 1/0. 1 = correct w/o timeout; 0 = correct w/ timeout
               #value3: con
area_ul = {}
area_uc = {}
area_ur = {}
area_dr = {}

area_mean_stdev = {}

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
    
def CalcAreaResults():
#    for item in areas:
#       print (item)
#       for valueList in areas[item]:
#           res =''
#           for valueListItem in valueList:
#               res+= str(valueListItem) + ';'
#           print (res)

    CreateAreas()
    
    area_ul.update({'combined_list_ul' : [[],[]]})       
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
    
    
   
#    print()
#    print('area_ul')    
#    for item in area_ul:
#        print ('\t' + str(item) + ' \t' + str(area_ul[item]))
#    
#    print('area_uc')
#    for item in area_uc:
#        print ('\t' + str(item) + ' \t' + str(area_uc[item]))
#    print('area_ur')    
#    for item in area_ur:
#        print ('\t' + str(item) + ' \t' + str(area_ur[item]))
#    print('area_dr')    
#    for item in area_dr:
#        print ('\t' + str(item) + ' \t' + str(area_dr[item]))
        
# Calculates cumulative statistics over all participants!
def CalcAreaStats(con = '', task = ''):
    print ('Stats Total (area, mean, stdev) in [ms] for ' + con + ' and ' + task + ':')    
    tmpList = list(map(int, area_ul.get('combined_list_ul')[0]))
    mean = statistics.mean(tmpList)
    stdev = statistics.stdev(tmpList)
    ul_normality = scipy.stats.shapiro(tmpList)

    area_mean_stdev.update({'ul' : [mean, stdev,ul_normality]})
    
    tmpList = list(map(int, area_uc.get('combined_list_uc')[0]))
    mean = statistics.mean(tmpList)
    stdev = statistics.stdev(tmpList)
    uc_normality = scipy.stats.shapiro(tmpList)
    area_mean_stdev.update({'uc' : [mean, stdev, uc_normality]})


    tmpList = list(map(int, area_ur.get('combined_list_ur')[0]))
    mean = statistics.mean(tmpList)
    stdev = statistics.stdev(tmpList)
    ur_normality = scipy.stats.shapiro(tmpList)
    area_mean_stdev.update({'ur' : [mean, stdev, ur_normality]})
    
    tmpList = list(map(int, area_dr.get('combined_list_dr')[0]))
    mean = statistics.mean(tmpList)
    stdev = statistics.stdev(tmpList)
    dr_normality = scipy.stats.shapiro(tmpList)
    area_mean_stdev.update({'dr' : [mean, stdev, dr_normality]})
    
    for item in area_mean_stdev:
         print ('\t' + str(item) + ' \t' + str(area_mean_stdev[item]))
         
    
    
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
  

def PrintSummary(CountErrorWrongItem,CountErrorListNotFinished,CountTimeCorrect,CountCorrect,CountTimeError,CountNewActiveListStr):
    TotalErrorWithTimouts = CountErrorWrongItem + CountErrorListNotFinished + CountTimeCorrect
    TotalErrorWithoutTimeouts = CountErrorWrongItem + CountErrorListNotFinished 

    TotalCorrectWithTimeouts = CountCorrect
    TotalCorrectWithoutTimeouts = CountCorrect - CountTimeCorrect
    
    if (True):
        print ('Summary:')
        print ('\tTotal Error w/ Timeouts    : ' + str(TotalErrorWithTimouts))
        print ('\tTotal Error w/o Timeouts   : ' + str(TotalErrorWithoutTimeouts))
        print ('\tTotal Correct w/ Timeouts  : '+ str(TotalCorrectWithTimeouts))
        print ('\tTotal Correct w/o Timeouts : '+ str(TotalCorrectWithoutTimeouts))
        print ('\tTimeout but correct        : '+str(CountTimeCorrect))
        print ('\tTimeouts and incorrect     : '+str(CountTimeError))
        #print (completiontimes_ls) 

    


    if (TotalCorrectWithoutTimeouts+TotalErrorWithTimouts != 24):
        print ('nay! not 24 but ' + str(CountNewActiveListStr))
    if (TotalCorrectWithoutTimeouts+TotalErrorWithTimouts != CountNewActiveListStr):
        print ('nay! not CountNewActiveListStr')
        
def CalcListStats(spamreader_var, con):

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
    
    #PrintSummary(CountErrorWrongItem,CountErrorListNotFinished,CountTimeCorrect,CountCorrect,CountTimeError,CountNewActiveListStr)
    
#    rowtowrite = []
#    rowtowrite.append(str(TotalErrorWithTimouts))
#    rowtowrite.append(str(TotalErrorWithoutTimeouts))
#    rowtowrite.append(str(TotalCorrectWithTimeouts))
#    rowtowrite.append(str(TotalCorrectWithoutTimeouts))
#    rowtowrite.append(str(CountTimeCorrect))
#    rowtowrite.append(str(CountTimeError))
#    
#    filewriter_LS_Counts.writerow(rowtowrite)       
    
    
    #CalcAreaResults()
    #CalcAreaStats()
