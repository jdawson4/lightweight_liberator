# Author: Jacob Dawson
#
# This file will take all of our raw fits data, lightly preprocess it, and save
# the data to simple png images. The idea here is that our images are
# over/under exposed, and we just want to remove all the weird clipping

from astropy.io import fits
import numpy as np
import os
import imageio

def processFile(path,filename):
    with fits.open(path) as hdul:
        dataFound = False
        for i in range(2):
            h = hdul[i]
            if h.data is None:
                continue
            if len(h.data.shape) == 2:
                dataFound = True
                data = h.data
                break
        if not dataFound:
            return
        data = data.astype(np.float32)
        data = np.nan_to_num(data)
        data = np.clip(data, np.percentile(data, 20.0), np.percentile(data, 99.625))
        if (np.amin(data) < 0.0):
            data += np.amin(data)
        if (np.amin(data) > 0.0):
            data -= np.amin(data)
        data /= np.amax(data)
        data *= 255.0
        print('writing',filename[:-5]+'.png')
        imageio.imwrite('pngs/'+filename[:-5]+'.png', data.astype(np.uint8))

list_of_files = {}
for (dirpath, dirnames, filenames) in os.walk('FITS'):
    for filename in filenames:
        if filename.endswith('.fits'):
            list_of_files[filename] = os.sep.join([dirpath, filename])

for k,v in list_of_files.items():
    processFile(v, k)
