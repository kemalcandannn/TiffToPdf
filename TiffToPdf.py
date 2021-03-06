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
    a4PaperRatio = 297 / 210
    orjinalImage = Image.open(path)

    orjinalImageWidth, orjinalImageHeight = orjinalImage.size

    if orjinalImageHeight < orjinalImageWidth:
        rotatedImage = orjinalImage.transpose(Image.ROTATE_270)
        orjinalImage = rotatedImage
        orjinalImageWidth, orjinalImageHeight = orjinalImage.size

    numberOfPages = 0
    imagelist = []
    firstCroppedImage = None

    if (orjinalImageHeight / orjinalImageWidth) > a4PaperRatio:
        numberOfPages = ceil(orjinalImageHeight / (orjinalImageWidth * a4PaperRatio))

    if numberOfPages > 0:
        print(" ======================================= ")
        
    for i in range(numberOfPages):
        left = 0
        top = floor(i * (orjinalImageHeight / numberOfPages))
        right = orjinalImageWidth
        bottom = floor((i + 1) * (orjinalImageHeight / numberOfPages))
        print(" =============== " + str(i+1) + ". PAGE =============== ")
        print("THE DIMENSIONS OF IMAGE HAVE BEEN TAKEN")
        print("LEFT TO RIGHT (" + str(left) + ", " + str(right) + ")")
        print("TOP TO BOTTOM (" + str(top) + ", " + str(bottom) + ")")
        croppedPilImage = orjinalImage.crop((left, top, right, bottom))
        print("THE IMAGE HAS BEEN CROPPED")
        
        #### THIS CODE BLOCK ALLOWS THE CREATED PDF TO BE LOWER SIZE ####
        croppedPilImage = croppedPilImage.convert('RGB')
        print("THE IMAGE HAS BEEN CONVERTED")
        #################################################################

        if i == 0:
            firstCroppedImage = croppedPilImage
        else:
            imagelist.append(croppedPilImage)
        print("THE IMAGE HAS BEEN ADDED TO LIST")
        print(" ======================================= ")

    if numberOfPages > 0:
        print("THE TIFF FILE WAS CONVERTED TO " + str(numberOfPages) + " PAGE PDF.")
        firstCroppedImage.save(target, save_all=True, append_images=imagelist)
        print("PDF SUCCESSFULLY CREATED.")
