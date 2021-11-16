import vapoursynth as vs
import mvsfunc as mvs
import adjust as adj
from vapoursynth import core
from easing_functions import *
import numpy as np

################################################################################################################################
## Styles
#def TitleStyle():

#def SubtitleStyle():


################################################################################################################################
## Monochrome filtering
################################################################################################################################
## Greyscale conversion with color filter.
## needs adjust: 'vsrepo.py install adjust' see https://github.com/dubhater/vapoursynth-adjust
## needs mvsfunc: 'vsrepo.py install mvsfunc' see https://github.com/HomeOfVapourSynthEvolution/mvsfunc
################################################################################################################################
## parameters
##	clip {clip}: RGB clip to be converted
##	hue {int}: target hue (color tint) (-180.0 .. 180.0)
##	cont {int}: target contrast (0.0=unchanged .. 10.0)
################################################################################################################################
def MonoFilter(clip, hue=0, cont=1):
	clip = Grayscale(clip)
	bl = core.std.BlankClip(clip, color=0)
	# greyscale on one of the planes
	clip=core.std.ShufflePlanes([clip, bl, bl], planes=[0, 0, 0], colorfamily=vs.RGB)
	clip=mvs.ToYUV(clip)
	clip=adj.Tweak(clip, hue=hue, cont=cont)
	return mvs.ToRGB(clip)

################################################################################################################################
## Greyscale
################################################################################################################################
## Greyscale conversion
################################################################################################################################
## parameters
##	clip {clip}: RGB clip to be converted
################################################################################################################################
def Grayscale(clip, format = vs.GRAY):
	r=core.std.ShufflePlanes(clip, 0, vs.GRAY)
	g=core.std.ShufflePlanes(clip, 1, vs.GRAY)
	b=core.std.ShufflePlanes(clip, 2, vs.GRAY)
	clip = core.std.Expr(clips=[r, g, b], expr=["x y + z + 3 /"])
	if format == vs.RGB24:
		clip= core.std.ShufflePlanes([clip, clip, clip], planes=[0, 0, 0], colorfamily=vs.RGB)
	return clip

################################################################################################################################
## ViewPortAdjust
################################################################################################################################
## crop and add borders to a layer to match a viewport dimensions at a defined position
################################################################################################################################
## parameters
##	layer {clip}: layer to be processed
##	viewPortWidth (int): the target viewport width
##	viewPortHeight (int): the target viewport height
##	layerPosX (int): the layer X position inside the viewport
##	layerPosY (int): the layer Y position inside the viewport
################################################################################################################################
def ViewPortAdjust(viewPortWidth, viewPortHeight, layer, layerPosX=0, layerPosY=0):
	layerPosX = round(layerPosX)
	layerPosY = round(layerPosY)
	if layerPosX+layer.width <= 0 or layerPosY+layer.height <= 0 or layerPosX >= viewPortWidth or layerPosY >= viewPortHeight:
		# layer is totally outside viewport
		layer = None
	else:
		# layer and viewport have an intersection
		deltaW = layerPosX+layer.width-viewPortWidth
		deltaH = layerPosY+layer.height-viewPortHeight
		layer = core.std.Crop(layer, left=max(0, -layerPosX), right=max(0, deltaW), top=max(0, -layerPosY), bottom=max(0, deltaH))
		layer = core.std.AddBorders(layer, left=max(0, layerPosX), right=max(0, -deltaW), top=max(0, layerPosY), bottom = max(0, -deltaH))
	return layer

################################################################################################################################
## AddLayer
################################################################################################################################
## merge a layer having an alpha channel on a background at a specific position
## the layer is cropped to fit the background if necessary
################################################################################################################################
## parameters
##	bakground {clip}: the target background
##	foregroundAndMask (clip): the foreground layer
##	layerPosX (int): the layer X position inside the viewport
##	layerPosY (int): the layer Y position inside the viewport
################################################################################################################################
def AddLayer(background, foregroundAndMask, posX, posY):
	foreground = ViewPortAdjust(background.width, background.height, foregroundAndMask[0], posX, posY)
	mask = ViewPortAdjust(background.width, background.height, foregroundAndMask[1], posX, posY)
	if foreground==None:
		return background
	else:
		return core.std.MaskedMerge(background, foreground, mask)


################################################################################################################################
## BuildTextLayer
################################################################################################################################
## Create a text layer on a transparent background
################################################################################################################################
## parameters
##	pixFile {str}: the path to a 1x1 png transparent pixel
##	text (str): the text to be displayed
##	style (str): the ASS style to be applied
################################################################################################################################
def BuildTextLayer(pixFile, text, styleMask, style):
	pix = core.imwri.Read(pixFile, alpha=True)
	txtAreaWidth=1999
	txtAreaHeight=1999
	pix[0] = core.resize.Point(pix[0], txtAreaWidth, txtAreaHeight)
	pix[1] = core.resize.Point(pix[1], txtAreaWidth, txtAreaHeight)
	pix[0] = core.sub.Subtitle(pix[0], text, style=style)
	#pix[1] = core.sub.Subtitle(pix[1], text, style=styleMask)
	return pix

################################################################################################################################
## MixPlanes
################################################################################################################################
## test
################################################################################################################################
def MixPlanes(clip):
	return core.std.ShufflePlanes([core.std.ShufflePlanes(clip, 1, vs.GRAY), core.std.ShufflePlanes(clip, 2, vs.GRAY), core.std.ShufflePlanes(clip, 0, vs.GRAY)], planes=[0, 0, 0], colorfamily=vs.RGB)

################################################################################################################################
## TextWrapper : creates a layer under the text
################################################################################################################################
## parameters
## text : string
## style : ASS style
## stylewhite : same style but color = white
## needs numpy (import numpy as np)
## returns an image with an alpha

def FindText(array, image):
	height = array.shape[0]
	width = array.shape[1]
	columns=[]
	lines=[]
	for j in range(width):
		for i in range(height):
			if array[i][j] == 255:
				columns.append(j)
				lines.append(i)
	return [min(columns), width-max(columns)-1, min(lines), height-max(lines)-1]

def TextWrapper(text, style, stylewhite):
	blank = core.std.BlankClip(format = vs.RGB24, width = 1000, height= 500, color = [255,255,255])
	textlayer = core.sub.Subtitle(blank, text, style = style)
	blankmask = core.std.BlankClip(format = vs.GRAY8, width = 1000, height= 500, color = 0)
	blankmask = core.sub.Subtitle(blankmask, text, style = stylewhite)
	blankmask = core.std.Binarize(blankmask,v0 = 0, v1 = 255,planes=[0,1,2])
	canny = core.tcanny.TCanny(textlayer)
	canny = Grayscale(canny, format = vs.RGB24)
	canny = core.std.Binarize(canny,v0 = 0, v1 = 255,planes=[0,1,2])
	npArray = np.asarray(canny.get_frame(0).get_read_array(0))
	boundingbox = FindText(npArray, textlayer)
	blankmask = core.std.Crop(blankmask, boundingbox[0], boundingbox[1], boundingbox[2], boundingbox[3])
	textlayer = core.std.Crop(textlayer,boundingbox[0], boundingbox[1], boundingbox[2], boundingbox[3])
	return [textlayer, blankmask]

##################################################
