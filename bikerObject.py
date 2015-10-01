# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from debugLog import *
from screenTools import android#,blitAlpha
#classe do ciclista
class bikerObject(object):
	def __init__(self,pos,img,accel,max_vel):
		self.init_pos=pos #x,y na tela
		self.img=img #imagem
		self.accel=accel #quanto aumenta a vel
		self.max_vel=max_vel #maximo deslocamento
		self.setZero()		
	def setZero(self):
		self.desaccel=1
		self.pos=[self.init_pos[0],self.init_pos[1]] #x,y na tela
		self.vel=0 #quanto desloca por movimento
		self.flip=False
		self.level=0
	def simpleAccel(self):
		#limitacao de velocidade
		if self.max_vel>0 and self.vel+self.accel>self.max_vel: 
			self.vel=self.max_vel
		elif self.max_vel<0 and self.vel+self.accel<self.max_vel:
			self.vel=self.max_vel
		else:
			self.vel+=self.accel #aceleracao

#classe do ciclista player
class playerObject(bikerObject):
	def __init__(self,hp,pos,img,accel,max_vel):
		self.maxlife=hp
		self.level=0
		self.sheet_move=1
		self.sheet_pos=1
		bikerObject.__init__(self,pos,img,accel,max_vel)
	def setImg(self,img):
		self.img=img
		color_key=(253,142,131)
		self.stun_img=pygame.Surface(img.get_size(),0,32)
		self.stun_img.fill(color_key)
		self.stun_img.set_alpha(100)
		self.stun_img.set_colorkey(color_key)
		self.stun_img.blit(img,(0,0))
		self.hit_box=self.img.get_rect()
		self.hit_box.w/=3
		self.hit_box.w-=self.hit_box.w/6
		self.hit_box.h-=(self.hit_box.h/3)+63# 62 é diferença entre o tamanho da imagem e o pedaço da roda recuada para fora da tela
		self.wheels_box=self.hit_box.inflate(-45,0)
	def setZero(self):
		self.h_vel=0
		self.collided=False
		self.score=0
		self.collision_counter=0
		bikerObject.setZero(self)
		self.desaccel=0.5
		try:
			self.hit_box=self.img.get_rect()
			self.hit_box.w/=3
			self.hit_box.w-=self.hit_box.w/6
			self.hit_box.h-=(self.hit_box.h/3)+63# 62 é diferença entre o tamanho da imagem e o pedaço da roda recuada para fora da tela
			self.wheels_box=self.hit_box.inflate(-45,0)
		except:pass
		
		self.damage=0
		self.odometer=0
		self.stun_counter=0
		pygame.time.set_timer(USEREVENT+3,0)
	def updateHitBox(self):
		self.hit_box.topleft=self.pos
		#diminui pela metade a caixa de colisao do player (perspectiva)
		self.hit_box.y+=(self.hit_box.h+62)/2
		self.hit_box.x+=self.hit_box.w/10
		self.wheels_box=self.hit_box.inflate(-45,0)
	def playerMove(self,direction):
		self.pos[0]+=direction*2+(self.vel//2*direction)#self.pos[0]+=self.vel//2*direction
	def playerBrake(self,stop):
		self.desaccel=stop
	def playerAccel(self,direction):#+1(direita) ou -1(esquerda)
		#self.flip = not self.flip
		if self.sheet_pos==2 or self.sheet_pos==0:
			self.sheet_move*=(-1)
		self.sheet_pos+=self.sheet_move
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
		if abs(self.h_vel)>0.1:
			self.h_vel-=self.h_vel*0.01*self.desaccel
		else:
			self.h_vel=0
		self.odometer+=self.vel #deslocamento/10 -> *nao pode diminuir aqui senao afeta a placa da prodam que usa isso pro proprio deslocamento*
		self.pos[0]+=self.h_vel
		#Limitacao do Ciclista com espaco levar penalidade
		if self.pos[0]>500:
			self.pos[0]=500
			self.h_vel=0
		if self.pos[0]<100:
			self.pos[0]=100
			self.h_vel=0
		try:self.updateHitBox()
		except Exception,e:print e
		self.vel=self.max_vel
	def receiveDamage(self,damage,recoil=(0,0),stun=100):
		if android and self.damage<self.maxlife: android.vibrate(0.5)
		if self.stun_counter<5:
			self.pos[0]+=recoil[0]
			self.odometer+=recoil[1]
		if self.stun_counter>50:
			self.stun_counter=0
		if self.stun_counter==0:
			pygame.time.set_timer(USEREVENT+3,stun)
			self.damage+=damage
			if not self.collided:self.collision_counter+=1
			self.collided=True
			self.stun_counter=1 # talvez isso seja a solução para algum problema futuro sobre danos absurdos, não sei, não tenho certeza
	def eventControler(self,event,resize):
		if event.type==USEREVENT+3 and self.stun_counter>0:
			self.stun_counter+=1
			#print self.stun_counter
			if self.stun_counter>50:#10
				self.stun_counter=0
				self.collided=False
				pygame.time.set_timer(USEREVENT+3,0)
	def blitOn(self,display):
		sheet_rect=pygame.Rect(self.sheet_pos*(self.img.get_width()/3),0,self.img.get_width()//3,self.img.get_height())
		player_img=self.img.subsurface(sheet_rect) if self.stun_counter<=0 or self.stun_counter%2==0 else self.stun_img.subsurface(sheet_rect)
		#display.fill((0,0,0),self.wheels_box)
		#player_img=pygame.transform.flip(self.img,self.flip,False)
		'''
		if self.stun_counter>0:
			opacity=((int(self.stun_counter%2)+1)*50)+self.stun_counter*2#15
			blitAlpha(display,player_img,self.pos,opacity)
		else:
			display.blit( player_img, self.pos )
		'''
		display.blit( player_img, self.pos )
		#display.fill((255,0,0),self.hit_box)
	def updateLevel(self,a):
		debugLog("\t\tlevel update:"+str(self.level))
		self.level=a
			
	def getCurrentLevel(self):
		return self.level
		
	def setScore(self,a):
		if self.score>=0:
			self.score+=a
		if self.score<0:
			self.score=0
		#print "score++: "+str(self.score)

#classe do ciclista npc
class passerbyObject(bikerObject):
	def __init__(self,pos,img,accel,max_vel,appearance_point):
		bikerObject.__init__(self,pos,img,accel,max_vel)
		self.odometer=appearance_point
		self.hit_box=img.get_rect()
	def setZero(self):
		bikerObject.setZero(self)
		self.stop=False
	def passerbyMotion(self,player_motion):
		self.simpleAccel()
		self.pos[1] += self.vel + player_motion if self.pos[1]>-self.img.get_height() else player_motion
	def collide(self,player):
		retorno=0
		if self.hit_box.inflate(self.hit_box.w*0.2,self.hit_box.h*0.6).colliderect(player.hit_box):
			drct=((int(player.hit_box.x>self.hit_box.x)*2)-1)
			player.receiveDamage(1,(drct*20,0))
			retorno=1
		if self.hit_box.inflate(self.hit_box.w*0.6,self.hit_box.h*0.2).colliderect(player.hit_box):
			if self.vel>0: self.vel=-100*player.accel*self.accel
			player.receiveDamage(1,(0,-20))
			player.vel=0
			retorno=1
		return retorno
	def blitOn(self,display):
		rect=self.img.get_rect(topleft=self.pos)
		scale=(rect.y+(rect.h)*1.5)/360
		new_size=(int(rect.w*scale),int(rect.h*scale))
		new_img=pygame.transform.scale(
			pygame.transform.flip(self.img,self.flip,False),
			new_size)
		if self.pos[0]<300:
			self.hit_box=new_img.get_rect(topright=rect.topright)
		else:
			self.hit_box=new_img.get_rect(topleft=rect.topleft)
		display.blit(new_img,self.hit_box.topleft)
		display.fill((255,0,0),self.hit_box.inflate(self.hit_box.w*0.6,self.hit_box.h*0.2))
