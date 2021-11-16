###imports
import sys, os, logging
sys.path.append(os.path.abspath('.'))
import numpy as np
import numpy.random as rd
import string
import Image
import Text

###imports vapousynth
import sys, os, logging
import vapoursynth as vs
import kagefunc as kgf
from vapoursynth import core
import functools
import mvsfunc as mvs
import adjust as adj
import fvsfunc as fvf
import math
from vapoursynth import core
from easing_functions import *
import havsfunc as haf
import sys
import kagefunc as kgf
import mvsfunc as mvs
from easing_functions import *
sys.path.append(os.path.abspath('.'))
import yetilib as ylib

fps = 30

### accord
"""
Parameter description:
clip : A clip. Constant format.
clipb : B clip. Must have identical format of A clip
overlap : transition time length in frames. Floating point. Must correspond to at least 8 frames and must be EVEN
dir : direction of opening 1.vertical or 0 horizontal
twin : twin or single section 1 for twin, 0 for single
open : 1. open : A opens revealing B. 0. B closes over A
"""

def accord(image1, image2, overlap): #dir, twin, open):
    image1 = image1 + image1[1:2]*int(overlap/2)
    image2 = image2 + image2[image2.num_frames-1:image2.num_frames]*int(overlap/2)
    overlap = overlap/fps
    return core.trans.Accord(image1, image2, overlap, 1, 0, 1)

### bubbles
"""

Parameter description:
clip : A clip. Constant format.
clipb : B clip. Must have identical format of A clip
overlap : transition time length in seconds. Floating point. Must correspond to at least 8 frames and must be EVEN and preferably 30+ frames
static : bubbles are static if 1 or move if 0.
"""

def bubbles(image1, image2, overlap): #, static):
    image1 = image1 + image1[1:2]*int(overlap/2)
    image2 = image2 + image2[image2.num_frames-1:image2.num_frames]*int(overlap/2)
    overlap = overlap/fps
    return core.trans.Bubbles(image1, image2, overlap, 1)

### central
"""
Parameter description:
clip : A clip. Constant format.
clipb : B clip. Must have identical format of A clip
overlap : transition time length in seconds. Floating point. Must correspond to at least 8 frames for each turn and must be EVEN
nturns : number of full rotations the frame makes during transition. Each turn must be over at least 8 frames.Negative number reverses rotation direction.
emerge : if 1: B emerges from within A. If 0: A disappears within B
resize : if 1 :Frame will be resized or if set to 0: cropped to fit.
"""
def central(image1, image2, overlap): #, nturns, emerge, resize)
    image1 = image1 + image1[1:2]*int(overlap/2)
    image2 = image2 + image2[image2.num_frames-1:image2.num_frames]*int(overlap/2)
    overlap = overlap/fps
    return core.trans.Central(image1, image2, overlap, 25, 1, 1)


### crumple
"""
Parameter description:
clip : A clip. Constant format.
clipb : B clip. Must have identical format of A clip
overlap : transition time length in seconds. Floating point. Must correspond to at least 8 frames and must be EVEN
crumple : if set to 1 crumpling . If 0 folding.
emerge : if 1: B emerges from within A. If 0: A disappears within B
"""
def crumple(image1, image2, overlap): #, crumple,  emerge):
    image1 = image1 + image1[1:2]*int(overlap/2)
    image2 = image2 + image2[image2.num_frames-1:image2.num_frames]*int(overlap/2)
    overlap = overlap/fps
    return core.trans.Crumple(image1, image2, overlap, 1, 1)

### fade in
"""
Parameter description:
overlap in seconds and
"""
def fadeIn(image1, image2, overlap):
    #image1 = image1 + image1[1:2]*int(overlap/2)
    image2 = image2 + image2[image2.num_frames-1:image2.num_frames]*int(overlap/2)
    overlap = overlap/fps
    return kgf.crossfade(image1, image2, int(overlap*30))

### slide
"""
Parameter description:
clip : A clip. Constant format.
clipb : B clip. Must have identical format of A clip
overlap : transition time length in seconds. Floating point. Must correspond to at least 8 frames and must be EVEN
dir : 1 to 8. 1:N in a clockwise direction with 8 for NW
slidein : 1: B slides in to view over stationary A. 0: A slides out over stationary B.
"""

def slideright(image1, image2, overlap): #, dir, slidein):
    #image1 = image1 + image1[image1.num_frames-overlap:image1.num_frames-overlap+1]*int(overlap/2)
    #image2 = image2 + image2[1:2]*int(overlap/2)
    overlap = overlap/fps
    return core.trans.Slide(image1, image2, overlap, 3, 1)


def slideleft(image1, image2, overlap): #, dir, slidein):
    image1 = image1 + image1[1:2]*int(overlap/2)
    image2 = image2 + image2[image2.num_frames-1:image2.num_frames]*int(overlap/2)
    overlap = overlap/fps
    return core.trans.Slide(image1, image2, overlap, 7, 1)


def slidetop(image1, image2, overlap): #, dir, slidein):
    image1 = image1 + image1[1:2]*int(overlap/2)
    image2 = image2 + image2[image2.num_frames-1:image2.num_frames]*int(overlap/2)
    overlap = overlap/fps
    return core.trans.Slide(image1, image2, overlap, 1, 1)


def slidebottom(image1, image2, overlap): #, dir, slidein):
    image1 = image1 + image1[1:2]*int(overlap/2)
    image2 = image2 + image2[image2.num_frames-1:image2.num_frames]*int(overlap/2)
    overlap = overlap/fps
    return core.trans.Slide(image1, image2, overlap, 5, 1)


def slidemiddle(image1, image2, overlap): #, dir, slidein):
    image1 = image1 + image1[1:2]*int(overlap/2)
    image2 = image2 + image2[image2.num_frames-1:image2.num_frames]*int(overlap/2)
    overlap = overlap/fps
    return core.trans.Slide(image1, image2, overlap, 1.5, 1)


### list of transitions
transition = [accord, bubbles, crumple, fadeIn, slideright, slideleft, slidebottom, slidetop, slidemiddle]

# ToDO "Disco", "Door", "FlipPage", "Funnel", "Paint", "Push", "Roll", "Ripple", "Shuffle", "Sprite", "Swing", "Swirl", "VenitianBlinds", "Weave", "Wipe"]