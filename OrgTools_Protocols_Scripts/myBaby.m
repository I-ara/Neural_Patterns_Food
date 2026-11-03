%% This is the whole script that does everything
% Author: Iara de ALmeida Ivo
%

%% Step 1 - New Dataset, who dis
%helps matlab get into gear, finds out if there are groups

% This is where every single dataset should be
dataFolder = 'D:\';
cd(dataFolder);

% Ask the user to choose the source folder interactively
sourceFolder = uigetdir('Select the Source Folder');
cd(sourceFolder);

% Check if the user selected a folder or canceled the dialog
if isequal(sourceFolder, 0)
    disp('Operation canceled by the user.');
    return;
end

% Get a list of all files and folders in the folder, those are the groups
% that the original dataset user created. I am thinking that these would be
% the two groups of patient vs control groups. 
groups = dir(fullfile(sourceFolder, '*.*'));

% Remove the entries for '.' and '..' (current and parent directories)
groups = groups(~ismember({groups.name}, {'.', '..'}));
groupFolder = {groups.name};

%% Step 2 - Step into each group and understand how many subjects we have

for i = 1:length(groups)
    groupLocation = fullfile(groupFolder{i});

    %Steps into each group
    cd(groupLocation)

    %Gets the list of Participants in this group
    parts = dir;
    parts = parts(~ismember({parts.name}, {'.', '..'}));
    partsFolder = {parts.name};

    

    for j = 1:length(partsFolder)

        %Identifies Participant name, important to step in the function
        %that deletes IMA files
        curPart = partsFolder{j};
        partLocation = fullfile(pwd, curPart);


        %If the Raw_data folder doesn't exist
        if exist(fullfile(part), 'dir') == 0
            % Create the folder "X"
            mkdir('Raw_data');
            disp('Folder "Raw_data" created successfully');


        else
            disp('Folder "Raw_data" already exists');
            renameFolders(dataFolder);
        end

        %Check folders for IMA files in each participant
        folders = dir(fullfile(partsFolder{j}));
        folders = {folders([folders.isdir]).name};
        folders = folders(~ismember(folders, {'.', '..'}));

        folderLocation = fullfile(partLocation, folders);


        
        
        
        
    end

    
end


