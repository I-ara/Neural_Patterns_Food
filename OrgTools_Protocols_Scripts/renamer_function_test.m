function [] = renamer_function_2(sorted_participant_file_og, anatomy_loc, func1_loc, func2_loc, func3_loc, func4_loc, groupFolder, cur_particpant_id, cur_participant_name)

%Gets put where renamer_function_2 is 

% This function transforms Leo's data, .IMA format, originally with this name:
% {'LEOPIM_180702_201.MR.LEO_SARAH_FMRI.0008.0001.2018.07.02.18.04.29.150997.43560386.IMA'}
% into dcm format, as this:
% {'LEOPIM_180702_201-0006-0001-0001.dcm'}
% to be read by BV

%% Counts the information in the folder, how many volumes per series, 
% which series are useful for anatomy and functional purposes

cd(sorted_participant_file_og)
cd Raw_Data

%Places files of type .IMA into cell array
[a] = dir('*.IMA');
files = {a.name};

%Collapsible variable with all file names in one string
col_filename = [files{:}];

%Then, we detect the string series and volume series for some reason
id_tot = extractBetween(col_filename, 'FMRI.', '.2018');
if isempty(id_tot)
    id_tot = extractBetween(col_filename, 'FMRI.', '.2019');
    if isempty(id_tot)
        id_tot = extractBetween(col_filename, 'FMRI.', '.2020');
        if isempty(id_tot)
            id_tot = extractBetween(col_filename, 'FMRI.', '.2021');
            if isempty(id_tot)
                id_tot = extractBetween(col_filename, 'FMRI.', '.2022');
            end
        end
    end
end

%Dumb volume counter for now

%Series 01
vol_num(1, :) = sum(count(id_tot, '0001.'));
%Series 02
vol_num(2,:) = sum(count(id_tot, '0002.'));
%Series 03
vol_num(3,:) = sum(count(id_tot, '0003.'));
%Series 04
vol_num(4,:) = sum(count(id_tot, '0004.'));
%Series 05
vol_num(5,:) = sum(count(id_tot, '0005.'));
%Series 06
vol_num(6,:) = sum(count(id_tot, '0006.'));
%Series 07
vol_num(7,:) = sum(count(id_tot, '0007.'));
%Series 08
vol_num(8,:) = sum(count(id_tot, '0008.'));
%Series 09
vol_num(9,:) = sum(count(id_tot, '0009.'));
%Series 10
vol_num(10,:)= sum(count(id_tot, '0010.'));
%Series 11
vol_num(11,:) = sum(count(id_tot, '0011.'));
%Series 12
vol_num(12,:) = sum(count(id_tot, '0012.'));
%Series 13
vol_num(13,:) = sum(count(id_tot, '0013.'));
%Series 14
vol_num(14,:) = sum(count(id_tot, '0014.'));
%Series 15
vol_num(15,:) = sum(count(id_tot, '0015.'));
%Series 16
vol_num(16,:) = sum(count(id_tot, '0016.'));
%Series 17
vol_num(17,:) = sum(count(id_tot, '0017.'));
%Series 18
vol_num(18,:) = sum(count(id_tot, '0018.'));
%Series 19
vol_num(19,:) = sum(count(id_tot, '0019.'));
%Series 20
vol_num(20,:) = sum(count(id_tot, '0020.'));

anat = [];
func = [];
vol = [];

%Takes all four functional runs (any run that is of length exp_func)
% and the last anatomical run (the last exp_anat length run) and places them into a "series useful vector"
vol_num