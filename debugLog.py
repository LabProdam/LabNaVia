basic_debug=False
super_debug=False
ultra_debug=False
screen_debug=False
gps_debug=False
import pygame,os
from pygame.locals import *

dinB_22=pygame.font.Font('fontes'+str(os.sep)+"DIN-Black.otf",22)
def debugLog(string):
	global basic_debug
	if basic_debug: print string
	
def debugGps(string):
	global gps_debug
	if gps_debug: print string
	
def debugLogSuper(string):
	global super_debug
	if super_debug: print string
	
def debugLogUltra(string):
	global ultra_debug
	if ultra_debug: print string
	
def debugLogScreen(display,text,pos,color=(0,0,0)):
	global screen_debug,dinB_22
	if screen_debug: display.blit(dinB_22.render(text,False,color),pos)
