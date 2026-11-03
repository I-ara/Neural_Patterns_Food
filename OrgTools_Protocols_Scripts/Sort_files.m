%%                         UNDER CONSTRUCTION                      %%


%% When you get MRI and fMRI raw data, it often needs some organisation into functional runs and anatomy runs. 
%% This script sorts your original files into a directory with dedicated folders for easy Brain Voyager access
%% This directory can be created by the "Folder Creator" script. 

%% Disclaimer: This script comes as it is - there might be errors at runtime and results might be wrong although the code was tested and did work as expected. 
%% made by: Iara de Almeida Ivo

%Script that copies files from og file location
og_location = 'D:\LeoData\Raw_data_OG';
%Into sorted locations
sorted_location = 'D:\LeoData\Raw_data';

addpath(genpath(og_location))
addpath(genpath(sorted_location))

cd(og_location)


file_list = dir;
participant_names = {file_list.name};
participant_names(:, 1:2) = [];

for cur_participant = 1:number_of_participants

    participant_id = participant_names(cur_participant);
    fprintf('We.re on Participant %s \n', participant_id{1,1})

    cur_participant_file = fullfile(og_location, participant_id);
    sorted_participant_file = fullfile(sorted_location, participant_id, strcat(participant_id, '_DCMs'));

    cd (cur_participant_file{1})

    %put function here
    renamer_function(sorted_participant_file, participant_id)

end
