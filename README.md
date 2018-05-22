# PyYacuDecu

A python wrapper for YacuDecu


Reads a list of files from a directory (list of filenaes is given as "filenames_input" variable, puts each file out according to strings saved in  "filename_output".

An example dataset is given.

The YacuDecu folder contains the original YacuDecu files with changes to "deconv.cu"
Changes: 
The "deconv.cu" file is annotated and contains the the addition that the function "FloatDiv" checks if any of the data values is 0 to prevent div0 errors, if data at a specific point is 0 or extremely close to 0 ( > 0.00001), the division is not performed, but rather the value is set to 0. Thisis important if e.g. padded data is used.

