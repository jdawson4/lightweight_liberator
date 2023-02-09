# Author: Jacob Dawson
#
# This file will take all of our raw fits data, lightly preprocess it, and save
# the data to simple png images. The idea here is that our images are
# over/under exposed, and we just want to remove all the weird clipping

from astropy.io import fits
import numpy as np
from os import listdir
from os.path import isfile, join
import imageio

onlyfiles = [f for f in listdir('FITS') if isfile(join('FITS', f))]
imgCount=0
for file in onlyfiles:
    with fits.open('FITS/' + file) as hdul:
        data = hdul[1].data
        data = np.clip(data, np.percentile(data, 20.0), np.percentile(data, 99.625))
        if (np.amin(data) < 0.0):
            data += np.amin(data)
        if (np.amin(data) > 0.0):
            data -= np.amin(data)
        data /= np.amax(data)
        data *= 255.0
        imgCount+=1
        imageio.imwrite('pngs/'+str(imgCount)+'.png', data)
