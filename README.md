This repository contains the analysis scripts and computational tools developed for the research project that is part of my doctoral thesis work: Attentional Focus Dependent Neural Responses to Food: 
Distinct Patterns of Activation, Deactivation, and Inter-individual Variability.
The project investigates how attentional focus influences neural responses to food stimuli, using functional magnetic resonance imaging (fMRI). Its stimuli and original data were developed, collected and analysed
by Leonardo Pimpini and Sarah Kochs.

The repository provides the scripts used for neuroimaging analysis, data organisation, and visualisation.
The repository is organised into three main directories:

1. OrgTools_Protocols_Scripts/ - MATLAB scripts developed for data organisation, experimental protocols, and supporting analysis workflows of the combined datasets of the original authors as well as the compatibility of
   the data and data organisation to BrainVoyager.

2. MRI_BrainVoyager_Scripts/ - Jupyter notebooks containing scripts for MRI data analysis using BrainVoyager. These notebooks support the processing, organisation, and analysis of neuroimaging data and
BrainVoyager-related outputs for large datasets.

3. Plotting_Scripts/ - Python scripts for data visualisation, statistical plotting, and figure generation.

Software and Dependencies
BrainVoyager: Neuroimaging analysis and processing.
bvbabel: Python package used throughout BrainVoyager-related workflows to read, write, and handle BrainVoyager file formats.
Additional Python and MATLAB dependencies may be required by individual scripts and notebooks.

Data Availability
This repository contains analysis scripts only.
This repository does not include raw neuroimaging data, participant-level data, or BrainVoyager project files (including .vmp, .vtc, .glm, and .voi files).
These files are excluded due to data-sharing restrictions and research data protection requirements.
Consequently, some scripts and notebooks require access to the corresponding data and BrainVoyager project files to be executed.

Before running the workflows:
Ensure that the required software and dependencies are installed.
Obtain appropriate access to the relevant neuroimaging data and project files.
Review file paths and directory references within individual scripts and notebooks.
Ensure that the required BrainVoyager files are available where applicable.

Reproducibility
The repository provides the computational scripts underlying the analyses reported in the associated manuscript.
Reproducing the complete analyses requires access to the relevant input data, BrainVoyager project files, and compatible software environments.
Document software versions and additional implementation details alongside the relevant workflows, where applicable.

Citation
If you use, adapt, or build upon any of the analysis scripts in this repository, please acknowledge and cite the repository as a software resource.
de Almeida Ivo, I. (2026). Neural Patterns of Food. GitHub. https://github.com/I-ara/Neural_Patterns_Food/

Associated research publication citation
If you refer to or discuss the scientific findings associated with these analyses, please also cite the corresponding preprint:
de Almeida Ivo, I., Roefs, A., Pimpini, L., Kochs, S., Linden, D. E. J., & Sorger, B. (2026). 
Attentional focus dependent neural responses to food: Distinct patterns of activation, deactivation, and inter-individual variability. OSF Preprints. https://doi.org/10.31219/osf.io/nv5ay_v1
Manuscript available on OSF: [Attentional Focus Dependent Neural Responses to Food: Distinct Patterns of Activation, Deactivation, and Inter-individual Variability.](https://doi.org/10.31219/osf.io/nv5ay_v1)

