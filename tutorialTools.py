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



'''Em desenvolvimento'''
#Falta movimento de "vai-e-volta" do icone(mão, seta)
#Falta adaptar para poder receber um objeto de animação no lugar de imagem
#classe de tutorial que funcionará durante o jogo
class tutorialIngame(object):
	def __init__(self,game,icon,icon_move,icon_vel,rect,img,pos,odo,icon_used,icon_pos):
		self.game=game#o objeto de classe onde este tutorial atuará
		self.icon=icon#lista de icones(mão, seta, etc..) que apontam
		self.icon_move=icon_move#lista de posições de inicio e fim para cada icone
		self.icon_vel=icon_vel#lista de inteiros indicando a velocidade do icone

		self.rect=rect#lista de retangulos para a ativação de cada etapa(onde o jogador deverá clicar)
		self.images=img#lista de imagens(texto, balão, área de foco... tudo precisa estar nesta imagem) de cada etapa
		self.position=pos#lista de posições da imagem de cada etapa
		self.odometer=odo#lista de odometro de cada etapa, quando passar daquele ponto ela ativa
		
		self.icon_used=icon_used#lista de inteiros que dizem qual icone aquela etapa usará
		self.icon_pos=icon_pos#lista de inteiros que dizem qual icone aquela etapa usará
		
	def preEvents(self):
		self.step=0#poisção atual das listas
		self.activated=False
		self.running=True
		self.icon_moved=[0,0]#o quanto o icone atual já se deslocou
	def eventControler(self,event,resize,move):
		#se a área atual está ativada, verifica se a condição de desativar foi cumprida
			#se desativada pausa o jogo e passa para próxima etapa
		#verifica se a área atual foi clicada para ativar
			#se ativada despausa o jogo
		if self.running:
			if self.activated:
				if event.type==MOUSEBUTTONUP and event.button==1:
					mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
					if self.rect[self.step].collidepoint(mouse_pos):
						self.activated=False
						self.game.pause_game=False
						self.step+=1
						if self.step>len(self.images): 
							self.step=0
							self.running=False
			else:	
				if self.game.player.odometer>self.odometer[self.step]:
					self.activated=True
					self.game.pause_game=True
	def blitOn(self,display):
		#se travado desenha na tela a imagem do tutorial
		if self.running and self.activated:
			display.blit(self.images[self.step],self.position[self.step])
			#aqui rodaria a função de movimento do icone
			pos=[self.icon_pos[self.step][x]+self.icon_moved[self.step][x] for x in xrange(2)]
			display.blit(self.icon[self.icon_used[self.step]],pos)
