% This script will resample a set of standard images into a bunch of 
% different voxel dimensions, and then possibly we can match images to
% these standards based on voxel dimension and image dimension

indir = '/scratch/users/vsochat/DATA/BRAINBEHAVIOR/standard';
voxdim = [1.5,1.5,1.5;
          1,1,1;
          2.5, 2.5,2.5;
          2,2,2;
          2,2,4;
          3,3,3;
          3,3,3.5;
          4,4,4];

% File with image names to resize
% tmp = '/scratch/users/vsochat/DATA/BRAINBEHAVIOR/need_resize_fnames.txt';
standards = dir(indir);

% For each file
for s=3:length(standards)
    standard = standards(s).name;
    fprintf('%s\n',[ 'Processing ' num2str(s-2) ' of ' num2str(length(standards)-2) ])
    % For each voxel size
    for v=1:length(voxdim)
      dimstring = [ num2str(voxdim(v,1)) 'x' num2str(voxdim(v,2)) 'x' num2str(voxdim(v,3))];
      standard_dim = strsplit(standard,'-');
      outname = standard_dim{1};
      standard_dim = standard_dim{2}(1:length(standard_dim{2})-4);
      if ~strcmp(standard_dim,dimstring)
        folder = [ indir '/' standards(s).name  ];
        outname = [ outname '-' dimstring '.nii' ];
        if ~exist([indir '/' outname],'file')
          fprintf('%s\n',[ 'Making image ' outname ]);
          resize_img(folder,voxdim(v,:), nan(2,3),[],outname)
        end
      end
   end
end