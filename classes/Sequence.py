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
import string
from Image import Image
from Text import Text
import ImageTransition as trans

w = 720
h = 420
fps = 30

###
class Sequence :

    """
Sequence, caracterised by :
    - totaltime = length of final video in seconds
    - texts = list of strings (the one we get with the API)
    - images = list of image paths
    - imagetransition = available transitions
    - textanimations1 = available animations for 1 line texts
    - textanimations3 = available animations for 3 lines texts
    - image effects = available image effects
    - units = list of SequenceUnits
    - seq = dictionary {imagei = [texti1, ... textin ], ... }
    """


    def __init__(self, totaltime, texts, images, imagetransitions, textanimations1, textanimations3, image_effects, units = []):
        self.totaltime = totaltime
        self.texts = texts
        self.images = images
        self.transitionlist = [imagetransitions[rd.randint(len(imagetransitions))] for i in range(len(images)-1)]
        self.textanimations1 = textanimations1
        self.textanimations3 = textanimations3
        self.units = []
        self.image_effects = [image_effects[rd.randint(len(image_effects))] for i in range(rd.randint(len(image_effects))) ]

#ToDO add random on textanimations (right now in sequencemanager)

    def getTotaltime():
        return self.totaltime

    def getTexts():
        return self.texts

    def getImages():
        return self.images

    def getTransitionlist():
        return self.transitionlist

    def getSeq():
        return self.seq

