# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os,random
from debugLog import *

#diretorios
dir_img='images'+str(os.sep)
dir_auto=dir_img+'auto'+str(os.sep)

#imagens
car_images=[[pygame.image.load(dir_auto+"autoC"+str(x)+".png").convert_alpha()] for x in range(1,6)]
car_images[4].append( pygame.image.load(dir_auto+"autoC5f.png").convert_alpha() )
truck_images=[[pygame.image.load(dir_auto+"autoT"+str(x)+".png").convert_alpha()] for x in range(1,3)]
traffic_img = pygame.Surface((640,360),SRCALPHA,32)
traffic_img.blit(pygame.transform.scale(pygame.image.load(dir_img+"faixas3.png"),(640,260)),(0,100))
traffic_img.convert_alpha()
light_img    = pygame.image.load(dir_img+"semaforo.png").convert_alpha()
light_scale=(light_img.get_width()//3)/light_img.get_height()
asphalt_img = pygame.image.load(dir_img+"asfalto.png").convert()
down_arrow= pygame.image.load(dir_img+"bikeArrowDown.png").convert_alpha()
up_arrow= pygame.image.load(dir_img+"bikeArrowUp.png").convert_alpha()

class carObject(object):
	def __init__(self,posx,vel,image,frequency):
		self.img=image
		self.vel=vel
		self.frequency=frequency#+random.randint(0,30)
		self.rect=image.get_rect(x=posx)
		self.scaled_rect=pygame.Rect(self.rect)
		self.scaled_img=image
		#pega o valor do sentido
		self.direction=(int(self.vel>0)*2)-1
		#multiplique isso por uma altura nova e obterá uma largura nova proporcional
		self.scale=float(self.rect.w)/self.rect.h
		self.move=0
	def moveCar(self):
		#soma a velocidade em x
		move=self.vel
		self.rect.x+=move
		self.move+=move
		#se passar de um dos limites retorna verdadeiro para ser removido
		return True if self.rect.x>640 or self.rect.x<-self.rect.w else False
	def stopCar(self):
		if abs(self.move) < 200:
			self.vel*=-1
			self.direction*=-1
		self.vel*=3
	def blitCar(self,display,y,h):
		self.rect.y=y
		self.scaled_rect=pygame.Rect(0,0,int(h*self.scale),h)
		self.scaled_rect.topleft=self.rect.topleft
		self.scaled_img=pygame.transform.scale(self.img,self.scaled_rect.size)
		display.blit(self.scaled_img,self.rect.topleft)
	def collideCar(self,player):
		try:
			if self.scaled_rect.colliderect(player.hit_box): 
				player.damage+=1
				player.pos[0]+=self.vel
				player.vel=0
		except Exception,e:debugLog(e)
		

def getViewport45(distancia_viewport,posicao_real,altura_camera):
	valor_1=( (posicao_real) - (altura_camera) )
	valor_2=( (posicao_real) + (altura_camera) )
	valor_3=distancia_viewport*valor_1
	return valor_3/valor_2
	
class trafficLight(object):
	def __init__(self,time,direction,vel,freq,appear):
		freq+=372
		self.odometer=appear#quando aparece no jogo
		self.vel=vel#velocidade dos carros na travessa
		self.frequency=freq#frequencia dos carros(tempo de criacao)
		self.freq_scale=freq/180
		self.direction=direction#-1=esquerda 0=faixa dupla +1=direita
		
		self.time=time#tempo de farol vermelho
		self.setZero()
	def setZero(self):
		self.crosswalk_rect=pygame.Rect(0,0,0,0)
		self.street_rect=pygame.Rect(0,0,0,0)
		self.turned_on=random.randrange(100)<40 #False se o farol esta vermelho
		debugLog(self.turned_on)
		self.timer_start=True
		self.running=False
		self.street=False
		self.crosswalk=False
		self.boolean=False
		self.player_infraction=False
		self.next_time=0
		self.car_list=[[],[]]#[0] para direita,[1] para esquerda
	def turnOnOff(self,turn_on=True):
		global car_images
		if not turn_on:
			self.car_list=[[],[]]
			new_freq=self.freq_scale*self.street_rect.h
			if self.direction>-1:#		0 or +1
				image=random.choice(car_images)
				image=pygame.transform.flip(image[0],True,False) if len(image)==1 else image[1]
				self.car_list[0].append(carObject(10-image.get_width(),self.vel,image,new_freq))
			if self.direction<+1:# -1 or 0
				image=random.choice(car_images)
				self.car_list[1].append(carObject(640,-self.vel,image[0],new_freq))
		else:
			for direction in self.car_list:
				for car in direction:
					car.stopCar()
		return not turn_on
	def eventControler(self,event,resize,move):
		if self.running:
			self.turned_on=self.turnOnOff(self.turned_on)
		value=int(self.running)
		self.running=False
		return value
	def getStreetRect(self):
		return self.street_rect if self.turned_on else None
	def getCrosswalkRect(self):
		return self.crosswalk_rect if self.turned_on else None
	def blitOn(self,final_display,listed_display,player,pause,gps,game_timer):
		global asphalt_img,traffic_img,light_img
		global car_images,truck_images
		auto_images=car_images+(truck_images if gps else [])
		if self.timer_start:
			self.next_time=pygame.time.get_ticks()-game_timer+self.time
			self.turned_on=self.turnOnOff(self.turned_on)
			self.timer_start=False
		pos=(0,player.odometer-self.odometer)
		y=getViewport45(400,(255*11)-(pos[1]*2),150)#y faixa1
		
		h=getViewport45(400,(255*12)-(pos[1]*2),150)#y faixa1 + h faixa1
		h_2=getViewport45(400,(255*(14+int(self.direction==0)))-(pos[1]*2),150)#y faixa1 + h rua(2)
		h_3=getViewport45(400,(255*(15+int(self.direction==0)))-(pos[1]*2),150)#y faixa1 + h faixa2(3)
		
		rect_0=pygame.Rect(pos[0],460-y,640,h-y)#faixa 1
		rect_1=pygame.Rect(pos[0],rect_0.y+rect_0.h,640,h_2-y)#rua
		rect_2=pygame.Rect(pos[0],rect_1.y+rect_1.h,640,h_3-y)#faixa 2
		self.crosswalk_rect=rect_0.union(rect_2)
		self.street_rect=pygame.Rect(rect_1)
		if not self.player_infraction and self.turned_on and rect_1.colliderect(player.hit_box):
			self.player_infraction=True
			player.receiveDamage(5,(0,0),5)
		#1º ciclo foreach, mas só repete duas vezes
		new_freq=self.freq_scale*rect_1.h
		for d in xrange(2):
			if self.direction==0: 
				car_y=rect_1.y+(rect_1.h/4)-(d*rect_1.h/2)
			else:
				car_y=rect_1.y-(rect_1.h/4)
			#2º ciclo foreach (dentro do 1º)
			car_len=len(self.car_list[d])
			for c,car in enumerate(self.car_list[d]):
				if new_freq!=car.frequency:
					car.rect.x+=(new_freq-car.frequency)*(car_len-c)*car.direction
					car.frequency=new_freq
				if not pause: 
					remove=car.moveCar()
					car.collideCar(player)
				car.blitCar(listed_display,car_y,rect_1.h)
				if not pause and remove: self.car_list[d].remove(car)
			if len(self.car_list[d])>0 and self.turned_on:
				if abs(self.car_list[d][-1].move)>new_freq:
					image=random.choice(auto_images)
					if d==0:
						image=pygame.transform.flip(image[0],True,False) if len(image)==1 else image[1]
					else:
						image=image[0]
					self.car_list[d].append(carObject(-image.get_width() if d==0 else 640, -self.vel*((d*2)-1), image  ,new_freq))
				
		if self.direction==0:
			rect_2.y+=rect_1.h*0.5
			rect_1.h*=1.5
		final_display.blit(pygame.transform.scale(down_arrow,((315-249)+((rect_0.y-int(rect_0.h/1.5))/4),int(rect_0.h/1.5))),(249-((rect_0.y-int(rect_0.h/1.5))/4),rect_0.y-int(rect_0.h/1.5)) )
		final_display.blit(pygame.transform.scale(up_arrow,((395-327)+((rect_2.y+(rect_2.h*2))/4),(rect_2.h*2))),(327,rect_2.y+rect_2.h) )
		#faixa de pedestre 1
		if rect_0.y<=360:
			final_display.blit(traffic_img.subsurface(pygame.Rect(rect_0.x,rect_0.y,rect_0.w,360-rect_0.y) if rect_0.h+rect_0.y>360 else rect_0),(rect_0.x,rect_0.y))

		#rua, asfalto
		#final_display.blit(pygame.transform.scale(asphalt_img,rect_1.size),rect_1.topleft)
		final_display.fill((50,50,50),rect_1)

		#faixa de pedestre 2
		if rect_2.y<=360:
			final_display.blit(traffic_img.subsurface(pygame.Rect(rect_2.x,rect_2.y,rect_2.w,360-rect_2.y) if rect_2.h+rect_2.y>360 else rect_2),(rect_2.x,rect_2.y))
		
		w_lt=light_img.get_width()/3
		h_lt=light_img.get_height()
		#poste da esquerda (costas)
		crop_rect=pygame.Rect(w_lt*2,0,w_lt,h_lt)
		croped_img=light_img.subsurface(crop_rect)
		#lt_size=(int(float(w_lt)/h_lt*rect_0.h*2),rect_0.h*2)
		#sign_pos=(270-new_size[0]-(sign_pos_vp)/1.7,sign_pos_vp-new_size[1])
		scale=abs(rect_0.y-150+float(h_lt*0.5))/360  #if bike.pos[1]<self.player.pos[1] else 1
		lt_size=(int(float(w_lt)*scale),int(float(h_lt)*scale))
		croped_img=pygame.transform.scale( croped_img ,lt_size)
		lt_pos=(250-lt_size[0]-(rect_0.y//1.7),(rect_0.y-lt_size[1]))
		listed_display.blit(croped_img,lt_pos)
		'''
		try:
			croped_img=pygame.transform.scale(croped_img,lt_size)
		except Exception,e:debugLog(e)
		listed_display.blit(croped_img,)
		'''
		#poste da direita (frente)
		crop_rect.x=w_lt*int(not self.turned_on)
		croped_img=light_img.subsurface(crop_rect)
		
		scale=abs(rect_2.y-150+float(h_lt*0.5))/360  #if bike.pos[1]<self.player.pos[1] else 1
		lt_size=(int(float(w_lt)*scale),int(float(h_lt)*scale))
		croped_img=pygame.transform.scale( croped_img ,lt_size)
		lt_pos=(400+(rect_2.y//1.7),(rect_2.y-lt_size[1])+lt_size[1]/10)
		listed_display.blit(croped_img,lt_pos)
		"""
		lt_size=(int(float(w_lt)/h_lt*rect_0.h*2),rect_0.h*2)
		try:
			croped_img=pygame.transform.scale(croped_img,lt_size)
		except Exception,e:debugLog(e)
		listed_display.blit(croped_img,(460+((rect_2.h+rect_2.y-lt_size[1])//4),(rect_2.h+rect_2.y-lt_size[1])))
		"""
		self.running=True
		return 0
