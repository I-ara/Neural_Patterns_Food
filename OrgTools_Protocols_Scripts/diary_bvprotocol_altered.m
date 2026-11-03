function [prt_ordered] = diary_bvprotocol_hedneut(filePath, prt)

[~, name, ~] = fileparts(filePath);
filename = sprintf('S%s.prt', name);

diary(filename)

disp('FileVersion:        2')
disp(' ');
disp('ResolutionOfTime:   msec');
disp(' ');
disp('Experiment:         LeoData');
disp(' ');
disp('BackgroundColor:    0 0 0');
disp('TextColor:          255 255 255');
disp('TimeCourseColor:    255 255 255');
disp('TimeCourseThick:    3');
disp('ReferenceFuncColor: 0 0 80');
disp('ReferenceFuncThick: 3');
disp(' ');
disp('NrOfConditions:     2');
disp(' ');

%orders first by condition and then by onset
prt_ordered = sortrows(prt, [4 3]);

%transforms seconds to miliseconds
prt_ordered(:, [4 5]) = prt_ordered(:, [4 5])*1000;

%creates endvalue

for k=1:length(prt_ordered)
   prt_ordered(k,6) = prt_ordered(k,4)+prt_ordered(k,5); 
end


%Removes decimals
prt_ordered(:, 4:6) = round(prt_ordered(:, 4:6));

%% These are kinda dumb... Replace this with a smarter way

% % % Health
% % disp('Health')
% % disp('8')
% % for k = 1:length(prt_ordered)
% %     if mod(prt_ordered(k,3), 3)==2
% % 
% %         thistrialonset = sprintf('%g   %g', prt_ordered(k, 4), prt_ordered(k, 6));
% %         disp(thistrialonset)
% %     end
% % end
% % disp('Color: 33 113 181')
% % disp(' ');

%% Hedonic
disp('Hedonic')
disp('8')
for k = 1:length(prt_ordered)
    if mod(prt_ordered(k,3), 3)==1
        thistrialonset = sprintf('%g   %g', prt_ordered(k, 4), prt_ordered(k, 6));
        disp(thistrialonset)
    end 
end
disp('Color: 206 18 86')
disp(' ');

%% Neutral
disp('Neutral')
disp('8')
for k = 1:length(prt_ordered)
    if mod(prt_ordered(k,3), 3)==0
        thistrialonset = sprintf('%g   %g', prt_ordered(k, 4), prt_ordered(k, 6));
        disp(thistrialonset) 
    end
end
disp('Color: 217 71 1')
disp(' ');

diary off
end