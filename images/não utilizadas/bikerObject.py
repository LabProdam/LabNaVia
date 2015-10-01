# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from screenTools import blitAlpha

#classe do ciclista
class bikerObject(object):
	def __init__(self,pos,img,accel,max_vel):
		self.init_pos=pos #x,y na tela
		self.img=img #imagem
		self.accel=accel #quanto aumenta a vel
		self.desaccel=1
		self.max_vel=max_vel #maximo deslocamento
		self.setZero()
	def setZero(self):
		self.pos=[self.init_pos[0],self.init_pos[1]] #x,y na tela
		self.vel=0 #quanto desloca por movimento
		self.flip=False
	def simpleAccel(self):
		#limitacao de velocidade
		if self.max_vel>0 and self.vel+self.accel>self.max_vel: 
			self.vel=self.max_vel
		elif self.max_vel<0 and self.vel+self.accel<self.max_vel:
			self.vel=self.max_vel
		else:
			self.vel+=self.accel #aceleracao

player_current_level=0

#classe do ciclista player
class playerObject(bikerObject):
	def __init__(self,hp,pos,img,accel,max_vel):
		self.maxlife=hp
		bikerObject.__init__(self,pos,img,accel,max_vel)
	def setZero(self):
		bikerObject.setZero(self)
		self.damage=0
		self.odometer=0
		self.stun_counter=0
		pygame.time.set_timer(USEREVENT+3,0)
	def playerAccel(self,direction):#+1(direita) ou -1(esquerda)
		self.flip = not self.flip
		self.pos[0]+=4*direction
		self.simpleAccel()
		#Penalidade de velociadade por sair da pista
		if self.pos[0]<150:
			self.vel*=0.7
		if self.pos[0]>450:
			self.vel*=0.7
	def playerMotion(self):
		#desaceleracao, com limite para desaceleracao total
		if self.vel>0.1:
			self.vel-=self.vel*0.01*self.desaccel
		else: 
			self.vel=0

		self.odometer+=self.vel #deslocamento/10 -> *nao pode diminuir aqui senao afeta a placa da prodam que usa isso pro proprio deslocamento*

		#Limitacao do Ciclista com espaco levar penalidade
		if self.pos[0]>500:
			self.pos[0]=500
		if self.pos[0]<100:
			self.pos[0]=100
	def receiveDamage(self,damage,recoil=(0,0),stun=100):
		if self.stun_counter==0:
			self.pos[0]+=recoil[0]
			self.odometer+=recoil[1]
			self.damage+=damage
			pygame.time.set_timer(USEREVENT+3,stun)
	def eventControler(self,event,resize):
		if event.type==USEREVENT+3:
			self.stun_counter+=1
			#print self.stun_counter
			if self.stun_counter>50:#10
				self.stun_counter=0
				pygame.time.set_timer(USEREVENT+3,0)
	def blitOn(self,display):
		player_img=pygame.transform.flip(self.img,self.flip,False)
		if self.stun_counter>0:
			opacity=((int(self.stun_counter%2)+1)*50)+self.stun_counter*2#15
			blitAlpha(display,player_img,self.pos,opacity)
		else:
			display.blit( player_img, self.pos )
	
	def updateLevel(self,a):
		print "update"
		player_current_level=a
			
	def getCurrentLevel(self):
		return player_current_level
			
#classe do ciclista npc
class passerbyObject(bikerObject):
	def __init__(self,pos,img,accel,max_vel,appearance_point):
		bikerObject.__init__(self,pos,img,accel,max_vel)
		self.odometer=appearance_point
	def setZero(self):
		bikerObject.setZero(self)
		self.stop=False
	def passerbyMotion(self,player_motion):
		self.simpleAccel()
		self.pos[1] += self.vel + player_motion if self.pos[1]>-self.img.get_height() else player_motion
