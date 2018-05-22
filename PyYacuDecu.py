# -*- coding: utf-8 -*-
"""
Created on Wed Mar 09 12:47:58 2016

@author: kaysch
"""
from __future__ import division
from __future__ import print_function

import numpy as np
import os
from ctypes import *
import numpy.ctypeslib as npct
import matplotlib.pyplot as plt
from skimage import data, img_as_float
from math import ceil, floor
from skimage.viewer import ImageViewer
import skimage.io

datapath = os.path.dirname(__file__) # looks for all files in the same directory as the script, change if it should look somewhere else.



iterations = 50
decon_directory = datapath+ "/"

psf_name = "PSF_C2_small.tif"

filenames_input = ["C2.tif"]
filenames_output = ["Decon_C2.tif"]


#_yacu = npct.load_library('libyacudecu.dll', '.')
_yacu = CDLL('libyacudecu.dll',  mode=RTLD_GLOBAL)

array_3d_float = npct.ndpointer(dtype=np.float32, ndim=3 , flags='CONTIGUOUS')


## Activate the correspnding CUDA moes: device is fastest, but needs loads of GPU memory, host is slow but needs only little memory, stream is a compromise
#fun=_yacu.deconv_device

#fun=_yacu.deconv_host

fun=_yacu.deconv_stream



fun.argtypes = [c_int, c_int,c_int,c_int, array_3d_float, array_3d_float, array_3d_float]



print("Processing " + str(len(filenames_input)) + " files")


print("Deconvolving with " + str(iterations) + " iterations")

for number, (filename, filename_out) in enumerate(zip(filenames_input, filenames_output)):
    print("Processing file " + str(number+1) + " of " + str(len(filenames_input)) + " : " + filename )
    indata  = skimage.io.imread(decon_directory+filename).astype("float32")
    orig_size = indata.shape
    print(orig_size)
    
    print("Read image, dimensions are " + str(orig_size))
    padded_psf = skimage.io.imread(datapath+"/"+psf_name).astype("float32")

    psf_size = padded_psf.shape
    print("Read PSF, dimensions are " + str(psf_size))
    
    padding_z = int((orig_size[0]-psf_size[0]))
    padding_z_lower = int(floor(padding_z/2))
    padding_z_higher = int(ceil(padding_z/2))
    
    print(padding_z_lower)
    print(padding_z_higher)
    padding_y = int((orig_size[1]-psf_size[1])/2)

    
    padding_x = int((orig_size[1]-psf_size[1])/2)
    
    #padded_psf = np.pad(padded_psf, [(0,0), (256,256) , (256,256)], "constant")
    padded_psf = np.pad(padded_psf, [(padding_z_lower, padding_z_higher), (padding_y,padding_y) , (padding_x,padding_x)], "constant")
    #print("padded PSF to input dimensions: " + str(padded_psf.shape))
    
    #indata = np.random.random_sample([256,256,60]).astype('float32')#, dt'=ype=np.float)
    #indata = 255*indata
    #indata= np.ascontiguousarray(indata)

    padded_psf = np.fft.ifftshift(padded_psf)
    #psf = np.ascontiguousarray(psf)
    #print psf
    print("Shifted PSF")
    
    result = np.copy(indata) ## this has to be the original image for the first round
    
    print(result)
    print("Generated result array")
    """the first thing done during deconvolution in the library is actually to FFT the result file (object ) 
    This is based on the need to reuse the object during the following iteration, i.e. the object is stored during deconvolution, however, the image is not.
    
    Therefore, the "result" should be identical to the "image" during the first round of deconvolution. Alterative implementaiton would be to run one complete round of decon first and then start iterating.
    therefore, this process is more effective.
    
    """

    
    
    a_p = indata.ctypes.data_as(POINTER(c_float))
    b_p = padded_psf.ctypes.data_as(POINTER(c_float))
    c_p = result.ctypes.data_as(POINTER(c_float))
    output = fun(iterations,int(indata.shape[0]),int(indata.shape[1]),int(indata.shape[2]), indata, padded_psf, result)
    
    
    if output == 0:
        print("Deconvolution finished successfully")
        
    #result = np.ascontiguousarray(result)
    print(result)
    skimage.io.imsave(decon_directory+filename_out, result)

print("All files processed, quitting")