
%% When you get MRI and fMRI raw data, it often needs some organisation into functional runs and anatomy runs. 
%% This script creates a directory with dedicated folders for easy Brain Voyager access

%% Disclaimer: This script comes as it is - there might be errors at runtime and results might be wrong although the code was tested and did work as expected. 
%% made by: Iara de Almeida Ivo

% % This is where every single dataset should be going to
dataFolder = 'D:\BV_data';

%% Group folder might be used where we have separate conditions, unused for Leo+sara
%groupFolder = [];
% groupFolder = strsplit(sourceFolder, "\");
% groupFolder = groupFolder{end};

%Sara's source folder
sourceFolder = '\\ca-um-nas201\fpn_rdm$\DM0596_BS_ATTBCI_P\Iara_others\06_Datasets\SaraData_Server'
cd(sourceFolder);

%Makes list of participant names and calculates number of participants
file_list = dir;
participant_names = {file_list.name};
participant_names(:, 1:2) = [];
number_of_participants = numel(participant_names);

%participants_notto_take = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 28, 29, 31];
%     skipsubject = cur_participant_id == participants_notto_take
% 
%     if any(skipsubject)
%         continue
%     end
    
for cur_participant_id = 1:number_of_participants

    cd(dataFolder)
    
    cur_participant_name = participant_names(cur_participant_id);
    fprintf('We.re on Participant %s \n', cur_participant_name{1,1})

    sorted_participant_file_og1 = fullfile(pwd, cur_participant_name);
    sorted_participant_file = char(sorted_participant_file_og1); 

    if exist(sorted_participant_file, 'file') ~=7
        mkdir(sorted_participant_file)
        fprintf('%s File Created \n', cur_participant_name{1,1})
    end

    cd(sorted_participant_file)

    %% Creates Folders
    %Add here a "if it already exists, then do nothing"
%     %Creates DCMs folder and a First Analysis Folder, goes in
     sorted_participant_file_og2 = fullfile(sorted_participant_file_og1, strcat(cur_participant_name, '_DCMs'));
     if exist(char(sorted_participant_file_og2), "file") ~=7
         mkdir(char(sorted_participant_file_og2))
     end
 
     analysis_file = fullfile(sorted_participant_file_og1, strcat(cur_participant_name, '_FirstSteps'));
     if exist(char(analysis_file), "file")~=7
        mkdir(char(analysis_file))
     end
 
     cd(char(sorted_participant_file_og2))
 
     %Creates Anatomy Folder
     anatomy_loc = fullfile(sorted_participant_file_og2, 'Anatomy');
     if exist(char(anatomy_loc), "file")~=7
        mkdir(char(anatomy_loc))
     end
 
     %Creates Functional Folder, goes in
     fun_loc = fullfile(sorted_participant_file_og2, 'Functional');
     if exist(char(fun_loc), "file")~=7
        mkdir(char(fun_loc))
     end

     %Goes into the functional file in order to create each of the runs
     cd(char(fun_loc))
 
     %Creates Functional folders (this example has four runs and it was a 3T experiment)
     func1_loc = fullfile(fun_loc, strcat('S', cur_participant_name, '_3T_01'));
     if exist(char(func1_loc), "file")~=7
         mkdir(char(func1_loc))
     end
 
     func2_loc = fullfile(fun_loc, strcat('S',cur_participant_name, '_3T_02'));
     if exist(char(func2_loc), "file")~=7
        mkdir(char(func2_loc))
     end
 
     func3_loc = fullfile(fun_loc, strcat('S',cur_participant_name, '_3T_03'));
     if exist(char(func3_loc), "file")~=7
        mkdir(char(func3_loc))
     end
 
     func4_loc = fullfile(fun_loc, strcat('S',cur_participant_name, '_3T_04'));
     if exist(char(func4_loc), "file")~=7
        mkdir(char(func4_loc))
     end

% Then we rename all the files 
renamer_function_2(sourceFolder, anatomy_loc, func1_loc, func2_loc, func3_loc, func4_loc, cur_participant_id, cur_participant_name)
  
end