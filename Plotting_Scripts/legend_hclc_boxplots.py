from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# File paths
file_paths = [
    'Cluster_b1.xlsx',
    'Cluster_b2.xlsx',
    'Cluster_b3.xlsx'
]

# List of labels
labels = [
    "r FG", "l AMG", "l FG"
]

# Set custom colors
boxplot_colours = ['#c26dbc', '#3cacae']
stripplot_colours = ['#d3bbdd', '#85D3D5']

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

# Weights dictionary
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

# Initialize storage for all clusters
all_cluster_data = []

for idx, path in enumerate(file_paths):
    # Load the Excel file for each cluster
    df = pd.read_excel(path)

    # Calculate differences between conditions per subject
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
    result = df_differences.groupby('Subject')['Difference'].apply(calculate_weighted_mean).reset_index(
        name='Weighted_Mean')

    # Add weights to df
    df['Weight'] = df['Predictor'].map(weights_dict)
    df['Predictor_Type'] = df['Predictor'].apply(
        lambda x: 'High Caloric Stimuli' if 'hc' in x else 'Low Caloric Stimuli')

    # Weighted mean for Hedonic and Neutral predictors
    weighted_means = df.groupby(['Subject', 'Predictor_Type']).apply(
        lambda x: (x['beta'] * x['Weight']).sum() / x['Weight'].sum()).reset_index(name='Weighted_Mean')
    weighted_mean_pertype = weighted_means.pivot(index='Subject', columns='Predictor_Type',
                                                 values='Weighted_Mean').reset_index()

    weighted_mean_pertype['Difference'] = result['Weighted_Mean']
    all_cluster_data.append(weighted_mean_pertype)

# Plotting #############################################################################################################

fig1, axes1 = plt.subplots(1, 3, figsize=(15, 5))
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))

for i, cluster_data in enumerate(all_cluster_data):
    # Boxplot & Stripplot subplot
    df_meltconds = cluster_data.melt(id_vars=['Subject'], value_vars=['High Caloric Stimuli', 'Low Caloric Stimuli'],
                                     var_name='Caloric Stimuli', value_name='Weighted Mean')

    # sns.despine(trim=True, left=True)
    sns.despine(offset=10, trim=True)
    sns.set_theme(style="ticks", palette="pastel")
    sns.stripplot(data=df_meltconds, y="Weighted Mean", hue="Caloric Stimuli", dodge=True, alpha=.25, zorder=1, palette=stripplot_colours,
                  jitter=0.4, legend=False, ax=axes1[i])
    sns.despine(offset=10, trim=True)
    sns.boxplot(data=df_meltconds, y='Weighted Mean', hue='Caloric Stimuli', palette=boxplot_colours, saturation=1,
                ax=axes1[i], fill=None)

    axes1[i].axhline(y=0, color='gray', linestyle='--', linewidth=1)

    axes1[i].set_title(labels[i], fontsize=18)
    axes1[i].set_yticks(np.round(np.linspace(-.8, 0.8, 4), 1))
    #axes1[i].set_ylabel('Percent Signal Changes (%)', fontsize=18)
    axes1[i].set_ylim(-0.8, 0.8)
    axes1[i].yaxis.grid(False)
    axes1[i].grid(False)

    # Pie chart subplot
    def determine_sign_outcome(row):
        high = row['High Caloric Stimuli']
        low = row['Low Caloric Stimuli']
        if high > 0 and low > 0:
            return "All Positive"
        elif high < 0 and low < 0:
            return "All Negative"
        elif high > 0 and low < 0:
            return "Hedonic Positive"
        elif high < 0 and low > 0:
            return "Neutral Positive"


    cluster_data['Sign Outcome'] = cluster_data.apply(determine_sign_outcome, axis=1)
    subject_counts = cluster_data.groupby('Sign Outcome')['Subject'].nunique().reset_index()
    subject_counts.columns = ['Sign Outcome', 'Number of Subjects']

    desired_order = ["All Negative", "Neutral Positive", "Hedonic Positive", "All Positive"]
    colour_map = {
        "All Negative": "#FF9999",
        "Neutral Positive": "#66B3FF",
        "Hedonic Positive": "#99FF99",
        "All Positive": "#FFCC99"
    }
    labels = subject_counts['Sign Outcome']
    colours = [colour_map[label] for label in labels]
    sizes = subject_counts['Number of Subjects']


    def absolute_value(val):
        return f'{int(val / 100 * sum(sizes))}'


    wedges, texts, autotexts = axes2[i].pie(sizes, autopct=absolute_value,
                                            startangle=140, colors=colours)
    #axes2[i].set_title(f'Cluster {i + 1}: Subject Counts per Sign Outcome')
    #axes2[i].set_title(labels, fontsize=16)
    axes2[i].axis('equal')  # Ensure the pie chart is circular

    for ax in axes1:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_ylabel("")

    for ax in axes2:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_ylabel("")

plt.tight_layout()
sns.despine(trim=True, left=True)
plt.subplots_adjust(top=0.9, hspace=0.3, wspace=0.2)

plt.show()

fig1.tight_layout()
fig1.savefig("legend_boxplot_hclc.svg", format='svg')

