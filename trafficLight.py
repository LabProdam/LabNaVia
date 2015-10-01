# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os,random

#diretorios
dir_img='images'+str(os.sep)
dir_auto=dir_img+'auto'+str(os.sep)

#imagens
car_images=[pygame.image.load(dir_auto+"autoC"+str(x)+".png").convert_alpha() for x in range(1,4)]
truck_images=[pygame.image.load(dir_auto+"autoT"+str(x)+".png").convert_alpha() for x in range(1,3)]
#car_images+=truck_images
traffic_img  = pygame.image.load(dir_img+"faixas3.png").convert_alpha()
light_img    = pygame.image.load(dir_img+"semaforo.png").convert_alpha()
light_scale=(light_img.get_width()//3)/light_img.get_height()
asphalt_img = pygame.image.load(dir_img+"asfalto.png").convert()
down_arrow= pygame.image.load(dir_img+"bikeArrowDown.png").convert_alpha()
up_arrow= pygame.image.load(dir_img+"bikeArrowUp.png").convert_alpha()

class carObject(object):
	def __init__(self,posx,vel,image,frequency):
		self.img=image
		self.vel=vel
		self.frequency=frequency
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
		move=self.vel#+(h*self.direction)#*self.scale*h
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
		self.scaled_rect=pygame.Rect(0,0,int(h*self.scale),h)# self.rect.inflate(int(h*self.scale),h)
		self.scaled_rect.topleft=self.rect.topleft
		self.scaled_img=pygame.transform.scale(self.img,self.scaled_rect.size)
		display.blit(self.scaled_img,self.rect.topleft)
	def collideCar(self,player):
		try:
			if self.scaled_rect.colliderect(player.hit_box): player.receiveDamage(1,(self.vel*self.direction,0))
		except Exception,e:print e
		

def getViewport45(distancia_viewport,posicao_real,altura_camera):
	valor_1=( (posicao_real) - (altura_camera) )
	valor_2=( (posicao_real) + (altura_camera) )
	valor_3=distancia_viewport*valor_1
	return valor_3/valor_2
	
class trafficLight(object):
	def __init__(self,time,direction,vel,freq,appear):
		freq+=372#396
		self.odometer=appear#quando aparece no jogo
		self.vel=vel#velocidade dos carros na travessa
		self.frequency=freq#frequencia dos carros(tempo de criacao)
		self.freq_scale=freq/180
		self.direction=direction#-1=esquerda 0=faixa dupla +1=direita
		
		self.time=time#tempo de farol vermelho
		#self.dy=0
		self.setZero()
	def setZero(self):
		self.crosswalk_rect=pygame.Rect(0,0,0,0)
		self.street_rect=pygame.Rect(0,0,0,0)
		self.turned_on=random.randrange(100)<40 #False se o farol esta vermelho
		print self.turned_on
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
				image=pygame.transform.flip(random.choice(car_images),True,False)
				self.car_list[0].append(carObject(10-image.get_width(),self.vel,image,new_freq))
			if self.direction<+1:# -1 or 0
				image=random.choice(car_images)
				self.car_list[1].append(carObject(640,-self.vel,image,new_freq))
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
		return self.crosswalk_rect if self.turned_on else None#pygame.Rect(0,0,0,0)
	def blitOn(self,final_display,listed_display,player,pause,gps,game_timer):
		global asphalt_img,traffic_img,light_img
		global car_images,truck_images
		auto_images=car_images+(truck_images if gps else [])
		if self.timer_start:
			self.next_time=pygame.time.get_ticks()-game_timer+self.time
			#pygame.time.set_timer(USEREVENT+2,self.time)
			self.turned_on=self.turnOnOff(self.turned_on)
			self.timer_start=False
		pos=(0,player.odometer-self.odometer)
		y=getViewport45(400,(255*11)-(pos[1]*2),150)#y faixa1
		
		h=getViewport45(400,(255*12)-(pos[1]*2),150)#y faixa1 + h faixa1
		h_2=getViewport45(400,(255*15)-(pos[1]*2),150)#y faixa1 + h rua(2)
		h_3=getViewport45(400,(255*20)-(pos[1]*2),150)#y faixa1 + h faixa2(3)
		
		rect_0=pygame.Rect(pos[0],360-y,640,h-y)#faixa 1
		rect_1=pygame.Rect(pos[0],rect_0.y+rect_0.h,640,h_2-y)#rua
		rect_2=pygame.Rect(pos[0],rect_1.y+rect_1.h,640,h_3-y)#faixa 2
		self.crosswalk_rect=rect_0.union(rect_2)
		self.street_rect=pygame.Rect(rect_1)
		if not self.player_infraction and self.turned_on and rect_1.colliderect(player.hit_box):
			self.player_infraction=True
		#1º ciclo foreach, mas só repete duas vezes
		new_freq=self.freq_scale*rect_1.h
		for d in range(2):
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
					remove=car.moveCar()#self.frequency*rect_1.y/720)
					car.collideCar(player)
				car.blitCar(listed_display,car_y,rect_1.h)
				if not pause and remove: self.car_list[d].remove(car)#;print 'removed'+str(len(self.car_list[d]))
			if len(self.car_list[d])>0 and self.turned_on:
				if abs(self.car_list[d][-1].move)>new_freq:#self.frequency*(1+(rect_1.y/36)):
					image=pygame.transform.flip(random.choice(auto_images),d==0,False)
					self.car_list[d].append(carObject(-image.get_width() if d==0 else 640, -self.vel*((d*2)-1), image  ,new_freq))
					#self.car_list[d].append(carObject(self.car_list[d][-1].rect.x+(self.frequency*((d*2)-1)), self.car_list[d][-1].vel, image  ))
				
		if self.direction==0:
			rect_2.y+=rect_1.h*0.5
			rect_1.h*=1.5
		final_display.blit(pygame.transform.scale(down_arrow,((315-249)+((rect_0.y-int(rect_0.h/1.5))/4),int(rect_0.h/1.5))),(249-((rect_0.y-int(rect_0.h/1.5))/4),rect_0.y-int(rect_0.h/1.5)) )
		final_display.blit(pygame.transform.scale(up_arrow,((395-327)+((rect_2.y+(rect_2.h*2))/4),(rect_2.h*2))),(327,rect_2.y+rect_2.h) )
		#faixa de pedestre 1
		if rect_0.y<=360:
			final_display.blit(traffic_img.subsurface(pygame.Rect(rect_0.x,rect_0.y,rect_0.w,360-rect_0.y) if rect_0.h+rect_0.y>360 else rect_0),(rect_0.x-1,rect_0.y))

		#rua, asfalto
		final_display.blit(pygame.transform.scale(asphalt_img,rect_1.size),rect_1.topleft)

		#faixa de pedestre 2
		if rect_2.y<=360:
			final_display.blit(traffic_img.subsurface(pygame.Rect(rect_2.x,rect_2.y,rect_2.w,360-rect_2.y) if rect_2.h+rect_2.y>360 else rect_2),(rect_2.x-1,rect_2.y))
		
		w_lt=light_img.get_width()/3
		h_lt=light_img.get_height()
		#poste da esquerda (costas)
		crop_rect=pygame.Rect(w_lt*2,0,w_lt,h_lt)
		listed_display.blit(light_img.subsurface(crop_rect),(120-((rect_0.y-h_lt)//4),(rect_0.y-h_lt)))
		#poste da direita (frente)
		crop_rect.x=w_lt*int(not self.turned_on)
		global light_scale
		listed_display.blit(light_img.subsurface(crop_rect),(460+((rect_2.h+rect_2.y-h_lt)//4),(rect_2.h+rect_2.y-h_lt)))
		
		self.running=True
		return 0
		

'''
class trafficLightOld(object):
	def __init__(self,time,direction,vel,freq,appear):
		self.odometer=appear#quando aparece no jogo
		self.vel=vel#velocidade dos carros na travessa
		self.frequency=freq#frequencia dos carros(tempo de criacao)
		self.direction=direction#-1=esquerda 0=faixa dupla +1=direita
		self.time=time#tempo de farol vermelho
		#self.dy=0
		self.setZero()
	def setZero(self):
		self.car_stop=10
		self.car_pos=0
		self.turned_on=False#True se o farol esta verde
		self.timer_start=True#inicia o timer na primeira passada do codigo
		self.street=False
		self.crosswalk=False
		self.boolean=False
	def eventControler(self,event,resize,move):
		if self.turned_on:
			pygame.time.set_timer(USEREVENT+2,0)
			self.turned_on = False
	def blitOn(self,real_display,display,player,bikers,traffic_img,car_img,light_img, pause_game,asphalt_img):
		if self.timer_start:
			pygame.time.set_timer(USEREVENT+2,self.time) #liga o timer
			self.turned_on=True #liga o semaforo
			self.timer_start=False
		#global traffic_img
		pos=(0,player.odometer-self.odometer)
		y=getViewport45(400,(255*11)-(pos[1]*2),150)#y faixa1
		
		h=getViewport45(400,(255*12)-(pos[1]*2),150)#y faixa1 + h faixa1
		h_2=getViewport45(400,(255*15)-(pos[1]*2),150)#y faixa1 + h rua(2)
		h_3=getViewport45(400,(255*20)-(pos[1]*2),150)#y faixa1 + h faixa2(3)
		
		rect_0=pygame.Rect(pos[0],360-y,640,h-y)#faixa 1
		rect_1=pygame.Rect(pos[0],rect_0.y+rect_0.h,640,h_2-y)#rua
		rect_2=pygame.Rect(pos[0],rect_1.y+rect_1.h,640,h_3-y)#faixa 2
		if self.direction==0:
			rect_2.y+=rect_1.h*0.5
			rect_1.h*=1.5
		#faixa de pedestre 1
		
		try:
			if rect_0.y<=360:real_display.blit(traffic_img.subsurface(pygame.Rect(rect_0.x,rect_0.y,rect_0.w,360-rect_0.y) if rect_0.h+rect_0.y>360 else rect_0),(rect_0.x,rect_0.y))
	
			#rua, asfalto
			#display.fill((50,50,50),rect_1)
			real_display.blit(pygame.transform.scale(asphalt_img,(rect_1.w,rect_1.h)),(rect_1.x,rect_1.y))
	
			#faixa de pedestre 2
			if rect_2.y<=360:real_display.blit(traffic_img.subsurface(pygame.Rect(rect_2.x,rect_2.y,rect_2.w,360-rect_2.y) if rect_2.h+rect_2.y>360 else rect_2),(rect_2.x,rect_2.y))
		except Exception,e:print e;print rect_0; print rect_2
		
		
		#global light_img
		
		sprite_sheet=0 if self.turned_on else 1
		
		w_lt=light_img.get_width()/3
		h_lt=light_img.get_height()
		
		#rect que define a parea de colisao do player
		player_hit_box=player.img.get_rect(x=player.pos[0],y=player.pos[1])
		#diminui pela metade a caixa de colisao do player (perspectiva)
		player_hit_box.y+=player_hit_box.h/3
		player_hit_box.h-=player_hit_box.h*2/3
		
		#poste da esquerda (costas)
		crop_rect=pygame.Rect(w_lt*2,0,w_lt,h_lt)
		display.blit(light_img.subsurface(crop_rect),(120-((rect_0.y-h_lt)//4),(rect_0.y-h_lt)))
		
		car_h=rect_1.h #if self.direction==0 else rect_1.h
			
		#global car_img
		car_scale=(car_h/float(car_img.get_height()))
		car_w=int(car_img.get_width()*car_scale)
		new_car_img=pygame.transform.scale(car_img,(car_w,car_h))
		#new_car_img2=pygame.Surface(new_car_img.get_size() )
		#carros na pista
		car_qnt=self.car_stop
		#print self.car_pos+self.frequency*car_qnt
		##
		if self.car_pos>640+(car_w+self.frequency)*(car_qnt-1):
			self.boolean=True
		if not self.boolean:
			if self.direction<+1:
				for car in range(car_qnt):
					carro_0=pygame.Rect(640-self.car_pos+(car_w+self.frequency)*car-car_w,-car_h+rect_1.y+rect_1.h/2 if self.direction==0 else -car_h+rect_1.y+(rect_1.h*3/4),car_w,car_h)
					#carro_0=pygame.Rect(640-self.car_pos+(car_w+self.frequency)*car-car_w,-car_h+rect_1.y+rect_1.h/2 if self.direction==0 else -car_h+rect_1.y+(rect_1.h*3/4),car_w,car_h)
					#display.fill((255,255,255),carro_0)
					#new_car_img2.fill((0,0,0))
					#new_car_img2.blit(new_car_img,(0,0))
					#new_car_img2.blit(dinB_22.render(str(car),False,(255,0,0)),(0,0))
					display.blit(new_car_img,(carro_0.x,carro_0.y))
					if not pause_game and player_hit_box.colliderect(carro_0): player.receiveDamage(1,(-10,0))
					if not self.turned_on and carro_0.x>640-car_w and self.car_stop==10: self.car_stop=car
			if self.direction>-1:
				for car in range(car_qnt):
					carro_1=pygame.Rect(-100+self.car_pos-(car_w+self.frequency)*car+car_w,rect_1.y+rect_1.h-car_h if self.direction==0 else -car_h+rect_1.y+(rect_1.h*3/4),car_w,car_h)
					#display.fill((255,255,255),carro_1)
					#new_car_img2.fill((0,0,0))
					#new_car_img2.blit(new_car_img,(0,0))
					#new_car_img2.blit(dinB_22.render(str(car),False,(255,0,0)),(0,0))
					display.blit(pygame.transform.flip(new_car_img,True,False),(carro_1.x,carro_1.y))
					if not pause_game and player_hit_box.colliderect(carro_1): player.receiveDamage(1,(+10,0))
					if not self.turned_on and carro_1.x<0 and self.car_stop==10: self.car_stop=car
	
			if not pause_game and self.car_pos<=640+(car_w+self.frequency)*car+car_w:self.car_pos+=self.vel#if self.turned_on: self.car_pos+=10
#			if not self.turned_on: #else: self.car_pos=100
#				if self.direction<+1: display.blit(new_car_img,(640-car_w,carro_0.y))
#				if self.direction>-1: display.blit(pygame.transform.flip(new_car_img,True,False),(0,carro_1.y))
#			else: 
			if self.turned_on:
				if self.car_pos>=640+car_w+self.frequency: self.car_pos-=car_w+self.frequency
		
		
		
		#poste da direita (frente)
		crop_rect.x=w_lt*sprite_sheet
		display.blit(light_img.subsurface(crop_rect),(460+((rect_2.h+rect_2.y-h_lt)//4),(rect_2.h+rect_2.y-h_lt)))
		
		tf_score_return=0
		if self.turned_on:
			#tratamentos no score (infracoes)
			if player_hit_box.colliderect(rect_1) and self.street==False:
				tf_score_return+=200#self.score-=200
				self.street=True
			if player_hit_box.colliderect(rect_2) and self.crosswalk==False:
				tf_score_return+=25#self.score-=25
				self.crosswalk=True
			#parar NPCs antes da faixa
			for bike in bikers:
				if bike.odometer<=player.odometer and bike.pos[1]<=360:
					if bike.pos[1]>rect_0.y-bike.img.get_height():
						if bike.accel>0: 
							bike.stop=True
							bike.vel=0
					if bike.pos[1]<rect_2.y+rect_2.h: 
						if bike.accel<0: 
							bike.stop=True
							bike.vel=0
				if bike.stop:
					if bike.accel<0: bike.pos[1]=rect_2.y+rect_2.h
					else: bike.pos[1]=rect_0.y-bike.img.get_height()
		else:
			#mover NPCs que foram parados
			for bike in bikers:
				if bike.odometer<=player.odometer and bike.pos[1]<=360:
					if bike.stop: bike.stop=False
		return tf_score_return
'''
