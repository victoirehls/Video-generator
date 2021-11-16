###imports
import vapoursynth as vs
from vapoursynth import core

###
w = 720
h = 420

####
class Image:
    """Class defining an image caracterised by :
        - its url/path
        - its start frame
        - its end frame

         """

    def __init__(self, path, beginning=0, end=0):
        self.path = path

    def setBeginning(self, beginning):
        self.beginning = beginning

    def setEnd(self, end):
        self.end = end

    def getClip(self):
        clip = core.resize.Bilinear(core.imwri.Read(self.path, alpha = True)[0], w, h)
        return clip*int(self.end-self.beginning)

#ToDO rescale images for viewport


