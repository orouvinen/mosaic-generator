from PIL import Image

class MosaicTile(object):
    def __init__(self):
        pass
    
    def createFrom(self, srcImage, width, height):
        """ Create a resized tile from an image.
        Args: srcImage: source image filename
              width, height: size of the tile in pixels
        """
        f = open(srcImage, "rb")
        self._img = Image.open(f).resize((width, height), Image.NEAREST)
         
        # Generate a list of R,G,B-tuples for each pixel in image
        # and then calculate the average value of each component
        rgbdata = list(self._img.getdata())
        self._avgRGB = self._getAvgColor(rgbdata)
        f.close() 
    
    def load(self, filename):
        f = open(filename, "rb")
        self._imgData = Image.open(f).getdata()
        self._tileWidth = self._img.size[0]
        self._tileHeight = self._img.size[1]
        self._avgRGB = self._getAvgColor(self._imgData) 
        f.close()

    
    def _getAvgColor(self, rgbData):
        """ Given a sequence of R,G,B-values passed in rgbData (e.g. list
        of 3-tuples), calculate the average value of each color component.
        Return a 3-tuple containing the average value of R, G and B components.
        """
        n = len(rgbData)
        avgR = sum(_nths(rgbData, 0)) / n
        avgG = sum(_nths(rgbData, 1)) / n
        avgB = sum(_nths(rgbData, 2)) / n

        return (avgR, avgG, avgB)


    def getAvgRGB(self):
        return self._avgRGB


    def save(self, fileName):
        self._img.save(fileName, "JPEG", quality=100)


def _nths(x,n):
    """ Given a list of sequences, returns a list of all the Nth elements of
    all the contained sequences
    """
    return [l[n] for l in x]
