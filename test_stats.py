

import pandas as pd
import numpy as np

df=pd.read_excel('right_cheek.xlsx')
df.head()

df.info()

from scipy import stats

#checking for normality of data
from scipy.stats import shapiro
for col in df.columns:
  test=shapiro(df[col])
  if test[1]>0.05:
    print(col,'is normally distributed')
  else:
    print(col,'is not normally distributed')

"""above code show that data is normally distribute i will go with ANOVA because same subjects are measured multiple time with different time point

"""

df['subject'] = df.index
df_right = pd.melt(df, id_vars='subject', var_name='timepoint', value_name='L*')
df_right.head(50)

from statsmodels.stats.anova import AnovaRM
ANOVA=AnovaRM(df_right,depvar='L*',subject='subject',within=['timepoint'])
result=ANOVA.fit()
if result.anova_table['Pr > F'][0]<0.05:
  print('reject null hypothesis,there is strong difference between timepoint')
else:
  print('fail to reject null hypothesis,there is no strong difference between time point')

df2=pd.read_excel('left_cheek.xlsx')
df2.head()

from scipy.stats import shapiro
for col in df2.columns:
  test=shapiro(df2[col])
  if test[1]>0.05:
    print(col,'is normally distributed')
  else:
    print(col,'is not normally distributed')

from statsmodels.stats.anova import AnovaRM
df2['subject'] = df2.index
df_left = pd.melt(df2, id_vars='subject', var_name='timepoint', value_name='L*')
df_left.head(50)

anova=AnovaRM(df_left,depvar='L*',subject='subject',within=['timepoint'])
result=anova.fit()
print(result.anova_table)
if result.anova_table['Pr > F'][0]<0.05:
  print('reject null hypothesis,there is strong difference between timepoint')
else:
  print('fail to reject null hypothesis,there is no strong difference between time point')

df_left['timepoint'].unique()

import matplotlib.pyplot as plt

# Compute mean and std for each timepoint by grouping the melted dataframes
left_mean = df_left.groupby('timepoint')['L*'].mean()
left_std = df_left.groupby('timepoint')['L*'].std()

right_mean = df_right.groupby('timepoint')['L*'].mean()
right_std = df_right.groupby('timepoint')['L*'].std()

# Ensure the timepoints are in the desired order for plotting
timepoint_order = ['Visit 1 - Baseline', 'Visit 1 - Timm', 'Visit 2', 'Visit 3']
left_mean = left_mean.reindex(timepoint_order)
left_std = left_std.reindex(timepoint_order)
right_mean = right_mean.reindex(timepoint_order)
right_std = right_std.reindex(timepoint_order)

# Plotting
plt.figure(figsize=(4, 4))
plt.errorbar(left_mean.index, left_mean, yerr=left_std, label='Left Cheek', marker='o', capsize=5)
plt.errorbar(right_mean.index, right_mean, yerr=right_std, label='Right Cheek', marker='o', capsize=5)

plt.title('Skin Brightness (L*) Over Time')
plt.xlabel('Time Point')
plt.ylabel('L* Value')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Timepoints to compare
baseline = 'Visit 1 - Baseline'
final = 'Visit 3'

# Compute mean and std for both cheeks at baseline and final visit
left_baseline_mean = df_left[df_left['timepoint'] == baseline]['L*'].mean()
left_baseline_std = df_left[df_left['timepoint'] == baseline]['L*'].std()
left_final_mean = df_left[df_left['timepoint'] == final]['L*'].mean()
left_final_std = df_left[df_left['timepoint'] == final]['L*'].std()

right_baseline_mean = df_right[df_right['timepoint'] == baseline]['L*'].mean()
right_baseline_std = df_right[df_right['timepoint'] == baseline]['L*'].std()
right_final_mean = df_right[df_right['timepoint'] == final]['L*'].mean()
right_final_std = df_right[df_right['timepoint'] == final]['L*'].std()

left_means = [left_baseline_mean, left_final_mean]
left_stds = [left_baseline_std, left_final_std]

right_means = [right_baseline_mean, right_final_mean]
right_stds = [right_baseline_std, right_final_std]


# Bar chart setup
labels = ['Baseline', 'Visit 3']
x = np.arange(len(labels))  # [0, 1]
width = 0.35  # Width of each bar

fig, ax = plt.subplots(figsize=(3, 3))

# Plot bars
bars1 = ax.bar(x - width/2, left_means, width, yerr=left_stds, capsize=5, label='Left Cheek', color='skyblue')
bars2 = ax.bar(x + width/2, right_means, width, yerr=right_stds, capsize=5, label='Right Cheek', color='lightgreen')

# Labels and titles
ax.set_ylabel('L* Value (Skin Brightness)')
ax.set_title('Improvement in Skin Brightness (Baseline vs Visit 3)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.grid(True, axis='y', linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()

#check for hydration

df3=pd.read_excel('/content/corneometer.xlsx')
df3.head()

df3=df3.drop(['Unnamed: 0'],axis=1)
df3.head()

from scipy.stats import shapiro
for col in df3.columns:
  test=shapiro(df3[col])
  if test[1]>0.05:
    print(col,'is normally distributed')

  else:
    print(col,'is not normally distributed')

from statsmodels.stats.anova import AnovaRM
df3['subject'] = df3.index
df_corneometer = pd.melt(df3, id_vars='subject', var_name='timepoint', value_name='corneometer')
anova=AnovaRM(df_corneometer,depvar='corneometer',subject='subject',within=['timepoint'])
result=anova.fit()
print(result.anova_table)
if result.anova_table['Pr > F'][0]<0.05:
  print('reject null hypothesis,there is strong difference between timepoint')
else:
  print('fail to reject null hypothesis,there is no strong difference between time point')

from scipy.stats import friedmanchisquare

# Friedman test needs each column as a separate argument
friedman = friedmanchisquare(df['Visit 1 - Baseline'],
                              df['Visit 1 - Timm'],
                              df['Visit 2'],

                              df['Visit 3'])
print(friedman)
if friedman[1]>=0.05:
  print('fail to reject null hypothesis,no significance difference')
else:
  print('reject null hypothesis,strong significance difference')

"""both test indicate there is significance difference in hydration in diferent interval of time

"""

# Calculate means and standard deviations
means = df_corneometer.groupby('timepoint')['corneometer'].mean()
stds = df_corneometer.groupby('timepoint')['corneometer'].std()

# Ensure the timepoints are in the desired order for plotting
timepoint_order = ['Visit 1 - Baseline', 'Visit 1 - Timm', 'Visit 2', 'Visit 3']
means = means.reindex(timepoint_order)
stds = stds.reindex(timepoint_order)

# Plot bar chart
plt.figure(figsize=(6, 6))
plt.bar(means.index, means.values, yerr=stds.values, capsize=5,
        color='lightgreen', edgecolor='black')

# Plot labels
plt.title('Mean Skin Hydration Over Visits (Corneometer)')
plt.ylabel('Hydration Value')
plt.xlabel('Visit')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming df_corneometer is already loaded

# Step 1: Calculate means and standard deviations
means = df_corneometer.groupby('timepoint')['corneometer'].mean()
stds = df_corneometer.groupby('timepoint')['corneometer'].std()

# Ensure the timepoints are in the desired order for plotting
timepoint_order = ['Visit 1 - Baseline', 'Visit 1 - Timm', 'Visit 2', 'Visit 3']
means = means.reindex(timepoint_order)
stds = stds.reindex(timepoint_order)

# Step 2: Create line plot
plt.figure(figsize=(6, 6))
plt.errorbar(means.index, means.values, yerr=stds.values, fmt='o-', capsize=5,
             color='seagreen', ecolor='darkgreen', linewidth=2, marker='s')

# Step 3: Customize the plot
plt.title('Skin Hydration Over Time (Corneometer)')
plt.xlabel('Visit')
plt.ylabel('Hydration Value')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Step 4: Show plot
plt.show()
