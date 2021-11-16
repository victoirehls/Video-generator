###
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
import TextTransition as txttrans
from SequenceUnit import SequenceUnit


w = 720
h = 420
fps = 30


### exemple : "new york est une ville des états unis" --> ["new york est", "une ville des", "etats unis"]

def countSpaces(text):
    count = 0
    for i in range(len(text)):
        if text[i]==" ":
            count+= 1
    return count

def words(text):
    index = 0
    words = []
    count = countSpaces(text)
    if count == 0:
        words = [text[0:len(text)]]
    else:
        index = 0
        for i in range(len(text)):
            if text[i] == " ":
                words.append(text[index:i])
                index = i+1
        words.append(text[index:len(text)])
    return words


def textSeparator(text): #string
    res= []
    if len(words(text)) < 4 :
        res = [text]
    else:
        separator = np.array_split(range(len(words(text))),3)
        for j in range(len(separator)):
            res_j = words(text)[separator[j][0]]
            for i in range(1,len(separator[j])):
                res_j += " " + words(text)[separator[j][i]]
            res.append(res_j)
    return res

####

# divide text according to the total time of the video and creating instances of Text()
# returns a list of instances of Text() with right beginning and end

def divideTexts(sequence):
    totaltime = sequence.totaltime
    texts = sequence.texts
    textdivision = np.array_split(range(totaltime*fps), len(texts))
    listtexts = []
    for i in range(len(textdivision)):#add beginning and end time in the objects text
        text_i = Text(texts[i])
        text_i.setBeginning(textdivision[i][0])
        text_i.setEnd(textdivision[i][len(textdivision[i])-1])
        listtexts.append(text_i)
    return listtexts


# divide images according to the number of texts and creating instances of Image()
# updating sequence.units
# returns a list of instances of Image() with right beginning and end
# must have less images than texts

def divideImages(sequence, listtexts):
    images = sequence.images
    imagedivision = np.array_split(range(len(listtexts)),len(images))
    listimages=[]
    for i in range(len(imagedivision)):
        image_i = Image(images[i])
        image_i.setBeginning(listtexts[imagedivision[i][0]].beginning)
        image_i.setEnd(listtexts[imagedivision[i][len(imagedivision[i])-1]].end)
        listimages.append(image_i)
        unit_i = SequenceUnit(image_i.getClip(), [listtexts[imagedivision[i][j]] for j in range(len(imagedivision[i]))])
        sequence.units.append(unit_i)
        #sequence.seq[image_i.getClip()] = [listtexts[imagedivision[i][j]] for j in range(len(imagedivision[i]))]

def addImageEffects(sequence):
    n = len(sequence.image_effects)
    units = sequence.units
    imageWithEffects = [units[i].image for i in range(n)]
    for i in range(len(sequence.units)):
        if units[i].image in imageWithEffects:
            beginning = units[i].textlist[0].beginning
            end = units[i].textlist[len(units[i].textlist)-1].end
            beginning += (end-beginning)//2
            sequence.units[i].image = sequence.image_effects[i](units[i].image, int(beginning), int(end))


def addText(sequence, listtexts):
    #seq = sequence.seq
    #keys = [k for k in seq.keys()]
    #video = keys[0]
    video = sequence.units[0].image
    for i in range(1,len(sequence.units)):
        video += sequence.units[i].image
    for i in range(len(listtexts)):
        text = listtexts[i]
        n = len(textSeparator(text.content))
        duration = listtexts[i].end-listtexts[i].beginning
        if n == 1:
            animation= sequence.textanimations1[rd.randint(2)]
        #elif n==2 :
         #   transition_i =sequence.textanimations2[i]
        elif n==3 :
            animation= sequence.textanimations3[rd.randint(len(sequence.textanimations3))]
        video = animation(video, textSeparator(listtexts[i].content), listtexts[i].style, listtexts[i].stylemask, listtexts[i].beginning)
    return video


def addImageTransitions(sequence, videoWithTexts):
    imagesWithTexts = []
    units = sequence.units
    for i in range(len(sequence.units)):
        start = units[i].textlist[0].beginning
        end = units[i].textlist[len(units[i].textlist)-1].end
        imagesWithTexts.append(videoWithTexts[start:end])
    video = imagesWithTexts[0]
    transitionlist = sequence.transitionlist
    for i in range(len(transitionlist)):
        transition_i = transitionlist[i]
        video = transition_i(video, imagesWithTexts[i+1], 10)
    return video




