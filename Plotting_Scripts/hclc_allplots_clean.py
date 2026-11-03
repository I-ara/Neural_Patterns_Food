from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statannotations.Annotator import Annotator

# File paths BV outputs
file_paths = [
    
]

# Labels for each subplot
labels = ["r FG", "l AMG", "l FG"]

# Colors for boxplot and stripplot
boxplot_colours = ['#c26dbc', '#3cacae']
stripplot_colours = ['#d3bbdd', '#85D3D5']

# Predictor pairs and weights dictionary
pairs = [('Hedonic_hc_P', 'Hedonic_lc_P'), ('Hedonic_hc_U', 'Hedonic_lc_U'), ('Neutral_hc_P', 'Neutral_lc_P'),
         ('Neutral_hc_U', 'Neutral_lc_U'), ('Health_hc_P', 'Health_lc_P'), ('Health_hc_U', 'Health_lc_U')]
weights_dict = {predictor: 1 for predictor in sum(pairs, ())}

# Store data for all clusters
all_cluster_data = []

# Load and process each cluster file
for path in file_paths:
    df = pd.read_excel(path)

    # Calculate differences per subject and condition pair
    differences_list = [{'Subject': subject,
                         'Difference': df[(df['Subject'] == subject) & (df['Predictor'] == cond1)]['beta'].values[0] -
                                       df[(df['Subject'] == subject) & (df['Predictor'] == cond2)]['beta'].values[0]}
                        for subject in df['Subject'].unique()
                        for cond1, cond2 in pairs]

    df_differences = pd.DataFrame(differences_list)
    df['Weight'] = df['Predictor'].map(weights_dict)
    df['Predictor_Type'] = df['Predictor'].apply(
        lambda x: 'High Caloric Stimuli' if 'hc' in x else 'Low Caloric Stimuli')

    # Weighted mean per subject and condition type
    weighted_means = df.groupby(['Subject', 'Predictor_Type']).apply(
        lambda x: (x['beta'] * x['Weight']).sum() / x['Weight'].sum()).reset_index(name='Weighted_Mean')
    weighted_mean_pertype = weighted_means.pivot(index='Subject', columns='Predictor_Type',
                                                 values='Weighted_Mean').reset_index()
    weighted_mean_pertype['Difference'] = df_differences.groupby('Subject')['Difference'].mean().values
    all_cluster_data.append(weighted_mean_pertype)

# Set up plots
fig1, axes1 = plt.subplots(1, 3, figsize=(15, 5))
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))

# Plotting for each cluster
for i, cluster_data in enumerate(all_cluster_data):
    # Boxplot and stripplot
    df_meltconds = cluster_data.melt(id_vars=['Subject'], value_vars=['High Caloric Stimuli', 'Low Caloric Stimuli'],
                                     var_name='Caloric Stimuli', value_name='Weighted Mean')
    # Calculate average for each condition, per cluster
    condition_averages = df_meltconds.groupby('Caloric Stimuli')['Weighted Mean'].mean()

    sns.despine(offset=10, trim=True)

    
    sns.set_theme(style="ticks", palette="pastel")
    sns.stripplot(data=df_meltconds, y="Weighted Mean", hue="Caloric Stimuli", dodge=True, alpha=.25, zorder=1,
                  palette=stripplot_colours, jitter=0.4, legend=False, ax=axes1[i])
    sns.boxplot(data=df_meltconds, y='Weighted Mean', hue='Caloric Stimuli', palette=boxplot_colours, saturation=1, fill=None, width=0.8,
                legend=False,
                ax=axes1[i])
    
    
    # Add condition averages as diamonds
    for condition, avg in condition_averages.items():
        x_pos = -0.2 if condition == 'High Caloric Stimuli' else 0.2
        axes1[i].scatter(x_pos, avg, marker='D', color='black', s=80, label=f'Avg {condition}')

    axes1[i].axhline(y=0, color='gray', linestyle='--', linewidth=1)
    axes1[i].set_title(labels[i], fontsize=18)
    axes1[i].yaxis.grid(False)
    axes1[i].grid(False)
    axes1[i].spines['top'].set_visible(False)
    axes1[i].spines['right'].set_visible(False)
    axes1[i].spines['left'].set_visible(False)
    axes1[i].spines['bottom'].set_visible(False)
    axes1[i].set_ylabel("")

    # Ticks
    new_yticks = np.linspace(-0.8, 0.8, 4)  # Ensure these are numeric values
    axes1[i].set_yticks(new_yticks)  # Set numeric tick values on y-axis
    axes1[i].set_yticklabels([f"{tick:.1f}" for tick in new_yticks], fontsize=12)  # Format tick labels if needed
    axes1[i].set_ylim(-0.4, 0.8)

    x1, x2 = -0.25, 0.25  # x-position for the bracket
    y, h = 0.65, 0.05  # Stable Positions for the annotations
    # Draw the bracket
    axes1[i].plot([x1, x1, x2, x2], [y, y + h, y + h, y], 
                  color='gray', lw=1)
    
    # Add p-value text
    text = "p < 0.001"
    axes1[i].text((x1 + x2) / 2, y + h, text, ha='center', va='bottom', fontsize=9, color='black')


    # Pie chart
    def determine_sign_outcome(row):
        high, low = row['High Caloric Stimuli'], row['Low Caloric Stimuli']
        return ("Increased Activation" if high > 0 and low > 0 and high > low else
                "Decreased Deactivation" if high < 0 and low < 0 and high > low else
                "Only High Caloric Stimuli Activation" if high > 0 and low < 0 else
                "Only Low Caloric Stimuli Activation")


    cluster_data['Sign Outcome'] = cluster_data.apply(determine_sign_outcome, axis=1)
    subject_counts = cluster_data['Sign Outcome'].value_counts().reindex(
        ["Decreased Deactivation", "Only Low Caloric Stimuli Activation", "Only High Caloric Stimuli Activation", "Increased Activation"]).fillna(0)
    colour_map = {"Decreased Deactivation": "#FF9999", "Only Low Caloric Stimuli Activation": "#66B3FF", "Only High Caloric Stimuli Activation": "#99FF99",
                  "Increased Activation": "#FFCC99"}
    #sizes = subject_counts.values

    # Convert counts to percentages
    subject_percentages = (subject_counts / subject_counts.sum()) * 100

    colours = [colour_map[cat] for cat in subject_counts.index]

    wedges, texts, autotexts = axes2[i].pie(subject_percentages, autopct=lambda p: f'{p:.1f}%', startangle=140,
                                            colors=[colour_map[cat] for cat in subject_percentages.index], pctdistance=0.85)
    for autotext in autotexts:
        autotext.set_fontsize(14)  # Adjust font size as needed
    
    axes2[i].axis('equal')
    for ax in axes2:
        ax.set_ylabel("")

    #axes2[i].legend(subject_percentages.index, title="Activation Profiles", loc="best", fontsize=12)

plt.tight_layout()
sns.despine(trim=True, left=True)
plt.subplots_adjust(top=0.9, hspace=0.3, wspace=0.2)

plt.show()

# Save figures
fig1.savefig("boxplot_hclc.svg", format='svg')
fig2.savefig("pies_hclc.svg", format='svg')
