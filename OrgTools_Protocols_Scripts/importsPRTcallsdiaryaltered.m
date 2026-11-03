%% All conds to cond1 vs cond 2


%% We want to change from all conditions: 
% Example:
% Health_hcP
% 2
% 271000   287013
% 497000   513013
% Color: 33 113 181
%  
% Health_hcU
% 2
% 18000   34013
% 754000   770013
% Color: 155 190 255
%  
% Health_lcP
% 2
% 206000   222013
% 561000   577013
% Color: 107 174 214
%  
% Health_lcU
% 2
% 301000   317013
% 467000   483013
% Color: 189 215 231
%  
% Hedonic_hcP
% 2
% 52000   68013
% 724000   740013
% Color: 206 18 86
%  
% Hedonic_hcU
% 2
% 174000   190013
% 593000   609013
% Color: 216 161 215
%  
% Hedonic_lcP
% 2
% 241000   257013
% 531000   547013
% Color: 223 101 176
%  
% Hedonic_lcU
% 2
% 142000   158013
% 627000   643013
% Color: 232 216 246
%  
% Neutral_hcP
% 2
% 367000   383013
% 399000   415013
% Color: 217 71 1
%  
% Neutral_hcU
% 2
% 82000   98013
% 692000   708013
% Color: 253 190 133
%  
% Neutral_lcP
% 2
% 333000   349013
% 433000   449013
% Color: 253 141 60
%  
% Neutral_lcU
% 2
% 112000   128013
% 659000   675013
% Color: 254 219 196

%to: Hedonic, Health and Neutral

%% Step 1: Read PRT
%Objective: load('201_run1.mat')

%We created a .mat file with protocol info, read that
directory = 'C:\Users\P70079871\Desktop\ProtocolLeo_mat';
%directory = 'C:\Users\P70079871\Desktop\ProtocolSara_mat';

cd(directory)

%read all files in directory
protList = dir(fullfile(directory, '*.mat'));


%Load each prt
for i=1:length(protList)

    prtName = protList(i).name;
    filePath = fullfile(directory, prtName);
    load(filePath);

    %Choose one at a time, they will be re-written on top of each other
    %otherwise

    %Calls 12 condition protocol
    diary_bvprotocol(filePath, prt)

    %Calls Hedonic v Health v Neutral bv function
    %diary_bvprotocol_healthhedneut(filePath, prt)

    %Calls Hedonic v Neutral diary bv function
    %diary_bvprotocol_hedneut(filePath, prt)
end

