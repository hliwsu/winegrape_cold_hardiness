# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:28:52 2020

@author: haoli
"""
# import struct
# file=open("X:\\data\\metdata\\MACA_Livneh_v2_VIC_Binary\\CNRM-CM5\\rcp85\\data_42.59375_-112.59375",'rb')
# byte=file.read(1)
# while byte:
#     print(byte)
#     byte=file.read(1)
# data_float=struct.unpack("f",byte)[0]
from datetime import datetime
import os
import pandas as pd
starting_clock = datetime.now()
print(starting_clock)
os.getcwd()
T_threshold=[]
acclimation_rate=[]
deacclimation_rate=[]
theta=[]
writer_1=pd.ExcelFile("C:\\Users\\haoli\\OneDrive\\Work\\Hardiness\\Model_for_distribution_beta_v2.7 (1) (1).xls")
par_df= writer_1.parse('input_parameters')
variety = par_df.iloc[0, 0]
Hc_initial = par_df.iloc[0, 1]
Hc_min = par_df.iloc[0, 2]
Hc_max = par_df.iloc[0, 3]
T_threshold = [0] # 0 is a place holder to match Excel file format, same below
T_threshold.append(par_df.iloc[0, 4])
T_threshold.append(par_df.iloc[0, 5])
ecodormancy_boundary = par_df.iloc[0, 6]
acclimation_rate=[0]
acclimation_rate.append(par_df.iloc[0, 7])
acclimation_rate.append(par_df.iloc[0, 8])
# acclimation_rate_2 = par_df.iloc[0, 8]
deacclimation_rate=[0]
deacclimation_rate.append(par_df.iloc[0, 9])
deacclimation_rate.append(par_df.iloc[0, 10])
theta=[0,0,0]
theta[1] = 1
theta[2] = par_df.iloc[0, 11]
# calculate range of hardiness values possible, this is needed for the logistic component
Hc_range = Hc_min - Hc_max
DD_heating_sum = 0
DD_chilling_sum = 0
base10_chilling_sum = 0
model_Hc_yesterday = Hc_initial
dormancy_period = 1

input_temps= writer_1.parse('input_temps')
input_temps=input_temps.loc[:, ~input_temps.columns.str.contains('^Unnamed')] # drop unnamed columns
model_out=[]
for j in range(0,len(input_temps)):
    jdate = input_temps.loc[j,"Date"]
    jday = input_temps.loc[j,"jday"]
    T_mean = input_temps.loc[j,"T_mean"]
    T_max = input_temps.loc[j,"T_max"]
    T_min = input_temps.loc[j,"T_min"]
    observed_Hc=input_temps.loc[j,"Observed_Hc"]
    # calculate heating degree days for today used in deacclimation
    if T_mean>T_threshold[dormancy_period]:
        DD_heating_today = T_mean - T_threshold[dormancy_period]
    else:
        DD_heating_today=0
    # calculate cooling degree days for today used in acclimation
    if T_mean <= T_threshold[dormancy_period]:
        DD_chilling_today = T_mean - T_threshold[dormancy_period]
    else:
        DD_chilling_today = 0    
    # calculate cooling degree days using base of 10c to be used in dormancy release
    if T_mean<=10:
        base10_chilling_today = T_mean - 10
    else:
        base10_chilling_today = 0
    deacclimation = DD_heating_today * deacclimation_rate[dormancy_period] * (1 - ((model_Hc_yesterday - Hc_max) / Hc_range) ** theta[dormancy_period])
    if DD_chilling_sum == 0:
        deacclimation = 0
    acclimation = DD_chilling_today * acclimation_rate[dormancy_period] * (1 - (Hc_min - model_Hc_yesterday) / Hc_range)
    Delta_Hc = acclimation + deacclimation
    model_Hc = model_Hc_yesterday + Delta_Hc
    Delta_Hc = acclimation + deacclimation
    model_Hc = model_Hc_yesterday + Delta_Hc
    if model_Hc <= Hc_max:
        model_Hc = Hc_max
    if model_Hc > Hc_min:
        model_Hc = Hc_min
    # sum up chilling degree days
    DD_chilling_sum = DD_chilling_sum + DD_chilling_today
    base10_chilling_sum = base10_chilling_sum + base10_chilling_today      
    # sum up heating degree days only if chilling requirement has been met
    # i.e dormancy period 2 has started
    if dormancy_period == 2:
        DD_heating_sum = DD_heating_sum + DD_heating_today
    # determine if chilling requirement has been met
    # re-set dormancy period
    # order of this and other if statements are consistant with Ferguson et al, or V6.3 of our SAS code
    if base10_chilling_sum <= ecodormancy_boundary:
        dormancy_period = 2  
    model_out.append(model_Hc)
    model_Hc_yesterday = model_Hc
ending_clock = datetime.now()
print(ending_clock-starting_clock)
# R7-3700X-16GB 0:00:01.179937
# i7-3610qm-12GB 0:00:02.441757
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
