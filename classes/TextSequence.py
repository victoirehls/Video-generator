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
import Image
from Image import Image
import Text
from Text import Text
import TextSequence
from TextSequence import TextSequence
import ImageSequence
from ImageSequence import ImageSequence
import ImageTransition


### functions
possibletexts=[]
for i in range(10):
    text_i = ""
    for j in range(5):
        text_i = text_i + string.ascii_lowercase[rd.randint(len(string.ascii_lowercase))]
    possibletexts.append(text_i)


def getRandomtexts(possibletexts, n): # avoir n textes différents de la liste des textes possibles
    texts = []
    index = []
    while len(texts) < n :
        var = rd.randint(len(possibletexts)-1)
        if var not in index:
            texts.append(possibletexts[var])
    return texts


fps = 30

#####
class TextSequence :
    """
    List of Text instances, caracterised by :
        - texts = list of possible texts (strings)
        - totalvideotime = length of final video in seconds
        - number of texts

        """

    def __init__(self, possibletexts, totalvideotime, n):
        self.n = n
        self.texts = getRandomtexts(possibletexts,n)
        self.totalvideotime = totalvideotime



    def divideTexts(self): #divide text following totalvideotime
        textdivision = np.array_split(range(self.totalvideotime*fps), len(self.texts))
        listtexts = []
        for i in range(len(textdivision)):#add beginning and end time in the objects text
            text_i = Text(self.texts[i])
            text_i.setBeginning(textdivision[i][0])
            text_i.setEnd(textdivision[i][len(textdivision[i])-1])
            listtexts.append(text_i)
        return listtexts

    #def setTextTransitions(self):





