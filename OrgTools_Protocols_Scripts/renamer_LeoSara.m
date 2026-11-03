function [] = renamer_LeoSara(files, anat, func, anatomy_loc, func1_loc, func2_loc, func3_loc, func4_loc, cur_particpant_id, cur_participant_name)
%This function transforms Leo's data, .IMA format, originally with this name: 
% {'LEOPIM_180702_201.MR.LEO_SARAH_FMRI.0008.0001.2018.07.02.18.04.29.150997.43560386.IMA'}
% into dcm format, as this:
% {'LEOPIM_180702_201-0006-0001-0001.dcm'}
% to be read by BV

%Filetype change
filetype_og = '.IMA';
filetype_dcm = '.dcm';

rawfile_loc = pwd;

%Iterates through current files in the cell array files
for cur_file = 1:numel(files)

    %saves og name for replacement
    filename_og = files(cur_file);

    %identifies volume/slice number for current file
    vol_slicer = extractAfter(filename_og, 'FMRI.');
   
    %Could be from the year 2018
    vol_slice = extractBefore(vol_slicer, '.2018');

    if (vol_slice == "")
        disp 'we assume that this data was recorded in 2019'
        vol_slice = extractBefore(vol_slicer, '.2019');

        if (vol_slice == "")
        disp 'we assume that this data was recorded in 2020'
        vol_slice = extractBefore(vol_slicer, '.2020');
        end

    end

    run = extractBefore(vol_slice, '.');
    vol = extractAfter(vol_slice, '.');
    
    %Then, we identify irrelevant time string, after volume id
    extractAftervol = extractAfter(filename_og, vol_slice);

    %We remove it
    filename_remove_1 = erase(filename_og, extractAftervol);

    %It looks like this: {'KAMSTP_020421_6D634B4DA865B3EAACCE.MR.KAMILAH_STPAUL_FMRI.0001.0001'}

    %Break Into parts
    filename_Parts = split(filename_remove_1, '_');

    author_idname = filename_Parts{1};
    datefMRI      = filename_Parts{2};
    volume_name   = filename_Parts{3};
    author_bin    = filename_Parts{4};
    rest_bin      = filename_Parts{5};

    
    filename_erase = erase(filename_remove_1, volume_name);
    filename_erase = erase(filename_erase, author_bin);
    
    %We now replace the long participant name with P0#_GN
    filename_participantrename = strrep(filename_erase, '___FMRI', strcat('_', cur_participant_name{1,1}));

    %Replaces dots for dashes
    filename_wdots = replace(filename_participantrename, '.', '-');

    %Adds second dash, second volume and dcm type file
    filename = strcat(filename_wdots, '-', vol{1,1}, filetype_dcm);

    %Now that your renaming is done, let's save it to the correct folder.
    %We get the run number from the renamer_function_2

    %Transform anat and func to '000#' format
    full_anat = sprintfc('%04d', anat);

    %DUMBFIX: If the anatomy series was removed and you need to rerun this: 
    %full_anat = sprintfc('%04d', 10);

    full_func1 = sprintfc('%04d', func(1));
    full_func2 = sprintfc('%04d', func(2));
    full_func3 = sprintfc('%04d', func(3));
    full_func4 = sprintfc('%04d', func(4));


if run{1} == full_anat{1}
    sorted_participant_file = anatomy_loc;

elseif run{1} == full_func1{1}
    sorted_participant_file = func1_loc;

elseif run{1} == full_func2{1}
    sorted_participant_file = func2_loc;

elseif run{1} == full_func3{1}
    sorted_participant_file = func3_loc;

elseif run{1} == full_func4{1}
    sorted_participant_file = func4_loc;

else
    sorted_participant_file = {pwd};
end

old = fullfile(rawfile_loc, filename_og{1,1});

new = fullfile(sorted_participant_file{1,1}, filename{1,1});

    %re-names in new folder
    movefile(old, new)
    filename_og = [];
    filename = [];
    old = [];
    new = [];

end

end
