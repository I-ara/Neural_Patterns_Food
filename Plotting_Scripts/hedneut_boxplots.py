from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
# Get data #############################################################################################################

# Get all datasets from Excel file - output from BV
excelsheet_path = ('Cluster_x.xlsx')

# Each will have a cluster
df = pd.read_excel(excelsheet_path)

# Filter out rows where 'Predictor' contains the string 'health'
df_filtered = df[~df['Predictor'].str.contains('health', case=False, na=False)]


# Difference of Weights ################################################################################################

# Defines the pairs of predictors and their corresponding weights
pairs = [
    ('Hedonic_hc_P', 'Neutral_hc_P'),
    ('Hedonic_hc_U', 'Neutral_hc_U'),
    ('Hedonic_lc_P', 'Neutral_lc_P'),
    ('Hedonic_lc_U', 'Neutral_lc_U')
]
weights = [1, 1, 1, 1]

# Calculates differences between conditions per subject
differences_list = []

for subject in df['Subject'].unique():
    subject_data = df[df['Subject'] == subject]
    for cond1, cond2 in pairs:
        # Extract the beta values for the conditions
        beta_cond1 = subject_data.loc[subject_data['Predictor'] == cond1, 'beta'].values[0]
        beta_cond2 = subject_data.loc[subject_data['Predictor'] == cond2, 'beta'].values[0]
        # Calculate the difference
        difference = beta_cond1 - beta_cond2
        differences_list.append({'Subject': subject, 'Difference': difference})

# Convert the list of differences into a DataFrame
df_differences = pd.DataFrame(differences_list)

# Weighted mean per subject jic
def calculate_weighted_mean(diffs):
    return sum(diffs * weights) / sum(weights)

# Group by Subject and apply the weighted mean
result = df_differences.groupby('Subject')['Difference'].apply(calculate_weighted_mean).reset_index(name='Weighted_Mean')


# Mean of Subjects

weights_dict = {
    'Hedonic_hc_P': 1,
    'Neutral_hc_P': 1,
    'Hedonic_hc_U': 1,
    'Neutral_hc_U': 1,
    'Hedonic_lc_P': 1,
    'Neutral_lc_P': 1,
    'Hedonic_lc_U': 1,
    'Neutral_lc_U': 1
}

# Create a new column 'Weight' based on the Predictor
df_filtered['Weight'] = df_filtered['Predictor'].map(weights_dict)

def weighted_condmean(group):
    return (group['beta'] * group['Weight']).sum() / group['Weight'].sum()

# Calculates weighted mean for Hedonic and Neutral predictors
# Group by Subject and categorize the predictors into Hedonic and Neutral
df_filtered['Predictor_Type'] = df_filtered['Predictor'].apply(lambda x: 'Hedonic' if 'Hedonic' in x else 'Neutral')

weighted_means = df_filtered.groupby(['Subject', 'Predictor_Type']).apply(weighted_condmean).reset_index(name='Weighted_Mean')

# Pivot the table so that each subject has a column for Hedonic and Neutral weighted means
weighted_mean_pertype = weighted_means.pivot(index='Subject', columns='Predictor_Type', values='Weighted_Mean').reset_index()


df_meltconds = weighted_mean_pertype.melt(id_vars=['Subject'],
                                       value_vars=['Hedonic', 'Neutral'],
                                       var_name='Condition',
                                       value_name='Weighted Mean')

df_meltconds['Subject Order'] = list(range(1, 109)) + list(range(1, 109))

# Ensure Subject is categorical for better plotting
df_meltconds['Subject Order'] = df_meltconds['Subject Order'].astype('category')
df_meltconds['Condition'] = df_meltconds['Condition'].astype('category')

# POLT

f, ax = plt.subplots()
sns.despine(bottom=True, left=True)
sns.set_theme(style="whitegrid", palette="pastel")
sns.stripplot(
    data=df_meltconds, y="Weighted Mean", hue="Condition",
    dodge=True, alpha=.25, zorder=1, legend=False, palette=['m', 'g'], size=5
)

sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(data=df_meltconds,
            y='Weighted Mean', hue='Condition', palette=['m', 'g'],
            saturation=1, fill=None
            )

#plt.title('Boxplot of Hedonic and Neutral Conditions for Cluster X')
#plt.ylabel('Weighted Mean - in percent signal change')
#plt.xlabel('')
#plt.legend('')
plt.ylim(-1, 1)

ax.yaxis.grid(True)
sns.despine(trim=True, left=True)

plt.show()

