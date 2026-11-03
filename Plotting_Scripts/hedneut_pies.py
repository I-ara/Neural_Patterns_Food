from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Define positive and negative clusters (observational classification)
test_clusters = [1,2,3]
positive_clusters = [1, 3, 11, 12, 13, 17, 18, 19, 21, 22]
negative_clusters = [2, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16, 20]

# Choose which cluster set to use
cluster_set = positive_clusters  # Change this to `negative_clusters` to use that set

# Labels for each subplot
labels_positive = ["r MTG", "r IPL", "b PCC", "b mPFC", "l SFG", "l INS", "l MFG", "l IFG", "l IPL", "l MTG"]
labels_negative = ["r SMG", "r ITG", "r IFG", "r postCG", "r MFG", "r INS", "r OCC/PAR", "r LG", "l SPL", "l LG", "l MOG", "l ITG"]

# Voxel counts for each cluster (from brainvoyager)
voxel_positive = ["496", "5424", "15440", "34616", "644", "440", "688", "672", "7176", "2776"]
voxel_negative = ["120", "2928", "1568", "536", "104", "192", "4328", "2280", "616", "1224", "560", "808"]

#Voxel label
voxel_label = "n= "

# Match labels to selected cluster set
if cluster_set == positive_clusters:
    cluster_labels = labels_positive  # Match indices
elif cluster_set == negative_clusters:
    cluster_labels = labels_negative  # Match indices
else:
    cluster_labels = []  # Default empty if neither set is used

# Directory containing cluster files - output from BV
base_dir = 'filename'

# Initialize subplots
num_clusters = len(cluster_set)
fig, axes = plt.subplots(nrows=3, ncols=4)
axes = axes.flatten()

# Define a color map for consistent colors
colour_map = {
        "All Negative": "#FF9999",      # Light Red
        "Neutral Positive": "#66B3FF",  # Light Blue
        "Hedonic Positive": "#99FF99",  # Light Green
        "All Positive": "#FFCC99"       # Light Orange
}

desired_order = ["All Negative", "Neutral Positive", "Hedonic Positive", "All Positive"]

# Loop through each cluster in the selected set and load data
for idx, cluster_num in enumerate(cluster_set):

    cluster_file = os.path.join(base_dir, f'Cluster_{cluster_num}.xlsx')
    df = pd.read_excel(cluster_file)

    # Filter out rows where 'Predictor' contains the string 'health'
    df_filtered = df[~df['Predictor'].str.contains('health', case=False, na=False)]


    # Difference of Weights

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
    weighted_mean_pertype['Cluster Label'] = 'Positive' if cluster_num in positive_clusters else 'Negative'

    # Function to determine the Sign Outcome
    def determine_sign_outcome(row):
        hedonic = row['Hedonic']
        neutral = row['Neutral']

        if hedonic > 0 and neutral > 0 and hedonic>neutral:
            return "All Positive"
        elif hedonic < 0 and neutral < 0 and hedonic>neutral:
            return "All Negative"
        elif hedonic > 0 and neutral < 0:
            return "Hedonic Positive"
        elif hedonic < 0 and neutral > 0:
            return "Neutral Positive"

    weighted_mean_pertype['Sign Outcome'] = weighted_mean_pertype.apply(determine_sign_outcome, axis=1)

    weighted_mean_pertype['Difference'] = result['Weighted_Mean']

    df_meltconds = weighted_mean_pertype.melt(id_vars=['Subject', 'Sign Outcome', 'Difference'],
                                           value_vars=['Hedonic', 'Neutral'],
                                           var_name='Condition',
                                           value_name='Weighted Mean')

    # Define data for pie chart based on `Sign Outcome` counts
    subject_counts = weighted_mean_pertype.groupby('Sign Outcome')['Subject'].nunique().reset_index()
    subject_counts.columns = ['Sign Outcome', 'Number of Subjects']
    subject_counts['Sign Outcome'] = pd.Categorical(subject_counts['Sign Outcome'], categories=desired_order,
                                                    ordered=True)
    subject_counts = subject_counts.sort_values('Sign Outcome').reset_index(drop=True)

    print("Labels in subject_counts:", subject_counts['Sign Outcome'].unique())

    labels = subject_counts['Sign Outcome'].dropna()
    sizes = subject_counts['Number of Subjects']
    colours = [colour_map[label] for label in labels]


# Hide any remaining unused subplots if not all are filled
for j in range(idx + 1, len(axes)):
    axes[j].axis('off')

# Final layout adjustments
plt.tight_layout()
plt.subplots_adjust(top=0.9, hspace=0.3, wspace=0.2)
plt.show()

fig.savefig('Pie_pos.svg', format='svg', dpi=300)