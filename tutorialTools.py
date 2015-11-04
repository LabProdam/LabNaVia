# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
from screenTools import*
from gameTools import dinB_22,chic_16

class tutorialFases(object):
	def __init__ (self,text,rect,image,icone=None,pos=None):
		self.text=text
		self.image=image
		self.icone=icone
		self.rect=rect
		self.icone_pos=pos
	def getImage(self):
		return self.image
	def getText(self):
		return self.text
	def getIcone(self):
		return self.icone
		
class tutorialObject(object):
	def __init__(self,passos_lista,home):
		self.passos_lista=passos_lista
		self.home=home
		#self.temp_img=temp_img
		self.y=0
		self.x=0
		self.subir=False
	
	def preEvents(self):
		self.apontador=0
		pygame.time.set_timer(USEREVENT+6,10)
		self.call=False
		
	def posEvents(self):
		pygame.time.set_timer(USEREVENT+6,0)
		
	def eventControler(self, event, resize,move):
		if event.type==USEREVENT+6:
		
			if self.y<20:
				self.x+=0.5
				self.y+=0.5
			else: self.subir=True
			if self.subir:
				self.y-=1
				if self.y<0: self.subir=False

		if event.type==USEREVENT+7:
			if self.changeHand==True:
				self.changeHand=False
			else: 
				self.changeHand=True

		if event.type==MOUSEBUTTONUP:
			pos = (event.pos[0]/resize[0],event.pos[1]/resize[1])
			if self.passos_lista[self.apontador].rect.collidepoint(pos):
				self.jumpFunction()
	
	def screenCall(self):
		return None if not self.call else self.home
		
	def jumpFunction(self):
		self.apontador+=1
		if self.apontador>=len(self.passos_lista):
			self.call=True
		
	def blitOn(self, display):
		#imagem screenshot
		display.blit(self.passos_lista[self.apontador].getImage(),(0,0))
		#mao animada
		pos=list(self.passos_lista[self.apontador].icone_pos)
		pos[1]+=self.y
		display.blit(self.passos_lista[self.apontador].getIcone(),pos)
