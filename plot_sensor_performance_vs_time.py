# -*- coding: utf-8 -*-
"""
March 2019 - Plotting sensor output characteristics 1-4 vs. time for a specific magnitude of a control parameter  
Description: The control parameter is applied to the sensor for fixed accumulated periods of time. The output characteristics
are plotted vs. unscaled time axis
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
def connectpoints(x,y,p1,p2,col):
    x1, x2 = x[p1], x[p2]
    y1, y2 = y[p1], y[p2]
    cl = str(col)
    plt.plot([x1,x2],[y1,y2],cl+'-')

plt.xlabel('Time(hr)')
plt.ylabel('Characteristic 1 (Units)')
a = np.arange(4)
b = [0,1,17,80]

ax = plt.axes()

#Controls
ax.plot([0,0], [4.34,4.34], 'm+' , label='Control-no transducer input', markersize=15)
ax.plot([1,1], [4.34,4.34], 'm+' , markersize=15 )
ax.plot([2,2], [4.34,4.35], 'm+' , markersize=15)
ax.plot([0,0,0,0,0], [3.98,4.31,4.31,4.33,4.31], 'ro' , label='no transducer input')
ax.plot([1,1,1,1,1], [3.95,4.3,4.3,4.31,4.29], 'bs', label='magnitude u1')

ax.plot([2,2,2,2,2], [3.97,4.33,4.31,4.34,4.31], 'bs')
ax.plot([3,3,3,3,3], [4.0,4.33,4.35,4.36,4.33], 'bs')
ax.xaxis.set_ticks(a)
ax.xaxis.set_ticklabels(b)

x = [0,0,0,0,0,1,1,1,1,1]
y= [3.98,4.31,4.31,4.33,4.31,3.95,4.3,4.3,4.31,4.29]
connectpoints(x,y,0,5,'g')
connectpoints(x,y,1,6,'b')
connectpoints(x,y,2,7,'c')
connectpoints(x,y,3,8,'k')
connectpoints(x,y,4,9,'y')
x1 = [1,1,1,1,1,2,2,2,2,2]
y1= [3.95,4.3,4.3,4.31,4.29,3.97,4.33,4.31,4.34,4.31]
connectpoints(x1,y1,0,5,'g')
connectpoints(x1,y1,1,6,'b')
connectpoints(x1,y1,2,7,'c')
connectpoints(x1,y1,3,8,'k')
connectpoints(x1,y1,4,9,'y')
x2 = [2,2,2,2,2,3,3,3,3,3]
y2= [3.97,4.33,4.31,4.34,4.31,4.0,4.33,4.35,4.36,4.33]
connectpoints(x2,y2,0,5,'g')
connectpoints(x2,y2,1,6,'b')
connectpoints(x2,y2,2,7,'c')
connectpoints(x2,y2,3,8,'k')
connectpoints(x2,y2,4,9,'y')

plt.legend()
plt.show()


plt.xlabel('Time(hr)')
plt.ylabel('Characteristic 2 (Units)')
ax1 = plt.axes()

ax1.plot([0,0], [0.449,0.418], 'm+' , label='Control-no transducer input', markersize=15)
ax1.plot([1,1], [0.456,0.417], 'm+' , markersize=15)
ax1.plot([2,2], [0.456,0.416], 'm+' , markersize=15)
ax1.plot([0,0,0,0,0], [0.369, 0.398, 0.384, 0.426, 0.424], 'ro' , label='no transducer input')
ax1.plot([1,1,1,1,1], [0.4, 0.431, 0.42, 0.477, 0.426], 'bs' , label='magnitude u1')
ax1.plot([2,2,2,2,2], [0.423, 0.469, 0.416, 0.461, 0.441],'bs') 
ax1.plot([3,3,3,3,3], [0.411, 0.449, 0.419, 0.521, 0.459],'bs') 
x = [0,0,0,0,0,1,1,1,1,1]
y= [0.369, 0.398, 0.384, 0.426, 0.424,0.4, 0.431, 0.42, 0.477, 0.426]
ax1.xaxis.set_ticks(a)
ax1.xaxis.set_ticklabels(b)
connectpoints(x,y,0,5,'g')
connectpoints(x,y,1,6,'b')
connectpoints(x,y,2,7,'c')
connectpoints(x,y,3,8,'k')
connectpoints(x,y,4,9,'y')
x1 = [1,1,1,1,1,2,2,2,2,2]
y1= [0.4, 0.431, 0.42, 0.477, 0.426,0.423, 0.469, 0.416, 0.461, 0.441]
connectpoints(x1,y1,0,5,'g')
connectpoints(x1,y1,1,6,'b')
connectpoints(x1,y1,2,7,'c')
connectpoints(x1,y1,3,8,'k')
connectpoints(x1,y1,4,9,'y')
x2 = [2,2,2,2,2,3,3,3,3,3]
y2= [0.423, 0.469, 0.416, 0.461, 0.441,0.411, 0.449, 0.419, 0.521, 0.459]
connectpoints(x2,y2,0,5,'g')
connectpoints(x2,y2,1,6,'b')
connectpoints(x2,y2,2,7,'c')
connectpoints(x2,y2,3,8,'k')
connectpoints(x2,y2,4,9,'y')

plt.legend()
plt.show()

plt.xlabel('Time(hr)')
plt.ylabel('Characteristic 3 (Units)')
ax = plt.axes()

ax.plot([0,0], [-3.37,-0.174], 'm+' , label='Control-no transducer input', markersize=15)
ax.plot([1,1], [-3.36,-0.153], 'm+' , markersize=15)
ax.plot([2,2], [-3.39,-0.19], 'm+' , markersize=15)
ax.plot([0,0,0,0,0], [2.21,-0.713,0.841,-0.669,0.317], 'ro' , label='no transducer input')
ax.plot([1,1,1,1,1], [1.69,-1.64,-0.987,-1,-0.0705], 'bs', label='magnitude u1')
ax.plot([2,2,2,2,2], [1.22,-0.699,0.376,-1.25,-0.852], 'bs')
ax.plot([3,3,3,3,3], [3.3,.0475,1.26,1.18,0.757],'bs') 
x = [0,0,0,0,0,1,1,1,1,1]
y= [2.21,-0.713,0.841,-0.669,0.317,1.69,-1.64,-0.987,-1,-0.0705]
ax.xaxis.set_ticks(a)
ax.xaxis.set_ticklabels(b)
connectpoints(x,y,0,5,'g')
connectpoints(x,y,1,6,'b')
connectpoints(x,y,2,7,'c')
connectpoints(x,y,3,8,'k')
connectpoints(x,y,4,9,'y')
x1 = [1,1,1,1,1,2,2,2,2,2]
y1= [1.69,-1.64,-0.987,-1,-0.0705,1.22,-0.699,0.376,-1.25,-0.852]
connectpoints(x1,y1,0,5,'g')
connectpoints(x1,y1,1,6,'b')
connectpoints(x1,y1,2,7,'c')
connectpoints(x1,y1,3,8,'k')
connectpoints(x1,y1,4,9,'y')
x2 = [2,2,2,2,2,3,3,3,3,3]
y2= [1.22,-0.699,0.376,-1.25,-0.852,3.3,.0475,1.26,1.18,0.757]
connectpoints(x2,y2,0,5,'g')
connectpoints(x2,y2,1,6,'b')
connectpoints(x2,y2,2,7,'c')
connectpoints(x2,y2,3,8,'k')
connectpoints(x2,y2,4,9,'y')


plt.legend()
plt.show()


plt.xlabel('Time(hr)')
plt.ylabel('Characteristic 4 (Units)')
ax = plt.axes()

ax.plot([0,0], [.102,.0953], 'm+' , label='Control-no transducer input', markersize=15)
ax.plot([1,1], [.0989,.0959], 'm+' , markersize=15)
ax.plot([2,2], [.101,.0924],  'm+' , markersize=15)
ax.plot([0,0,0,0,0], [0.0911,0.0996,0.0976,0.0975,0.0999], 'ro' , label='no transducer input')
ax.plot([1,1,1,1,1], [0.106,0.101,0.108,0.103,0.101], 'bs', label='magnitude u1')
ax.plot([2,2,2,2,2], [0.0153,0.103,0.107,0.103,0.102], 'bs')
ax.plot([3,3,3,3,3], [0.0454,0.0839,0.0809,0.0807,0.107],'bs') 
x = [0,0,0,0,0,1,1,1,1,1]
y= [0.0911,0.0996,0.0976,0.0975,0.0999,0.106,0.101,0.108,0.103,0.101]
ax.xaxis.set_ticks(a)
ax.xaxis.set_ticklabels(b)
connectpoints(x,y,0,5,'g')
connectpoints(x,y,1,6,'b')
connectpoints(x,y,2,7,'c')
connectpoints(x,y,3,8,'k')
connectpoints(x,y,4,9,'y')
x1 = [1,1,1,1,1,2,2,2,2,2]
y1= [0.106,0.101,0.108,0.103,0.101,0.0153,0.103,0.107,0.103,0.102]
connectpoints(x1,y1,0,5,'g')
connectpoints(x1,y1,1,6,'b')
connectpoints(x1,y1,2,7,'c')
connectpoints(x1,y1,3,8,'k')
connectpoints(x1,y1,4,9,'y')
x2 = [2,2,2,2,2,3,3,3,3,3]
y2= [0.0153,0.103,0.107,0.103,0.102,0.0454,0.0839,0.0809,0.0807,0.107]
connectpoints(x2,y2,0,5,'g')
connectpoints(x2,y2,1,6,'b')
connectpoints(x2,y2,2,7,'c')
connectpoints(x2,y2,3,8,'k')
connectpoints(x2,y2,4,9,'y')

plt.legend()
plt.show()


