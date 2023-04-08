# Author: Jacob Dawson
#
# This is just a small script which takes 4 images and combines them into a
# single image made up of 4 quadrants
# It will take these images from a folder called "quadrants"
#
# Please note that this script does some fairly agressive cropping,
# so I'd recommend doing some resizing and cropping of your own beforehand
# to make square images that you like. Really all that this script does
# is make the quadrant images!

import os
from PIL import Image

# walk through the files:
list_of_files = {}
for (dirpath, dirnames, filenames) in os.walk('quadrants'):
    for filename in filenames:
        if filename.endswith('.png'):
            list_of_files[filename] = os.sep.join([dirpath, filename])

# only select 4 of them:
imagePaths = []
i = 0
for k,v in list_of_files.items():
    i+=1
    imagePaths.append(v)
    print("Reading "+v)
    if i==4:
        break

# find the smallest axis. We'll crop each image to be a perfect square based
# off of this
sizes = []
images = []
for imagePath in imagePaths:
    curImg = Image.open(imagePath)
    images.append(curImg)
    width, height = curImg.size
    sizes.append(width)
    sizes.append(height)
smallest = 65535
for size in sizes:
    if size < smallest:
        smallest = size

# hardcoding because I feel lazy:
img1 = images[0].crop((0, 0, smallest, smallest))
img2 = images[1].crop((0, 0, smallest, smallest))
img3 = images[2].crop((0, 0, smallest, smallest))
img4 = images[3].crop((0, 0, smallest, smallest))

# make the new image and add our current images to it
new_im = Image.new('RGB', (smallest*2, smallest*2))
new_im.paste(img1, (0,0))
new_im.paste(img2, (smallest,0))
new_im.paste(img3, (0,smallest))
new_im.paste(img4, (smallest,smallest))

new_im.save('quadrants.png')
