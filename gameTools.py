# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os,cPickle,random
from popUp import *
from trafficLight import getViewport45
from screenTools import mixer,renderList, textBox,playSound,android,rotateCenter
from geo import*

auto_gps_ingame=android
def setAutoGpsIngame(auto=True):
	global auto_gps_ingame
	auto_gps_ingame=auto
#diretorios
dir_font='fontes'+str(os.sep)
dir_img='images'+str(os.sep)
dir_menu=dir_img+'menu'+str(os.sep)
dir_obs=dir_img+'obstacles'+str(os.sep)
dir_bikers=dir_img+'bikers'+str(os.sep)
dir_music='musics'+str(os.sep)
dir_sound='sounds'+str(os.sep)
dir_data='data'+str(os.sep)
#fontes
arial_12=pygame.font.SysFont('arial',12)

chic_12=pygame.font.Font(dir_font+"ChicagoFLF.ttf",12)
chic_14=pygame.font.Font(dir_font+"ChicagoFLF.ttf",14)
chic_16=pygame.font.Font(dir_font+"ChicagoFLF.ttf",16)
chic_18=pygame.font.Font(dir_font+"ChicagoFLF.ttf",18)
chic_22=pygame.font.Font(dir_font+"ChicagoFLF.ttf",22)
chic_30=pygame.font.Font(dir_font+"ChicagoFLF.ttf",30)
chic_72=pygame.font.Font(dir_font+"ChicagoFLF.ttf",72)

dinB_22=pygame.font.Font(dir_font+"DIN-Black.otf",22)
dinB_16=pygame.font.Font(dir_font+"DIN-Black.otf",16)
dinB_12=pygame.font.Font(dir_font+"DIN-Black.otf",12)
dinB_72=pygame.font.Font(dir_font+"DIN-Black.otf",72)
dinBd_32=pygame.font.Font(dir_font+"DIN-Bold.otf",32)
dinL_16=pygame.font.Font(dir_font+"DIN-Light.otf",16)
dinL_12=pygame.font.Font(dir_font+"DIN-Light.otf",12)
dinL_10=pygame.font.Font(dir_font+"DIN-Light.otf",10)
#imagens
pointer_img  = pygame.Surface((10,10),SRCALPHA,32).convert_alpha()
pygame.draw.circle(pointer_img,(255,0,0),(5,5),5)
grass_img    = pygame.image.load(dir_img+'grama.png').convert()
track_img    = pygame.image.load(dir_img+'pista4.png').convert_alpha()
panel_img   = pygame.image.load(dir_img+'painel_menor2.png').convert_alpha()
cap_img = [pygame.image.load(dir_img+"pequenoCap"+str(x)+".png").convert_alpha() for x in xrange(2)]

end_img      = pygame.image.load(dir_img+'faixa.png').convert()
pop_bar_score = pygame.image.load(dir_img+"popBar1.png").convert_alpha()

level_img     = [pygame.image.load(dir_img+"heart"+str(x)+".png").convert_alpha()for x in xrange(2)]
				
cores  	      =	[(149,34,48),(176,4,24),(200,21,42),(210,2,27),(255,4,33)]	

asphalt_img = pygame.image.load(dir_img+"asfalto.png").convert()

culture_img = pygame.image.load(dir_img+"placaBlank.png")
culture_rect=pygame.Rect(3,8,114-3,56-8)
obs_img=[
	pygame.image.load(dir_obs+"obs"+str(x)+".png").convert_alpha() for x in xrange(3)
]
render_list=renderList()
from animatedSprite import *
dog=[pygame.image.load(dir_img+"dogAnimado.png").convert_alpha(),pygame.image.load(dir_img+"dogLatindo.png").convert_alpha()]
dog_img=[animatedSprite(dog[d],dog[d].get_rect(w=dog[d].get_width()/2),[0,0],USEREVENT+d) for d in xrange(2)]
dog_bark=mixer.Sound(dir_sound+"dogBark.mp3")

class gameObject(object):
	def __init__(self,name,end_pos,odometer,player,biker_list,traffic_list,obstacle_list,dog_list,sign_img,scr_lose,scr_win,scr_score,retry_button,home_button,stages_button,pause_button,resume_button,pause_scr,move_button,gps_item):
		global pop_bar_score,level_img
		self.name=name
		self.left_side_name=pygame.transform.rotate(chic_72.render(name,True,(255,255,255)),90)
		#ciclista jogador 
		self.player=player
		self.end_pos=end_pos
		#lista de ciclistas transeuntes
		self.odometer_img=odometer
		self.bikers=biker_list
		self.obstacles=[[obs*30,None,0,False] for obs in obstacle_list]
		self.dogs=[[dog*30,False] for dog in dog_list]
		self.sign_img=sign_img
		self.home_button=home_button
		self.retry_button=retry_button
		self.pause_button=pause_button
		self.stages_button=stages_button
		self.resume_button=resume_button
		self.move_button=move_button
		self.loser_screen=scr_lose
		self.winner_screen=scr_win
		self.score_screen=scr_score
		self.gps=gps_item
		self.traffic_light=traffic_list
		self.pop_up=popUp((0,360),(0,360-pop_bar_score.get_height()),(0,-1),pop_bar_score,(40,15))
		self.pause_tgscr=pause_scr
		self.setZero()
		self.fade=pygame.Surface((640,360))
		self.fade.set_alpha(204)
		self.color=(0,0,0)
		self.high_score=[]#NOME,1helmets,2hearts,3time,4red_trlt,5bikers_hit,6bikers_leftbehind,7things_hit,8dog,9check_points,10wrong_side,score calculado
		self.tutorial=False
		self.blit_panel=True
		self.blit_timer=True
		self.blit_track=True
		self.blit_score=True
		self.blit_life=True
		self.blit_level=True
		self.heart_pos=(5-14,188-12)
		self.unlock=None
		self.found=False
	def clearScore(self):
		try:
			score_file=open(dir_data+"score_data_"+self.name.replace(' ','_')+".lab","wb")
			score_file.truncate()
			score_file.close()
		except Exception,e:print e
		self.high_score=[]
		if self.unlock!=None:
			self.unlock.setLock()
			self.unlock.setHide()
	def loadScore(self):
		try:
			score_file=open(dir_data+"score_data_"+self.name.replace(' ','_')+".lab","rb")
			self.high_score=cPickle.load(score_file)
			if self.unlock!=None:
				self.unlock.lock=cPickle.load(score_file)
				self.unlock.hide=cPickle.load(score_file)
			score_file.close()
		except Exception,e:
			self.saveScore()
			print e
	def saveScore(self):
		score_file=open(dir_data+"score_data_"+self.name.replace(' ','_')+".lab","wb")
		try:
			cPickle.dump(self.high_score,score_file)
			if self.unlock!=None:
				cPickle.dump(self.unlock.lock,score_file)
				cPickle.dump(self.unlock.hide,score_file)
		except Exception,e:print e
		score_file.close()
	def calculateScore(self,helmets,hearts,time,red_trlt,bikers_hit,bikers_left,things_hit,dog,check_points,wrong_side):
		number_trlt=len(self.traffic_light)
		ingame_score=((number_trlt-red_trlt)*50)-(red_trlt*250)-(bikers_hit*100)+(bikers_left*100)-(things_hit*30)-(dog*100)+(check_points*100)-(wrong_side)
		time_score=1+abs(time-(self.end_pos/10)-number_trlt )
		outgame_score=((helmets*75)+(hearts*100))/time_score
		final_score=ingame_score+outgame_score
		return int(final_score)
	def printHighScore(self):
		for s,score in enumerate(self.high_score):
			print str(1+s)+') '+score[0]+': '+str(score[-1])
	def blitHighScore(self,display=None,pos=(0,0)):
		global dinL_12,dinB_12,chic_12
		font=chic_16
		colorG=(33,33,33)
		colorB=(255,255,255)
		#fonthB=dinB_12
		render_list=[]
		size=[0,0]
		for s,score in enumerate(self.high_score):
			#render=fonth.render(str(1+s)+') '+score[0]+': '+str(score[-1]),True,(0,0,0))
			color=colorG if s!=self.rank else colorB
			render=font.render('#'+str(1+s)+' : '+str(score[-1]),True,color)
			if display!=None: 
				display.blit(render,(pos[0],pos[1]+((fonth.get_height()+2)*s)))
			else:
				render_list.append(render)
				if size[0]<render.get_width():
					size[0]=render.get_width()
				size[1]+=render.get_height()
		if display==None:
			surface=pygame.Surface(size,SRCALPHA,32)
			posy=0
			for text in render_list:
				surface.blit(text,(0,posy))
				posy+=text.get_height()
		else:surface=None
		return surface
	def blitFinalScore(self,display,pos,ident):
		global dinL_10,dinB_12
		fonth=dinL_10
		fonthB=dinB_12
		names=["Nome","Capacetes","Coracoes","Tempo(s)","Farois Vermelhos","Ciclistas\Carros colididos","Ciclistas ultrapassados","Objetos colididos","Caes perturbados","Check-Points","Lado errado da pista","Total"]
		line=pygame.Surface( (ident+(max([fonth.size(str(x))[0] for x in self.score[1:] ]) ),1) )
		for n in range(1,len(names)):
			render_1=fonth.render(names[n]+":",True,(0,0,0))
			font=fonth if n!=len(names)-1 else fonthB
			render_2=font.render(str(self.score[n]),True,(0,0,0))
			display.blit(render_1,(pos[0],pos[1]+((fonth.get_height()+2)*(n-1))))
			display.blit(render_2,(pos[0]+ident,pos[1]+((fonth.get_height()+2)*(n-1))))
			display.blit(line,(pos[0],-1+pos[1]+((fonth.get_height()+2)*n)))
	def printScore(self):
		names=["Nome","Capacetes","Coracoes","Tempo(s)","Farois Vermelhos","Ciclistas\Carros colididos","Ciclistas ultrapassados","Objetos colididos","Caes perturbados","Check-Points","Lado errado da pista","Total"]
		for n in range(len(names)):
			print names[n]+":"+" "*(30-len(names[n]))+str(self.score[n])
	def setZero(self):
		global obs_img,level_img
		for obs in self.obstacles:
			obs[1]=random.choice(obs_img)
			obs[2]=random.randint(250,395)
			obs[3]=False
		for dog in self.dogs:
			dog[1]=False
		self.rank=6
		self.end_game=False
		#pontuacao incial do jogador
		self.score=["PLAYER",0,0,0,0,0,0,0,0,0,0,0]
		self.health =0
		self.recover=[False,0]
		self.heart_up=[False,0]
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
		
		self.culture_pointer=0
		self.sign_build=False
		
		self.popup_bool=[True,True,True]
		#variavel que define o movimento de pedal
		self.bool=[False,False,False]#K_RIGHT,K_LEFT
		self.alpha=False
		self.pause_tgscr.lockOnOff(False)
		self.pause_tgscr.turned_on=False
		self.pause_game=False
		self.start_time+=pygame.time.get_ticks()
	def setUnlock(self,stage):
		self.unlock=stage
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
		self.score_screen.turnOn(False)
		self.pause_button.turnOn()
		for mvbtt in self.move_button: mvbtt.turnOn()
	def setNewHighScore(self):
		if self.win:
			try:
				if self.unlock!=None: 
					self.unlock.setHide(False)
					self.unlock.setLock(False)
			except Exception,e:print e
			lenght=len(self.high_score)
			if lenght>0:
				for s in xrange(lenght):
					if self.score[-1]>self.high_score[s][-1]:
						self.high_score=self.high_score[:s]+[self.score]+self.high_score[s:]
						self.rank=s
						break
				if lenght<5 and lenght==len(self.high_score):
					self.high_score.append(self.score)
					self.rank=len(self.high_score)-1
			else:
				self.high_score.append(self.score)
				self.rank=0
		try:self.high_score=self.high_score[:5]
		except:pass
		self.printHighScore()
	def preEvents(self):
		pygame.time.set_timer(USEREVENT,800)
		pygame.time.set_timer(USEREVENT+1,300)
		global auto_gps_ingame,dog_img
		for dog in dog_img:
			dog.preEvents()
		try:self.loadScore()
		except Exception,e:print e
		self.printHighScore()
		if android and auto_gps_ingame:
			location=self.gps.getLocation()
			if location[0]!=0.0 or location[1]!=0.0:
				try:self.gps.update()
				except Exception,e:print 'gameTools.gameObject.gps.update:\n\t'+str(e)
				try:self.found=self.gps.finder.checkUrl(location)
				except Exception,e:print 'gameTools.gameObject.gps.finder.checkURL:\n\t'+str(e)
		for home in self.home_button: home.function = self.setAllZero
		for retry in self.retry_button: retry.function = self.setAllZero
		self.stages_button.function=self.setAllZero
		if not self.pause_game:self.start_time+=pygame.time.get_ticks()
		if pygame.time.get_ticks()-self.start_time<0:
			self.start_time=pygame.time.get_ticks()
			debugLog('start_timer<0')
		else:
			debugLog('start_timer>=0')
	def posEvents(self):
		self.saveScore()
		if not self.pause_game:self.start_time-=pygame.time.get_ticks()
		self.found=False
	#controle dos eventos
	def eventControler(self, event,resize,move):
		if self.pause_game==False and self.end_game==False:
			self.runEventControler(event, resize,move)
		else:
			self.bool=[False,False,False]
			try:
				for button in self.move_button:
					button.state=0
					button.pressed=False
					button.actived=False
					self.player.playerBrake(0.5)
			except Exception,e:print e
	def useHeart(self):
		if not self.recover[0] and self.player.damage>0 and self.health>0:
			self.player.damage-=self.player.maxlife/2
			if self.player.damage<0: self.player.damage=0
			self.health-=1
			self.recover=[True,0]
			pygame.time.set_timer(USEREVENT+7,3000)
	def runEventControler(self, event, resize,move):
		if event.type==KEYUP:
			if event.key==K_RIGHT: 
				self.bool[0]=False
				self.player.playerAccel(+1)#aceleracao esquerda
			if event.key==K_LEFT: 
				self.bool[1]=False
				self.player.playerAccel(-1)#aceleracao direita
			if event.key==K_DOWN: 
				self.player.desaccel=0.5
			if event.key==K_d:
				self.player.playerAccel(+1)#aceleracao do player para a esquerda --- guidao
			elif event.key==K_a:
				self.player.playerAccel(-1)#aceleracao do player para a direita ---- guidao

		if event.type==KEYDOWN:
			if event.key==K_SPACE: self.pause_tgscr.turnOn()
			if event.key==K_RIGHT: self.bool[0]=True
			if event.key==K_LEFT: self.bool[1]=True
			if event.key==K_DOWN: self.player.desaccel=4 ################################################### <<<<<<----------- mude o valor para mudar o quanto desacelera
		if event.type==USEREVENT+7:
			self.recover[0]=False
			self.heart_up[0]=False
			pygame.time.set_timer(USEREVENT+7,3000)
		if event.type==USEREVENT+1:
			for bike in self.bikers:
				if bike.odometer<=self.player.odometer and bike.pos[1]<=360+bike.img.get_height():
					if not bike.stop: bike.flip=not bike.flip
		for trlt in self.traffic_light:
			if trlt.running:
				if trlt.next_time<pygame.time.get_ticks()-self.start_time: 
					trlt.eventControler(event,resize,move)
					trlt.next_time=pygame.time.get_ticks()-self.start_time+trlt.time
		for dog in dog_img:
			dog.eventControler(event, resize,move)
		self.player.eventControler(event,resize)
		self.pop_up.eventControler(event, resize,move)
		if event.type==MOUSEBUTTONUP:
			mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
			global level_img
			rect=level_img[0].get_rect(topleft=self.heart_pos)
			rect.inflate_ip(-29,-25)
			if rect.collidepoint(mouse_pos):
				try:self.useHeart()
				except Exception,e:print e
			elif len(self.move_button)>0:
				#hardcode{
				#desfrear fora do freio
				if self.move_button[2].pressed_out:
					if self.player.desaccel!=0.5: 
						self.move_button[2].callActivation()
				'''
				#pedalar fora do pedal/guidão
				for x in xrange(2):
					if self.move_button[x].pressed_out and not self.move_button[1 if x==0 else 0].pressed:
						self.move_button[x].callActivation()
				'''
				if not self.move_button[0].rect.collidepoint(mouse_pos) and not self.move_button[1].rect.collidepoint(mouse_pos) and not self.move_button[2].rect.collidepoint(mouse_pos):
					for x in xrange(3):
						self.move_button[x].callActivation(False)
				#'''
				#}hardcode
		if event.type==MOUSEMOTION:
			mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
			move_motion=self.move_button[0].actived or self.move_button[0].pressed or self.move_button[1].actived or self.move_button[1].pressed
			if self.move_button[2].rect.collidepoint(mouse_pos) and move_motion:
				for x in xrange(2):
					self.move_button[x].callActivation(False)
	def screenCall(self):
		if self.pause_tgscr.turned_on:
			self.alpha=True
			self.color=(120,120,150)
			self.pause_button.turnOn(False)
			for mvbtt in self.move_button: mvbtt.turnOn(False)
			if not self.pause_game: self.start_time-=pygame.time.get_ticks()
			self.pause_game=True
		elif not self.end_game:
			self.alpha=False
			self.pause_button.turnOn()
			if not self.pause_tgscr.moving:
				if self.pause_game: self.start_time+=pygame.time.get_ticks()
				self.pause_game=False
				for mvbtt in self.move_button: mvbtt.turnOn()
		self.endGame(self.win,self.winner_screen,(20,89,75))
		self.endGame(self.lose,self.loser_screen,(33,33,33))
		return None
	def endGame(self,win_lose,scr,color):
		if win_lose and not self.end_game:
			try:self.score[1]=(float(self.player.maxlife-self.player.damage)/self.player.maxlife)*4
			except Exception,e:print e
			
			self.score[2]=self.health
			for trlt in self.traffic_light:
				self.score[4]+=trlt.player_infraction
			self.score[5]=self.player.collision_counter
			self.score[-1]=self.calculateScore(*self.score[1:-1])
			self.alpha=True
			self.color=color
			scr.turnOn()
			try:
				scr.itens[0].img=chic_16.render(str(self.score[1]),True,(51,51,51)).convert_alpha()
				scr.itens[1].img=chic_16.render(str(self.score[2]),True,(51,51,51)).convert_alpha()
				scr.itens[2].img=chic_16.render(str(self.score[4]),True,(51,51,51)).convert_alpha()
				scr.itens[3].img=chic_16.render(str(self.score[5]+self.score[7]+self.score[8]),True,(51,51,51)).convert_alpha()
				scr.itens[4].img=chic_16.render(str(self.score[3])+"s",True,(255,255,255)).convert_alpha()
				scr.itens[5].img=chic_22.render(str(self.score[11]),True,(51,51,51)).convert_alpha()
			except Exception,e:print e
			self.score_screen.turnOn(True)
			self.pause_tgscr.lockOnOff(True)
			self.pause_button.turnOn(False)
			for mvbtt in self.move_button: mvbtt.turnOn(False)
			self.end_game=True
			self.pause_game=True
			try:self.printScore()
			except Exception,e:print 'sc'+str(e)
			try:self.setNewHighScore()
			except Exception,e:print 'hsc'+str(e)
			self.score_screen.itens[0].img=self.blitHighScore().convert_alpha()
		
	#manipulacao dos elementos HUD da tela
	def blitPanel(self,display,pos):
		global panel_img
		#blitAlpha(display,panel_img,pos,100)
		display.blit(panel_img,pos)
		display.blit(pygame.transform.flip(panel_img,True,False),(pos[0]+640-panel_img.get_width(),pos[1]))
	def blitTimer(self,display,pos):
		global dinL_16, dinB_22
		tempo=(pygame.time.get_ticks()-self.start_time)
		self.score[3]=tempo/1000
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
		
	def blitSpeedOld(self,display,pos):
		global dinB_16,dinB_22,dinBd_32
		display.blit(dinBd_32.render(str(int(self.player.vel*3.6)),True,(0,0,0)),(pos[0]-dinBd_32.size(str(int(self.player.vel*3.6)))[0],pos[1]))
		display.blit(dinB_22.render('km/h',True,(0,0,0)),(pos[0],pos[1]+10))
	speed_rects=[
		pygame.Rect( (600+(x*5),150+(25*x) ),(35-(x*5),20 ) ) for x in xrange(5) ]
	def blitSpeed(self,display,pos):
		value=self.player.vel/self.player.max_vel
		for x,rect in enumerate(self.speed_rects):
			color=((50*x)+55,255-(50*x),55)
			print color
			display.fill(color,rect)
		
	def blitTrack(self,display,pos):
		global dinL_16, pointer_img
		display.blit(self.odometer_img,pos)
		display.blit(pointer_img,(pos[0]+38,pos[1]+(self.odometer_img.get_height()*((self.end_pos-self.player.odometer)/self.end_pos))-(pointer_img.get_height()//2)))

		render=dinL_16.render( str(self.end_pos/30)+"m" if self.end_pos<30000 else str(float(self.end_pos)/30000)+"km",True,(0,0,0))
		x=render.get_rect(center=(pos[0]+self.odometer_img.get_width()/2,0)).x
		display.blit(render,(x,pos[1]-dinL_16.get_height()))
	def blitLife(self,display,pos):
		global cap_img
		display.blit(pygame.transform.chop(cap_img[1],pygame.Rect(0,0,0,cap_img[1].get_height()*self.player.damage/self.player.maxlife)),(pos[0],pos[1]+cap_img[1].get_height()*self.player.damage/self.player.maxlife))
		display.blit(cap_img[0],pos)
	def blitLevel(self,display,pos):
		global dinB_22, level_img, dinL_16, cores, bar_level2
		if self.player.odometer/30 > 200*(self.score[9]+1) and self.player.odometer<self.end_pos:
			self.pop_up.callPopup(chic_22.render(str(200*(self.score[9]+1))+'m',True, (47,240,67)),3000)
			self.health+=1
			self.score[9]+=1
			self.heart_up=[True,0]
			pygame.time.set_timer(USEREVENT+7,3000)
		#imagem do level(coracao)
		display.blit(level_img[int(self.health>0)],pos)
		#escrita do level
		render=dinL_16.render(str(self.health),True,(0,0,0))
		rect=render.get_rect(center=level_img[0].get_rect(topleft=pos).center)
		display.blit(render,rect.topleft)
		if self.heart_up[0]:
			render=dinB_22.render("+1",True,(0,255,0))
			display.blit(render,[rect.right,rect.bottom-self.heart_up[1]])
			self.heart_up[1]+=0.3
		if self.recover[0]:
			render=dinB_22.render("-1",True,(0,0,0))
			display.blit(render,[rect.right,pos[1]+self.recover[1]-render.get_height()])
			self.recover[1]+=0.3
	def blitScore(self,display,pos):
		text="score atual: " + str(int(self.player.score))
		lentext=dinL_16.size(text)
		
		display.blit(dinL_16.render(text,True,(0,0,0)),(pos[0]-lentext[0]/1.5,pos[1]))

	#desenho dos elementos na tela	
	def blitOn(self, display):
		global grass_img,track_img,end_img,asphalt_img,traffic_img,car_img,light_img#,tutorial_img
		global culture_img,culture_rect
		global dinB_22
		global render_list
		render_list.setZero()
		if not self.pause_game:
			if self.bool[0]==True:#K_RIGHT
				self.player.pos[0]+=self.player.vel//2
			if self.bool[1]==True:#K_LEFT
				self.player.pos[0]-=self.player.vel//2
			self.player.playerMotion()
			#Penalidade por ficar na faixa esquerda
			if self.player.pos[0]<300 and self.player.pos[0]>150:
				self.score[10]+=0.01
				#self.left_ride_score+=0.03#self.score-=1.03
				self.player.setScore(-0.04)
			self.grass_pos+=self.player.vel
			self.dy_faixas-=self.player.vel*2

		if self.grass_pos>=grass_img.get_height(): self.grass_pos=0
		display.blit(grass_img,(((grass_img.get_height()+self.grass_pos)//4),self.grass_pos ))
		display.blit(grass_img,((self.grass_pos//4),self.grass_pos-grass_img.get_height()))
		display.blit(grass_img,(-100+(-(grass_img.get_height()+self.grass_pos)//4)-grass_img.get_width()*0.25,self.grass_pos ))
		display.blit(grass_img,(-100+(-self.grass_pos//4)-grass_img.get_width()*0.25,self.grass_pos-grass_img.get_height()))
		
		display.blit(track_img,(0,0))

		#calculo com o viewport para represetar a perspectiva na tela
		qnt_faixas=18
		tamanho_faixa=1800/qnt_faixas
		if self.dy_faixas<=-tamanho_faixa*2:self.dy_faixas+=tamanho_faixa*2
		for i in range(1,qnt_faixas*2,2):
			y=getViewport45(400,(tamanho_faixa*i)+self.dy_faixas+100,150)
			h=getViewport45(400,(tamanho_faixa*(i+1))+self.dy_faixas+100,150)
			display.fill((221,70,67),pygame.Rect(310,360-y,40,h-y))#(212,7,21)

		crosswalk_rect=[]
		for trlt in self.traffic_light:
			if trlt.odometer<=self.player.odometer and self.player.odometer-trlt.odometer<=1377:
				try:trlt.blitOn(display,render_list,self.player,self.pause_game,self.found or not android,self.start_time)
				except Exception,e: print 'trlt.blitOn() error:\n\t'+str(e)
				crosswalk=trlt.getCrosswalkRect()
				if crosswalk:crosswalk_rect.append(crosswalk)
		
		if self.sign_pos<=self.player.odometer:
			if self.player.odometer-self.sign_pos-self.sign_img[self.sign_pointer].get_height()<=1377:
				sign_pos_vp=360-getViewport45(400,(255*11)-(self.player.odometer-self.sign_pos)*2,150)
				
				render_list.blit(self.sign_img[self.sign_pointer],(120-sign_pos_vp/4,sign_pos_vp-self.sign_img[self.sign_pointer].get_height()))
				try:
					if self.found:
						if not self.sign_build:
							culture_name=textBox(unicode(self.gps.finder.getLocals()[self.culture_pointer]['name']),dinL_12,culture_rect.width,(0,0,0),2)
							culture_dist=dinL_12.render(unicode(int(self.gps.finder.getDistances()[self.culture_pointer]))+" m",True,(0,0,0))
							surf=pygame.Surface(culture_rect.size)
							surf.fill((255,255,255))
							surf.blit(culture_name,(0,0))
							surf.blit(culture_dist,(0,culture_name.get_height()))
							culture_img.fill((255,255,255),culture_rect)
							culture_img.blit(surf.convert(),culture_rect.topleft)
							self.sign_build=True
							print 'builded'
						render_list.blit(culture_img,(400+sign_pos_vp/4,sign_pos_vp-culture_img.get_height()))
				except Exception,e:print e
			else: 
				self.sign_pos+=1377
				self.sign_pointer+=1
				if len(self.sign_img)<=self.sign_pointer: self.sign_pointer=0
				if self.found:
					self.sign_build=False
					self.culture_pointer+=1
					if len(self.gps.finder.getLocals())<=self.culture_pointer: self.culture_pointer=0
		if self.end_pos-360-100<=self.player.odometer:
			for i in range(7): render_list.blit(end_img,(end_img.get_width()*i,self.player.odometer-self.end_pos+360))

		#verifica os eventos de colisao com cada obstaculo
		for obs in self.obstacles:
			if obs[0]<=self.player.odometer:
				if self.player.odometer-obs[0]<=360:
					pos=[obs[2],self.player.odometer-obs[0]]
					scale=abs(pos[1]+150 )/(360+150)
					new_size=(int(obs[1].get_width()*scale),int(obs[1].get_height()*scale))
					scaled_obs=pygame.transform.scale(obs[1],new_size)
					if obs[2]<=315:
						pos[0]+= obs[1].get_width()-new_size[0]
						pos[0]-=(pos[1]/3.5)*(float(315-pos[0])/120)
					elif obs[2]>=326:
						pos[0]+=(pos[1]/3.5)*(float(pos[0]-326)/120)
					else:
						pos[0]-=new_size[0]//2
					rect=obs[1].get_rect(topleft=pos)
					if self.player.wheels_box.colliderect(rect):
						if self.player.vel>0: self.player.vel-=self.player.vel*0.1*self.player.desaccel
						if obs[3]==False and not self.end_game and not self.pause_game:
							if android: android.vibrate(0.2)
							if self.player.vel>0: self.player.vel-=1
							self.score[7]+=1
							obs[3]=True
					else:
						if obs[3]: obs[3]=False
					render_list.blit(scaled_obs,pos)
		#verifica os eventos dos cães
		try:
			for dog in self.dogs:
				if dog[0]<=self.player.odometer:
					if self.player.odometer-dog[0]<=460:
						scale=abs(self.player.odometer-dog[0]+150)/(360+150)
						image=dog_img[int(dog[1])].getImage()
						new_size=(int(scale*image.get_width()),int(scale*image.get_height()))
						dog_image=pygame.transform.scale(image,new_size)
						pos=[480,self.player.odometer-dog[0]-dog_image.get_height()]
						pos[0]+=pos[1]/4
						if dog[1]==False:
							rect=pygame.Rect(pos[0]-150,pos[1],140,new_size[1])
							if self.player.hit_box.colliderect(rect):
								self.player.h_vel=-10
								self.player.vel=0
								self.score[8]+=1
								playSound(dog_bark)
								if android: android.vibrate(0.3)
								dog[1]=True
						render_list.blit(dog_image,pos)
		except Exception,e:print e
					
		#verifica os eventos de colisao com cada ciclista transeunte
		biker_counter=0
		for bike in self.bikers:
			if bike.odometer<=self.player.odometer: 
				if bike.pos[1]<=360:
					#flipa
					fliped_bike=pygame.transform.flip(bike.img,bike.flip,False)
					#bike.pos
					scale=abs(bike.pos[1]+(bike.img.get_height()*1.5) )/360  #if bike.pos[1]<self.player.pos[1] else 1
					new_size=(int(bike.img.get_width()*scale),int(bike.img.get_height()*scale))
					scaled_bike=pygame.transform.scale( fliped_bike ,new_size)
					if bike.pos[0]<=315:
						new_pos=[ bike.pos[0]+ bike.img.get_width()-new_size[0] , bike.pos[1]+((bike.img.get_height()-new_size[1])//2)]
						new_pos[0]-=(new_pos[1]/3.5)*(float(315-bike.pos[0])/120)
					elif bike.pos[0]>=326:
						new_pos=[ bike.pos[0], bike.pos[1]+((bike.img.get_height()-new_size[1])//2)]
						new_pos[0]+=(new_pos[1]/3.5)*(float(bike.pos[0]-326+new_size[0])/120)
					else:
						new_pos=[bike.pos[0]-(new_size[0]/2),bike.pos[1]]
					bike_hit_box_x=pygame.Rect(new_pos[0],new_pos[1]+int(new_size[1]*0.2),bike.img.get_width(),int(new_size[1]*0.6))#horizontal
					bike_hit_box_y=pygame.Rect(int(new_pos[0]+new_size[0]*0.2),new_pos[1],int(bike.img.get_width()*0.6),new_size[1])#vertical
					#colisao horizontal
					if bike_hit_box_x.colliderect(self.player.hit_box):
						if self.player.pos[0]>new_pos[0]+(new_size[0]//2):
							if not self.pause_game:self.player.receiveDamage(1,(+20,0))
						else:
							if not self.pause_game:self.player.receiveDamage(1,(-20,0))
						self.collision_counter+=1
						#retira pontos
						self.player.setScore(-50)
					#colisao vertical
					elif bike_hit_box_y.colliderect(self.player.hit_box) and new_pos[1]<360:
						if self.player.stun_counter==0: 
							if bike.vel>0: bike.vel=-100*self.player.accel*bike.accel
							if not self.pause_game:self.player.receiveDamage(1,(0,-20))
							self.player.vel=0
							self.collision_counter+=1
							#retira pontos
							self.player.setScore(-50)
					if len(crosswalk_rect)==0: bike.stop=False
					for crosswalk in crosswalk_rect:
						if bike.accel>0:
							if bike_hit_box_x.colliderect(crosswalk):
								if bike.pos[1]>crosswalk.bottom:
									bike.pos[1]+=(crosswalk.bottom-bike_hit_box_x.y)*2
								else:
									bike.stop=True
									bike.vel=0
							if bike.stop:
								bike.pos[1]=crosswalk.y-bike.img.get_height()
						elif bike.accel<0:
							if bike_hit_box_x.colliderect(crosswalk):
								if bike.pos[1]<crosswalk.y:
									bike.pos[1]+=(crosswalk.y-bike_hit_box_x.bottom)
									bike.vel=bike.max_vel
								else:
									bike.stop=True
									bike.vel=0
							if bike.stop:
								bike.pos[1]=crosswalk.y+crosswalk.h
						
					if not self.pause_game and not bike.stop: bike.passerbyMotion(self.player.vel)
					
					render_list.blit(scaled_bike ,new_pos )
				#pontuacao para ultrapassagem
				else:
					biker_counter+=1
					if bike.pos[1]<460: 
						self.player.setScore(100)
						bike.pos[1]=460
		self.score[6]=biker_counter
		#condicao vitoria e derrota
		if self.end_pos<=self.player.odometer:
			self.win=True
		if self.player.damage>=self.player.maxlife: 
			self.lose=True
		self.player.blitOn(render_list)
		render_list.sortList()
		render_list.blitOn(display)

		#informacoes na tela
		if self.pause_game==False or self.tutorial==True:
			#painel fundo
			try:
				if self.blit_panel:self.blitPanel(display,(0,0))
			except Exception,e: print 'blitPanel() error:\n\t'+str(e)
			#timer
			try:
				if self.blit_timer:self.blitTimer(display,(5,0))
			except Exception,e: print 'blitTimer() error:\n\t'+str(e)
			#speedometer
			#self.blitSpeed(display,(580,150))
			#track
			try:
				if self.blit_track:self.blitTrack(display,(580,77))
			except Exception,e: print 'blitTrack() error:\n\t'+str(e)
			#estrela
			try:
				if self.blit_life:self.blitLife(display,(15,39))
			except Exception,e: print 'blitLife() error:\n\t'+str(e)
			#coracao level
			try:
				if self.blit_level:self.blitLevel(display,self.heart_pos)
			except Exception,e: print 'blitLevel() error:\n\t'+str(e)
			#popup
			try:self.pop_up.blitOn(display)
			except Exception,e: print e
		if self.alpha:
			self.fade.fill(self.color)
			display.blit(self.fade,(0,0))
		if self.end_game:
			try:display.blit(self.left_side_name,(45,45))
			except Exception,e:print e
	def screenManipulation(self,screen):pass
