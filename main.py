# -*- coding: utf-8 -*-
'''
 Programa: Lab na Via
 Objetivo: Incentivar o uso e as boas praticas nas ciclovias, atraves do entretenimento ludico.
 Autor: Lab Prodam
 Data de Inicio: 23/03/2015
'''

import time
import pygame,sys
from pygame.locals import *

FPS=60
pygame.init()

pygame.display.init()
video_info = pygame.display.Info()
full_size_display = (video_info.current_w, video_info.current_h)
scaled_full=(640,int(float(full_size_display[1])/full_size_display[0]*640))
temporary_display = pygame.display.set_mode(scaled_full)

bk_n=0
bk_i=1
from gameTools import dir_menu
loading_image=[pygame.image.load(dir_menu+"carregando-entrada"+str(n)+".png").convert_alpha() for n in xrange(4)]
def loadBlit():
	global temporary_display,bk_n,bk_i
	temporary_display.fill((255,255,255))
	temporary_display.blit(loading_image[bk_n],(0,0))
	pygame.display.flip()
	pygame.time.wait(100)
	bk_n+=bk_i
	if bk_n==3 or bk_n==0:bk_i*=-1

from screenTools import *
loadBlit()
from gameTools import *
loadBlit()
from bikerObject import *
loadBlit()
from popUp import *
loadBlit()
from trafficLight import trafficLight
loadBlit()
from debugLog import *
loadBlit()
from avatarTools import *
loadBlit()
from tutorialTools import*
loadBlit()

if not os.path.exists('data'):
	os.mkdir('data')
	print 'Directory data created!'
else:
	print 'Directory data already exists.'
loadBlit()

####---- ----####
try:
	import android
except ImportError:
	android = None

#controles de janela
class extraControls(object):
	def __init__(self):
		self.esc_bool=False
		self.F4_bool=False
	def eventControler(self,event,resize,move):
		if event.type==KEYUP:
			if event.key==K_ESCAPE:
				self.esc_bool=True
			if event.key==K_F4:
				self.F4_bool=True
	def screenManipulation(self,screen):
		global full_size_display
		if self.esc_bool:
			self.esc_bool=False
			screen.running=False
		if self.F4_bool:
			self.F4_bool=False
			screen.setNewSizeScale(screen.size if screen.full_screen else full_size_display)
			screen.setFullscreen(not screen.full_screen)

def scaleGroup(img_list_origin,scale=0.5):
	img_list=img_list_origin[:]
	for i in range(len(img_list)):
		img_list[i]=pygame.transform.scale(img_list[i],(int(img_list[i].get_width()*scale),int(img_list[i].get_height()*scale)))
	return img_list

def clearFile(data_file):
	opened_file=open(data_file,'wb')
	opened_file.truncate()
	opened_file.close()

#inicializacao dos objetos #################################################################
pause_img =[pygame.image.load(dir_img+'pause.png').convert_alpha(),
			pygame.image.load(dir_img+'pausePress.png').convert_alpha()]

home_img = [pygame.image.load(dir_img+'home.png').convert_alpha(),
			pygame.image.load(dir_img+'homePress.png').convert_alpha()]

retry_img =[pygame.image.load(dir_img+'retry.png').convert_alpha(),
			pygame.image.load(dir_img+'retryPress.png').convert_alpha()]

stages_img =[pygame.image.load(dir_img+'stages.png').convert_alpha(),
			pygame.image.load(dir_img+'stagesPress.png').convert_alpha()]

def centerText(img,font,text,color,pos,h_bool=False):
	center_pos=[]
	for i in range(2):
		center_img=img.get_size()[i]//2
		center_text=font.size(text)[i]//2
		center_pos.append(pos[i]+center_img-center_text)
	render_text=font.render(text,True,color)
	pos_text=(center_pos[0],center_pos[1] if h_bool else pos[1])
	return [render_text,pos_text]

wheel_img	 = pygame.image.load(dir_menu+'menuPausa0.png').convert_alpha()
wheel_pos=640-wheel_img.get_width(),wheel_img.get_rect(center=(640,180)).y
pause_tgscr  = toggleScreen(wheel_img.get_size(),None,(640,wheel_pos[1]),wheel_pos,(-20,0),20,False)
confirm_bg=pygame.image.load(dir_menu+'telaEntrada-SimNaoTransp.png').convert_alpha()
confirmation_tgscr = toggleScreen(confirm_bg.get_size(),confirm_bg,((640-confirm_bg.get_width())//2,360),((640-confirm_bg.get_width())//2,(430-confirm_bg.get_height())//2),(0,-40),0,True)
cartilha_bg=pygame.image.load(dir_menu+'telaCartilhaCiclista.png').convert_alpha()
cartilha_tgscr = toggleScreen(cartilha_bg.get_size(),cartilha_bg,((640-cartilha_bg.get_width())//2,360),((640-cartilha_bg.get_width())//2,(430-cartilha_bg.get_height())//2),(0,-40),0,True)
info_tgscr = toggleScreen((640,360),None,(0,64),(0,0),(0,-64),0)
info_tgscr.turnOn()
menu_tgscr = toggleScreen((640,360),None,(310,0),(0,0),(-38.75,0),0)
menu_tgscr.turnOn()
pause_tgscr.setAngle(180)

pause_button=toggleFunctionButton(pause_tgscr.turnOn,None,scaleGroup(pause_img),(640-(scaleGroup(pause_img)[0].get_width()*1.5),scaleGroup(pause_img)[0].get_height()*0.5))
pause_button.inflateButton( 30,30 )
button_ident=((360-150)/4)+50
buttons_x=100
resume_button=functionButton(lambda : pause_tgscr.turnOn(False),None,[pygame.Surface((50,50),SRCALPHA,32) for x in range(2)],(95,20) )
home_button=functionButton(None,None,[pygame.Surface((50,50),SRCALPHA,32) for x in range(2)],(30,65))
retry_button=functionButton(None,None,[pygame.Surface((50,50),SRCALPHA,32) for x in range(2)],(95,170))

class turnOffScreen(object):
	def __init__(self,scr):
		self.scr=scr
	def preEvents(self):
		self.actived=0
	def eventControler(self,event,resize,move):
		if self.scr.turned_on:
			if event.type==KEYDOWN:
				if event.key==K_SPACE:
					if self.actived==0:self.actived=1
			if event.type==KEYUP:
				if event.key==K_SPACE:
					self.actived+=1
		else:
			self.actived=(-1)
		if self.actived==2:self.scr.turned_on=False


pause_tgscr.addItens(resume_button,home_button,retry_button )

win_img=pygame.image.load(dir_menu+"tela_TabuaVenceu.png").convert_alpha()
lose_img=pygame.image.load(dir_menu+"tela_TabuaPerdeu.png").convert_alpha()
rank_img=pygame.image.load(dir_menu+"tela_Ranking.png").convert_alpha()


retry_button_2=functionButton(None,None,retry_img,((322//2)-(home_img[0].get_width()*0.5),350-home_img[0].get_height()) )
home_button_2=functionButton(None,None,home_img,(53,350-home_img[0].get_height()) )
bg_all=pygame.image.load(dir_img+'bg.png').convert()
scr_stages=screenObject((640,360),FPS,bg_all)
scr_stages.setLoading(pygame.image.load(dir_menu+"loading2.png").convert_alpha())
stages_button=functionButton(None,scr_stages,stages_img,(270-stages_img[0].get_width(),346-stages_img[0].get_height()) )

lista_score=[
	simpleImage(pygame.Surface((0,0)).convert_alpha(),(60,180),True),
	simpleImage(pygame.Surface((0,0)).convert_alpha(),(125,180),True),
	simpleImage(pygame.Surface((0,0)).convert_alpha(),(189,180),True),
	simpleImage(pygame.Surface((0,0)).convert_alpha(),(254,180),True),
	simpleImage(pygame.Surface((0,0)).convert_alpha(),(160,211),True),
	simpleImage(pygame.Surface((0,0)).convert_alpha(),(170,245),True)
	]
scr_win=toggleScreen(win_img.get_size(),win_img,(130,360), (130,370-win_img.get_height() ),(0,-20),0,True, *lista_score)
scr_lose=toggleScreen(lose_img.get_size(),lose_img,(130,360), (130,370-lose_img.get_height() ),(0,-20),0,True,*lista_score)
scr_score=toggleScreen(rank_img.get_size(),rank_img,(455,-rank_img.get_height()), (455,65),(0,20),0,True,simpleImage(pygame.Surface((0,0)).convert_alpha(),(25,85)))
scr_win.addItens(home_button_2,retry_button_2,stages_button)
scr_lose.addItens(home_button_2,retry_button_2,stages_button)

biker_img=pygame.image.load(dir_img+'ciclista.png').convert_alpha()
bikerFront_img=pygame.image.load(dir_img+'ciclistaDeFrente.png').convert_alpha()
b_width=biker_img.get_width()

player=playerObject(10,[375,360-128-4],None,0.5,13)#194

biker_pos_00 = [320-biker_img.get_width(),0-biker_img.get_height()]
biker_pos_01 = [280+biker_img.get_width(),0-biker_img.get_height()]

biker_pos_02 = [300-biker_img.get_width(),0-biker_img.get_height()]
biker_pos_03 = [300+biker_img.get_width(),0-biker_img.get_height()]

biker_pos_04 = [280-biker_img.get_width(),0-biker_img.get_height()]
biker_pos_05 = [320+biker_img.get_width(),0-biker_img.get_height()]

biker_list_1=[
passerbyObject(biker_pos_02,bikerFront_img,0.2,4,20*30),
passerbyObject(biker_pos_03,biker_img,-0.3,-3,35*30),
passerbyObject(biker_pos_04,bikerFront_img,0.15,2,50*30),
passerbyObject(biker_pos_00,bikerFront_img,0.2,2,100*30),
passerbyObject(biker_pos_01,biker_img,-0.4,-4,150*30),
passerbyObject(biker_pos_00,bikerFront_img,0.3,2,184*30),
passerbyObject(biker_pos_03,biker_img,-0.02,-4,234*30),
passerbyObject(biker_pos_02,bikerFront_img,0.15,3,267*30),
passerbyObject(biker_pos_05,biker_img,-0.15,-5,335*30)
]

biker_list_2=[
passerbyObject((275,0-biker_img.get_height()),bikerFront_img,0.2,4,120*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.2,-4,230*30),
passerbyObject((250,0-biker_img.get_height()),bikerFront_img,0.1,5,230*30),
passerbyObject((370,0-biker_img.get_height()),biker_img,-0.1,-3,250*30),
passerbyObject((220,0-biker_img.get_height()),bikerFront_img,0.3,3,320*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.2,-4,400*30),
passerbyObject((340,0-biker_img.get_height()),biker_img,-0.5,-3,480*30),
passerbyObject((275,0-biker_img.get_height()),bikerFront_img,0.2,4,510*30),
passerbyObject((250,0-biker_img.get_height()),bikerFront_img,0.1,5,550*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.3,-4,650*30)
]

biker_list_3=[
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.2,-4,50*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.2,-4,100*30),
passerbyObject((275,0-biker_img.get_height()),bikerFront_img,0.2,4,125*30),
passerbyObject((280,0-biker_img.get_height()),bikerFront_img,0.2,3,150*30),
passerbyObject((350,0-biker_img.get_height()),biker_img,-0.2,-4,225*30),
passerbyObject((260,0-biker_img.get_height()),bikerFront_img,0.3,5,230*30),
passerbyObject((265,0-biker_img.get_height()),bikerFront_img,0.2,4,360*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.2,-4,365*30),
passerbyObject((250,0-biker_img.get_height()),bikerFront_img,0.2,4,430*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.1,-5,420*30),
passerbyObject((275,0-biker_img.get_height()),bikerFront_img,0.4,5,550*30),
passerbyObject((250,0-biker_img.get_height()),bikerFront_img,0.1,3,570*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.2,-4,620*30),
passerbyObject((275,0-biker_img.get_height()),bikerFront_img,0.5,1,650*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.2,-4,750*30),
passerbyObject((280,0-biker_img.get_height()),bikerFront_img,0.2,5,755*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.2,-4,820*30),
passerbyObject((370,0-biker_img.get_height()),biker_img,-0.3,-6,850*30),
passerbyObject((280,0-biker_img.get_height()),bikerFront_img,0.3,6,888*30),
passerbyObject((360,0-biker_img.get_height()),biker_img,-0.2,-4,950*30),
]


trlt_list_1= [
trafficLight(9000,0,2,400,1500),
trafficLight(5000,1,15,300,5000),
trafficLight(9000,-1,5,200,9000)]

trlt_list_2=[
trafficLight(7000,1,8,200,175*30),
trafficLight(5000,0,10,300,350*30),
trafficLight(6000,0,7,420,450*30)
]

trlt_list_3=[
trafficLight(4000,0,5,320,260*30),
trafficLight(5000,1,8,350,480*30),
trafficLight(6000,-1,10,175,575*30),
trafficLight(4000,0,7,420,900*30)
]


obs_list_2=[
50,
80,
100,
180,
190,
210,
280,
320,
350,
420,
480,
500,
530,
540,
670
]

obs_list_3=[
80,
100,
240,
300,
350,
360,
400,
425,
450,
475,
650,
750,
830,
850,
880,
950
]

dog_list_3=[
70,
220,
550,
800,
980
]

sign_img=['placaLab.png','placaPref.png','placaGestao.png','placaSPAberta.png','placaSPCultura.png','placa00.png']
sign_list=[ pygame.image.load(dir_img+placa).convert_alpha() for placa in sign_img]


fundo_inicio=pygame.image.load(dir_menu+'bg_menu.png').convert()

back_button_img=[pygame.image.load(dir_img+"back_button.png").convert_alpha(),pygame.image.load(dir_img+"back_buttonOn.png").convert_alpha()]
inviButton=[pygame.Surface((32,32),SRCALPHA,32)]
avatarBorda=pygame.image.load(dir_img+"avatarBorda.png").convert_alpha()
backb_pos=(30,5)
back_button=backButton(back_button_img,backb_pos)
scr_start=screenObject((640,360),FPS,fundo_inicio)
button_img_no=[pygame.image.load(dir_menu+'button_no'+str(n)+'.png').convert_alpha() for n in xrange(2)]
button_img_yes=[pygame.image.load(dir_menu+'button_yes'+str(n)+'.png').convert_alpha() for n in xrange(2)]
confirmation_tgscr.addItens(functionButton(lambda : [confirmation_tgscr.turnOn(False),menu_tgscr.turnOn(),info_tgscr.turnOn()],None,button_img_no,(confirm_bg.get_width()-button_img_no[0].get_width()-50,145) ),
							functionButton(scr_start.closeGame,None,button_img_yes,(50,145) )
							)
cartilha_tgscr.addItens(functionButton(lambda : [cartilha_tgscr.turnOn(False),menu_tgscr.turnOn(),info_tgscr.turnOn()],None,button_img_no,(confirm_bg.get_width()-button_img_no[0].get_width()-50,178) ),
							urlButton("http://www.issuu.com/cetsp/docs/CartilhaDoCiclista",button_img_yes,(50,178) )
							)
home_back_button=functionButton(lambda:[tuto_tgscr.turnOn(False),stages_tgscr.turnOn(False),options_tgscr.turnOn(False),delete_tgscr.turnOn(False)],scr_start,back_button_img,backb_pos)
#home_from_options=functionButton(lambda:[options_tgscr.turnOn(False),delete_tgscr.turnOn(False)],scr_start,back_button_img,backb_pos)
clear_back_button=backButton(back_button_img,backb_pos,None,True)
back_button.inflateButton(70,70)
clear_back_button.inflateButton(70,70)
home_back_button.inflateButton(70,70)
onOffButton=[pygame.image.load(dir_img+"onOff"+str(x)+".png").convert_alpha()for x in xrange(3)]

scr_gps=screenObject((640,360),FPS,bg_all)

options_tgscr=toggleScreen((640,360),None,(0,0),(640,0),(64,0))
options_tgscr.hideTurnedOff(False)
scr_options=screenObject((640,360),FPS,bg_all,options_tgscr)

mute=functionButton(lambda:[setMuteMusic(True),mixer.music.stop()],None,[onOffButton[1],onOffButton[2]],(400,200),None)
unmute=functionButton(lambda:[setMuteMusic(False),mixer.music.play()],None,[onOffButton[0],onOffButton[2]],(400,200),None)
mute_unmute=buttonList(mute,unmute)

gpsingame_on=functionButton(setAutoGpsIngame,None,[onOffButton[1],onOffButton[2]],(400,150),None,None,False)
gpsingame_off=functionButton(setAutoGpsIngame,None,[onOffButton[0],onOffButton[2]],(400,150),None,None,True)
gpsingame_onoff=buttonList(gpsingame_on,gpsingame_off)


scr_tutorial=screenObject((640,360),FPS,(100,255,100))
scr_about=screenObject((640,360),FPS,bg_all )


scr_about_img_logos = pygame.image.load(dir_img+"bgsobre01_partedebaixo.png").convert_alpha()
scr_about_img_links = pygame.image.load(dir_img+"bgsobre01_partedecima.png").convert_alpha()

avatar_background=[68,68,137]
apagar_roda_avatar=pygame.Surface((50,100), pygame.SRCALPHA, 32)
scr_about_headline=pygame.image.load(dir_img+"topSobre.png").convert_alpha()
scr_tutorial_headline=pygame.image.load(dir_img+"topTutorial.png").convert_alpha()
scr_options_headline=pygame.image.load(dir_img+"topOpcoes.png").convert_alpha()
scr_avatar_headline=pygame.image.load(dir_img+"topAvatar.png").convert_alpha()
scr_gps_headline=pygame.image.load(dir_img+"topCultura.png").convert_alpha()
scr_stages_headline=pygame.image.load(dir_img+"topJogar.png").convert_alpha()

for y in xrange(11):
	apagar_roda_avatar.fill(avatar_background+[(y*25)+4],pygame.Rect((0,y*4),apagar_roda_avatar.get_size() ))
scr_avatar=screenObject((640,360),FPS,bg_all,playerImage(player,(315,80),1.5 ), simpleImage(apagar_roda_avatar,(360,270)), simpleImage(avatarBorda, (580,0)) )
for scr in [scr_avatar,scr_about,scr_tutorial]:
	scr.setEscFunction(back_button.callActivation)


try:
	arq=open("tuto_data.plab","rb")
	first_time_tutorial=cPickle.load(arq)
	arq.close()
except:
	first_time_tutorial=True

def setFirstTime(boolean=True):
	global first_time_tutorial
	arq=open("tuto_data.plab","wb")
	if boolean:
		arq.truncate()
		first_time_tutorial=True
	else:
		first_time_tutorial=False
	cPickle.dump(first_time_tutorial,arq)
	arq.close()
tuto_confirm_bg=pygame.image.load(dir_menu+"telaTutorial-SimNao.png").convert_alpha()
tuto_tgscr=toggleScreen((640,360),tuto_confirm_bg,((640-tuto_confirm_bg.get_width())//2,360),((640-tuto_confirm_bg.get_width())//2,(420-tuto_confirm_bg.get_height())//2),(0,-36))
tuto_tgscr.addItens(functionButton(lambda : [tuto_tgscr.turnOn(False),stages_tgscr.turnOn(False),setFirstTime(False),stages_buttons[0].setLink(scr_stage_01),stages_buttons[0].callActivation()],None,button_img_no,(confirm_bg.get_width()-button_img_no[0].get_width()-50,145) ),
							functionButton(lambda : [tuto_tgscr.turnOn(False),stages_tgscr.turnOn(False),setFirstTime(False),stages_buttons[0].setLink(scr_stage_01)],scr_tutorial,button_img_yes,(50,145))
					)
stages_tgscr=toggleScreen((640,360),None,(0,0),(640,0),(64,0))
scr_stages.setEscFunction(lambda : [home_back_button.callActivation() if not tuto_tgscr.turned_on else [tuto_tgscr.turnOn(False),stages_tgscr.turnOn(False)]])
scr_gps.setEscFunction(clear_back_button.callActivation)
scr_options.setEscFunction(lambda:[options_tgscr.turnOn(False),delete_tgscr.turnOn(False)] if delete_tgscr.turned_on else home_back_button.callActivation())
scr_start.setEscFunction(lambda: [ cartilha_tgscr.turnOn(False) if cartilha_tgscr.turned_on else confirmation_tgscr.toggleOnOff(),menu_tgscr.toggleOnOff(),info_tgscr.toggleOnOff()])
if basic_debug:
	scr_gps.setTitle("Lab na Via - GPS")
	scr_avatar.setTitle("Lab na Via - Avatar")
	scr_options.setTitle("Lab na Via - Options")
	scr_tutorial.setTitle("Lab na Via - Tutorial")
	scr_about.setTitle("Lab na Via - About")
#AVATAR PERSONALIZADO:
#'''
shoes=[u"Papete Azul","Sapato Marrom", u"Tênis Verde"]
pants=[u"Calça Jeans Azul",u"Calça Verde",u"Shorts Esportivo",u"Calça Jeans Preta",u"Calça Branca","Shorts Esportivo com Saia"]
shirt=["Camisa Social Branca","Regata Azul","Blusa Verde","Camisa da CET","Blusa Preta Estampada","Regata Rosa","Camisa Social Acizentada","Camisa Social Rosa"]
hair=["Castanho Curto","Ruivo Cacheado","Loiro Curto","Preto Arrepiado","Loiro Escuro Longo","Castanho Cacheado","Rabo de Cavalo Acobreado","Black Power","Topete Loiro"]
head=["Capacete Azul","Capacete Rosa","Elmo Grego",u"Chapéu de Pierrot","Elmo de Hermes",u"Chapéu de Palha"]
avatar_tools=avatarTools(player
	#,[pygame.image.load(dir_avatar+'skin'+str(x)+'.png').convert_alpha() for x in range(3)]
	,[[pygame.image.load(dir_avatar+'shoes'+str(x)+'.png').convert_alpha(),shoes[x]] for x in range(3)]
	,[[pygame.image.load(dir_avatar+'pants'+str(x)+'.png').convert_alpha(),pants[x]] for x in range(6)]
	,[[pygame.image.load(dir_avatar+'shirt'+str(x)+'.png').convert_alpha(),shirt[x]] for x in range(8)]
	,[[pygame.image.load(dir_avatar+'hair'+str(x)+'.png').convert_alpha(),hair[x]] for x in range(9)]+[[pygame.Surface((1,1), pygame.SRCALPHA, 32),"Careca"]]
	,[[pygame.image.load(dir_avatar+'head'+str(x)+'.png').convert_alpha(),head[x]] for x in range(6)]+[[pygame.Surface((1,1), pygame.SRCALPHA, 32),"Desprotegido"]]
	,(0,0)
	,72
	)

skin_tgscr=toggleScreen((640,360),None,(-220,0),(0,0),(22,0),0,False )
color_picker=colorPickerHLS((10,240),(0.556,1),(10,180),(2,40),None,None,(32,50,44),avatar_tools.setSkinColor)

titulo_skin=textBox("Selecione a\ncor da pele",dinB_22,220)
skin_tgscr.addItens(simpleRect((58,134,152),pygame.Rect(0,110,220,250)),color_picker,simpleImage(titulo_skin,(titulo_skin.get_rect(center=(110,0)).left,120) ))
scr_avatar.addItens(avatar_tools,skin_tgscr)#,color_confirm)#,*skin_buttons)

limpar_button=[pygame.image.load(dir_img+'limpar'+str(x)+'.png').convert_alpha()for x in xrange(2)]

class radioList(object):
	def __init__(self,buttons):
		self.buttons=buttons
	def setSelected(self,sk):
		for button in self.buttons:
			button.setSkin(0)
		print sk
		self.buttons[sk].setSkin(1)

move_img=[pygame.image.load(dir_img+'arrow'+str(x)+'.png').convert_alpha() for x in xrange(2)]
move_buttons=[functionButton(avatar_tools.moveFocus,None,[pygame.transform.flip(move_img[x],y==0,False) for x in xrange(2)],((y*250)+220,288),None,None,(y*2)-1) for y in xrange(2)]
avatar_buttons=[]
radio_list=radioList(avatar_buttons)
for a in range(5):
	avatar_buttons.append(functionButton(lambda x : [avatar_tools.focusAvatar(x),radio_list.setSelected(4-x), skin_tgscr.turnOn(False)]+[move_buttons[y].setHide(False) for y in range(2)] ,None,[pygame.image.load(dir_avatar+'icon'+str(a)+'0.png').convert_alpha()],(580,a*60),None,None,4-a ) )
	avatar_buttons[-1].addSkin([pygame.image.load(dir_avatar+'icon'+str(a)+'1.png').convert_alpha()])
avatar_buttons.append(functionButton(lambda x:[skin_tgscr.turnOn(),radio_list.setSelected(x),avatar_tools.focusAvatar(x)]+[move_buttons[y].setHide() for y in range(2)],None,[pygame.image.load(dir_avatar+'icon50.png').convert_alpha()],(580,300),None,None,5) )
avatar_buttons[-1].addSkin([pygame.image.load(dir_avatar+'icon51.png').convert_alpha()])
scr_avatar.addItens(*avatar_buttons)
scr_avatar.addItens(*move_buttons)

loadBlit()

avatar_tools.setSkinColor((191,143,88))
avatar_tools.preEvents()
avatar_buttons[0].callActivation()

#AVATAR PERSONAGENS:

gps_item=None
loadBlit()
if android:
	brake_img=[pygame.image.load(dir_img+'brakeN.png').convert_alpha(),pygame.image.load(dir_img+'brakeC.png').convert_alpha()]
	move_img=[pygame.image.load(dir_img+'botaoTeste.png').convert_alpha()]#scaleGroup([])[0]  Agora isso tá lá em cima nos avatares
	
	right_button=toggleFunctionButton(
		lambda: player.playerAccel(+1), 							#click_function
		None,														#link
		move_img,													#img
		(640-move_img[0].get_width()-32,360-move_img[0].get_height()-32),	#pos
		None,														#text
		lambda: player.playerMove(+1))								#press_function

	left_button=toggleFunctionButton(lambda: player.playerAccel(-1),None,[pygame.transform.flip(move,True,False) for move in move_img],(32,360-move_img[0].get_height()-32),None,lambda: player.playerMove(-1))
	right_button.inflateButton(128,55)
	left_button.inflateButton(128,55)
	brake_button=toggleFunctionButton(lambda: [player.playerBrake(0.5),left_button.callActivation(False),right_button.callActivation(False)],None,brake_img,(160,360-brake_img[0].get_height()),None,lambda: player.playerBrake(8))
	brake_button.inflateButton(0,100)
	
	from jnius import *
	from geo import*
	lastUpdateText = renderText(chic_22,u"Última Atualização:", (255,255,255),(30,180))
	lastUpdateTime = renderText(chic_16,u"-", (255,255,255),(30,210))
	atualizar_button=[pygame.image.load(dir_img+'int-CultbtnAtualizaOff.png').convert_alpha(),
						   pygame.image.load(dir_img+'int-CultbtnAtualizaOn.png').convert_alpha()]
						   
	infogps_img=scaleGroup([pygame.image.load(dir_img+'info.png').convert_alpha(),
				pygame.image.load(dir_img+'infoPress.png').convert_alpha()])
	loadBlit()
	class verificadorGPS(object):
		def __init__ (self,screen, parentScreen = None):
			self.cgps_hardware = autoclass("com.lab.labnavia.Hardware")
			self.gps_hardware = self.cgps_hardware()
			self.locationManager = self.gps_hardware.startLocationManager()
			self.gps_hardware.startLocationUpdater(self.locationManager,10000,1)
			loc=self.gps_hardware.location
			self.lnglat=(loc.longitude,loc.latitude,1500)
			url=('http://spcultura.prefeitura.sp.gov.br/api/space/find?@select=id,',
				 '&@order=name%20ASC&_geoLocation=GEONEAR')
			self.finder=findUrl(url,self.lnglat,"name","location")#,"horario","site","acessibilidade")
			self.auto=False
			self.screen=screen
			self.parentScreen = parentScreen
			self.loading=False
		def toggleAuto(self):
			self.auto = not self.auto
			self.loading=self.auto
			pygame.time.set_timer(USEREVENT+6,1500 if self.auto else 0)
			print self.auto
		def preEvents(self):
			self.posEvents()
		def posEvents(self):
			pygame.time.set_timer(USEREVENT+6,0)
			self.loading=False
		def getLocation(self):
			loc=self.gps_hardware.location
			return (loc.longitude,loc.latitude,1500)
		def setLastUpdate(self):
			try:
				global lastUpdateTime
				timeStr = time.strftime("%d/%m/%y - %H:%M", time.localtime())
				lastUpdateTime.setNewText(timeStr)
			except Exception as ex:
				print "setLastUpdate Error:\n\t"+str(ex)				
		def update(self):
									
			loc=self.gps_hardware.location
			self.lnglat=(loc.longitude,loc.latitude,1500)
			if self.lnglat[0]!=0.0 and self.lnglat[1]!=0.0:
				debugGps('localização válida')
				self.finder.run(self.lnglat)
				dict_locals=self.finder.getLocals()
				distances=self.finder.getDistances()
				dict_events=self.finder.getEvents()
				box_list=[]
				linkSpace=[]
				linkEvent=[]
				debugGps('encontrou '+str(len(dict_locals))+' locais')
				if len(dict_locals)>0:
					text=dinB_22.render("LOCAIS",True,(255,255,255))
					surf=pygame.Surface((330,text.get_height()+30))
					surf.fill((150,200,200))
					surf.blit(text,(10,10))
					box_list.append( (simpleImage(surf,(15,15)),None) )
				#Top separator
				surf=pygame.Surface((0, 0))
				surf.fill((0,0,0,0))
				pos=box_list[-1][0].img.get_height()+box_list[-1][0].pos[1]
				box_list.append( (simpleImage(surf,(15,pos)),None) )
				num_elements = len(dict_locals)
				for i in range(num_elements):
					text_1=textBox(unicode(dict_locals[i]['name']),dinB_16,330-((20+15+25)*2),(255,255,255))
					text_2=textBox(u'\nDistância : '+unicode(int(distances[i]))+' metros',dinL_12,330-((52+15)*2),(255,255,255))
					surf_h=text_1.get_height()+text_2.get_height()+30
					surface=pygame.Surface((330,surf_h if surf_h>70 else 70))
					surface.fill((9,78,129))
					surface.blit(text_1,(10,10))
					surface.blit(text_2,(10,10+text_1.get_height()))
				
					if i < num_elements -1:
						separator=pygame.Surface((330,5))
						separator.fill((9,90,148))
						surface.blit(separator, (0, surface.get_height()-5))

					pos=box_list[-1][0].img.get_height()+box_list[-1][0].pos[1]
					box_list.append((
										simpleImage(surface, (15, pos)),										
										urlButton(
											"http://spcultura.prefeitura.sp.gov.br/busca/##(global:(enabled:(event:!t,space:!t),filterEntity:"
											+"space"
											+",map:(center:(lat:"
											+str(self.lnglat[1])+",lng:"+str(self.lnglat[0])
											+"),zoom:15),openEntity:(id:"+str(dict_locals[i]["id"])
											+",type:"+"space"+")))"
											,infogps_img,(270,pos + 7)),
									))
				debugGps('buscando '+str(len(dict_events))+' eventos')
				if len(dict_events)>0:
					text=dinB_22.render("EVENTOS",True,(255,255,255))
					surf=pygame.Surface((330,text.get_height()+30))
					surf.fill((150,200,200))
					surf.blit(text,(10,10))
					pos=box_list[-1][0].img.get_height()+box_list[-1][0].pos[1]
					box_list.append( (simpleImage(surf,(15,pos)),None) )
				num_elements = len(dict_events)
				for i in range(0,num_elements):
					text_1=textBox(unicode(dict_events[i]['name']),dinB_16,330-((20+15+25)*2),(255,255,255))
					surf_h=text_1.get_height()+30
					surface=pygame.Surface((330,surf_h if surf_h>70 else 70))
					surface.fill((9,78,129))
					surface.blit(text_1,(10,10))
					
					if i < num_elements -1:
						separator=pygame.Surface((330,5))
						separator.fill((9,90,148))
						surface.blit(separator, (0, surface.get_height()-5))
					
					pos=box_list[-1][0].img.get_height()+box_list[-1][0].pos[1]
					box_list.append(
										(
										simpleImage(surface,(15,pos) ),
										urlButton(
											"http://spcultura.prefeitura.sp.gov.br/evento/"+str(dict_events[i]["id"])
											,infogps_img,(270,pos + 7))
										)
									)
									
				debugGps('deletando itens antigos')
				debugGps(len(self.screen.itens))
				try:self.screen.delAllItens()
				except Exception,e:print e
				debugGps(len(self.screen.itens))
				debugGps('adicionando itens novos')
				for item in box_list:
					self.screen.addItens(item[0],item[1])
				debugGps('definindo novo tamanho do display')
				size=( self.screen.display.get_width(),box_list[-1][0].img.get_height()+box_list[-1][0].pos[1]+15 )
				self.screen.display=pygame.Surface(size)
				debugGps('seting_timer')
				pygame.time.set_timer(USEREVENT+6,120000 if self.auto else 0)
				debugGps('loading=false')
				self.loading=False
				debugGps('done')
				self.setLastUpdate()
			else:
				debugGps('localização nula')
				pygame.time.set_timer(USEREVENT+6,15000)
		def loadUpdate(self):
			global openUrl
			if self.loading==False:
				self.loading=True
				pygame.time.set_timer(USEREVENT+6,0)
		def eventControler(self,event,resize,move):
			if event.type==USEREVENT+6:
				self.loadUpdate()
		def blitOn(self,display):
			if self.loading: 
				text_render=dinBd_32.render("CARREGANDO . . .",True,(255,255,0))
				text_rect=text_render.get_rect()
				text_rect.center=display.get_rect().center
				display.blit(text_render,text_rect.topleft)
				self.update()
	loadBlit()
	inner_screen=innerScreen((330,600),(0,0),None)
	outer_screen=innerScreen((440,360),(300,0),None,
		inner_screen,
		innerScroller(inner_screen,10,1,(9,90,148),(9,78,129))
	)	
		
	gps_item=verificadorGPS(inner_screen, scr_gps)
	alerta=textBox(u"Este mecanismo necessita acesso\nao GPS e à Internet do seu celular",chic_14,320,(255,255,255))
	scr_gps.addItens(simpleImage(alerta,(33,310)))
	
	scr_gps.addItens(outer_screen,
		gps_item,
		lastUpdateText,
		lastUpdateTime,
		functionButton(gps_item.update,None,atualizar_button,(25,250))
		)
	
###########---------------------------FASES---------------------------###########
stage_01=gameObject(
		"Fase 1",
		400*30,
		pygame.image.load(dir_menu+"odometro_400m.png").convert_alpha(),
		player,
		biker_list_1,
		trlt_list_1,
		[],
		[],
		sign_list,
		
		scr_lose,
		scr_win,
		scr_score,
		[retry_button,retry_button_2],
		[home_button,home_button_2],
		stages_button,
		pause_button,
		resume_button,
		pause_tgscr,
		[right_button,left_button,brake_button] if android else [],
		gps_item
		)
loadBlit()
stage_02=gameObject(
		"Fase 2",
		700*30,
		pygame.image.load(dir_menu+"odometro_700m.png").convert_alpha(),
		player,
		biker_list_2,
		trlt_list_2,
		obs_list_2,
		[],
		sign_list,
		
		scr_lose,
		scr_win,
		scr_score,
		[retry_button,retry_button_2],
		[home_button,home_button_2],
		stages_button,
		pause_button,
		resume_button,
		pause_tgscr,
		[right_button,left_button,brake_button] if android else [],
		gps_item
		)
loadBlit()		
stage_03=gameObject(
		"Fase 3",
		1000*30,
		pygame.image.load(dir_menu+"odometro_1000m.png").convert_alpha(),
		player,
		biker_list_3,
		trlt_list_3,
		obs_list_3,
		dog_list_3,
		sign_list,
		
		scr_lose,
		scr_win,
		scr_score,
		[retry_button,retry_button_2],
		[home_button,home_button_2],
		stages_button,
		pause_button,
		resume_button,
		pause_tgscr,
		[right_button,left_button,brake_button] if android else [],
		gps_item
		)
loadBlit()

scr_stage_01=screenObject((640,360),FPS,(100,0,0), stage_01 ,extraControls(),pause_button,pause_tgscr,scr_lose,scr_win,scr_score)
if android: scr_stage_01.addItens(right_button,left_button,brake_button)
scr_stage_01.setTitle("Lab na Via")
scr_stage_01.showFps()

scr_stage_02=screenObject((640,360),FPS,(100,0,0), stage_02 ,extraControls(),pause_button,pause_tgscr,scr_lose,scr_win,scr_score)
if android: scr_stage_02.addItens(right_button,left_button,brake_button)
scr_stage_02.setTitle("Lab na Via")
scr_stage_02.showFps()

scr_stage_03=screenObject((640,360),FPS,(100,0,0), stage_03 ,extraControls(),pause_button,pause_tgscr,scr_lose,scr_win,scr_score)
if android: scr_stage_03.addItens(right_button,left_button,brake_button)
scr_stage_03.setTitle("Lab na Via")
scr_stage_03.showFps()
for scr in [scr_stage_01,scr_stage_02,scr_stage_03]:
	#hardcode no primeiro if do lambda
	scr.setEscFunction(lambda: [[stages_button.callActivation()] if stage_01.end_game or stage_02.end_game or stage_03.end_game else [resume_button.callActivation() if pause_tgscr.turned_on else pause_button.callActivation()]] )


stages_buttons=[
	functionButton(lambda : [[stages_tgscr.turnOn(),tuto_tgscr.turnOn()] if first_time_tutorial else None ],None if first_time_tutorial else scr_stage_01,[pygame.image.load(dir_menu+"stage0_"+str(x)+".png").convert_alpha() for x in xrange(2)],[0,100])
]+[
	linkButton(scr,[pygame.image.load(dir_menu+"stage"+str(s+1)+"_"+str(x)+".png").convert_alpha() for x in xrange(2)],[220*(s+1),100] )
	for s,scr in enumerate([scr_stage_02,scr_stage_03])
]

for b in xrange(1,3,1):
	stages_buttons[b].setHide(True)
	stages_buttons[b].setLock(True)

try:
	load_stages=open(dir_data+"stages_data.lab","rb")
	load_stages.close()
except:pass
stage_01.setUnlock(stages_buttons[1])
stage_02.setUnlock(stages_buttons[2])
for stage in [stage_01,stage_02,stage_03]:
	stage.loadScore()


stages_tgscr.addItens(*[simpleImage(pygame.image.load(dir_menu+"stage"+str(s)+"_2.png").convert_alpha(),(220*s,100) ) for s in xrange(1,3,1)]+stages_buttons)
stages_tgscr.hideTurnedOff(False)
scr_stages.addItens(stages_tgscr,tuto_tgscr)

scr_and_text=[
			  (scr_stages,u'Jogar')
			  ,(scr_avatar,u'Avatar')
			  ,(scr_options,u'Opções')
			  ,(scr_gps,u'Cultura')
			  ,(scr_tutorial,u'Tutorial')
			  ,(scr_about,u'Sobre')
			  ]

loadBlit()
if not android:
	culture_url="http://spcultura.prefeitura.sp.gov.br/busca/##(global:(enabled:(event:!t,space:!t),filterEntity:event))"

class idleBikers(object):
	def __init__(self, min_time,max_time,event,imgs,moves):
		self.min_time=min_time
		self.max_time=max_time
		self.event=event
		self.imgs_list=imgs
		self.moves_list=moves
		self.diff=[0,0]
		self.preEvents()
	def preEvents(self):
		try:
			pygame.time.set_timer(self.event,random.randint(self.min_time,self.max_time))
			self.draw=False
			self.vel=random.randint(1,5)
			self.img=random.choice(self.imgs_list)
			self.move=random.choice(self.moves_list)
			self.pos=self.move[0][0]
			self.move_state=0
		except Exception,e:print 'pre: '+str(e)
	def posEvents(self):
		try:
			pygame.time.set_timer(self.event,0)
			self.draw=True
		except Exception,e:print 'pos: '+str(e)
	def eventControler(self,event,resize,move):
		try:
			if event.type==self.event:
				self.posEvents()
		except Exception,e:print 'event: '+str(e)
	def idleMotion(self):
		self.pos=[self.pos[x]+(self.move[self.move_state][1][x]*self.vel) for x in xrange(2)]
		move=self.move[self.move_state+1][0]
		try:
			previous_move=self.move[self.move_state][0]
			diff = [1 if previous_move[n]>move[n] else -1 for n in xrange(2)]
		except:
			diff = [1,1]
		if self.pos[0]<=move[0]*diff[0] or self.pos[1]<=move[1]*diff[1]:
			self.move_state+=1
			if self.move_state==len(self.move)-1:
				self.preEvents()
	def blitOn(self,display):
		try:
			if self.draw:
				self.idleMotion()
				display.blit(self.img[self.move_state],self.pos)
		except Exception,e:print 'blit: '+str(e)

menu_tgscr.addItens(geniusButton((142,134),60,120,[pygame.image.load(dir_menu+'menu'+str(x)+'.png').convert_alpha() for x in range(6)],(335,47),[scr_gps if android else culture_url,scr_avatar,scr_options,scr_tutorial,scr_stages],[mixer.Sound(dir_sound+"buttonSound.mp3"),0] ))#(0,0)=(335,47)
info_tgscr.addItens(linkButton(scr_about,[pygame.image.load(dir_menu+'sobre'+str(x)+'.png').convert_alpha() for x in range(2)],(16,296)))#(0,0)=(16,296)
loadBlit()
pygame.time.set_timer(USEREVENT+2,400)
c_ciclista_animation=animatedSprite(pygame.image.load(dir_img+"cciclista_off.png").convert_alpha(),pygame.Rect(0,0,70,70),(0,0),USEREVENT+2)
scr_start.addItens( 
						idleBikers(500,5000,USEREVENT+6,
							[[pygame.image.load(dir_bikers+"biker"+str(x)+str(y)+".png").convert_alpha() for y in xrange(1,-1,-1)]for x in xrange(3)],
							[[ [(-80,75),(1,-0.245)]
							, [(500,-65),(-1,0.245)]
							, [(-80,100)]]]),
						idleBikers(1500,5500,USEREVENT,
							[[pygame.image.load(dir_bikers+"biker"+str(x)+str(y)+".png").convert_alpha() for y in xrange(2)]for x in xrange(3)],
							[[ [(640,-25),(-1,0.29)]
							, [(200,300),(1,-0.29)]
							, [(640,-20)]]]),
						idleBikers(1000,6000,USEREVENT+1,
							[[pygame.image.load(dir_bikers+"biker"+str(x)+str(y)+".png").convert_alpha() for y in xrange(2)]for x in xrange(3)],
							[[ [(640,60),(-1,0.33)]
							, [(200,300),(1,-0.33)]
							, [(640,60)]]]),
						functionButton(lambda:[cartilha_tgscr.turnOn(),info_tgscr.turnOn(False),menu_tgscr.turnOn(False),confirmation_tgscr.turnOn(False)],None,[c_ciclista_animation,pygame.image.load(dir_img+"cciclista_on.png").convert_alpha()], (100,289)),
						extraControls(),
						info_tgscr,
						menu_tgscr,
						confirmation_tgscr,
						cartilha_tgscr )

#tutorial
screenshot_0=pygame.image.load(dir_img+"tuto0.png").convert()
screenshot_1=pygame.image.load(dir_img+"tuto1.png").convert()
screenshot_2=pygame.image.load(dir_img+"tuto2.png").convert()
screenshot_3=pygame.image.load(dir_img+"tuto3.png").convert()
screenshot_4=pygame.image.load(dir_img+"tuto4.png").convert()
screenshot_5=pygame.image.load(dir_img+"tuto5.png").convert()
screenshot_6=pygame.image.load(dir_img+"tuto6.png").convert()
screenshot_7=pygame.image.load(dir_img+"tuto7.png").convert()
screenshot_8=pygame.image.load(dir_img+"tuto8.png").convert_alpha()
#icone de mãos
mao_icone_baixo=pygame.image.load(dir_img+"maoBaixo.png").convert_alpha()
mao_icone_cima=pygame.image.load(dir_img+"maoCima.png").convert_alpha()
ponteiro=pygame.image.load(dir_img+"ponteiro.png").convert_alpha()
ponteiro_cima=pygame.transform.flip(ponteiro,False,True)

lista_de_fases=[tutorialFases(u"Início",pygame.Rect(220,110,200,60), screenshot_0,mao_icone_cima,(290,140)),
				tutorialFases(u"Toque alternadamente as setas para pedalar",pygame.Rect(32,258,50,70), screenshot_1,mao_icone_baixo,(32,200)),
				tutorialFases(u"Mantenha uma das setas pressionada\npara usar o guidão\ne mover-se lateralmente.",pygame.Rect(555,258,50,70), screenshot_2,mao_icone_baixo,(555,200)),
				tutorialFases(u"O freio é útil para evitar acidentes e respeitar o trânsito",pygame.Rect(160,300,320,60),screenshot_3,mao_icone_baixo,(300,250)),
				tutorialFases(u"As placas à direita da pista podem\nexibir pontos culturais próximos a você. \nAtive GPS e internet para vê-los!",pygame.Rect(460,180,119,75),screenshot_4,ponteiro,(480,90)),
				tutorialFases(u"Cuidado, sua proteção pode sofrer danos ao colidir.\n Preste atenção na sua proteção, \nela é representada por estes capacetes.",pygame.Rect(0,110,70,70),screenshot_5,ponteiro_cima,(0,160)),
				tutorialFases(u"Você pode recuperar sua proteção \nusando a sua saúde acumulada na corrida, \npara isso clique neste coração.",pygame.Rect(0,180,60,50),screenshot_6,mao_icone_baixo,(0,120)),
				tutorialFases(u"Os corações são coletados a cada 200 metros da pista.\nO círculo vermelho representa a sua posição na pista.",pygame.Rect(580,65,60,200),screenshot_7,ponteiro_cima,(580,240)),
				tutorialFases(u"Seja cuidadoso, aproveite os benefícios da pedalada e bom passeio!",pygame.Rect(180,230,280,60),screenshot_8,mao_icone_cima,(300,280))]
tutorial=tutorialObject(lista_de_fases,scr_stages)

scr_tutorial.addItens(tutorial)

posText= (30,20+scr_about_img_links.get_height())
about_text=textBox(u'''O jogo "LabNaVia" é uma inciativa do LabProdam em conjunto com a Prefeitura de São Paulo que tem por objetivo consolidar a cultura do ciclismo na vida do cidadão. Alinhado com o ideário do São Paulo Aberta (saopauloaberta.prefeitura.sp.gov.br), o jogo enquadra-se na agenda de Governo Aberto, que tem como objetivo articular ações de transparência, integridade, participação popular e inovação tecnológica em todo ciclo de políticas públicas.
					\nUtilizando os desafios encontrados nas vias públicas, o "LabNaVia" não só educa o jogador, incentivando-o à pratica esportiva e a conduta adequada às ciclovias, como também o convida a explorar os equipamentos culturais de seu município: através da geolocalização em conjunto com os mapas culturais - iniciativa do SP Cultura - o jogo é capaz de exibir de maneira interativa informações de eventos, espaços e agentes de cultura próximos de sua posição.
					\nA idéia deste projeto foi divertir, incentivar e informar com um produto do governo. 
					\n"LabNaVia" é software livre sob a licença CC-GNU-GPL e seu código pode ser obtido no GitHub do LabProdam:\nhttps://github.com/LabProdam\nEncorajamos nossos jogadores a enviarem críticas, dúvidas, sugestões e aprimoramentos para a nossa equipe.
					\nDesenvolvedores: Fernando Luiz Neme, Guilherme de Almeida e Sabrina Tomy.
					\nApoio: Alexandre Calil, Caio Bedulli, Fernanda Tamaio, \nJCarlos ‘Billy’ Costa, Paulo Spinelli.
					\nFerramentas utilizadas: Python, Pygame e Pygame Subset for Android.'''
					,chic_16,580,(255,255,255)).convert_alpha()
about_text_img=simpleImage(about_text,posText)

about_text_data=textBox("Data: Setembro/2015",chic_16,640,(255,255,255)).convert_alpha()
about_data_img=simpleImage(about_text_data,(posText[0]+about_text.get_width()-about_text_data.get_width()-50,posText[1]+about_text.get_height()))

inner_screen_about = innerScreen((640,scr_about_img_links.get_height()+scr_about_img_logos.get_height()+about_text.get_height()+100),(0,0), None,
								urlButton("https://www.facebook.com/pages/LabProdam/778608428928263",inviButton,(504,61)),
								urlButton("https://www.youtube.com/labprodam",inviButton,(550,61)))

about_links=simpleImage(scr_about_img_links,(0,0))
about_logos= simpleImage(scr_about_img_logos,(posText[0],posText[1]+about_text.get_height()+about_text_data.get_height()+30))


scr_about_scroller = innerScroller(inner_screen_about,10,1,(0,0,0),(255,255,255),(64010,0))
inner_screen_about.addItens(about_links, about_text_img,about_data_img, about_logos)
scr_about.addItens(inner_screen_about,scr_about_scroller,simpleImage(scr_about_headline,(0,0)),
					simpleImage(bg_all.subsurface(pygame.Rect(0,333,640,27)),(0,333)))

scr_start.setMusic(dir_music+'menuLoop.mp3')
scr_stages.setMusic(dir_music+'menuLoop.mp3')
scr_stage_01.setMusic(dir_music+'gameplayLoop.mp3',True)
scr_stage_02.setMusic(dir_music+'Jaunty Gumption.mp3',True)
scr_stage_03.setMusic(dir_music+'In a Heartbeat.mp3',True)
loadBlit()
scr_tutorial.addItens(simpleImage(scr_tutorial_headline,(0,0)))
scr_options.addItens(simpleImage(scr_options_headline,(0,0)))
scr_avatar.addItens(simpleImage(scr_avatar_headline,(0,0)))
scr_gps.addItens(simpleImage(scr_gps_headline,(0,0)))
scr_stages.addItens(simpleImage(scr_stages_headline,(0,0)))

delete_img=pygame.image.load(dir_menu+'telaLimpar-SimNaoTransp.png').convert_alpha()
delete_tgscr=toggleScreen(delete_img.get_size(),delete_img,((640-delete_img.get_width())//2,360),((640-delete_img.get_width())//2,(430-delete_img.get_height())/2),(0,-36))
delete_tgscr.addItens(functionButton(lambda:[avatar_tools.clearSave(),avatar_buttons[0].callActivation(),color_picker.resetColor(),clearFile(dir_data+"config_data.lab"),mute_unmute.setState(1),gpsingame_onoff.setState(1),mute_unmute.callActivation(),gpsingame_onoff.callActivation(),options_tgscr.turnOn(False),delete_tgscr.turnOn(False),setFirstTime(),stages_buttons[0].setLink(None)]+[scr.clearScore() for scr in [stage_01,stage_02,stage_03]],None,button_img_yes,(50,165),None),
						functionButton(lambda:[options_tgscr.turnOn(False),delete_tgscr.turnOn(False)],None,button_img_no,(delete_img.get_width()-button_img_no[0].get_width()-50,165),None))
scr_options.addItens(delete_tgscr)
options_tgscr.addItens(renderText(chic_30,"Placas Culturais:",(255,255,255), (100,150)), renderText(chic_30,u"Recurso Música:",(255,255,255), (100,200)), renderText(chic_30,"Dados Salvos:",(255,255,255), (100,250)),
						gpsingame_onoff,mute_unmute,
						functionButton(lambda: [options_tgscr.turnOn(),delete_tgscr.turnOn()],None,limpar_button,(400,250),None))

scr_stages.addItens(home_back_button)
scr_options.addItens(home_back_button)
scr_tutorial.addItens(back_button)
scr_about.addItens(back_button)
scr_avatar.addItens(back_button)
scr_gps.addItens(clear_back_button)

scr_start.setTitle("Lab na Via")

home_button.link=scr_start
home_button_2.link=scr_start

culture_img=[pygame.Surface((50,50),SRCALPHA,32) for x in range(2)]#[pygame.image.load(dir_img+"cultura.png").convert_alpha(),pygame.image.load(dir_img+"culturaPress.png").convert_alpha()]
culture_pos=(30,130)#(buttons_x,-50+wheel_recoil+button_ident*2*(1+(0.25/1.5)))
culture_button=linkButton(scr_gps,culture_img,culture_pos) if android else urlButton(culture_url, culture_img, culture_pos)
wheel_buttons=pauseButtons((0,0),(resume_button,home_button,culture_button,retry_button),[pygame.image.load(dir_menu+"menuPausa"+str(x)+".png").convert_alpha()for x in xrange(5)])
pause_tgscr.addItens(culture_button,wheel_buttons)


############################################################################################

###---Descomente estas linhas para começar em FULLSCREEN---###
#scr_stage_01.setNewSizeScale(full_size_display)#;scr_stage_01.setFullscreen()
#print full_size_display
#print scaled_full
scr_start.setNewSizeScale(scaled_full)#;scr_start.setFullscreen()
loadBlit()
def main():
	initTools()
	try:
		load_file=open(dir_data+"config_data.lab","rb")
		gpsingame_onoff.state=cPickle.load(load_file)
		gpsingame_onoff.buttons[gpsingame_onoff.getPreviousState()].callFunction()
		mute_unmute.state=cPickle.load(load_file)
		mute_unmute.buttons[mute_unmute.getPreviousState()].callFunction()
		load_file.close()
	except Exception,e:
		print "load_file\n\t"+str(e)
	screenLoop(scr_start)
	load_file=open(dir_data+"config_data.lab","wb")
	try:
		cPickle.dump(gpsingame_onoff.state,load_file)
		cPickle.dump(mute_unmute.state,load_file)
	except Exception,e:print "load_file\n\t"+str(e)
	load_file.close()
	debugLog('fim programa\nfechando display...')
	try:pygame.display.quit()
	except Exception, e: 
		debugLog('!!! '*20+'\n\tpygame.quit() error : \n\t'+str(e)+'\n'+'!!! '*20)
		sys.exit()

	debugLog('fechando mixer...')
	try:mixer.quit()
	except Exception, e: 
		debugLog('!!! '*20+'\n\tmixer.quit() error : \n\t'+str(e)+'\n'+'!!! '*20)
		sys.exit()

	debugLog('fechando pygame...')
	try:pygame.quit()
	except Exception, e: 
		debugLog('!!! '*20+'\n\tpygame.quit() error : \n\t'+str(e)+'\n'+'!!! '*20)
		sys.exit()

	debugLog('pygame quitou, adeus')
	sys.exit()


if __name__ == "__main__":
	main()
