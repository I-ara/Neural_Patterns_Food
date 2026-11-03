function renameFolders(parentFolder)
    % Find all subfolders with the name "IMA_files"
    subfolders = dir(fullfile(parentFolder, '**', 'IMA_files'));
    
    % Loop through each subfolder
    for i = 1:length(subfolders)
        if subfolders(i).isdir
            oldFolderPath = fullfile(subfolders(i).folder, subfolders(i).name);
            newFolderPath = fullfile(subfolders(i).folder, 'Raw_Data');

            
            % Move files using mkdir/movefile
            mkdir oldFolderPath
            movefile oldFolderPath newFolderPath
        end
    end
end



