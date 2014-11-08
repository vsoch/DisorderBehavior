indir = '/scratch/users/vsochat/DATA/BRAINBEHAVIOR/MNI2mm';
files = dir(indir);

% For each file
for s=3:length(files)
    fprintf('%s\n',[ 'Processing ' num2str(s) ' of ' num2str(length(files)) ])
    folder = [ indir '/' files(s).name  ];
    if strcmp(folder(length(folder)-1:length(folder)),'gz')
      folder = gunzip(folder);
    else
      folder = {folder};
    end
    [path nam ext] = fileparts(files(s).name);
    outname = [ '8mm' nam  ];
    resize_img(folder{1},[8 8 8], nan(2,3),[],outname)
end