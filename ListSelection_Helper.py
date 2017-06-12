# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:47:37 2017

@author: fweidner
"""

import scipy
from scipy import stats
import statistics

def CalcStatForOneArea(area_mean_stdev, current_area, combined_list_string, final_c, final_t, final_i):
    area_mean_stdev.update({final_c : [0,0,[],0]}) #mean, stdev, norm, count
    area_mean_stdev.update({final_t : [0,0,[],0]}) #mean, stdev, norm, count
    area_mean_stdev.update({final_i : [0,0,[],0]}) #mean, stdev, norm, count
    tmplist_c = []
    tmplist_i = []
    tmplist_t = []
    tmpListTimes = current_area.get(combined_list_string)[0]
    tmpList012 = current_area.get(combined_list_string)[1]
    length = len(tmpList012)
    
    for j in range (0, length):
        if (tmpList012[j] == 0):
                area_mean_stdev.get(final_t)[3]+=1
                tmplist_t.append(tmpListTimes [j])

        elif (tmpList012[j] == 1):
            area_mean_stdev.get(final_c)[3]+=1
            tmplist_c.append(tmpListTimes [j])
             
        elif (tmpList012[j] ==2):
            area_mean_stdev.get(final_i)[3]+=1
            tmplist_i.append(tmpListTimes [j])
        else:
            print ('what')
   
    mean = statistics.mean(tmplist_i)
    stdev = statistics.stdev(tmplist_i)
    normality = scipy.stats.shapiro(tmplist_i)
    area_mean_stdev.update({final_i : [mean, stdev,normality, len(tmplist_i)]})
 
    mean = statistics.mean(tmplist_c)
    stdev = statistics.stdev(tmplist_c)
    normality = scipy.stats.shapiro(tmplist_c)
    area_mean_stdev.update({final_c : [mean, stdev,normality,len(tmplist_c)]})
    
    mean = statistics.mean(tmplist_t)
    stdev = statistics.stdev(tmplist_t)
    normality = scipy.stats.shapiro(tmplist_t)
    area_mean_stdev.update({final_t : [mean, stdev,normality, len(tmplist_t)]})