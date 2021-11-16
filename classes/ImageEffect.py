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

### Ken Burns
def zoomInOut(clip, start_frame, end_frame, easingFunction, mode, x_initial, x_final, y_initial, y_final, dir):
	if dir == "horizontal":
		f = eval(easingFunction + "Ease" + mode)
		fx = f(x_initial, x_final, end_frame-start_frame)
	elif dir == "vertical":
		f = eval(easingFunction + "Ease" + mode)
		fx = f(y_initial, y_final, end_frame-start_frame)
	def animateZoomInOut(n, clip):
		if n>=start_frame and n<= end_frame:
			clip_i = core.resize.Bilinear(clip, w+fx.ease(n-start_frame), h+(h*fx.ease(n-start_frame))/w)
			clip_i = core.std.Crop(clip_i,fx.ease(n-start_frame),0,0,(h*fx.ease(n-start_frame))/w)
			return clip_i
		elif n<= start_frame:
			return clip
		elif n>= end_frame:
			clip_i = core.resize.Bilinear(clip, w+fx.ease(end_frame-start_frame), h+(h*fx.ease(end_frame-start_frame))/w)
			clip_i = core.std.Crop(clip_i,fx.ease(end_frame-start_frame),0,0,(h*fx.ease(end_frame-start_frame))/w)
			return clip_i
	return core.std.FrameEval(clip, functools.partial(animateZoomInOut, clip=clip))



### imageFreeze
def imageFreeze(clip, freeze_frame):
	clipA = clip[:freeze_frame-1]
	return clipA + clip[freeze_frame]*100

### imageFreeze with filter
def imageFreeze(clip, freeze_frame, hue, cont, duration): #duration in frames
	clipA = clip[:freeze_frame-1]
	clipB = clip[freeze_frame] * duration
	clipB = ylib.MonoFilter(clipB, hue, cont)
	return clipA + clipB

###
def kenBurns(clip, beginning, end):
	return zoomInOut(clip, beginning, end, "Quintic", "Out", 0, 300, 100, 100, "horizontal")

def freezeAndFilter(clip, beginning, end): #end of the image
	return imageFreeze(clip, beginning, hue=1, cont=1, duration = int(end-beginning) )