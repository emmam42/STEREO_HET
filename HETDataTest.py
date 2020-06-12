#!/usr/bin/env python
# coding: utf-8

# In[65]:


#imports
import numpy as np
import scipy as sp
import astropy as ap
import matplotlib.pyplot as plt
import pandas as pd
from time import strptime


# In[66]:


#ASCII reading in data 

#Adjust filename and inttime as necessary
filename = 'AeH11Feb.15m'
inttime = '15minute'
###########################

from astropy.extern.six.moves.urllib import request
url = 'http://www.srl.caltech.edu/STEREO/DATA/HET/Ahead/%s/%s' % (inttime,filename)
open(filename, 'wb').write(request.urlopen(url).read())
f = open(filename, 'r')

#all data 
data_in = pd.read_csv(filename, header=22, delimiter='\s+')


# In[67]:


#creating variables for each data collumn
year = data_in.iloc[0,1]
month = data_in.iloc[0,2]
month = strptime(month,'%b').tm_mon
#month = dt.strptime((month),'%b')  #NOTE month is now one number *not array (data is only one month at a time)
day = data_in.iloc[0:,3]
time = data_in.iloc[0:,4]
hour = (np.floor(time/100))
minute = abs(time) % 100

#make pandas dataframe for data and convert to datetime variable
df = pd.DataFrame({'year': year,'month': month,'day': day,'hour':hour,'minute':minute})
times = pd.to_datetime(df)
#print(times)

#electron measurements, errors are column following http://www.srl.caltech.edu/STEREO/Public/HET_public.html
#for time averaged data #COMMENT OUT THIS BLOCK AND UNCOMMENT NEXT BLOCK FOR NON AVERAGED (ONE MINUTE) INT

#'''

e1 = data_in.iloc[0:,9]
e2 = data_in.iloc[0:,11]
e3 = data_in.iloc[0:,13]

#error
se1 = data_in.iloc[0:,10]
se2 = data_in.iloc[0:,12]
se3 = data_in.iloc[0:,14]


#proton measurements
p1 = data_in.iloc[0:,15]
p2 = data_in.iloc[0:,17]
p3 = data_in.iloc[0:,19]
p4 = data_in.iloc[0:,21]
p5 = data_in.iloc[0:,23]
p6 = data_in.iloc[0:,25]
p7 = data_in.iloc[0:,27]
p8 = data_in.iloc[0:,29]
p9 = data_in.iloc[0:,31]
p10 = data_in.iloc[0:,33]
p11 = data_in.iloc[1:,35]

#error
sp1 = data_in.iloc[0:,16]
sp2 = data_in.iloc[0:,18]
sp3 = data_in.iloc[0:,20]
sp4 = data_in.iloc[0:,22]
sp5 = data_in.iloc[0:,24]
sp6 = data_in.iloc[0:,26]
sp7 = data_in.iloc[0:,28]
sp8 = data_in.iloc[0:,30]
sp9 = data_in.iloc[0:,32]
sp10 = data_in.iloc[0:,34]
sp11 = data_in.iloc[0:,36]



'''
#for one minute data (no end time)
e1 = data_in.iloc[0:,5]
e2 = data_in.iloc[0:,7]
e3 = data_in.iloc[0:,9]

#error
se1 = data_in.iloc[0:,6]
se2 = data_in.iloc[0:,8]
se3 = data_in.iloc[0:,10]

#proton measurements
p1 = data_in.iloc[0:,11]
p2 = data_in.iloc[0:,13]
p3 = data_in.iloc[0:,15]
p4 = data_in.iloc[0:,17]
p5 = data_in.iloc[0:,19]
p6 = data_in.iloc[0:,21]
p7 = data_in.iloc[0:,23]
p8 = data_in.iloc[0:,25]
p9 = data_in.iloc[0:,27]
p10 = data_in.iloc[0:,29]
#p11 = data_in.iloc[1:,31]

#error
sp1 = data_in.iloc[0:,12]
sp2 = data_in.iloc[0:,14]
sp3 = data_in.iloc[0:,16]
sp4 = data_in.iloc[0:,18]
sp5 = data_in.iloc[0:,20]
sp6 = data_in.iloc[0:,22]
sp7 = data_in.iloc[0:,24]
sp8 = data_in.iloc[0:,26]
sp9 = data_in.iloc[0:,28]
sp10 = data_in.iloc[0:,30]
sp11 = data_in.iloc[0:,32]
'''

#error propagation
#electrons
se = np.sqrt((.7*se1)**2+(1.4*se2)**2+(1.2*se3)**2)
#protons 
spl = np.sqrt((sp1)**2+(sp2)**2+(sp3)**2+(sp4)**2)/10.2
sph = np.sqrt((sp5)**2+(sp6)**2+(sp7)**2+(sp8)**2+(sp9)**2)/16.7


# In[68]:


#set up figure 
plt.figure(figsize=(9, 6), dpi= 80, facecolor='w', edgecolor='k')

#plot three scatter plots on same graph
plt.plot(times,(e1*.7+e2*1.4+e3*1.2)/3.3, 'bs',  markersize=4,label = 'Electrons (0.7 - 4.0 MeV)')
plt.plot(times, (p1+p2+p3+p4)/10.2, 'cs',  markersize=4,label = 'Protons (13.6 - 23.8 MeV)')
plt.plot(times, (p5+p6+p7+p8+p9)/16.7, 'gs', markersize=4,label = 'Protons (23.8 - 40.5 MeV)')

#Axes format
plt.xticks(rotation=45)
#plt.xlim(times[300], times[1500]) #UNCOMMENT FOR PORTION OF PLOT (DAYS/HOURS)
plt.yscale('log')
# Add legend
plt.legend(loc=2, ncol=1,fontsize = 16)
# Add titles
plt.title("STEREO IMPACT HET Electron and Proton Intensity (%s averages)" % inttime, loc='center', fontsize=18, fontweight=2)
plt.xlabel("Time",fontsize=18)
plt.ylabel("Intensity (cm2-sr-sec-MeV)",fontsize=18)

plt.show()

#Figure with error bars ########New figure

plt.figure(figsize=(9, 6), dpi= 80, facecolor='w', edgecolor='k')
plt.plot(times,(e1*.7+e2*1.4+e3*1.2)/3.3, 'bs',  markersize=4,label = 'Electrons (0.7 - 4.0 MeV)')
plt.plot(times, (p1+p2+p3+p4)/10.2, 'cs',  markersize=4,label = 'Protons (13.6 - 23.8 MeV)')
plt.plot(times, (p5+p6+p7+p8+p9)/16.7, 'gs', markersize=4,label = 'Protons (23.8 - 40.5 MeV)')

plt.xticks(rotation=45)
#plt.xlim(times[300], times[1500])
plt.yscale('log')
# Add legend
plt.legend(loc=2, ncol=1,fontsize = 16)
# Add titles
plt.title("STEREO IMPACT HET Electron and Proton Intensity (%s averages)" % inttime, loc='center', fontsize=18, fontweight=2)
plt.xlabel("Time",fontsize=18)
plt.ylabel("Intensity (cm2-sr-sec-MeV)",fontsize=18)

plt.errorbar(times,(e1*.7+e2*1.4+e3*1.2)/3.3, yerr=se, color='b',ls = 'none')
plt.errorbar(times,(p1+p2+p3+p4)/10.2, yerr=spl, color='c',ls = 'none')
plt.errorbar(times,(p5+p6+p7+p8+p9)/16.7, yerr=sph, color='g',ls = 'none')


plt.show()


# In[ ]:




