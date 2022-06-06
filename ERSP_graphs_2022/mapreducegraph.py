
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

my_dict = {'1': [69.9, 55.6, 58.9, 51.7, 48.9], '2': [45, 39.3, 47.2, 53.3, 86], '3':[90.4, 89.6, 73.2, 58.4, 49.1],
           '4':[231, 230.3]}


my_dict2 = {'1': [57.538, 58.159, 57.381, 56.64, 58.483], '2': [45.182, 43.363, 49.109, 45.71, 43.817], 
            '3':[41.563, 45.792, 40.792, 40.993 ,46.439],
           '4':[30.002, 28.072, 37.444, 28.427, 37.274]}
from matplotlib.offsetbox import AnchoredText



N = [1, 2, 3, 4, 5]
Energy = [1, 2, 3, 4, 5]
fig = plt.figure()

plt.style.use('seaborn-whitegrid')
# to change size of subplot's
# set height of each subplot as 8
fig.set_figheight(10)
# set width of each subplot as 8
fig.set_figwidth(12)

gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1]) 
ax = plt.subplot(gs[1])
#fig, fig1 =  plt.subplots(figsize=(10, 6))
#fig1 = plt.subplot(gs[0], sharex = ax, sharey = ax)
#fig1.set_ylabel("Energy ")
#line4, = plt.plot(N, Energy, c="green", lw=2, label = "Energy Consumption")
plt.setp(fig1.get_xlabel(), visible = False)
plt.setp(fig1.get_xticklabels(), visible=False)
fig1.set_ylabel('Latency (s)', fontsize = 24)

plt.subplots_adjust(hspace=.2)

#fig, ax = plt.subplots()
#fig1.boxplot(my_dict.values())
ax.boxplot(my_dict2.values())

ax.set_xlabel('Number of phones', fontsize=24)
ax.set_ylabel('Latency (s)', fontsize =24)
ax.set_xticklabels(my_dict.keys(), fontsize = 20)
font = {'size': 20}
plt.rc('font', **font)

at = AnchoredText(
    "Network 2", prop=dict(size=15), frameon=True, loc='center right')
at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
ax.add_artist(at)
#at = AnchoredText(
 #   "Network 1", prop=dict(size=15), frameon=True, loc='center right')
#at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
#fig1.add_artist(at)
#plt.yticks(np.arange(0, 232, 30), fontsize = 20)
plt.title('Map Reduce Timings on Cluster',fontsize = 30)

plt.savefig('mapping9.svg')
plt.show()
