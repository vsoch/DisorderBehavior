outdir = '/scratch/users/vsochat/DATA/BRAINBEHAVIOR/standard';
indir = '/scratch/users/vsochat/DATA/BRAINBEHAVIOR/mrs';

% File with image names to resize
tmp = '/scratch/users/vsochat/DATA/BRAINBEHAVIOR/need_resize_fnames.txt';
files = importdata(tmp,'\n');

% For each file
for s=1:length(files)
    fprintf('%s\n',[ 'Processing ' num2str(s) ' of ' num2str(length(files)) ])
    folder = [ indir '/' files{s}  ];
    folder = gunzip(folder);
    resize_img(folder{1},[2 2 2], nan(2,3),[],'2mm')
end