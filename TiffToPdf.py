import pip
import sys
"""
########### RUN COMMAND LINE ###########

# python3 TiffToPdf.py [PATH] [TARGET]

########################################
"""

n = len(sys.argv)

if n != 3:
    print("THIS SCRIPT RUNS WITH 3 PARAMETER.")

    print("USAGE TEMPLATE: 'python3 TiffToPdf.py [PATH] [TARGET]'")
    print("arg[0] ==> SCRIPT_NAME")
    print("arg[1] ==> PATH")
    print("arg[2] ==> TARGET")
else:
    try:
        from math import floor, ceil
    except ModuleNotFoundError:
        pip.main(['install', "math"])
    try:
        from PIL import Image
    except ModuleNotFoundError:
        pip.main(['install', "Pillow"])

    Image.MAX_IMAGE_PIXELS = None

    path, target = sys.argv[1], sys.argv[2]
    a4KagidiOrani = 297 / 210
    orjinalImage = Image.open(path)

    orjinalImageWidth, orjinalImageHeight = orjinalImage.size

    if orjinalImageHeight < orjinalImageWidth:
        rotatedImage = orjinalImage.transpose(Image.ROTATE_270)
        orjinalImage = rotatedImage
        orjinalImageWidth, orjinalImageHeight = orjinalImage.size

    kacSayfayaBolunecek = 0
    imagelist = []
    firstCroppedImage = None

    if (orjinalImageHeight / orjinalImageWidth) > a4KagidiOrani:
        kacSayfayaBolunecek = ceil(orjinalImageHeight / (orjinalImageWidth * a4KagidiOrani))

    if kacSayfayaBolunecek > 0:
        print(" ==================================== ")
        
    for i in range(kacSayfayaBolunecek):
        left = 0
        top = floor(i * (orjinalImageHeight / kacSayfayaBolunecek))
        right = orjinalImageWidth
        bottom = floor((i + 1) * (orjinalImageHeight / kacSayfayaBolunecek))
        print(" ============== " + str(i+1) + ". PAGE ============= ")
        print("THE DIMENSIONS OF IMAGE HAVE BEEN TAKEN")
        print("LEFT TO RIGHT (" + str(left) + ", " + str(right) + ")")
        print("TOP TO BOTTOM (" + str(left) + ", " + str(right) + ")")
        croppedPilImage = orjinalImage.crop((left, top, right, bottom))
        #croppedPilImage = croppedPilImage.convert('RGB')
        print("THE IMAGE HAS BEEN CROPPED")

        if i == 0:
            firstCroppedImage = croppedPilImage
        else:
            imagelist.append(croppedPilImage)
        print("THE IMAGE HAS BEEN ADDED TO LIST")
        print(" ==================================== ")

    if kacSayfayaBolunecek > 0:
        print("THE TIFF FILE WAS CONVERTED TO " + str(kacSayfayaBolunecek) + " PAGE PDF.")
        firstCroppedImage.save(target, save_all=True, append_images=imagelist)
        print("PDF SUCCESSFULLY CREATED.")
