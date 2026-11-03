import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os

# Define positive and negative clusters
test_clusters = [1,2,3]
positive_clusters = [1, 3, 11, 12, 13, 17, 18, 19, 21, 22]
negative_clusters = [2, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16, 20]

# List of labels
labels = [
    "r MTG", "r SMG", "r IPL", "r ITG", "r IFG", "r postCG", "r MFG",
    "r INS", "r OCC/PAR", "r LG", "b PCC", "b mPFC", "l SFG",
    "l SPL", "l LG", "l MOG", "l INS", "l MFG", "l IFG", "l ITG",
    "l IPL", "l MTG"
]

# Choose which cluster set to use
cluster_set = positive_clusters  # Change this to `negative_clusters` to use that set

# Directory containing cluster files
base_dir = 'fileplace'

# Initialize subplots
num_clusters = len(cluster_set)
fig, axes = plt.subplots(nrows=3, ncols=4)
axes = axes.flatten()

# Set custom colors
boxplot_colours = ['#ED7D31', '#4472C4']
stripplot_colours = ['#F4A261', '#A4C4E0']

#

# Loop through each cluster in the selected set and load data
for idx, cluster_num in enumerate(cluster_set):

    cluster_file = os.path.join(base_dir, f'Cluster_{cluster_num}.xlsx')
    df = pd.read_excel(cluster_file)

    # Filter out rows where 'Predictor' contains the string 'health'
    df_filtered = df[~df['Predictor'].str.contains('health', case=False, na=False)]

    # Difference of Weights
    pairs = [
        ('Hedonic_hc_P', 'Neutral_hc_P'),
        ('Hedonic_hc_U', 'Neutral_hc_U'),
        ('Hedonic_lc_P', 'Neutral_lc_P'),
        ('Hedonic_lc_U', 'Neutral_lc_U')
    ]
    weights = [1, 1, 1, 1]

    # Calculate differences between conditions per subject
    differences_list = []

    for subject in df['Subject'].unique():
        subject_data = df[df['Subject'] == subject]
        for cond1, cond2 in pairs:
            beta_cond1 = subject_data.loc[subject_data['Predictor'] == cond1, 'beta'].values[0]
            beta_cond2 = subject_data.loc[subject_data['Predictor'] == cond2, 'beta'].values[0]
            difference = beta_cond1 - beta_cond2
            differences_list.append({'Subject': subject, 'Difference': difference})

    df_differences = pd.DataFrame(differences_list)


    def calculate_weighted_mean(diffs):
        return sum(diffs * weights) / sum(weights)


    # Group by Subject and apply the weighted mean
    result = df_differences.groupby('Subject')['Difference'].apply(calculate_weighted_mean).reset_index(
        name='Weighted_Mean')

    # Weighted mean per predictor type
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

    df_filtered['Weight'] = df_filtered['Predictor'].map(weights_dict)


    def weighted_condmean(group):
        return (group['beta'] * group['Weight']).sum() / group['Weight'].sum()


    df_filtered['Predictor_Type'] = df_filtered['Predictor'].apply(lambda x: 'Hedonic' if 'Hedonic' in x else 'Neutral')
    weighted_means = df_filtered.groupby(['Subject', 'Predictor_Type']).apply(weighted_condmean).reset_index(
        name='Weighted_Mean')
    weighted_mean_pertype = weighted_means.pivot(index='Subject', columns='Predictor_Type',
                                                 values='Weighted_Mean').reset_index()

    df_meltconds = weighted_mean_pertype.melt(id_vars=['Subject'],
                                              value_vars=['Hedonic', 'Neutral'],
                                              var_name='Condition',
                                              value_name='Weighted Mean')
    df_meltconds['Subject Order'] = list(range(1, 109)) + list(range(1, 109))
    df_meltconds['Subject Order'] = df_meltconds['Subject Order'].astype('category')
    df_meltconds['Condition'] = df_meltconds['Condition'].astype('category')

    # Plot for the current cluster
    ax = axes[idx]

    sns.boxplot(
        data=df_meltconds,
        y='Weighted Mean', hue='Condition',
        palette=boxplot_colours,
        gap=0, linewidth=2, saturation=1, fill=None, width=0.80,
        ax=ax,
        legend=False
    )

    sns.set_theme(style="whitegrid")

    sns.stripplot(
        data=df_meltconds, y="Weighted Mean", hue="Condition",
        palette=stripplot_colours,
        jitter=0.4, native_scale=True,
        dodge=True, alpha=.25, zorder=1, size=7, ax=ax,
        legend=False
    )

    ax.axhline(y=0, color='gray', linestyle='--', linewidth=1)

    # Labels with cluster number
    # ax.set_title(f'Cluster {cluster_num}', fontsize=18)
    # Labels with cluster name
    ax.set_title(labels[cluster_num - 1], fontsize=18)
    ax.set_ylim(-0.6, 1.6)
    ax.set_ylabel('')


# Display the final figure with all cluster plots
plt.show()
fig.savefig('BP_pos_grid.pdf', format='pdf', dpi=300)
fig.savefig('BP_pos_grid.svg', format='svg', dpi=300)
