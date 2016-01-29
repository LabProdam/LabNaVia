# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os,cPickle,random
from popUp import *
from trafficLight import getViewport45
from screenTools import mixer,renderList, textBox,playSound,android,rotateCenter
from geo import*
from debugLog import*

auto_gps_ingame=android
def setAutoGpsIngame(auto=True):
	global auto_gps_ingame
	auto_gps_ingame=auto
#diretorios
dir_font='fontes'+str(os.sep)
dir_img='images'+str(os.sep)
dir_pan=dir_img+'panorama'+str(os.sep)
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
chic_20=pygame.font.Font(dir_font+"ChicagoFLF.ttf",22)
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

sansB_12=pygame.font.Font(dir_font+"OpenSans-Bold.ttf",12)
#imagens
track_shadow = pygame.Surface((640,50),SRCALPHA,32)
surf=pygame.Surface((640,1))
surf.fill((0,80,0))
for x in xrange(51):
	surf.set_alpha(202-(4*x))
	track_shadow.blit(surf,(0,(1*x)))
pointer_img  = pygame.Surface((10,10),SRCALPHA,32).convert_alpha()
pygame.draw.circle(pointer_img,(255,0,0),(5,5),5)
grass_img    = pygame.image.load(dir_img+'grama.png').convert()
track_img    = pygame.transform.scale(pygame.image.load(dir_img+'pista4.png').convert_alpha(),(640,260))
panel_img   = pygame.image.load(dir_img+'painel_menor2.png').convert_alpha()
cap_img = [pygame.image.load(dir_img+"pequenoCap"+str(x)+".png").convert_alpha() for x in xrange(2)]

end_img      = pygame.image.load(dir_img+'faixa.png').convert_alpha()
pop_bar_score = pygame.image.load(dir_img+"popBar1.png").convert_alpha()

level_img     = [pygame.image.load(dir_img+"heart"+str(x)+".png").convert_alpha()for x in xrange(2)]
				
cores  	      =	[(149,34,48),(176,4,24),(200,21,42),(210,2,27),(255,4,33)]	

asphalt_img = pygame.image.load(dir_img+"asfalto.png").convert()

culture_img = pygame.image.load(dir_img+"placaBlank.png")
culture_rect=pygame.Rect(7,8,112,49)
obs_img=[
	pygame.image.load(dir_obs+"obs"+str(x)+".png").convert_alpha() for x in xrange(3)
]
sewer_img=pygame.image.load(dir_obs+"closed_sewer.png").convert_alpha()
hole_img=pygame.image.load(dir_obs+"opened_sewer.png").convert_alpha()
render_list=renderList()
from animatedSprite import *
dog=[pygame.image.load(dir_img+"dogAnimado.png").convert_alpha(),pygame.image.load(dir_img+"dogLatindo.png").convert_alpha()]
dog_img=[animatedSprite(dog[d],dog[d].get_rect(w=dog[d].get_width()/2),[0,0],USEREVENT+d) for d in xrange(2)]
tumbleweed=pygame.image.load(dir_obs+"feno.png").convert_alpha()
tumbleweed_img=animatedSprite(tumbleweed,tumbleweed.get_rect(w=tumbleweed.get_width()/3),[0,0],USEREVENT+3)
dog_bark=mixer.Sound(dir_sound+"dogBark.mp3")
nuvem=pygame.image.load(dir_img+"nuvem.png").convert_alpha()
light=pygame.image.load(dir_img+"light.png").convert_alpha()
panorama_dia=[pygame.image.load(dir_pan+"dia"+str(x)+".png").convert_alpha() for x in xrange(4)]
panorama_noite=[pygame.image.load(dir_pan+"noite"+str(x)+".png").convert_alpha() for x in xrange(4)]
pedal_2=pygame.image.load(dir_img+"pedal1.png").convert_alpha()
pedal_1=pygame.image.load(dir_img+"pedal2.png").convert_alpha()
odo_heart=pygame.image.load(dir_menu+"heart.png").convert_alpha()
plane_img=pygame.image.load(dir_pan+"plane.png").convert_alpha()
bird_img=pygame.image.load(dir_pan+"birds.png").convert_alpha()
solarfilter_img=pygame.image.load(dir_obs+"filtrosolar.png").convert_alpha()
glow_img=pygame.image.load(dir_img+"playerGlow.png").convert_alpha()
night_alpha=pygame.Surface((640,360),SRCALPHA,32)
np=pygame.Surface((640,252))
np.set_alpha(155)
np.fill((55,55,155))
night_alpha.blit(np,(0,0))
np=pygame.Surface((640,1))
np.fill((55,55,155))
for x in xrange(108):
	np.set_alpha(155-x)
	night_alpha.blit(np,(0,252+x))
night_alpha.convert_alpha()

frases=[u"Dê um like no face do Lab","Cuidado com os cachorros",u"Bueiros são perigosos","Toque 10x no logo do Jogo","Ligue o GPS","E = MC2","Eu sou seu pai",u"A aventura esta lá fora","Use sempre a faixa, a ciclofaixa","Continue a pedalar",u"Ao inifinito e além",u"Toque no coração","Use Python","Eu S2 software livre","Use filtro solar","Cuidado com o feno",u"No semáforo não desperdice tempo"]

class gameObject(object):
	def __init__(self,name,end_pos,number_of_checkpoints,player,clear_score,biker_list,traffic_list,obstacle_list,dog_list,sewers_list,hole_list,tumbleweed_list,solar_filter,sign_img,scr_lose,scr_win,scr_score,retry_button,home_button,stages_button,pause_button,resume_button,pause_scr,move_button,gps_item,wheater="random",time="random"):
		global pop_bar_score,level_img
		self.name=name
		self.left_side_name=pygame.transform.rotate(chic_72.render(name,True,(255,255,255)),90)
		#ciclista jogador 
		self.player=player
		self.end_pos=end_pos
		self.clear_score=clear_score
		#lista de ciclistas transeuntes
		self.number_of_checkpoints=number_of_checkpoints
		self.makeOdometer(number_of_checkpoints)
		self.checkpoints_distance=(end_pos/30)/(number_of_checkpoints+1)
		debugLog( self.checkpoints_distance,name)
		#self.odometer_img=odometer
		self.bikers=biker_list
		self.sewers=[[sewer[0]*30,sewer[1],False] for sewer in sewers_list]
		self.holes=[[hole[0]*30,hole[1],False] for hole in hole_list]
		#self.sewers+=[[cover[0]*30,cover[1]+10,False] for cover in hole_list]
		self.obstacles=[
			[obs*30 if type(obs).__name__!="list" else obs[0]*30,
			None,
			0 if type(obs).__name__!="list" else obs[1],
			False,
			type(obs).__name__=="list"] for obs in obstacle_list]
		self.tumbleweed= [[tw[0]*30,0,tw[1],False] for tw in tumbleweed_list]
		self.solar_filter=[[sf[0]*30,sf[1],True] for sf in solar_filter]
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
		self.pop_up=popUp((320-(pop_bar_score.get_width()//2),-pop_bar_score.get_height()),(320-(pop_bar_score.get_width()//2),0),(0,1),pop_bar_score,(40,15))
		self.pause_tgscr=pause_scr
		self.wheater=wheater
		self.time=time
		self.found=False
		self.setZero()
		self.fade=pygame.Surface((640,360))
		self.fade.set_alpha(155)
		self.color=(0,0,0)
		self.high_score=[]#NOME,1helmets,2hearts,3time,4red_trlt,5bikers_hit,6bikers_leftbehind,7things_hit,8dog,9check_points,10wrong_side,score calculado
		self.tutorial=False
		self.blit_panel=True
		self.blit_timer=True
		self.blit_track=True
		self.blit_score=True
		self.blit_life=True
		self.blit_level=True
		self.blit_player=True
		self.heart_pos=(5-14,188-12)
		self.unlock=None
	'''
	def makeOdometerOld(self,checkpoints):
		checkpoints=float(self.end_pos/30)/200)
		global odo_heart
		size=(61,183)
		self.odometer_img=pygame.Surface(size,SRCALPHA,32)
		self.odometer_img.fill((0,0,0),(42,0,1,size[1]))
		self.odometer_img.fill((0,0,0),(28,0,29,1))
		self.odometer_img.fill((0,0,0),(28,size[1]-1,29,1))
		cp_dist=(size[1]/checkpoints)
		h=odo_heart.get_height()/2
		for n in xrange(int(checkpoints)):
			self.odometer_img.fill((0,0,0),(28,size[1]-int(cp_dist*(n+1)),29,1))
			y=size[1]-int(cp_dist*(n+1))-h
			if y>0 and y+h*2<size[1]: self.odometer_img.blit(odo_heart,(5,y))
	'''
	def makeOdometer(self,checkpoints):
		checkpoints+=1
		global odo_heart
		size=(61,183)
		self.odometer_img=pygame.Surface(size,SRCALPHA,32)
		self.odometer_img.fill((0,0,0),(42,0,1,size[1]))
		self.odometer_img.fill((0,0,0),(28,0,29,1))
		self.odometer_img.fill((0,0,0),(28,size[1]-1,29,1))
		cp_dist=(size[1]/checkpoints)
		h=odo_heart.get_height()/2
		for n in xrange(int(checkpoints)):
			self.odometer_img.fill((0,0,0),(28,int(cp_dist*n),29,1))
			y=int(cp_dist*n)-h
			if y>=0: self.odometer_img.blit(odo_heart,(5,y))
	def clearScore(self):
		try:
			score_file=open(dir_data+"score_data_"+self.name.replace(' ','_')+".lab","wb")
			score_file.truncate()
			score_file.close()
		except Exception,e:debugLog(e)
		self.high_score=[]
		if self.unlock!=None:
			self.unlock.setLock()
			self.unlock.setHide()
	def loadScore(self):
		try:
			score_file=open(dir_data+"score_data_"+self.name.replace(' ','_')+".lab","rb")
			self.high_score=cPickle.load(score_file)
			if self.unlock!=None and self.high_score[0][-1]>self.clear_score:
				self.unlock.lock=cPickle.load(score_file)
				self.unlock.hide=cPickle.load(score_file)
			score_file.close()
		except Exception,e:
			self.saveScore()
			debugLog(e)
	def saveScore(self):
		score_file=open(dir_data+"score_data_"+self.name.replace(' ','_')+".lab","wb")
		try:
			cPickle.dump(self.high_score,score_file)
			if self.unlock!=None:
				cPickle.dump(self.unlock.lock,score_file)
				cPickle.dump(self.unlock.hide,score_file)
		except Exception,e:debugLog(e)
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
			debugLog(str(1+s)+') '+score[0]+': '+str(score[-1]))
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
			debugLog(names[n]+":"+" "*(30-len(names[n]))+str(self.score[n]))
	def setZero(self):
		global obs_img,level_img
		for obs in self.obstacles:
			obs[1]=random.choice(obs_img)
			if obs[4]==False:
				obs[2]=random.randint(250,395)
			obs[3]=False
		for sewer in self.sewers:
			sewer[2]=False
		for hole in self.holes:
			hole[2]=False
		for dog in self.dogs:
			dog[1]=False
		for tw in self.tumbleweed:
			tw[1]=0
			tw[3]=False
		for sf in self.solar_filter:
			sf[2]=True
		self.glow=0
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
		if self.found:self.culture_pointer=0
		else:self.culture_pointer=random.randrange(len(frases))
		self.sign_build=False
		
		self.popup_bool=[True,True,True]
		#variavel que define o movimento de pedal
		self.bool=[False,False,False]#K_RIGHT,K_LEFT
		self.alpha=False
		self.pause_tgscr.lockOnOff(False)
		self.pause_tgscr.turned_on=False
		self.pause_game=False
		self.start_time+=pygame.time.get_ticks()
		self.cloud_pos=random.randrange(640)
		self.cloud_accel=random.randrange(1,6)*0.1
		debugLog(self.cloud_accel)
		self.plane=[False,[-plane_img.get_width(),random.randint(0,24)-(plane_img.get_height()//2)],random.randrange(100)<50]
		if self.plane[2]:debugLog("plane will be created")
		self.bird=[random.randrange(100)<50,[-bird_img.get_width(),random.randint(0,35)-(bird_img.get_height()//2)]]
		pygame.time.set_timer(USEREVENT+5,0)
		if not self.bird[0]:
			time=random.randint(5,25)*1000
			pygame.time.set_timer(USEREVENT+5,time)
			debugLog("bird will be created in "+str(time))
		else:
			debugLog("bird created")
		self.fog=False#random.randrange(100)<40
		if self.time=="random":
			self.night=random.randrange(100)<40
		else:
			self.night=self.time
		if self.wheater=="random":
			self.rain=random.randrange(4)
		else:
			self.rain=self.wheater
		pygame.time.set_timer(USEREVENT+6,15*1000)
		self.user_event_6=0
		self.bg_pos=(-random.randrange(900-640),0)
		self.blit_player=True
		self.drama=0
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
			try:
				if self.unlock!=None and self.high_score[0][-1]>self.clear_score: 
					self.unlock.setHide(False)
					self.unlock.setLock(False)
			except Exception,e:debugLog(e)
		try:self.high_score=self.high_score[:5]
		except:pass
		self.printHighScore()
	def preEvents(self):
		pygame.time.set_timer(USEREVENT,800)
		pygame.time.set_timer(USEREVENT+1,300)
		pygame.time.set_timer(USEREVENT+3,200)
		global auto_gps_ingame,dog_img
		for dog in dog_img:
			dog.preEvents()
		try:self.loadScore()
		except Exception,e:debugLog(e)
		self.printHighScore()
		self.culture_pointer=random.randrange(len(frases))
		if not self.pause_game:
			self.start_time+=pygame.time.get_ticks()
			if android and auto_gps_ingame:
				location=self.gps.getLocation()
				if location[0]!=0.0 or location[1]!=0.0:
					try:self.gps.update()
					except Exception,e:debugLog('gameTools.gameObject.gps.update:\n\t'+str(e))
					try:
						self.found=self.gps.finder.checkUrl(location)
						self.culture_pointer=0
					except Exception,e:debugLog('gameTools.gameObject.gps.finder.checkURL:\n\t'+str(e))
		for home in self.home_button: home.function = self.setAllZero
		for retry in self.retry_button: retry.function = self.setAllZero
		self.stages_button.function=self.setAllZero
		if pygame.time.get_ticks()-self.start_time<0:
			self.start_time=pygame.time.get_ticks()
			debugLog('start_timer<0')
		else:
			debugLog('start_timer>=0')
	def posEvents(self):
		self.saveScore()
		if not self.pause_game:
			self.start_time-=pygame.time.get_ticks()
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
			except Exception,e:debugLog(e)
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
		if event.type==USEREVENT+6:
			if self.user_event_6==0:
				if self.plane[2]:
					self.plane[0]=True
					debugLog('plane created')
			if self.rain>0:
				if self.user_event_6%1==0:
					rain=self.rain
					while rain==self.rain:
						self.rain=random.randint(1,3)
			self.user_event_6+=1
		try:
			if event.type==USEREVENT+5:
				self.bird=[True,[-bird_img.get_width(),random.randint(0,35)-(bird_img.get_height()//2)]]
				debugLog("bird created")
				pygame.time.set_timer(USEREVENT+5,0)
		except Exception,e:debugLog(e)
		if event.type==USEREVENT+1:
			if self.drama==3:
				self.player.damage=self.player.maxlife
				self.score[7]+=1
				self.drama=0
			if self.drama==6:
				self.player.pos[1]-=40
				self.drama=0
			if self.drama>0:self.drama+=1
			if self.glow>0:
				self.glow-=1
			for bike in self.bikers:
				if bike.odometer<=self.player.odometer and bike.pos[1]<=1377+bike.img.get_height():
					if not bike.stop: bike.flip=not bike.flip
		for trlt in self.traffic_light:
			if trlt.running:
				if trlt.next_time<pygame.time.get_ticks()-self.start_time: 
					trlt.eventControler(event,resize,move)
					trlt.next_time=pygame.time.get_ticks()-self.start_time+trlt.time
		for dog in dog_img:
			dog.eventControler(event, resize,move)
		tumbleweed_img.eventControler(event,resize,move)
		self.player.eventControler(event,resize)
		self.pop_up.eventControler(event, resize,move)
		if event.type==MOUSEBUTTONUP:
			mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
			global level_img
			rect=level_img[0].get_rect(topleft=self.heart_pos)
			rect.inflate_ip(-29,-25)
			if rect.collidepoint(mouse_pos):
				try:self.useHeart()
				except Exception,e:debugLog(e)
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
			except Exception,e:debugLog(e)
			
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
			except Exception,e:debugLog(e)
			self.score_screen.turnOn(True)
			self.pause_tgscr.lockOnOff(True)
			self.pause_button.turnOn(False)
			for mvbtt in self.move_button: mvbtt.turnOn(False)
			self.end_game=True
			self.pause_game=True
			try:self.printScore()
			except Exception,e:debugLog('sc'+str(e))
			try:self.setNewHighScore()
			except Exception,e:debugLog('hsc'+str(e))
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
			debugLog(color)
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
		if self.player.odometer/30 > self.checkpoints_distance*(self.score[9]+1) and self.player.odometer<self.end_pos and self.score[9]<self.number_of_checkpoints:
			self.pop_up.callPopup(chic_22.render(str(self.checkpoints_distance*(self.score[9]+1))+'m',True, (0,0,0)),3000)
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
		global grass_img,track_img,end_img,asphalt_img,traffic_img,car_img,light_img,panorama_dia, panorama_noite#,tutorial_img
		global culture_img,culture_rect
		global dinB_22
		global render_list
		render_list.setZero()
		if not self.pause_game:
			if self.rain==1:
				self.player.vel-=0.03
			if self.player.desaccel<1:
				if self.rain==2:
					self.player.pos[0]+=0.5
				if self.rain==3:
					self.player.pos[0]-=0.5
				if self.bool[0]==True:#K_RIGHT
					self.player.playerMove(+1)#self.player.pos[0]+=self.player.vel//2
				if self.bool[1]==True:#K_LEFT
					self.player.playerMove(-1)#self.player.pos[0]-=self.player.vel//2
			self.player.playerMotion()
			#Penalidade por ficar na faixa esquerda
			if self.player.pos[0]<280 and self.player.pos[0]>150:
				self.score[10]+=0.01
				#self.left_ride_score+=0.03#self.score-=1.03
				self.player.setScore(-0.04)
			self.grass_pos+=self.player.vel
			self.dy_faixas-=self.player.vel*2
		display.fill((80,180,120))
		try:
			panorama=panorama_noite if self.night else panorama_dia
			display.blit(panorama[0],self.bg_pos)
			display.blit(panorama[1],(500,0))
			if not self.night:
				if self.plane[0]:
					if self.plane[1][0]<640+plane_img.get_width():
						display.blit(plane_img,self.plane[1])
						self.plane[1][0]+=0.2
				if self.bird[0]:
					if self.bird[1][0]<640+bird_img.get_width():
						display.blit(bird_img,self.bird[1])
						self.bird[1][0]+=0.35
					else:
						time=random.randint(5,25)*1000
						pygame.time.set_timer(USEREVENT+5,time)
						self.bird[0]=False
						debugLog('bird will be created in '+str(time))
			display.blit(panorama[2],self.bg_pos)
			display.blit(panorama[3],(self.cloud_pos,0))
			display.blit(panorama[3],(self.cloud_pos-900,0))
			self.cloud_pos+=self.cloud_accel#0.5
			if self.cloud_pos>=900:
				debugLog("resetou nuvens")
				self.cloud_pos-=900
		except Exception,e:debugLog(e)
		display.blit(track_img,(0,100))


		#calculo com o viewport para represetar a perspectiva na tela
		qnt_faixas=9
		tamanho_faixa=1300/qnt_faixas# cinco vezes o tamanho da área de desenho
		if self.dy_faixas<=-tamanho_faixa*2:self.dy_faixas+=tamanho_faixa*2
		for i in range(1,qnt_faixas*2,2):
			y=getViewport45(400,(tamanho_faixa*i)+self.dy_faixas+100,150)
			h=getViewport45(400,(tamanho_faixa*(i+1))+self.dy_faixas+100,150)
			display.fill((234,100,96),pygame.Rect(310,460-y,40,h-y))#(212,7,21)

		crosswalk_rect=[]
		for trlt in self.traffic_light:
			if trlt.odometer<=self.player.odometer and self.player.odometer-trlt.odometer<=1377:
				try:trlt.blitOn(display,render_list,self.player,self.pause_game,self.found or not android,self.start_time)
				except Exception,e: debugLog('trlt.blitOn() error:\n\t'+str(e))
				crosswalk=trlt.getCrosswalkRect()
				if crosswalk:crosswalk_rect.append(crosswalk)
		display.blit(track_shadow,(0,100))
		try:
			if self.sign_pos<=self.player.odometer:
				if self.player.odometer-self.sign_pos-self.sign_img[self.sign_pointer].get_height()+100<=1377:
					sign_pos_vp=430-getViewport45(400,(255*11)-(self.player.odometer-self.sign_pos)-1377,150)
				
					sign_img=self.sign_img[self.sign_pointer]
					scale=abs(sign_pos_vp-150+(sign_img.get_height()*2) )/260  #if bike.pos[1]<self.player.pos[1] else 1
					new_size=(int(sign_img.get_width()*scale),int(sign_img.get_height()*scale))
					sign_img=pygame.transform.scale( sign_img ,new_size)
					sign_pos=(270-new_size[0]-(sign_pos_vp)/1.7,sign_pos_vp-new_size[1])
					render_list.blit(sign_img,sign_pos)
					if sign_img.get_rect(topleft=sign_pos).colliderect(self.player.hit_box):
						self.player.vel=0
						self.player.odometer-=10
					if not self.sign_build:
						surf=pygame.Surface(culture_rect.size)
						surf.fill((255,255,255))
						if self.found:
							#culture_name=textBox(unicode(self.gps.finder.getLocals()[self.culture_pointer]['name']),dinL_12,culture_rect.width,(0,0,0),2)
							#culture_dist=dinL_12.render(unicode(int(self.gps.finder.getDistances()[self.culture_pointer]))+" m",True,(0,0,0))
							culture_name=textBox(unicode(self.gps.finder.listObj[self.culture_pointer]["nome"]),sansB_12,culture_rect.width,(0,0,0),2)
							culture_dist=sansB_12.render(unicode(int(self.gps.finder.listObj[self.culture_pointer]["distancia"]))+" m",True,(0,0,0))
							surf.blit(culture_name,(0,-1))
							surf.blit(culture_dist,(0,culture_name.get_height()-2))
						else:
							text=textBox(frases[self.culture_pointer],sansB_12,culture_rect.width,(0,0,0),3)
							surf.blit(text,(0,0))
						culture_img.fill((255,255,255),culture_rect)
						culture_img.blit(surf.convert(),culture_rect.topleft)
						self.sign_build=True
						debugLog('builded')
					sign_img=pygame.transform.scale( culture_img ,new_size)
					sign_pos=(390+(sign_pos_vp/1.9),sign_pos_vp-sign_img.get_height())
					render_list.blit(sign_img,sign_pos)
					if sign_img.get_rect(topleft=sign_pos).colliderect(self.player.hit_box):
						self.player.vel=0
						self.player.odometer-=10
				else: 
					self.sign_pos+=1377
					self.sign_pointer+=1
					if len(self.sign_img)<=self.sign_pointer: self.sign_pointer=0
					self.sign_build=False
					self.culture_pointer+=1
					if self.found:
						if len(self.gps.finder.listObj)<=self.culture_pointer: self.culture_pointer=0
					else:
						if len(frases)<=self.culture_pointer: self.culture_pointer=0
		except Exception,e:
			debugLog(e)
			debugLog(new_size)
		try:
			if self.end_pos-self.player.odometer<=1560:
				end_vp=340-getViewport45(400,(255*11)-(self.player.odometer-self.end_pos)-2210,150)
				new_img=end_img
				scale=abs(end_vp-150+(new_img.get_height()) )/260
				new_size=(int(new_img.get_width()*scale),int(new_img.get_height()*scale))
				new_img=pygame.transform.scale( new_img ,new_size)
				new_pos=(320-(new_img.get_width()/2),end_vp)
				render_list.blit(new_img,new_pos)
				'''
				if self.end_pos-self.player.odometer<260:
					self.player.playerAccel(0)
				'''
		except Exception,e:
			debugLog(e)

		try:
			for hole in self.holes:
				if hole[0]<=self.player.odometer:
					if self.player.odometer-hole[0]<=1377:
						hole_pos_vp=420-getViewport45(400,(255*11)-(self.player.odometer-hole[0])-1377,150)
						pos=[hole[1],hole_pos_vp]
						scale=abs(hole_pos_vp-150+(hole_img.get_height()*2.5) )/260
						new_size=(int(hole_img.get_width()*scale),int(hole_img.get_height()*scale))
						scaled_hole=pygame.transform.scale(hole_img,new_size)
						if hole[1]<=318:
							pos[0]+= (hole_img.get_width()/2.5)-new_size[0]
							pos[0]-=(pos[1]/3.5)*(float(318-hole[1])/120)
						elif hole[1]>=329:
							pos[0]+=(pos[1]/3.5)*(float(abs(pos[0]-329))/120)
						else:
							pos[0]-=new_size[0]//2
						rect_1=scaled_hole.get_rect(topleft=pos)
						rect_1.w/=2
						rect_2=rect_1.copy()
						rect_2.x+=rect_1.w
						if self.player.wheels_box.colliderect(rect_1):
							if not self.end_game and not self.pause_game:
								if android: android.vibrate(0.2)
								self.blit_player=False
								self.drama=1
								#self.score[7]+=1
								#debugLog(self.score[7])
						elif self.player.wheels_box.colliderect(rect_2):
							if self.player.vel>0: self.player.vel-=self.player.vel*0.1*self.player.desaccel
							if hole[2]==False and not self.end_game and not self.pause_game:
								if android: android.vibrate(0.2)
								if self.player.vel>0: self.player.vel-=1
								self.score[7]+=1
								debugLog(self.score[7])
								hole[2]=True
								self.player.pos[1]-=6
						else:
							if hole[2]: 
								if android: android.vibrate(0.2)
								hole[2]=False
								self.player.pos[1]+=6
								self.player.odometer+=7
						display.blit(scaled_hole,pos)
		except Exception,e:debugLog(e)
		#verifica os eventos de colisao com cada bueiro fechado
		try:
			for sewer in self.sewers:
				if sewer[0]<=self.player.odometer:
					if self.player.odometer-sewer[0]<=1377:
						sewer_pos_vp=420-getViewport45(400,(255*11)-(self.player.odometer-sewer[0])-1377,150)
						pos=[sewer[1],sewer_pos_vp]
						scale=abs(sewer_pos_vp-150+(sewer_img.get_height()*2.5) )/260
						new_size=(int(sewer_img.get_width()*scale),int(sewer_img.get_height()*scale))
						scaled_sewer=pygame.transform.scale(sewer_img,new_size)
						if sewer[1]<=318:
							pos[0]+= (sewer_img.get_width()/2.5)-new_size[0]
							pos[0]-=(pos[1]/3.5)*(float(abs(318-pos[0]))/150)
						elif sewer[1]>=329:
							pos[0]+=(pos[1]/3.5)*(float(abs(pos[0]-329))/150)
						else:
							pos[0]-=new_size[0]//2
						rect=scaled_sewer.get_rect(topleft=pos)
						if self.player.wheels_box.colliderect(rect):
							if self.player.vel>0: self.player.vel-=self.player.vel*0.1*self.player.desaccel
							if sewer[2]==False and not self.end_game and not self.pause_game:
								if android: android.vibrate(0.2)
								if self.player.vel>0: self.player.vel-=1
								self.score[7]+=1
								debugLog(self.score[7])
								sewer[2]=True
								self.player.pos[1]-=6
						else:
							if sewer[2]: 
								if android: android.vibrate(0.2)
								sewer[2]=False
								self.player.pos[1]+=6
								self.player.odometer+=7
						display.blit(scaled_sewer,pos)
		except Exception,e:debugLog(e)
		#verifica os eventos de colisao com cada obstaculo
		try:
			for obs in self.obstacles:
				if obs[0]<=self.player.odometer:
					if self.player.odometer-obs[0]<=1377:
						obs_pos_vp=420-getViewport45(400,(255*11)-(self.player.odometer-obs[0])-1377,150)
						pos=[obs[2],obs_pos_vp]
						scale=abs(obs_pos_vp-150+(obs[1].get_height()) )/360
						new_size=(int(obs[1].get_width()*scale),int(obs[1].get_height()*scale))
						scaled_obs=pygame.transform.scale(obs[1],new_size)
						if obs[2]<=318:
							pos[0]+= obs[1].get_width()-new_size[0]
							pos[0]-=(pos[1]/3.5)*(float(abs(318-pos[0]))/120)
						elif obs[2]>=329:
							pos[0]+=(pos[1]/3.5)*(float(abs(pos[0]-329))/120)
						else:
							pos[0]-=new_size[0]//2
						rect=scaled_obs.get_rect(topleft=pos)
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
		except Exception,e:debugLog(e)
		
		try:
			for tw in self.tumbleweed:
				if tw[0]<=self.player.odometer:
					if self.player.odometer-tw[0]-tw[1]<=1377:
						tw_pos_vp=420-getViewport45(400,(255*11)-(self.player.odometer-tw[0]-tw[1])-1377,150)
						pos=[tw[2],tw_pos_vp]
						image=tumbleweed_img.getImage()
						scale=abs(tw_pos_vp-150+(image.get_height()) )/360
						new_size=(int(image.get_width()*scale),int(image.get_height()*scale))
						scaled_tw=pygame.transform.scale(image,new_size)
						if tw[2]<=318:
							pos[0]+= image.get_width()-new_size[0]
							pos[0]-=(pos[1]/3.5)*(float(abs(318-pos[0]))/120)
						elif tw[2]>=329:
							pos[0]+=(pos[1]/3.5)*(float(abs(pos[0]-329))/120)
						else:
							pos[0]-=new_size[0]//2
						rect=scaled_tw.get_rect(topleft=pos)
						if self.player.wheels_box.colliderect(rect):
							if self.player.vel>0: self.player.vel-=self.player.vel*0.1*self.player.desaccel
							if tw[3]==False and not self.end_game and not self.pause_game:
								if not self.pause_game:self.player.receiveDamage(1,(0,0))
								if self.drama==0: self.drama=4
								self.player.pos[1]+=40
								if self.player.vel>0: self.player.vel-=1
								self.score[7]+=1
								tw[3]=True
						else:
							if tw[3] and self.drama==0: tw[3]=False
						render_list.blit(scaled_tw,pos)
						if not self.pause_game:tw[1]-=10
		except Exception,e:debugLog(e)
		try:
			for sf in self.solar_filter:
				if sf[0]<=self.player.odometer:
					if self.player.odometer-sf[0]<=1377:
						sf_pos_vp=420-getViewport45(400,(255*11)-(self.player.odometer-sf[0])-1377,150)
						pos=[sf[1],sf_pos_vp]
						image=solarfilter_img
						scale=abs(sf_pos_vp-150+(image.get_height()) )/360
						new_size=(int(image.get_width()*scale),int(image.get_height()*scale))
						scaled_sf=pygame.transform.scale(image,new_size)
						if sf[1]<=318:
							pos[0]+= image.get_width()-new_size[0]
							pos[0]-=(pos[1]/3.5)*(float(abs(318-pos[0]))/120)
						elif sf[1]>=329:
							pos[0]+=(pos[1]/3.5)*(float(abs(pos[0]-329))/120)
						else:
							pos[0]-=new_size[0]//2
						rect=scaled_sf.get_rect(topleft=pos)
						if self.player.wheels_box.colliderect(rect):
							if sf[2] and not self.end_game and not self.pause_game:
								#self.score[7]+=1
								sf[2]=False
								self.player.setScore(100)
								self.glow=3
						if sf[2]: render_list.blit(scaled_sf,pos)
		except Exception,e:debugLog(e)
		
		#verifica os eventos dos cães
		try:
			for dog in self.dogs:
				if dog[0]<=self.player.odometer:
					if self.player.odometer-dog[0]<=1377:
						dog_pos_vp=430-getViewport45(400,(255*11)-(self.player.odometer-dog[0])-1377,150)
						image=dog_img[int(dog[1])].getImage()
						scale=abs(dog_pos_vp-150+(image.get_height()*0.7) )/260
						new_size=(int(scale*image.get_width()),int(scale*image.get_height()))
						dog_image=pygame.transform.scale(image,new_size)
						pos=[390,dog_pos_vp-(dog_image.get_height()*0.7)]
						pos[0]+=pos[1]/1.6
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
		except Exception,e:debugLog(e)
					
		#verifica os eventos de colisao com cada ciclista transeunte
		try:
			biker_counter=0
			for bike in self.bikers:
				if bike.odometer<=self.player.odometer:
					bike_pos_vp=360-getViewport45(400,(255*11)-(bike.pos[1])-1377,150)
					if bike.pos[1]<=1377:
						#flipa
						fliped_bike=pygame.transform.flip(bike.img,bike.flip,False)
						#bike.pos
						scale=abs(bike_pos_vp+(bike.img.get_height()*0.6) )/360  #if bike_pos_vp<self.player.pos[1] else 1
						new_size=(int(bike.img.get_width()*scale),int(bike.img.get_height()*scale))
						scaled_bike=pygame.transform.scale( fliped_bike ,new_size)
						new_pos=[ bike.pos[0], bike_pos_vp+((bike.img.get_height()-new_size[1])//2)]
						if bike.pos[0]<=315:
							new_pos[0]+=bike.img.get_width()-new_size[0]
							new_pos[0]-=(new_pos[1]/3.5)*(float(315-bike.pos[0])/120)
						elif bike.pos[0]>=326:
							new_pos[0]+=(new_pos[1]/3.5)*(float(bike.pos[0]-326+new_size[0])/120)
						else:
							new_pos[0]-=(new_size[0]/2)
						bike_hit_box_x=pygame.Rect(new_pos[0],new_pos[1]+int(new_size[1]*0.2),bike.img.get_width(),int(new_size[1]*0.6))#horizontal
						bike_hit_box_y=pygame.Rect(int(new_pos[0]+new_size[0]*0.2),new_pos[1],int(bike.img.get_width()*0.6),new_size[1])#vertical
						if len(crosswalk_rect)==0: bike.stop=False
						#colisao semaforo
						for crosswalk in crosswalk_rect:
							if bike.accel>0:
								if bike_hit_box_x.colliderect(crosswalk):
									if bike_pos_vp>crosswalk.bottom:
										bike.pos[1]+=(crosswalk.bottom-bike_hit_box_x.y)*2
									else:
										bike.stop=True
										bike.vel=0
								if bike.stop:
									cw_pos=crosswalk.y-bike.img.get_height()
									bike_hit_box_x.y+=cw_pos-new_pos[1]
									new_pos[1]+=cw_pos-bike_pos_vp
									bike_pos_vp=cw_pos
									bike.pos[1]+=self.player.vel
							elif bike.accel<0:
								if bike_hit_box_x.colliderect(crosswalk):
									if bike_pos_vp<crosswalk.y:
										bike.pos[1]+=(crosswalk.y-bike_hit_box_x.bottom)
										bike.vel=bike.max_vel
									else:
										bike.stop=True
										bike.vel=0
								if bike.stop:
									cw_pos=(crosswalk.y+crosswalk.h)
									bike_hit_box_x.y+=cw_pos-new_pos[1]
									new_pos[1]+=cw_pos-bike_pos_vp
									bike_pos_vp=cw_pos
									bike.pos[1]+=self.player.vel
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
						
						if not self.pause_game and not bike.stop: bike.passerbyMotion(self.player.vel)
					
						if bike_pos_vp>30:render_list.blit(scaled_bike ,new_pos )
					#pontuacao para ultrapassagem
					else:
						biker_counter+=1
						if bike_pos_vp<460: 
							self.player.setScore(100)
							bike_pos_vp=460
		except Exception,e:debugLog(e)
		self.score[6]=biker_counter
		#condicao vitoria e derrota
		if self.end_pos<=self.player.odometer:
			self.win=True
		if self.player.damage>=self.player.maxlife: 
			self.lose=True
		if self.blit_player: 
			self.player.blitOn(render_list)
			if self.glow:
				display.blit(glow_img,(self.player.pos[0]-15,self.player.pos[1]+10))
		render_list.sortList()
		render_list.blitOn(display)		
		
		if self.fog:
			global nuvem
			display.blit(nuvem,(0,0))
		if self.night and not self.pause_game:
			self.color=(55,55,155)
			self.alpha=True
		if self.rain==1:
			for n in xrange(100):
				pos=(random.randrange(640),random.randrange(360))
				display.fill((200,200,255),pygame.Rect(pos,(1,(pos[1]*20//360)+1)))
			for n in xrange(50):
				pos=(random.randrange(640),random.randrange(360))
				display.fill((200,200,255),pygame.Rect(pos,(1,20)))
		if self.rain>1:
			direction=1 if self.rain==2 else -1
			for n in xrange(100):
				pos=(random.randrange(640),random.randrange(360))
				size=(1,(pos[1]*7//360)+1)
				display.fill((200,200,255),pygame.Rect(pos,size))
				display.fill((200,200,255),pygame.Rect((pos[0]+direction,pos[1]+size[1]),size))
				display.fill((200,200,255),pygame.Rect((pos[0]+direction*2,pos[1]+(size[1]*2)),size))
			for n in xrange(50):
				pos=(random.randrange(640),random.randrange(360))
				size=(1,7)
				display.fill((200,200,255),pygame.Rect(pos,size))
				display.fill((200,200,255),pygame.Rect((pos[0]+direction,pos[1]+size[1]),size))
				display.fill((200,200,255),pygame.Rect((pos[0]+direction*2,pos[1]+(size[1]*2)),size))
				
		if self.night and not self.pause_game and self.blit_player:
			global light,night_alpha
			display.blit(night_alpha,(0,0))
			display.blit(light,(self.player.pos[0]+30,self.player.pos[1]+110))
		elif self.alpha:
			self.fade.fill(self.color)
			display.blit(self.fade,(0,0))
		
		#informacoes na tela
		if self.pause_game==False or self.tutorial==True:
			#painel fundo
			try:
				if self.blit_panel:self.blitPanel(display,(0,0))
			except Exception,e: debugLog('blitPanel() error:\n\t'+str(e))
			#timer
			try:
				if self.blit_timer:self.blitTimer(display,(5,0))
			except Exception,e: debugLog('blitTimer() error:\n\t'+str(e))
			#speedometer
			#self.blitSpeed(display,(580,150))
			#track
			try:
				if self.blit_track:self.blitTrack(display,(580,77))
			except Exception,e: debugLog('blitTrack() error:\n\t'+str(e))
			#estrela
			try:
				if self.blit_life:self.blitLife(display,(15,39))
			except Exception,e: debugLog('blitLife() error:\n\t'+str(e))
			#coracao level
			try:
				if self.blit_level:self.blitLevel(display,self.heart_pos)
			except Exception,e: debugLog('blitLevel() error:\n\t'+str(e))
			#popup
			try:self.pop_up.blitOn(display)
			except Exception,e: debugLog(e)
		global pedal_1, pedal_2
		#display.blit(pygame.transform.flip(pedal_1,True,False),(640-pedal_1.get_width()-32,360-pedal_1.get_height()-32))
		#display.blit(pedal_2,(32,360-pedal_2.get_height()-32))
		if self.end_game:
			try:display.blit(self.left_side_name,(45,45))
			except Exception,e:debugLog(e)
	def screenManipulation(self,screen):pass
