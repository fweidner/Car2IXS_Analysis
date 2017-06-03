# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 13:09:15 2017

@author: fweidner
"""
highlighton = 'Highlight-1'
highligtoff = 'Highlight-0'
yay = 'yay'
nay = 'nay'

    
def CalcTime(t1, t2, responsetimes_cd):
    res = int(t2)-int(t1)
    responsetimes_cd.append(res)


def GetResponseTimesForCorrectValues(spamreader_var):
    
    bShouldPress = False
    bShouldCalcTime = True
    responsetimes_cd = []
    count_correct = 0
    count_wrong = 0
    count_highlight =0
    tmp_t1=0
    tmp_t2=0
    tmp_t_response=0
    
    for tmprow in spamreader_var:
    #calc response time
      if (bShouldCalcTime):  
          CalcTime(tmp_t1, tmp_t_response, responsetimes_cd)
          bShouldCalcTime = False
    #time began
      if (highlighton in tmprow.get('A')):
          bShouldPress = True
          count_highlight+=1
          tmp_t1=tmprow.get('timestamp')
          continue
    #time ended  
      if (highligtoff in tmprow.get('A')):
          bShouldPress = False
          tmp_t2 = tmprow.get('timestamp')
          continue
      
    #correct button press
      if ((yay in tmprow.get('A')) & bShouldPress):
          count_correct+=1
          bShouldPress=False
          bShouldCalcTime = True
          tmp_t_response = tmprow.get('timestamp')
      
    #wrong button press
      if ((nay in tmprow.get('A'))):
          count_wrong+=1
          bShouldPress=False
           
    print (responsetimes_cd)
    print ("Triggers: " + str(count_highlight))
    print ("yay: " + str(count_correct))
    print ("nay: " + str(count_wrong))
    print ("missed: " + str(int(count_highlight)-(int(count_wrong)+int(count_correct))))

              
          
 
        