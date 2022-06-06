#CDN Results


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import AnchoredText

SizeFile = [1/10, 1, 5,  10]

LoadTimePhone = [1.1952,	6.063,	20.8296,	87.54675]
LoadTimeAWS = [0.959,1.2083, 2.451375, 4.2368 ] #cloudfront

plt.figure(figsize=(16,6))
font = {'size': 24}
plt.rc('font', **font)  # pass in the font dict as kwargs

x = np.arange(0, 10, 0.1)

fig, ax1 = plt.subplots(figsize=(12,6))

ax2 = ax1.twinx()
line1, = ax1.plot(SizeFile, LoadTimePhone, 'g-', linestyle='--', linewidth =2)
line2, =ax2.plot(SizeFile, LoadTimeAWS, 'b-', linestyle='dotted', linewidth = 3)

ax1.set_xlabel('Size of File (mb)', fontsize=24)
ax1.set_ylabel('Load Time of File on phones(s)', fontsize =24)
ax2.set_ylabel('Load time of File on AWS (s)' , fontsize=24)


plt.xlabel("Number of Phones", fontsize = 24)
plt.title('CDN',fontsize = 30)
#plt.xticks(SizeFile)
#ax1.set_xticklabels(SizeFile, rotation = (45), fontsize = 24)
plt.style.use('seaborn-whitegrid')

plt.legend((line1, line2), ('Phones', 'AWS'), loc='upper center', fontsize = 24)

at = AnchoredText(
    "Network 1", prop=dict(size=15), frameon=True, loc='center right')
at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
ax1.add_artist(at)

plt.savefig('cdn2.svg')
plt.show()
