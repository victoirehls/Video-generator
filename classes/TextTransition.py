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

###

fps = 30

###transparent
style = "bangers,80,&HFF08bdfb,&HFF000000,&FF000000,&HFF000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"

stylemask = "bangers,80,&HFFFFFFFF,&HFF000000,&HFFFFFFFF,&HFFFFFFFF,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"

###opaque
style = "bangers,80,&H0008bdfb,&H00000000,&00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"

stylemask = "bangers,80,&H00FFFFFF,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"

###
"""
def textDisappear(clip, text, x, y):
	def Animate(n,clip, text):
		text.setStyle("bangers,80,&H"+str(n)+"08bdfb,&H"+str(n)+"000000,&H"+str(n)+"000000,&H"+str(n)+"000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1")
		text.setStylemask("bangers,80,&H"+str(n)+"FFFFFF,&H"+str(n)+"000000,&H"+str(n)+"FFFFFF,&H"+str(n)+"FFFFFF,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1")
		wrappedtext = ylib.TextWrapper(text.content, text.style, text.stylemask)
		return ylib.AddLayer(clip, wrappedtext, x, y)
	return core.std.FrameEval(clip, functools.partial(Animate, clip=clip))
"""
### fonctions de base
def textSlide(clip, text, style, stylewhite, start_frame, duration, x_initial, x_final, y_initial, y_final, easingFunction, mode, dir, lecture_time):
	f = eval(easingFunction + "Ease" + mode)
	wrappedtext = ylib.TextWrapper(text, style, stylewhite)
	if dir == "horizontal":
		fx = f(x_initial, x_final, duration)
	elif dir == "vertical":
		fy = f(y_initial, y_final, duration)
	def Animate(n, clip):
		if n>=start_frame and n <= start_frame + duration + lecture_time:
			if dir == "horizontal":
				return ylib.AddLayer(clip, wrappedtext, (x_final,fx.ease(n-start_frame))[n<=duration + start_frame], y_initial)
			if dir == "vertical":
				return ylib.AddLayer(clip, wrappedtext, x_initial, (y_final,fy.ease(n-start_frame))[n<=duration + start_frame] )
		else:
			return clip
	return core.std.FrameEval(clip, functools.partial(Animate, clip=clip))

def textDisappear(clip, text, style, stylemask, x, y, start_frame, end_frame):
	wrappedtext = ylib.TextWrapper(text, style, stylemask)
	a = 1/(start_frame-end_frame)
	b = -a*end_frame
	def Animate(n,clip):
		wrappedtext[1] = adj.Tweak(wrappedtext[1], cont= a*n + b )
		return ylib.AddLayer(clip, wrappedtext, x, y)
	return core.std.FrameEval(clip, functools.partial(Animate, clip=clip))

###

### animations pour 3 lignes

def textAnimation31(clip, text, style, stylewhite, beginning): ### texte de 3 lignes
	n = len(text)
	for i in range(n):
		clip = textSlide(clip, text[i], style, stylewhite, 20*i + beginning , 20, -200, 100, 50+100*i, 50+100*i, "Quintic", "Out", "horizontal", 100-40*i)
	return clip


def textAnimation32(clip, text, style, stylewhite, beginning): ### texte de 3 lignes
	n = len(text)
	for i in range(n):
		clip = textSlide(clip, text[i], style, stylewhite, 20*i + beginning , 20, -200, 100, 50+100*i, 50+100*i, "Quintic", "Out", "horizontal", 100-40*i)
		clip = textSlide(clip, text[n-i-1], style, stylewhite, 80+20*i + beginning , 50, 100, 100, 250-100*i, 600, "Quad", "Out", "vertical", 20 )
	return clip


def textAnimation33(clip, text, style, stylewhite, beginning): ### texte de 3 lignes
	n = len(text)
	for i in range(n):
		clip = textSlide(clip, text[i], style, stylewhite, 20*i + beginning, 20, -200, 100, 50+100*i, 50+100*i, "Quintic", "Out", "horizontal", 60)
	return clip

def textAnimation34(clip, text, style, stylewhite, beginning): ### texte de 3 lignes
	n = len(text)
	for i in range(n):
		clip = textSlide(clip, text[i], style, stylewhite, 20*i + beginning, 20, -200, 100, 50+100*i, 50+100*i, "Quintic", "Out", "horizontal", 60)
		clip = textSlide(clip, text[i], style, stylewhite, 80+20*i + beginning, 20, 100, 100, 50+100*i, -200, "Quad", "Out", "vertical", 20 )
	return clip


def textAnimation35(clip, text, style, stylewhite, beginning): ### texte de 3 lignes
	n = len(text)
	for i in range(n):
		clip = textSlide(clip, text[i], style, stylewhite, 20*i + beginning, 20, -200, 100, 50+100*i, 50+100*i, "Quintic", "Out", "horizontal", 60)
	clip = textSlide(clip, text[0], style, stylewhite, 80 + beginning, 20, 100, 100, 50, -200, "Quad", "Out", "vertical", 20 )
	clip = textSlide(clip, text[1], style, stylewhite, 100 + beginning, 20, 100, 800, 150, 150, "Quad", "Out", "horizontal", 20 )
	clip = textSlide(clip, text[2], style, stylewhite, 120 + beginning, 20, 100, 100, 250, 600, "Quad", "Out", "vertical", 20 )
	return clip



def textAnimation36(clip, text, style, stylewhite, beginning): ### texte de 3 lignes
	n = len(text)
	clip = textSlide(clip, text[0], style, stylewhite, 0 + beginning, 40, 100, 100, -200, 50, "Quad", "Out", "vertical", 40 )
	clip = textSlide(clip, text[1], style, stylewhite, 0 + beginning, 40, -200, 100, 150, 150, "Quad", "Out", "horizontal", 60 )
	clip = textSlide(clip, text[2], style, stylewhite, 0 + beginning, 40, 100, 100, 600, 250, "Quad", "Out", "vertical", 70 )
	return clip


def textAnimation37(clip, text, style, stylewhite, beginning): ### texte de 3 lignes
	n = len(text)
	for i in range(n):
		clip = textSlide(clip, text[i], style, stylewhite, 20*i + beginning, 20, -200, 100, 50+100*i, 50+100*i, "Quintic", "Out", "horizontal", 80-20*i)
	clip = textSlide(clip, text[0], style, stylewhite, 100 + beginning, 20, 100,-200, 50, 50, "Quad", "Out", "horizontal", 0 )
	clip = textSlide(clip, text[1], style, stylewhite, 100 + beginning, 20, 100, 800, 150, 150, "Quad", "Out", "horizontal", 0 )
	clip = textSlide(clip, text[2], style, stylewhite, 100 + beginning, 20, 100, -200, 250, 250, "Quad", "Out", "horizontal", 0 )
	return clip

def textAnimation38(clip, text, style, stylewhite, beginning): ### texte de 3 lignes
	n = len(text)
	clip = textSlide(clip, text[0], style, stylewhite, 0 + beginning, 20, -200,100, 50, 50, "Quad", "Out", "horizontal", 80 )
	clip = textSlide(clip, text[1], style, stylewhite, 0 + beginning, 20, 800, 100, 150, 150, "Quad", "Out", "horizontal", 100 )
	clip = textSlide(clip, text[2], style, stylewhite, 0 + beginning, 20, -200, 100, 250, 250, "Quad", "Out", "horizontal", 110 )
	return clip

### animations pour 1 ligne
def textAnimation11(clip, text, style, stylewhite, beginning): ### texte de 1 ligne
	n = len(text)
	clip = textSlide(clip, text[0], style, stylewhite, 0 + beginning, 20, -200,100, 50, 50, "Quad", "Out", "horizontal", 100 )
	clip = textSlide(clip, text[0], style, stylewhite, 120 + beginning, 20, 100, 800, 50, 50, "Quad", "Out", "horizontal", 30)
	return clip

def textAnimation12(clip, text, style, stylewhite, beginning): ### texte de 1 ligne
	n = len(text)
	clip = textSlide(clip, text[0], style, stylewhite, 0 + beginning, 20, 100,100, -100, 50, "Quad", "Out", "vertical", 100 )
	clip = textSlide(clip, text[0], style, stylewhite, 120 + beginning, 20, 100, 800, 50, 50, "Quad", "Out", "horizontal", 30 )
	return clip




