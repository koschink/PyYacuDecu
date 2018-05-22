# PyYacuDecu

A python wrapper for YacuDecu

Reads a list of files from a directory (list of filenaes is given as "filenames_input" variable, puts each file out according to strings saved in  "filename_output".

An example dataset is given.

The PSF should have the same pixel size and z spacing as the image file, but does not need to be full size as the file is zero-padded in XYZ (works best for "even" z stack sizes, but pads also for uneven ones; the XY size should be even)

The YacuDecu folder alsocontains the original YacuDecu files with changes to "deconv.cu"
Changes: 
The "deconv.cu" file is annotated and contains the the addition that the function "FloatDiv" checks if any of the data values is 0 to prevent div0 errors, if data at a specific point is 0 or extremely close to 0 ( > 0.00001), the division is not performed, but rather the value is set to 0. Thisis important if e.g. padded data is used.



For questions & comments please contact 
Kay Schink (kay.oliver.schink@rr-research.no)
@kschink
