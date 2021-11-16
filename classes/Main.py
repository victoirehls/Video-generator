###imports
import sys, os, logging
sys.path.append(os.path.abspath('.'))
import vapoursynth as vs
import mvsfunc as mvs
import adjust as adj
from vapoursynth import core
from easing_functions import * #pip install easing_functions*
import numpy as np #pip install numpy
import numpy.random as rd
import string
from Image import Image
from Text import Text
import ImageTransition as trans
from Sequence import Sequence
import SequenceManager
import TextTransition as txttrans
import api_call as api
from SequenceUnit import SequenceUnit
import ImageEffect as imgeff


###create a timeframe : choose total time of clip in seconds
totaltime = 60
fps = 30
w = 720
h = 420
###
style = "bangers,80,&H00FF0000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"

textanimations1 = [txttrans.textAnimation11, txttrans.textAnimation12]
textanimations3 = [txttrans.textAnimation31, txttrans.textAnimation32, txttrans.textAnimation33, txttrans.textAnimation34, txttrans.textAnimation35, txttrans.textAnimation36, txttrans.textAnimation37, txttrans.textAnimation38]
#textanimations2 =




### get images
location_id = 'ozkjra' # New-york
iso_3166_country = 'us'
iso_639_language = 'fr'
images = api.get_photos(location_id)[0:2]


#for i in range(1):
 #   images.append(r"C:\Users\victo\Desktop\moneyeti\images\paris_" + str(i) + ".jpg")



### create texts

location_id = 'ozkjra'
iso_639_language = 'fr'
iso_3166_country = 'us'


texts = [api.get_city_name(location_id, iso_639_language), api.get_currency(iso_3166_country, iso_639_language), 'Le budget moyen est de '+str(api.get_budget(location_id, iso_639_language)),'vat: '+str(api.payment_info['vatRate']),'contactlessLimit:'+str(api.payment_info['contactlessLimit']),'paymentPreference: '+ api.payment_info['paymentPreference']]


### image transitions

imagetransitions = [trans.slideright, trans.slideleft, trans.slidetop, trans.slidebottom, trans.bubbles, trans.slidemiddle]

### image effects

image_effects = [imgeff.kenBurns, imgeff.freezeAndFilter]
#ToDO add affects

### create Sequence
sequence = Sequence(totaltime, texts, images, imagetransitions, textanimations1, textanimations3, image_effects)

###divide texts, divide images, update dictionary
listtexts = SequenceManager.divideTexts(sequence)
SequenceManager.divideImages(sequence, listtexts)
SequenceManager.addImageEffects(sequence)
listImagesWithText = SequenceManager.addText(sequence, listtexts)
video = SequenceManager.addImageTransitions(sequence, listImagesWithText)

video = core.resize.Bicubic(video, format=vs.YUV420P8, matrix_s="709")
video.set_output()



