###imports
import sys, os, logging
sys.path.append(os.path.abspath('.'))
import vapoursynth as vs
import mvsfunc as mvs
import adjust as adj
from vapoursynth import core
from easing_functions import *
import numpy as np
import numpy.random as rd
import TimeFrame
from TimeFrame import TimeFrame
import Image
from Image import Image
import Text
from Text import Text
import TextSequence
from TextSequence import TextSequence
import ImageSequence
from ImageSequence import ImageSequence
import ImageTransition as trans

fps = 30
w = 720
h = 420
###
class ImageSequence :
    """
    List of Image instances, caracterised by :
        - images = list of images collected on the internet
        - textsequence = instance of TextSequence
        """

    def __init__(self, images, listtexts, transition, dict = {}):
        self.images = images
        self.listtexts = listtexts
        self.transition = transition
        self.dict = {}
        self.transitionlist= [self.transition[rd.randint(len(self.transition))] for i in range(len(images)-1)]


    def divideImage(self): #transforming images into Image() with right beginning and end time
        imagedivision = np.array_split(range(len(self.listtexts)),len(self.images))
        listimages=[]
        for i in range(len(imagedivision)): #moins d'images que de texte
            image_i = Image(self.images[i].path)
            image_i.setBeginning(self.listtexts[imagedivision[i][0]].beginning)
            image_i.setEnd(self.listtexts[imagedivision[i][len(imagedivision[i])-1]].end)
            listimages.append(image_i)
            self.dict[image_i.getClip()] = [self.listtexts[imagedivision[i][j]] for j in range(len(imagedivision[i]))]
        return listimages


    def addText(self):
        for key in self.dict.keys():
            for text in self.dict[key]:
                video = core.sub.Subtitle(key, text.content, style = text.style)




    def videoWithTransitions(self):
        #video = core.std.BlankClip(width = w,height = h, length = 1, fpsnum = 30, fpsden = 1)
        keys = [key for key in self.dict]
        video = keys[0]
        for i in range(len(self.transitionlist)):
            transition_i = self.transitionlist[i]
            video = transition_i(video, keys[i+1], 20)
        return video




