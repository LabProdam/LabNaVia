# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os
from popUp import *
from trafficLight import getViewport45
from screenTools import blitAlpha
from bikerObject import playerObject

#diretorios
dir_font='fontes'+str(os.sep)
dir_img='images'+str(os.sep)
#fontes
arial_12=pygame.font.SysFont('arial',12)
dinB_22=pygame.font.Font(dir_font+"DIN-Black.otf",22)
dinB_16=pygame.font.Font(dir_font+"DIN-Black.otf",16)
dinB_72=pygame.font.Font(dir_font+"DIN-Black.otf",72)
dinBd_32=pygame.font.Font(dir_font+"DIN-Bold.otf",32)
dinL_16=pygame.font.Font(dir_font+"DIN-Light.otf",16)
#imagens
odometer_img = pygame.image.load(dir_img+"odometer.png").convert_alpha()
pointer_img  = pygame.image.load(dir_img+"pointer.png").convert_alpha()
traffic_img  = pygame.image.load(dir_img+"faixas.png").convert_alpha()
light_img    = pygame.image.load(dir_img+"semaforo.png").convert_alpha()
car_img      = pygame.image.load(dir_img+"newcar.png").convert_alpha()
grass_img    = pygame.image.load(dir_img+'gramaFeia2.png').convert()
track_img    = pygame.image.load(dir_img+'pista3.png').convert_alpha()
#panelesq_img= pygame.image.load(dir_img+'painelesq.png').convert_alpha()
#paneldir_img= pygame.image.load(dir_img+'paineldir.png').convert_alpha()
panel_img   = pygame.image.load(dir_img+'painelDuplo.png').convert_alpha()
#star_img     =[pygame.image.load(dir_img+'estrelaMolde.png').convert_alpha(),
#			   pygame.image.load(dir_img+'estrelaCor.png').convert_alpha()]
#cap_img = [pygame.image.load(dir_img+"capcontorno.png").convert_alpha(),
#			pygame.image.load(dir_img+"cappreenchido.png").convert_alpha()]
cap_img = [pygame.image.load(dir_img+"pequenoCapContorno.png").convert_alpha(),
			pygame.image.load(dir_img+"pequenoCap.png").convert_alpha()]
#heart_img    = pygame.image.load(dir_img+'coracao1.png').convert_alpha()
tutorial_img = pygame.image.load(dir_img+'tutorial.png').convert_alpha()
tutorial_img = pygame.transform.smoothscale(tutorial_img,(int(tutorial_img.get_width()/2.5),int(tutorial_img.get_height()/2.5)) )
end_img      = pygame.image.load(dir_img+'faixa.png').convert()
pop_bar_score = pygame.image.load(dir_img+"popBar1.png").convert_alpha()
#####################################3

level_img     = [pygame.image.load(dir_img+"corLv1.png").convert_alpha(),
				pygame.image.load(dir_img+"corLv2.png").convert_alpha(),
				pygame.image.load(dir_img+"corLv3.png").convert_alpha(),
				pygame.image.load(dir_img+"corLv4.png").convert_alpha(),
				pygame.image.load(dir_img+"corLv5.png").convert_alpha()]
				
cores  	      =	[(149,34,48),(176,4,24),(200,21,42),(210,2,27),(255,4,33)]	
		
bar_level=[pygame.image.load(dir_img+"levelBar.png").convert_alpha(),
		pygame.image.load(dir_img+"levelBarTransparency.png").convert_alpha()]
bar_level2=[pygame.image.load(dir_img+"levelBarPreenchido.png").convert_alpha(),
		pygame.image.load(dir_img+"levelBarContorno.png").convert_alpha()]

#objetos interandos do jogo
class gameObject(object):
	def __init__(self,end_pos,player,biker_list,traffic_list,sign_img,scr_lose,scr_win,retry_button,home_button,pause_button,resume_button,pause_scr):
		#ciclista jogador 
		self.player=player#vel*3.6
		self.end_pos=end_pos
		#lista de ciclistas transeuntes
		self.bikers=biker_list
		self.sign_img=sign_img
		
		self.home_button=home_button
		self.retry_button=retry_button
		self.pause_button=pause_button
		self.resume_button=resume_button
		
		self.loser_screen=scr_lose
		self.winner_screen=scr_win
		pygame.time.set_timer(USEREVENT+1,300)
		
		####---itens em desenvolvimento---####
		self.traffic_light=traffic_list#[trafficLight(9000,0,5,300,1500),trafficLight(5000,1,15,100,3500),trafficLight(9000,-1,5,300,5500)]
		surf=pygame.Surface((400,30))
		surf.fill((0,0,0))
		self.pop_up=popUp((0,360),(30,330),(1,-1),pop_bar_score,(5,2))
		self.pause_tgscr=pause_scr
		self.setZero()
		
	def setZero(self):
		#pontuacao incial do jogador
		self.i = 0
		self.score = 100
		self.left_ride_score=0
		self.collision_counter=0
		self.traffic_score=0
		self.start_time=0
		self.lose=False #quando colidir
		self.win=False #quando o array de ciclistas terminar
		self.dy_faixas=0
		self.grass_pos=0
		self.sign_pos=100
		self.sign_pointer=0
		self.popup_bool=[True,True,True]
		#variavel que define o movimento de pedal
		self.bool=[False,False,False]#K_RIGHT,K_LEFT
		self.alpha=0
		self.pause_tgscr.turned_on=False
		self.pause_game=False
		self.start_time+=pygame.time.get_ticks()
	def setAllZero(self):
		self.player.setZero()
		for bike in self.bikers:
			bike.setZero()
		for trlt in self.traffic_light:
			trlt.setZero()
		self.pop_up.setZero()
		self.setZero()
		self.loser_screen.turnOn(False)
		self.winner_screen.turnOn(False)
	def preEvents(self):
		for home in self.home_button: home.function = self.setAllZero
		for retry in self.retry_button: retry.function = self.setAllZero
		self.start_time+=pygame.time.get_ticks()

	def posEvents(self):
		self.start_time-=pygame.time.get_ticks()
	#controle dos eventos
	def eventControler(self, event,resize,move):
		if self.pause_game==False:
			self.runEventControler(event, resize,move)
	def runEventControler(self, event, resize,move):
		if event.type==MOUSEBUTTONUP:
			mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
			if pygame.Rect(0,160,320,200).collidepoint(mouse_pos):
				self.bool=[False,False]# nao eh mais separado o [0] e [1] pois ao clicar e arrastar para o outro lado deixava o primeiro verdadeiro como se continuasse clicando
				self.player.playerAccel(-1)
			if pygame.Rect(320,160,320,200).collidepoint(mouse_pos):
				self.bool=[False,False]#self.bool[0]=False
				self.player.playerAccel(+1)
		if event.type==MOUSEBUTTONDOWN:
			mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
			if pygame.Rect(0,160,320,200).collidepoint(mouse_pos): self.bool[1]=True
			if pygame.Rect(320,160,320,200).collidepoint(mouse_pos): self.bool[0]=True
		if event.type==KEYUP:
			if event.key==K_RIGHT: 
				self.bool[0]=False
				self.player.playerAccel(+1)#aceleracao esquerda
			if event.key==K_LEFT: 
				self.bool[1]=False
				self.player.playerAccel(-1)#aceleracao direita
			if event.key==K_DOWN: 
				self.player.desaccel=1
			if event.key==K_d:
				self.player.playerAccel(+1)#aceleracao do player para a esquerda --- guidao
			elif event.key==K_a:
				self.player.playerAccel(-1)#aceleracao do player para a direita ---- guidao

		if event.type==KEYDOWN:
			if event.key==K_RIGHT: self.bool[0]=True
			if event.key==K_LEFT: self.bool[1]=True
			if event.key==K_DOWN: self.player.desaccel=4 ################################################### <<<<<<----------- mude o valor para mudar o quanto desacelera
		if event.type==USEREVENT+1:
			for bike in self.bikers:
				if bike.odometer<=self.player.odometer and bike.pos[1]<=360+bike.img.get_height():
					if not bike.stop: bike.flip=not bike.flip
		if event.type==USEREVENT+2:
			for trlt in self.traffic_light:
				if trlt.turned_on:
					trlt.turned_on=False #desliga o semaforo
					pygame.time.set_timer(USEREVENT+2,0) #desliga o timer
		self.player.eventControler(event,resize)
		self.pop_up.eventControler(event, resize,move)
	def screenCall(self):#return self.loser_screen if self.lose else self.winner_screen if self.win else None
		'''if self.pause_button.actived:
			global pause_tgscr
			pause_tgscr.turned_on=True
			self.pause_button.actived=False'''
		#global pause_tgscr
		if self.pause_tgscr.turned_on:
			self.alpha=200
			self.color=(120,120,150)
			if not self.pause_game: self.start_time-=pygame.time.get_ticks()
			self.pause_game=True
		else:
			self.alpha=0
			if not self.pause_tgscr.moving:
				if self.pause_game: self.start_time+=pygame.time.get_ticks()
				self.pause_game=False
		if self.lose:
			self.alpha=200
			self.color=(255,0,0)
			self.loser_screen.turnOn()
			self.lose=False
			self.pause_game=True
		if self.win:
			self.alpha=200
			self.color=(0,255,0)
			self.winner_screen.turnOn()
			self.win=False
			self.pause_game=True
		return None#self.loser_screen if self.lose else self.winner_screen if self.win else None
	
#manipulacao dos elementos HUD da tela #####################################################
	def blitPanel(self,display,pos):
		global panel_img
		display.blit(panel_img,pos)
		#display.blit(paneldir_img,(pos[0]+2,pos[1]))
		#display.blit(panelesq_img,(638-panelesq_img.get_width(),0))
	
	def blitTimer(self,display,pos):
		global dinL_16, dinB_22
		tempo=(pygame.time.get_ticks()-self.start_time)
		resto_tempo=tempo%60000
		fonte_timer=dinB_22
		recuo=fonte_timer.size('00 : ')[0]
		if (tempo - resto_tempo)/60000>9:
			display.blit(fonte_timer.render( str((tempo - resto_tempo)/60000)+' : ',True,(0,0,0)),(pos[0],pos[1]))
		else:
			display.blit(fonte_timer.render( '0'+str((tempo - resto_tempo)/60000)+' : ',True,(0,0,0)),(pos[0],pos[1]))
		if (resto_tempo - (resto_tempo%1000) )/1000>9:
			display.blit(fonte_timer.render( str( (resto_tempo - (resto_tempo%1000) )/1000),True,(0,0,0)),(pos[0]+recuo,pos[1]))
		else:
			display.blit(fonte_timer.render( '0'+str( (resto_tempo - (resto_tempo%1000) )/1000),True,(0,0,0)),(pos[0]+recuo,pos[1]))
		#display.blit(fonte_timer.render( str(resto_tempo%100),True,(0,0,0)),(140-fonte_timer.size(str(resto_tempo%100))[0],0))
		
	def blitSpeed(self,display,pos):
		global dinB_16,dinB_22,dinBd_32
		display.blit(dinBd_32.render(str(int(self.player.vel*3.6)),True,(0,0,0)),(pos[0]-dinBd_32.size(str(int(self.player.vel*3.6)))[0],pos[1]))
		display.blit(dinB_22.render('km/h',True,(0,0,0)),(pos[0],pos[1]+10))
		
	def blitTrack(self,display,pos):
		global dinL_16, odometer_img,pointer_img
		#display.blit(dinB_16.render(str(round((self.player.odometer/30),1))+' m',True,(200,200,0)),(pos[0]-dinB_16.size(str(round((self.player.odometer/30),1))+' km')[0],pos[1]))
		#display.blit(dinB_16.render('de '+str(self.end_pos/30)+' m',True,(155,0,0)),(pos[0]-58,pos[1]+22))
		display.blit(odometer_img,pos)
		display.blit(pointer_img,(pos[0]+(odometer_img.get_width()*(self.player.odometer/self.end_pos))-(pointer_img.get_width()//2),pos[1]-pointer_img.get_height()+odometer_img.get_height()))
		if self.end_pos<30000:
			#display.blit(dinL_16.render(str(self.end_pos/30)+"m",True,(0,0,0)),(20+odometer_img.get_width(),pointer_img.get_height()-10))
			display.blit(dinL_16.render(str(self.end_pos/30)+"m",True,(0,0,0)),(odometer_img.get_width()/2,pos[1]+odometer_img.get_height()))
		else:
			display.blit(dinL_16.render(str(self.end_pos/30000)+"km",True,(0,0,0)),(30+odometer_img.get_width(),pointer_img.get_height()))
	def blitLife(self,display,pos):
		global cap_img
		#display.blit(pygame.transform.chop(star_img[1],pygame.Rect(0,0,star_img[1].get_width()*self.player.damage/self.player.maxlife,0)),(pos[0]+star_img[1].get_width()*self.player.damage/self.player.maxlife,pos[1]))
		#display.blit(star_img[0],pos)
	
		#display.blit(pygame.transform.chop(cap_img[1],pygame.Rect(0,0,cap_img[1].get_width()*self.player.damage/self.player.maxlife,0)),(pos[0]+cap_img[1].get_width()*self.player.damage/self.player.maxlife,pos[1]))
		display.blit(pygame.transform.chop(cap_img[1],pygame.Rect(0,0,0,cap_img[1].get_height()*self.player.damage/self.player.maxlife)),(pos[0],pos[1]+cap_img[1].get_height()*self.player.damage/self.player.maxlife))
		display.blit(cap_img[0],pos)
		
	'''def blitHeart(self,display,pos):
		global heart_img
		heart=pygame.Surface(heart_img.get_size())
		health=self.player.odometer/self.end_pos
		#health=(health*105)+150 if self.player.odometer//250%2==0 else (health*155)+50
		heart.blit(display,(-pos[0],-pos[1]))
		heart.fill((255,30,50),pygame.Rect(0,heart_img.get_height()-(heart_img.get_height()*health),heart_img.get_width(),(heart_img.get_height()*health)))
		heart.set_colorkey((100,255,0))
		heart.blit(heart_img,(0,0))
		display.blit(heart,pos)'''
	
	def blitExp(self,display,pos):
		global dinB_22, bar_level, level_img, dinL_16, cores, bar_level2
		meters_score=0
		xpMax=[300,500,700,900,1100]
		xpFull=False

		# a cada terco do caminho completo, o jogador tera uma pontuacao para o caminho percorrido diferente
		if self.player.odometer > self.end_pos/3:
			meters_score=200
			if self.popup_bool[0]:
				self.pop_up.callPopup(dinB_22.render(' 1/3 completo da pista ++PONTOS!!',True, (47,240,67)),1000)
				self.popup_bool[0]=False
			
		if self.player.odometer > self.end_pos/1.5:
			meters_score=400
			if self.popup_bool[1]:
				self.pop_up.callPopup(dinB_22.render('2/3 da pista completos ++PONTOS!!',True, (47,240,67)),1000)
				self.popup_bool[1]=False
			
		if self.player.odometer > self.end_pos/1-50:
			meters_score=600
			if self.popup_bool[2]:
				self.pop_up.callPopup(dinB_22.render('Voce terminou ++PONTOS!!',True, (47,250,67)),1000) 
				self.popup_bool[2]=False
		
		if self.score < -30:
			self.resetScore()
			print "score resetado: "+str(self.score)

		
		if self.score > xpMax[self.i]:
			self.i+=1
			xpFull = True
			self.player.updateLevel(self.i)
			print 'xpMax = '+ str(xpMax[self.i])

		current_level=self.player.getCurrentLevel()
		self.i=current_level

		#calculo score geral
		self.score=meters_score+(self.biker_counter*100-(self.collision_counter*110))-self.left_ride_score-self.traffic_score


		#score necessário para próximo nível
	
		text=str(int(self.score))+str(xpMax[self.i])+'/'
		lenText=dinL_16.size(text)
		'''
		#FLIPAGEm
		temp=pygame.Surface(bar_level[0].get_size())
		temp.blit(dinL_16.render('text',True,(0,0,0)),(0,0))
		flipado=pygame.transform.flip(temp,True,False)
		display.blit(flipado,(200,200))
		'''
		#DEITADA
		#barra interna de level
		#display.blit(pygame.transform.chop(bar_level[0],pygame.Rect(bar_level[0].get_width()*int(self.score)/(xpMax[self.i]),0,bar_level[0].get_width(),0)),(pos[0],pos[1]))
		#score/xpMax
		#display.blit(dinL_16.render(str(int(self.score))+'/'+str(xpMax[self.i]),True,(0,0,0)),((pos[0]+(bar_level[0].get_width()/2)),pos[1]+bar_level[0].get_height()/2+lenText/2))
		#preenchimento
		#display.blit(pygame.transform.chop(bar_level2[0],pygame.Rect(0,bar_level[0].get_width()*int(self.score)/(xpMax[self.i]),0,bar_level2[0].get_height())),(pos[0],pos[1]))

		
		#DE Pe
		#preenchimento
		display.blit(pygame.transform.chop(bar_level2[0],pygame.Rect(0,bar_level2[0].get_width()*int(self.score)/(xpMax[self.i]),0,bar_level2[0].get_height())),(pos[0],pos[1]))
		#score/xpMax
		display.blit(dinL_16.render(str(int(self.score))+'/'+str(xpMax[self.i]),True,(0,0,0)),((pos[0]+(bar_level2[0].get_width()/2-lenText[0]/2)),pos[1]-15))
		#contorno da barra de level
		display.blit(bar_level2[1],(pos[0],pos[1]))
		
		#blit teste
		#display.blit(dinB_22.render('covMeters:'+str(meters_score),True,(0,0,0)),(30,120))
		#display.blit(dinB_22.render('bkCounter'+str(self.biker_counter),True,(0,0,0)),(30,140))
		#display.blit(dinB_22.render('colCOunter'+str(self.collision_counter),True,(0,0,0)),(30,160))
		#display.blit(dinB_22.render('Stun'+str(self.player.stun_counter),True,(0,0,0)),(30,180))
		#display.blit(dinB_22.render('Pontos: '+str(int(self.score)),True, (0,0,0)),(30,100))
		
	def blitLevel(self,display,pos):
		#imagem do level(coracao)
		display.blit(level_img[self.i],(pos[0],pos[1]))
		#escrita do level
		#text2=str(self.i)+'Lv '
		text2=str(self.i)
		lenText2=dinL_16.size(text2)
		#display.blit(dinL_16.render('Lv '+str(self.i),True,cores[self.i]),(pos[0]+level_img[self.i].get_width()+2,pos[1]))
		display.blit(dinL_16.render(str(self.i),True,cores[self.i]),(pos[0],pos[1]+level_img[self.i].get_height()/2))
		
	
	def resetScore(self):
		self.biker_counter=0
		self.collision_counter=0
		self.left_ride_score=0
		self.traffic_score=0
		self.meters_score=0
		print 'colisao '+str(self.collision_counter)
		
############################################################################################

	#desenho dos elementos na tela	
	def blitOn(self, display):
		global grass_img,track_img,end_img#,tutorial_img
		global dinB_22
		if not self.pause_game:
			if self.bool[0]==True:#K_RIGHT
				self.player.pos[0]+=self.player.vel//2
			if self.bool[1]==True:#K_LEFT
				self.player.pos[0]-=self.player.vel//2
			self.player.playerMotion()
			#Penalidade por ficar na faixa esquerda
			if self.player.pos[0]<300 and self.player.pos[0]>150 and self.score>0:				
				self.left_ride_score+=0.03#self.score-=1.03
			self.grass_pos+=self.player.vel
			self.dy_faixas-=self.player.vel*2

		if self.grass_pos>=grass_img.get_height(): self.grass_pos=0
		display.blit(grass_img,(((grass_img.get_height()+self.grass_pos)//4),self.grass_pos ))
		display.blit(grass_img,((self.grass_pos//4),self.grass_pos-grass_img.get_height()))
		display.blit(grass_img,(-100+(-(grass_img.get_height()+self.grass_pos)//4)-grass_img.get_width()*0.25,self.grass_pos ))
		display.blit(grass_img,(-100+(-self.grass_pos//4)-grass_img.get_width()*0.25,self.grass_pos-grass_img.get_height()))
		
		display.blit(track_img,(0,0))

		#calculo com o viewport para represetar a perspectiva na tela
		limite=450
		if self.dy_faixas<=-limite:self.dy_faixas+=limite+50
		for i in range(1,16,2):
			y=getViewport45(400,(255*i)+self.dy_faixas+100,150)
			h=getViewport45(400,(255*(i+1))+self.dy_faixas+100,150)
			display.fill((212,7,21),pygame.Rect(310,360-y,40,h-y))

		for trlt in self.traffic_light:
			if trlt.odometer<=self.player.odometer and self.player.odometer-trlt.odometer<=1377:
				global traffic_img, car_img, light_img
				self.traffic_score+=trlt.blitOn(display,self.player,self.bikers,traffic_img, car_img, light_img, self.pause_game)
				

		if self.sign_pos<=self.player.odometer:
			if self.player.odometer-self.sign_pos-self.sign_img[self.sign_pointer].get_height()<=1377:
				sign_pos_vp=360-getViewport45(400,(255*11)-(self.player.odometer-self.sign_pos)*2,150)
				
				display.blit(self.sign_img[self.sign_pointer],(120-sign_pos_vp/4,sign_pos_vp-self.sign_img[self.sign_pointer].get_height()))
				#display.blit(self.sign_img,(420+(self.player.odometer-self.sign_pos)/4,self.player.odometer-self.sign_pos-self.sign_img.get_height()))
			else: 
				self.sign_pos+=1377
				self.sign_pointer+=1
				if len(self.sign_img)<=self.sign_pointer: self.sign_pointer=0
		if self.end_pos-360-100<=self.player.odometer:
			for i in range(7): display.blit(end_img,(end_img.get_width()*i,self.player.odometer-self.end_pos+360))
			#display.fill((0,0,0),pygame.Rect(0,self.player.odometer-self.end_pos+360, 640, 50))
		
		#verifica os eventos de colisao com cada ciclista transeunte
		
		self.biker_counter=0# biker_counter=0
		for bike in self.bikers:
			if bike.odometer<=self.player.odometer: 
				if bike.pos[1]<=360:#+bike.img.get_height():
					try:
						fliped_bike=pygame.transform.flip(bike.img,bike.flip,False)
						scale=(bike.pos[1]+(bike.img.get_height())*1.5)/360  #if bike.pos[1]<self.player.pos[1] else 1
						new_size=(int(bike.img.get_width()*scale),int(bike.img.get_height()*scale))
						scaled_bike=pygame.transform.smoothscale( fliped_bike ,new_size)
						if bike.pos[0]<300:
							new_pos=( bike.pos[0]+ bike.img.get_width()-new_size[0] , bike.pos[1]+((bike.img.get_height()-new_size[1])//2))
						else:
							new_pos=( bike.pos[0], bike.pos[1]+((bike.img.get_height()-new_size[1])//2))
						bike_hit_box_x=pygame.Rect(bike.pos[0],new_pos[1]+int(new_size[1]*0.2),bike.img.get_width(),int(new_size[1]*0.6))#horizontal
						bike_hit_box_y=pygame.Rect(int(new_pos[0]+new_size[0]*0.2),new_pos[1],int(bike.img.get_width()*0.6),new_size[1])#vertical
						player_hit_box=self.player.img.get_rect(x=self.player.pos[0],y=self.player.pos[1])
					except: print 'erro antes do hitbox'
					#colisao horizontal
					if bike_hit_box_x.colliderect(player_hit_box):
						if self.player.pos[0]>new_pos[0]+(new_size[0]//2):self.player.receiveDamage(1,(+20,0))
						else:self.player.receiveDamage(1,(-20,0))
						#self.collision_counter+=1
					#colisao vertical
					if bike_hit_box_y.colliderect(player_hit_box) and new_pos[1]<360:
						if self.player.stun_counter==0: 
							if bike.vel>0: bike.vel=-100*self.player.accel*bike.accel
							self.player.receiveDamage(1,(0,-20))
							self.player.vel=0
							self.collision_counter+=1
							#if self.score > 0: self.score-=175
							#if self.score<0: self.score=0
					if not self.pause_game and not bike.stop: bike.passerbyMotion(self.player.vel)
					display.blit(scaled_bike ,new_pos )
				#pontuacao para ultrapassagem
				else:
					self.biker_counter+=1# biker_counter+=1
					'''
					if bike.pos[1]<460: Contratar pessoas carecas, assim não teria mais cabelos na comida.
						self.score+=100
						bike.pos[1]=460
					'''
		
		#condicao vitoria e derrota
		if self.end_pos<=self.player.odometer:#if biker_counter==len(self.bikers):
			self.win=True
		if self.player.damage>=self.player.maxlife: 
			self.lose=True
		self.player.blitOn(display)

		#informacoes na tela
		if not self.pause_game:
			#painel fundo
			self.blitPanel(display,(0,0))
			#timer
			self.blitTimer(display,(15,50+odometer_img.get_height()))
			#speedometer
			#self.blitSpeed(display,((odometer_img.get_width()//2),40))
			#track
			self.blitTrack(display,(15,25))
			#score
			self.blitExp(display,(600,110))#display.blit(dinB_22.render('Pontos: '+str(int(self.score)),True, (0,0,0)), (30,144))
			#estrela
			self.blitLife(display,(15,105))
			#coracao level
			self.blitLevel(display,(600,90-level_img[self.i].get_height()))
			#coracao
			#self.blitHeart(display,(490,50))
			#popup
			self.pop_up.blitOn(display)
#	def blitPause(self,display):
		#self.pause_button.blitOn(display)
		esmaecer=pygame.Surface((640,360))
		esmaecer.fill(self.color)
		blitAlpha(display,esmaecer,(0,0),self.alpha)
	def notblitOn(self,display):
		if self.pause_game:
			self.blitPause(display)
		else:
			self.blitGame(display)
	def screenManipulation(self,screen):pass

class winObject(object):
	def __init__(self,player):
		self.player=player
		self.score=[('Champion',100000),
					('Champlix',10000),
					('Champlow',1000),
					('Chanklsh',100),
					('Champlum',10)]
		self.pos=len(self.score)+2
	def preEvents(self):
		for pos in len(self.score):
			if self.player.score>self.score[pos][1]:
				self.pos=pos
	def posEvents(self):
		self.pos=len(self.score)+2
	def blitOn(self,display):pass
	
	
