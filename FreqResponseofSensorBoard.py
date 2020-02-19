# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 17:38:51 2019

@author: vbalaji
"""

import time, os, sys, math, numpy as np, matplotlib.pyplot as plt
from connect import connect
from dg1022z import dg1022z
from agilent34410a import agilent34410a
from excelClass import excelClass
from F_createPathStr import F_createPathStr
from F_createDir import F_createDir

#Set addresses of digital multimeter(s) and function generator
dvm1Addr = 'GPIB0::Num1::INSTR'
dvm2Addr = 'GPIB0::Num2::INSTR'
fgAddr = 'USB0::Hex1::Hex2::SerialNumofInstr::0::INSTR'

#######################################################################
#         Fill the Device information              #
#######################################################################
#Device 
Device = "DUT"

#Define list of frequencies at which measurements are to be taken
FreqArray = [1000,10000,50000,75000,100000,150000,200000,300000,500000,600000,700000,800000,900000,980000];
nFreqArray = len(FreqArray);
#Time to wait after changing a setting of an instrument
equipDelay = 1.25;

#Configure instruments
dvm1Port = connect(dvm1Addr);
dvm1 = agilent34410a(dvm1Port);
dvm1.reset();  
dvm1.clrError();                         # clears any exisiting DVM errors
dvm1.configure.voltageAc();              # sets voltage mode
dvm1.beeperOff();

dvm1.trigger.source.immediate();         # set internal signal as trigger
dvm1.trigger.delay.minimum();
dvm1.trigger.sampleCount(10);            # sets sample count to 10


dvm2Port = connect(dvm2Addr);
dvm2 = agilent34410a(dvm2Port);
dvm2.reset();  
dvm2.clrError();                         # clears any exisiting DVM errors
dvm2.configure.currentAc();              # sets voltage mode

dvm2.beeperOff();


dvm2.trigger.source.immediate();         # set internal signal as trigger
dvm2.trigger.delay.minimum();
dvm2.trigger.sampleCount(10);            # sets sample count to 10


fgPort = connect(fgAddr);
fg = dg1022z(fgPort);

subDir = 'C:/Freq_Response/Results/';

dirName = F_createPathStr(subDir);
    
# Create Directory (if needed)
F_createDir(dirName);

excelFileName = Device + 'FreqResp.xlsx';

#Initialize arrays for ratio of parameters
RatioArray = [];
DenomParamArray = [];
NumParamArray = [];
#Initialize peak-peak amplitude of function generator waveform
ampPP   = 0.25;


#######################################################################
#                         Start Measurements                          #
#######################################################################

#-- Start the meters
#set starting frequency to 100 Hz and Vpp to 0.15V


fg.reset(); 
fg.clear();
 	
fg.set.ch1.shapeType.sine()
fg.set.ch1.shapeParameter.sine.freq(100)
fg.set.ch1.shapeParameter.sine.ampPkpk(0.25)
fg.set.ch1.output.on()

fg.set.powerAmp.gain.gain10X();

fg.set.powerAmp.output.on();

time.sleep(equipDelay);      
# measure RMS Current through sense resistor     
[minRead, out_i, maxRead] = dvm2.measure.current.ac.averageDvm(10);
#calculate Ipeak-peak
Ipp = out_i*2.86;
IppConst = Ipp 
DenomParamArray.append(out_i);

#measure RMS Voltage at sensor output
[minRead, out_v, maxRead] = dvm1.measure.voltage.ac.averageDvm(10);

#calculate ratio parameter
CC = out_v/out_i
RatioArray.append(CC);
NumParamArray.append(out_v);



for k in range(nFreqArray):
    freq_curr = FreqArray[k]
    fg.set.ch1.shapeParameter.sine.freq(freq_curr)
    time.sleep(equipDelay);  
    print("Read Parameter 1\n")
    [minRead, out_i, maxRead] = dvm2.measure.current.ac.averageDvm(10);
    print(str(out_i)+" A")
    Ipp = out_i*2.86;
    while Ipp < (IppConst*.98):
        ampPP = ampPP + 0.03;
        fg.set.ch1.shapeParameter.sine.ampPkpk(ampPP)
        time.sleep(equipDelay);  
        [minRead, out_i, maxRead] = dvm2.measure.current.ac.averageDvm(10);
        print(str(out_i)+" A")
        Ipp = out_i*2.86;
       
   
    DenomParamArray.append(out_i);
    #measure RMS Voltage at sensor output
    [minRead, out_v, maxRead] = dvm1.measure.voltage.ac.averageDvm(10);   
    print("Parameter 2 Measured\n")
    print(str(out_v)+" V")
    CC = out_v/out_i
    RatioArray.append(CC);
    NumParamArray.append(out_v);


# Save Results in Excel File
objCheck = 'excelObj' in locals();
    
if not objCheck:
    excelObj = excelClass();
    excelObj.createExcel(dirName, excelFileName);
        
try:    
    excelObj.setActiveSheet();
except:
    excelObj.addSheet(Device);
    excelObj.setActiveSheet(Device);

FreqArray = [100,1000,10000,50000,75000,100000,150000,200000,300000,500000,600000,700000,800000,900000,980000];
excelObj.addColumn('Frequency [Hz]', FreqArray);
excelObj.addColumn('Parameter 1 [A]', DenomParamArray);
excelObj.addColumn('Parameter 2 [V]', NumParamArray);
excelObj.addColumn('Ratio [V/A]', RatioArray); 

excelObj.saveExcel();

fg.set.powerAmp.output.off(); 
fg.set.powerAmp.offset.off(); 
fg.set.ch1.output.off(); 

del(excelObj);
