# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:25:16 2017

@author: flwe6397
"""

import scipy
from scipy import stats

def CalcMannWhitneyU(list1, list2):
    scipy.stats.mannwhitneyu(list1, list2)
    