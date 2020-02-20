# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 13:48:07 2019

@author: vbalaji
This script is used to calculate the ratio of two parameter matrices of a sensor board with two busbars.
Each sensor is located above a busbar and a parameter sweep is performed consecutively through the two busbars.
The slopes of the best fit lines for the sensor outputs (param2) versus the swept input parameter (param1) provide the ratio matrix elements.
With the ratio matrix, the input applied corresponding to the sensor output parameter measured can be calculated.

"""

import time, os, sys, math, numpy as np, matplotlib.pyplot as plt
import re
import random
from connect import connect
from InstrType1 import InstrType1
from InstrType2 import InstrType2
from InstrType3 import InstrType3
from excelClass import excelClass
from F_createPathStr import F_createPathStr
from F_createDir import F_createDir


InstrType1_1Addr = 'GPIB0::Num1::INSTR'
InstrType1_2Addr = 'GPIB0::Num2::INSTR'
InstrType2Addr = 'GPIB0::Num3::INSTR'
InstrType3Addr = 'GPIB0::Num4::INSTR'

#######################################################################
#         Fill the Device information              #
#######################################################################
#Device 
Device = "DUT"
zero = 0.0;
Param1_1_1Array = [];
Param1_2_1Array = [];
Param2_1_1Array = [];
Param2_2_1Array = [];

Param1_1_2Array = [];
Param1_2_2Array = [];
Param2_1_2Array = [];
Param2_2_2Array = [];

Param1_1_meas = [];
Param1_2_meas = [];
Param1_diff = [];

Param1_1_calc_wo_CC = [];
Param1_2_calc_wo_CC = [];

Param1_1_calc_with_CC = [];
Param1_2_calc_with_CC = [];

Error1Array_1x1 = [];
Error2Array_1x1 = [];
Error1Array_2x2 = [];
Error2Array_2x2 = [];
RelErr1Array_1x1 = [];
RelErr2Array_1x1 = [];
RelErr1Array_2x2 = [];
RelErr2Array_2x2 = [];
FS_Err1Array_1x1 = [];
FS_Err1Array_2x2 = [];
FS_Err2Array_1x1 = [];
FS_Err2Array_2x2 = [];

Param1Array = [1,2,3,4,5,6,7,8];
FS_val = 8;
nParam1Array = len(Param1Array);
equipDelay = 1.25;

# Line of best fit: y=mx+b where m = (sum(yixi)-mean(y)*sum(xi))/(sum(xi^2)-mean(x)*sum(xi)) and b = mean(y)*sum(xi^2)-mean(x)*sum(yixi)/(sum(xi^2)-mean(x)*sum(xi))
def best_fit_line(x,y):
    denom = x.dot(x) - x.mean() * x.sum()
    m = (x.dot(y) - y.mean()*x.sum())/denom
    print('Slope of line:{}'.format(m))
    b = (y.mean()*x.dot(x) - x.mean()*x.dot(y))/denom
    y_pred = m*x + b;
    plt.scatter(x,y)
    plt.plot(x,y_pred,'r')
    return m

InstrType1_1Port = connect(InstrType1_1Addr);
InstrType1_1 = InstrType1(InstrType1_1Port);
InstrType1_1.reset();  
InstrType1_1.clrError();                         # clears any exisiting DVM errors
InstrType1_1.configure.param2Dc();              # sets param2 mode
InstrType1_1.beeperOff();


InstrType1_1.trigger.source.immediate();         # set internal signal as trigger
InstrType1_1.trigger.delay.minimum();
InstrType1_1.trigger.sampleCount(10);            # sets sample count to 10


InstrType1_2Port = connect(InstrType1_2Addr);
InstrType1_2 = InstrType1(InstrType1_2Port);
InstrType1_2.reset();  
InstrType1_2.clrError();                         # clears any exisiting DVM errors
InstrType1_2.configure.param2Dc();              # sets param2 mode
InstrType1_2.beeperOff();


InstrType1_2.trigger.source.immediate();         # set internal signal as trigger
InstrType1_2.trigger.delay.minimum();
InstrType1_2.trigger.sampleCount(10);            # sets sample count to 10


ps1Port = connect(InstrType2Addr);
ps1 = InstrType2(ps1Port);

ps1.output.off();             # turn output off

ps1.source.set.param2(0);    # set param2 limit to 0V
ps1.source.set.param1(0);    # set param1 limit to 0A

ps1.output.on();              # turn output on


ps2Port = connect(InstrType3Addr);
ps2 = InstrType3(ps2Port);

ps2.output.off();             # turn output off

ps2.source.set.param2(0);    # set param2 limit to 0V
ps2.source.set.param1(0);    # set param1 limit to 0A

ps2.output.on();              # turn output on

subDir = 'Dir_path' + Device;

dirName = F_createPathStr(subDir);

# Create Directory (if needed)
F_createDir(dirName);

excelFileName = Device + 'Name_of_excel_file.xlsx';

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

ps1.source.set.param1(0);
ps2.source.set.param1(0);
time.sleep(equipDelay);  
print("Read Sensor1 Output Parameter at Zero Input Parameter\n")
[minRead, zero_out_v1, maxRead] = InstrType1_1.measure.param2.dc.averageDvm(10);
print("Read Sensor2 Output Parameter at Zero Input Parameter\n")
[minRead, zero_out_v2, maxRead] = InstrType1_2.measure.param2.dc.averageDvm(10);
print("Zero param1 Output param2 of sensor 1:"+str(zero_out_v1)+" units")
print("Zero param1 Output param2 of sensor 2:"+str(zero_out_v2)+" units")
Param1_1_1Array.append(zero);
Param1_2_1Array.append(zero);
Param2_1_1Array.append(zero_out_v1);
Param2_2_1Array.append(zero_out_v2);

#Apply param1 sweep to first busbar, keeping param1 through second busbar zero
for k in range(nParam1Array):
    Param1_val = Param1Array[k]
    ps1.source.set.param1(Param1_val);
    ps1.source.set.param2(Param1_val*2.0); #specific relation between param1 and param2 setting for power supply
    time.sleep(equipDelay);  
    print("Read Sensor1 Output param2\n")
    [minRead, out_v1, maxRead] = InstrType1_1.measure.param2.dc.averageDvm(10);
    print("Read Sensor2 Output param2\n")
    [minRead, out_v2, maxRead] = InstrType1_2.measure.param2.dc.averageDvm(10);
    print("Output param2 of sensor 1:"+str(out_v1)+" units")
    print("Output param2 of sensor 2:"+str(out_v2)+" units")
    Param2_1_1Array.append(out_v1);
    Param2_2_1Array.append(out_v2);
    cmd2 = 'IOUT?';
    curr1_str = ps1.measure.outputparam1();   # measures output param1
    curr2_str = ps2.rawRead(cmd2);   # measures output param1
    curr2_val = [float(s) for s in re.findall(r"[\d*\.\d+]+", curr2_str)]
    Param1_1_1Array.append(float(curr1_str));
    Param1_2_1Array.append(curr2_val[0]);
    
excelObj.addColumn('Param1_1_1 [units]', Param1_1_1Array);
excelObj.addColumn('Param1_2_1 [units]', Param1_2_1Array);
excelObj.addColumn('Param2_1_1 [units]', Param2_1_1Array);
excelObj.addColumn('Param2_2_1 [units]', Param2_2_1Array);   

ps1.source.set.param1(0);    # set param1 limit to 0

# calculate slope using best fit line approach
Param1_1_1nd=np.asarray(Param1_1_1Array)
Param2_1_1nd=np.asarray(Param2_1_1Array)
Param2_2_1nd=np.asarray(Param2_2_1Array)
alpha_bfl_11 = best_fit_line(Param1_1_1nd,Param2_1_1nd)    
alpha_bfl_21 = best_fit_line(Param1_1_1nd,Param2_2_1nd)    
Param1_1_2Array.append(zero);
Param1_2_2Array.append(zero);
Param2_1_2Array.append(zero_out_v1);
Param2_2_2Array.append(zero_out_v2);
 
#Apply param1 sweep to second busbar, keeping param1 through first busbar zero   
for k in range(nParam1Array):
    curr_val = Param1Array[k]
    ps2.source.set.param1(curr_val);
    ps2.source.set.param2(curr_val*2.0);#specific relation between I and V setting for 6032a supply
    time.sleep(equipDelay);  
    print("Read Sensor1 Output param2\n")
    [minRead, out_v1, maxRead] = InstrType1_1.measure.param2.dc.averageDvm(10);
    print("Read Sensor2 Output param2\n")
    [minRead, out_v2, maxRead] = InstrType1_2.measure.param2.dc.averageDvm(10);
    print("Output param2 of sensor 1:"+str(out_v1)+" units")
    print("Output param2 of sensor 2:"+str(out_v2)+" units")
    Param2_1_2Array.append(out_v1);
    Param2_2_2Array.append(out_v2);

    cmd2 = 'IOUT?';
    curr1_str = ps1.measure.outputparam1();   # measures output param1
    curr2_str = ps2.rawRead(cmd2);   # measures output param1
    curr2_val = [float(s) for s in re.findall(r"[\d*\.\d+]+", curr2_str)]
    Param1_1_2Array.append(float(curr1_str));
    Param1_2_2Array.append(curr2_val[0]);
    
excelObj.addColumn('Param1_1_2 ', Param1_1_2Array);
excelObj.addColumn('Param1_2_2 ', Param1_2_2Array);
excelObj.addColumn('Param2_1_2 ', Param2_1_2Array);
excelObj.addColumn('Param2_2_2 ', Param2_2_2Array); 

ps2.source.set.param1(0);    # set param1 limit to 8A

    
# calculate slope using best fit line approach
Param1_2_2nd=np.asarray(Param1_2_2Array)
Param2_1_2nd=np.asarray(Param2_1_2Array)
Param2_2_2nd=np.asarray(Param2_2_2Array)
alpha_bfl_12 = best_fit_line(Param1_2_2nd,Param2_1_2nd)    
alpha_bfl_22 = best_fit_line(Param1_2_2nd,Param2_2_2nd)    
   
print("Alpha values calculated using best fit for VI line:\n")
print("Alpha11: "+str(alpha_bfl_11)+"units  \n")
print("Alpha12: "+str(alpha_bfl_12)+"units  \n")
print("Alpha21: "+str(alpha_bfl_21)+"units  \n")
print("Alpha22: "+str(alpha_bfl_22)+"units  \n")


# calculate slope using param2 matrix corresponding to highest param1 passed through busbar
alpha11 = (Param2_1_1Array[7]-zero_out_v1)/8;
alpha12 = (Param2_1_2Array[7]-zero_out_v1)/8;
alpha21 = (Param2_2_1Array[7]-zero_out_v2)/8;
alpha22 = (Param2_2_2Array[7]-zero_out_v2)/8;

v11 = Param2_1_1Array[0]-zero_out_v1
v21 = Param2_2_1Array[0]-zero_out_v2
# input two matrices 
alphamat_I7 = np.matrix([[alpha11,alpha12],[alpha21,alpha22]]) 
vmat =np.matrix([[v11],[v21]]) 
  
alphainv_I7 = alphamat_I7.I
# This will return dot product 
param1_mat = np.dot(alphainv_I7,vmat) 

print("Param1 values calculated using alpha matrix:\n")
print("Param1_1:"+str(param1_mat[0])+" units\n")
print("Param1_2:"+str(param1_mat[1])+" units\n")

print("Param1 values captured from DMM:\n")
print("Param1_1:"+str(Param1_1_1Array[0])+" units\n")
print("Param1_2:"+str(Param1_2_1Array[0])+" units\n")

#Calculate alpha matrix with cross-coupling coefficients
alphamat_CC = np.matrix([[alpha_bfl_11,alpha_bfl_12],[alpha_bfl_21,alpha_bfl_22]]) 
alphainv_CC = alphamat_CC.I


#Supply random param1, calculate the param1 supplied from alpha matrix and compare with values read from power sources through DMM to find percentage error
print("Apply random param1\n")
for x in range(10):
   y2=round(random.uniform(1.0,10.0),2)
   ps2.source.set.param1(y2);
   ps2.source.set.param2(y2*2);
   ps2.output.on();             
   time.sleep(equipDelay);  

   [minRead, out_v1, maxRead] = InstrType1_1.measure.param2.dc.averageDvm(10);

   [minRead, out_v2, maxRead] = InstrType1_2.measure.param2.dc.averageDvm(10);

   v1 = out_v1 - zero_out_v1
   v2 = out_v2 - zero_out_v2
   vmat_measured =np.matrix([[v1],[v2]]) 
   print("Calculate param1 values using alpha matrix 2x2 based on param2 measured:\n")
   param1_mat_measured = np.dot(alphainv_CC,vmat_measured) 
   print('param1 of sensor 1 calculated:{}\n'.format(param1_mat_measured[0]))
   print('param1 of sensor 2 calculated:{}\n'.format(param1_mat_measured[1]))
   Param1_1_calc_with_CC.append(param1_mat_measured[0]);
   Param1_2_calc_with_CC.append(param1_mat_measured[1]);
   #Calculate param1 without cross-coupling coefficients
   print("Calculate param1 values using alpha11 and alpha22 (cross-coupling neglected) based on param2 measured:\n")
   param1_measured_0 = v1/alpha_bfl_11
   param1_measured_1 = v2/alpha_bfl_22
   print('param1 of sensor 1 calculated with cross-coupling neglected:{}\n'.format(param1_measured_0))
   print('param1 of sensor 2 calculated with cross-coupling neglected:{}\n'.format(param1_measured_1))
   Param1_1_calc_wo_CC.append(param1_measured_0);
   Param1_2_calc_wo_CC.append(param1_measured_1);

   cmd2 = 'IOUT?';
   curr1_str = ps1.measure.outputparam1();   # measures output param1
   curr2_str = ps2.rawRead(cmd2);  # measures output param1
 
   curr2_val = [float(s) for s in re.findall(r"[\d*\.\d+]+", curr2_str)]
   print("Calculate Percent Error\n")
   curr1_mag = abs(float(curr1_str))
   curr2_mag = abs(curr2_val[0])
   curr_diff = abs(curr1_mag-curr2_mag)
   print('param1 of sensor 1 measured:{}\n'.format(curr1_mag))
   print('param1 of sensor 2 measured:{}\n'.format(curr2_mag))
   Param1_1_meas.append(curr1_mag);
   Param1_2_meas.append(curr2_mag);
   Param1_diff.append(curr_diff);

   if (curr1_mag == 0 or (curr1_mag<0 and int(str(curr1_mag).split('.')[1][0])== 0)):
       error1_1x1 = 0.0
       error1_2x2 = 0.0
       relative_error1_1x1 = 0.0
       relative_error1_2x2 = 0.0

   else:
       error1_1x1 = abs(abs(param1_measured_0)-curr1_mag)
       error1_2x2 = abs(abs(param1_mat_measured[0])-curr1_mag)
       relative_error1_1x1 = float(error1_1x1)/curr1_mag
       relative_error1_2x2 = float(error1_2x2)/curr1_mag

   FS_error1_1x1 = (float(abs(abs(param1_measured_0)-curr1_mag))/FS_val)*100
   FS_error1_2x2 = (float(abs(abs(param1_mat_measured[0])-curr1_mag))/FS_val)*100
   
   if (curr2_mag == 0 or (curr2_mag<0 and int(str(curr2_mag).split('.')[1][0])== 0)):
       error2_1x1 = 0.0
       error2_2x2 = 0.0
       relative_error2_1x1 = 0.0
       relative_error2_2x2 = 0.0

   else:
       error2_1x1 = abs(abs(param1_measured_1)-curr2_mag)
       error2_2x2 = abs(abs(param1_mat_measured[1])-curr2_mag)
       relative_error2_1x1 = float(error2_1x1)/curr2_mag
       relative_error2_2x2 = float(error2_2x2)/curr2_mag
      
   FS_error2_1x1 = (float(abs(abs(param1_measured_1)-curr2_mag))/FS_val)*100
   FS_error2_2x2 = (float(abs(abs(param1_mat_measured[1])-curr2_mag))/FS_val)*100     
        

   percent_error1_1x1 = relative_error1_1x1*100
   percent_error2_1x1 = relative_error2_1x1*100
   percent_error1_2x2 = relative_error1_2x2*100
   percent_error2_2x2 = relative_error2_2x2*100
   Error1Array_1x1.append(percent_error1_1x1);
   Error2Array_1x1.append(percent_error2_1x1);
   Error1Array_2x2.append(percent_error1_2x2);
   Error2Array_2x2.append(percent_error2_2x2);
   RelErr1Array_1x1.append(relative_error1_1x1)
   RelErr2Array_1x1.append(relative_error2_1x1)
   RelErr1Array_2x2.append(relative_error1_2x2)
   RelErr2Array_2x2.append(relative_error2_2x2)
   FS_Err1Array_1x1.append(FS_error1_1x1)
   FS_Err1Array_2x2.append(FS_error1_2x2)
   FS_Err2Array_1x1.append(FS_error2_1x1)
   FS_Err2Array_2x2.append(FS_error2_2x2)

ps1.output.off();             # turn output off for power supply 1
ps2.output.off();             # turn output off for power supply 2     
SumRelError1_1x1 = sum(RelErr1Array_1x1)  
SumRelError2_1x1 = sum(RelErr2Array_1x1)  
SumRelError1_2x2 = sum(RelErr1Array_2x2)  
SumRelError2_2x2 = sum(RelErr2Array_2x2)  
MPE1_1x1 = (100/len(RelErr1Array_1x1))*SumRelError1_1x1
MPE2_1x1 = (100/len(RelErr2Array_1x1))*SumRelError2_1x1
MPE1_2x2  = (100/len(RelErr1Array_2x2 ))*SumRelError1_2x2 
MPE2_2x2  = (100/len(RelErr2Array_2x2 ))*SumRelError2_2x2 

print('Maximum percent error in Param1_1 calculation using alpha11 and alpha22 is: ', max(Error1Array_1x1))   
print('Maximum percent error in Param1_2 calculation using alpha11 and alpha22 is: ', max(Error2Array_1x1)) 
print('Mean percentage error in Param1_1 calculation using alpha11 and alpha22 is: ', MPE1_1x1)   
print('Mean percentage error in Param1_2 calculation using alpha11 and alpha22 is: ', MPE2_1x1) 
print('Maximum percent error in Param1_1 calculation using alpha matrix 2x2 is: ', max(Error1Array_2x2))   
print('Maximum percent error in Param1_2 calculation using alpha matrix 2x2 is: ', max(Error2Array_2x2)) 
print('Mean percentage error in Param1_1 calculation using alpha matrix 2x2 is: ', MPE1_2x2)   
print('Mean percentage error in Param1_2 calculation using alpha matrix 2x2 is: ', MPE2_2x2) 

print('FS Error Param1_1 using alpha11 & 22 [%] ', FS_Err1Array_1x1)   
print('FS Error Param1_2 using alpha11 & 22 [%] ', FS_Err2Array_1x1) 
print('FS Error Param1_1 using alpha 2x2 [%] ', FS_Err1Array_2x2)   
print('FS Error Param1_2 using alpha 2x2 [%] ', FS_Err2Array_2x2) 

excelObj.addColumn('Param1 through busbar 1 measured [A]', Param1_1_meas);
excelObj.addColumn('Param1 through busbar 2 measured [A]', Param1_2_meas);
excelObj.addColumn('Param1 Difference [A]', Param1_diff);

excelObj.addColumn('Percent Error Param1_1 using alpha11 & 22 [%]', Error1Array_1x1);
excelObj.addColumn('Percent Error Param1_2 using alpha11 & 22 [%]', Error2Array_1x1);

excelObj.addColumn('Percent Error Param1_1 using alpha 2x2 [%]', Error1Array_2x2);
excelObj.addColumn('Percent Error Param1_2 using alpha 2x2 [%]', Error2Array_2x2); 
excelObj.addColumn('FS Error Param1_1 using alpha11 & 22 [%]', FS_Err1Array_1x1);
excelObj.addColumn('FS Error Param1_2 using alpha11 & 22 [%]', FS_Err2Array_1x1);
excelObj.addColumn('FS Error Param1_1 using alpha 2x2 [%]', FS_Err1Array_2x2);
excelObj.addColumn('FS Error Param1_2 using alpha 2x2 [%]', FS_Err2Array_2x2); 

excelObj.saveExcel();
            
del(excelObj);  

   
       