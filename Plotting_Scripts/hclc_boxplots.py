from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
# Get data #############################################################################################################

# Get all datasets from Excel file - output from BV
excelsheet_path = ('cluster.xlsx')

# Each will have a cluster
df = pd.read_excel(excelsheet_path)

# Difference of Weights ################################################################################################

# Defines the pairs of predictors and their corresponding weights
pairs = [
    ('Hedonic_hc_P', 'Hedonic_lc_P'),
    ('Hedonic_hc_U', 'Hedonic_lc_U'),
    ('Neutral_hc_P', 'Neutral_lc_P'),
    ('Neutral_hc_U', 'Neutral_lc_U'),
    ('Health_hc_P', 'Health_lc_P'),
    ('Health_hc_U', 'Health_lc_U')
]
weights = [1, 1, 1, 1, 1, 1]

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
    'Health_hc_P': 1,
    'Hedonic_hc_U': 1,
    'Neutral_hc_U': 1,
    'Health_hc_U': 1,
    'Hedonic_lc_P': 1,
    'Neutral_lc_P': 1,
    'Health_lc_P': 1,
    'Hedonic_lc_U': 1,
    'Neutral_lc_U': 1,
    'Health_lc_U': 1
}

# Create a new column 'Weight' based on the Predictor
df['Weight'] = df['Predictor'].map(weights_dict)

def weighted_condmean(group):
    return (group['beta'] * group['Weight']).sum() / group['Weight'].sum()

# Calculates weighted mean for Hedonic and Neutral predictors
# Group by Subject and categorize the predictors into Hedonic and Neutral
df['Predictor_Type'] = df['Predictor'].apply(lambda x: 'High Caloric Stimuli' if 'hc' in x else 'Low Caloric Stimuli')

weighted_means = df.groupby(['Subject', 'Predictor_Type']).apply(weighted_condmean).reset_index(name='Weighted_Mean')

# Pivot the table so that each subject has a column for Hedonic and Neutral weighted means
weighted_mean_pertype = weighted_means.pivot(index='Subject', columns='Predictor_Type', values='Weighted_Mean').reset_index()


df_meltconds = weighted_mean_pertype.melt(id_vars=['Subject'],
                                       value_vars=['High Caloric Stimuli', 'Low Caloric Stimuli'],
                                       var_name='Caloric Stimuli',
                                       value_name='Weighted Mean')

df_meltconds['Subject Order'] = list(range(1, 109)) + list(range(1, 109))

# Ensure Subject is categorical for better plotting
df_meltconds['Subject Order'] = df_meltconds['Subject Order'].astype('category')
df_meltconds['Caloric Stimuli'] = df_meltconds['Caloric Stimuli'].astype('category')

# POLT

f, ax = plt.subplots()
sns.despine(bottom=True, left=True)
sns.set_theme(style="whitegrid", palette="pastel")
sns.stripplot(
    data=df_meltconds, y="Weighted Mean", hue="Caloric Stimuli",
    dodge=True, alpha=.25, zorder=1, legend=False, palette=['r', 'b'], size=5
)

sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(data=df_meltconds,
            y='Weighted Mean', hue='Caloric Stimuli', palette=['r', 'b'],
            saturation=1, fill=None
            )

#plt.title('Boxplot of Caloric Stimuli for Cluster X')
#plt.ylabel('Weighted Mean - in percent signal change')
#plt.xlabel('')
#plt.legend('')
plt.ylim(-0.8, 0.8)

ax.yaxis.grid(False)
ax.legend().remove()
sns.despine(trim=True, left=True)

# Function to determine the Sign Outcome
def determine_sign_outcome(row):
    high = row['High Caloric Stimuli']
    low = row['Low Caloric Stimuli']

    if high > 0 and low > 0 and high>low:
        return "All Positive"
    elif high < 0 and low < 0 and high>low:
        return "All Negative"
    elif high > 0 and low < 0:
        return "High Caloric Positive"
    elif high < 0 and low > 0:
        return "Low Caloric Positive"

weighted_mean_pertype['Sign Outcome'] = weighted_mean_pertype.apply(determine_sign_outcome, axis=1)

weighted_mean_pertype['Difference'] = result['Weighted_Mean']

df_meltconds = weighted_mean_pertype.melt(id_vars=['Subject', 'Sign Outcome', 'Difference'],
                                       value_vars=['High Caloric Stimuli', 'Low Caloric Stimuli'],
                                       var_name='Condition',
                                       value_name='Weighted Mean')

subject_counts = weighted_mean_pertype.groupby('Sign Outcome')['Subject'].nunique().reset_index()
# Rename the columns for clarity
subject_counts.columns = ['Sign Outcome', 'Number of Subjects']
# Define the desired order
desired_order = ["All Negative", "Low Caloric Positive", "High Caloric Positive", "All Positive"]
# Reorder the 'Sign Outcome' column according to the desired order
subject_counts['Sign Outcome'] = pd.Categorical(subject_counts['Sign Outcome'], categories=desired_order, ordered=True)
# Sort the DataFrame by the reordered 'Sign Outcome' column
subject_counts = subject_counts.sort_values('Sign Outcome')
# Reset index
subject_counts = subject_counts.reset_index(drop=True)



df_meltconds['Sign Outcome'] = pd.Categorical(df_meltconds['Sign Outcome'], categories=desired_order, ordered=True)

# Define a color map for consistent colors
colour_map = {
    "All Negative": "#FF9999",      # Light Red
    "Low Caloric Positive": "#66B3FF",  # Light Blue
    "High Caloric Positive": "#99FF99",  # Light Green
    "All Positive": "#FFCC99"       # Light Orange
}

# Get the colors for each "Sign Outcome"
colours = [colour_map[label] for label in subject_counts['Sign Outcome']]

# Data for the pie chart
labels = subject_counts['Sign Outcome']
sizes = subject_counts['Number of Subjects']

# Create the pie chart
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct=absolute_value, startangle=140, colors=colours)

# Equal aspect ratio ensures that the pie is drawn as a circle.
ax.axis('equal')

# Add a title
plt.title("Subject Counts per Sign Outcome")
ax.legend(wedges, labels, title="Sign Outcome")
sns.despine(trim=True, left=True)

plt.tight_layout()
plt.show()
