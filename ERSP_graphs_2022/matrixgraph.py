import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#font = {'size'   : 20}

#plt.rc('font', **font)
#plt.rcParams.update({'font.size': 22})
#plt.style.use('default')
font = {'size': 20}
plt.rc('font', **font)  # pass in the font dict as kwargs
N = [10	,20	,50	,100,	200,	300,	400,	500,	1000];

y2 = [0, 1, 2, 3, 4, 5 , 6, 7, 8, 9, 10];
avgAWS = [0.0353,0.04766666667,	0.08433333333	,0.585,	2.868	,9.466333333,	22.676,	44.956,	361.2243333];
N = [10	,20	,50	,100,	200,	300,	400,	500,	1000];
Ratio= [5.889203651,	4.407925408,	7.528326746,	5.939411206,	9.075003874,	9.295444675,	9.264538131,	10.56835573,	9.996320846];
avgPhones = [0.2078888889,	0.2101111111,	0.6348888889,	3.474555556,	26.02711111,	87.99377778,	210.0826667,	475.111,	3610.914333];
#fig, ax1 = plt.subplots(figsize=(10, 6))
my_yticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13];
Energy = [2.30 , 2.33,  2.44, 2.52, 2.69, 2.80, 2.81 , 2.70, 1.91 ] #average 
#EnergyMax = [2.88 ,2.93,3.00,3.10, 3.27, 3.51, 3.47,3.63 ,3.39]
N2 = [10	,20	,50	,100,	200,	300,	400,	500, 1000];
fig = plt.figure()
# to change size of subplot's
# set height of each subplot as 8
fig.set_figheight(10)
# set width of each subplot as 8
fig.set_figwidth(12)
plt.style.use('seaborn-whitegrid')
plt.rc('axes', axisbelow=True)
 
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 2]) 
ax1 = plt.subplot(gs[1])
ax2 = ax1.twinx();

fig, fig1 =  plt.subplots(figsize=(10, 6))
fig1 = plt.subplot(gs[0], sharex = ax1)
line4, = plt.plot(N2, Energy, c="green", lw=2, label = "Energy Consumption")
#line5, = plt.plot(N2, EnergyMax, c="teal", lw=2, label = "Energy Consumption")

fig1.set_ylabel('Power (Watts)', fontsize = 24)
fig1.tick_params(axis='both', which='major', labelsize=24)

#fig1.set_xlabel('N number of rows/columns in matrices',fontsize = 15)

line1, = ax1.plot(N, avgAWS,linewidth=3, color = "red", label = "AWS", linestyle='--');
line2, =ax1.plot(N, avgPhones,linewidth=3, color = "blue", label = "Phones", linestyle='--');
line3, = ax2.plot(N, Ratio, 'purple', label = "Slowdown Ratio", linewidth= 5)
ax1.scatter(N, avgAWS,linewidth=1, color = "red");
ax1.scatter(N, avgPhones,linewidth=1, color = "blue");

ax2.set_yticks(my_yticks, minor=True);
plt.setp(fig1.get_xticklabels(), visible=False)
plt.setp(fig1.get_xlabel(), visible = False)
plt.subplots_adjust(hspace=.0)

ax2.set_ylabel('Slowdown ratio (Phone/AWS)', fontsize = 24)
ax1.set_ylabel('Latency (s)',fontsize = 24)
plt.title('Matrix Multiplication Performance Phones VS AWS Average',fontsize = 30)
ax1.tick_params(axis='both', which='major', labelsize=24)
ax2.tick_params(axis='both', which='major', labelsize=24)
ax1.set_xlabel('N number of rows/columns in matrices',fontsize = 24)

#ax1.legend(loc = "upper left")
#ax2.legend(loc="upper left")
plt.subplots_adjust(hspace=.2)
ax2.annotate("Slowdown Ratio", (600,11), fontsize=24)
#fig1.legend((line3, line4), ('Slowdown Ratio','Energy'), loc='lower right')
ax1.set_axisbelow(True)
ax2.set_axisbelow(True)

ax1.legend((line2, line1), ('Phones', 'AWS'), fontsize = 24, frameon = True, facecolor = "white")

#plt.xlabel('N number of rows/columns in matrices',fontsize = 15)


plt.savefig('MatrixMultResult3.svg')
plt.show()
