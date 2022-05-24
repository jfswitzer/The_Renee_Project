#AVERAGE Carbon Metrics for Phones colored by company 
import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
# import seaborn
import seaborn as sns
%matplotlib inline

plt.style.use('seaborn')  # to get seaborn scatter plot
data = pd.read_csv('Smartphones - AVERAGE carbon.csv')
plt.figure(figsize=(10,6))
sns.set(font_scale = 20)
sns.set(style="whitegrid")
d =sns.scatterplot(x="Year released", y="Carbon",hue="Company",linewidth=1, data=data, s = 90, legend = False);

plt.title('Manufacturing Carbon of Mobile Phones',fontsize = 20)
plt.xlabel('Year Released',fontsize = 20)
plt.ylabel('Carbon (kgCO2e)',fontsize = 20)

fontsize = 20

plt.legend(loc="upper left", frameon=True)
ax = sns.lineplot(x="Year released", y="Carbon",hue="Company",linewidth=3, data=data);
plt.rc('ytick', labelsize=25) 
plt.setp(ax.get_legend().get_texts(), fontsize='15')
plt.setp(ax.get_legend().get_title(), fontsize='18')
plt.yticks(fontsize = 13)
plt.xticks(fontsize = 13)
plt.savefig("Averagecarbonmetric.svg");
