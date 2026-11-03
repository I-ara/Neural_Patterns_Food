function deleteNonIMAFilesInFolders(folders, partName)
    % Loop through each folder
    for x = 1:length(folders)
        folder = folders{x};
        folder = fullfile(pwd, partName, folder);
        files = dir(folder);
        files = {files.name};
        files = files(~ismember(files, {'.', '..'}));
        
        % Check each file/folder in the current folder
        for y = 1:length(files)
            if ~endsWith(files(y), '.IMA', 'IgnoreCase', true)
                    delete(fullfile(folder, files(y)));
            end
        end
    end
end

