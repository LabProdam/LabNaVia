# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from debugLog import *
#import pylygon
try :
	import android
except ImportError:
	android = None
try:
	import pygame.mixer as mixer
except ImportError:
	import android.mixer as mixer

if android:
	from jnius import *
	copen_url = autoclass("com.lab.labnavia.OpenURL")
	open_url = copen_url()
else:
	import webbrowser

def initTools():
	if android:
		android.init()
		android.map_key( android.KEYCODE_BACK , pygame.K_q )
	mixer.init()

mute_music=False
def setMuteMusic(mute=True):
	global mute_music
	mute_music=mute
''' !!!!!! As seguintes funções estão deixando o jogo lento !!!!!! '''

def rotateCenter(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()#pega retangulo da imagem
    rot_image = pygame.transform.rotate(image, angle)#rotaciona a imagem
    rot_rect = orig_rect.copy()#copia o retangulo que pegou
    rot_rect.center = rot_image.get_rect().center#muda o centro do retangulo para o centro da imagem rotacionada
    rot_image = rot_image.subsurface(rot_rect).copy()#recorta dentro do novo retangulo
    return rot_image


'''
def blitAlpha(display, img, pos, opacity):
    x = pos[0]
    y = pos[1]
    temp = pygame.Surface((img.get_width(), img.get_height())).convert()
    temp.blit(display, (-x, -y))
    temp.blit(img, (0, 0))
    temp.set_alpha(opacity)        
    display.blit(temp, pos)
'''
'''
def roundedRect(color,size):
	surface=pygame.Surface(size)
	rect=surface.get_rect()
	color_key=(255-color[0],255-color[1],255-color[2])
	surface.fill(color_key)
	surface.set_colorkey(color_key)
	pygame.draw.ellipse(surface,color,rect)
'''
def screenLoop(main_screen):
	main_screen.startMusic()
	while main_screen.running:
		debugLog('\tcomeco tela')
		'''
		debugLog('\t'+str(len(main_screen.previous_screen_list))+' telas anteriores')
		for i,p in enumerate(main_screen.previous_screen_list):
			debugLog('\t\t'+str(i)+' : '+str(p.title) )
		'''
		main_screen.run()
		if main_screen.stored_screen:
			debugLog('\t||comeco troca tela')
			next_screen=main_screen.stored_screen
			next_screen.full_screen=main_screen.full_screen
			if next_screen.stopmusic:mixer.music.stop()
			main_screen.play=False
			if main_screen.music!=None or next_screen.stopmusic:
				if next_screen.music and main_screen.music!=next_screen.music: next_screen.play=True
			next_screen.resize_scale=(main_screen.resize_scale[0],main_screen.resize_scale[1])
			next_screen.final_display=main_screen.final_display
			main_screen.stored_screen=None
			
			if not next_screen.previous_screen:
				next_screen.previous_screen=main_screen
			
			'''
			if main_screen.previous_screen==True:
				next_screen.previous_screen_list=main_screen.previous_screen_list[:-1]
				main_screen.previous_screen=False
			else:
				next_screen.previous_screen_list=main_screen.previous_screen_list+[main_screen]
			'''
			main_screen=next_screen
			debugLog('\t||fim troca tela')
		debugLog('\tfim tela')

class motherScreen(object):
	def __init__(self,size,color,*itens):
		self.size=size
		self.color=color
		self.itens=list(itens)
	def blitBg(self,display):
		if self.color!=None:
			try:display.fill(self.color)
			except:display.blit(self.color,(0,0))
	def blitOn(self,display):
		debugLogSuper('\t\t\tblitOn')
		self.blitBg(display)
		for item in self.itens:
			debugLogUltra('\t\t\t\tblitOn : '+str(type(item)))
			try: item.blitOn(display)
			except: pass
	def eventControler(self,event,resize,move=(0,0)):
		debugLogSuper('\t\t\teventControler')
		for item in self.itens:
			debugLogUltra('\t\t\t\teventControler : '+str(type(item)))
			try: item.eventControler(event,resize,move)
			except: pass
	def screenCall(self):
		debugLogSuper('\t\t\tscreenCall')
		screen=None
		for item in self.itens:
			debugLogUltra('\t\t\t\tscreenCall'+str(type(item)))
			try: screen=item.screenCall()
			except: pass
			if screen: break
		return screen
	def screenManipulation(self, screen):
		debugLogSuper('\t\t\tscreenManipulation')
		for item in self.itens:
			debugLogUltra('\t\t\t\tscreenManipulation'+str(type(item)))
			try: item.screenManipulation(screen)
			except: pass
	def preEvents(self):
		debugLog('\t**'+str(type(self).__name__)+' with '+str(len(self.itens))+' itens')
		debugLogSuper('\t\t\tpreEvents')
		for item in self.itens:
			debugLogUltra('\t\t\t\tpreEvents'+str(type(item)))
			try: item.preEvents()
			except: pass
	def posEvents(self):
		debugLogSuper('\t\t\tposEvents')
		for item in self.itens:
			debugLogUltra('\t\t\t\tposEvents'+str(type(item)))
			try: item.posEvents()
			except: pass
	def addItens(self, *new_itens):
		for new_item in new_itens:
			self.itens.append(new_item)
	def delItem(self, del_item, qnt=1):
		for i in range(len(self.itens)):
			if self.itens[i]==del_item:
				self.itens=self.itens[:i]+self.itens[i+1:]
				qnt-=1
				if qnt==0:break
	def delItens(self, *del_itens):
		for item in del_itens:
			self.delItem(item)
	def delAllItens(self):
		self.itens=[]
	def delIndex(self, *index):
		for idx in index:
			for i in range(len(self.itens)):
				if i==idx:
					self.itens=self.itens[:i]+self.itens[i+1:]
					break
	def hasItem(self, searched_item):
		qnt=0
		for item in self.itens:
			if item==searched_item:
				qnt+=1
		return qnt
		

class innerScreen(motherScreen):
	def __init__(self,size,pos,color,*itens):
		motherScreen.__init__(self,size,color,*itens)
		self.display=pygame.Surface(size,pygame.SRCALPHA,32)
		self.pos=[pos[0],pos[1]]
		self.init_pos=(pos[0],pos[1])
		self.collide=False
	def resetPos(self):
		self.pos=[self.init_pos[0],self.init_pos[1]]
	def eventControler(self,event,resize,move=(0,0)):
		move=(self.pos[0]+move[0],self.pos[1]+move[1])
		#''' descomente esse comentário para retroceder o clique estritamente interno
		if self.display.get_rect().collidepoint( (float(event.pos[0]-move[0])/resize[0],float(event.pos[1]-move[1])/resize[1]) ):
			self.collide=True
		else:
			self.collide=False
		if self.collide:
		#'''
			motherScreen.eventControler(self,event,resize,move)
	def blitOn(self,display):
		self.display.blit(display,(-self.pos[0],-self.pos[1]))
		motherScreen.blitOn(self,self.display)
		display.blit(self.display,self.pos)#self.display.subsurface(self.display.get_rect())
	def screenManipulation(self, screen):
		for item in self.itens:
			try: item.screenManipulation(screen)
			except: pass
			try: item.innerManipulation(self)
			except: pass
'''
class rollingBar(object):
	def __init__(self,surface,
'''
class movableScreen(innerScreen):
	def __init__(self,vel,move,size,pos,color,*itens):
		self.vel=vel
		self.move_key=move
		innerScreen.__init__(self,size,pos,color,*itens)
	def keyInput(self,event):
		if event.type==KEYDOWN:
			if event.key==self.move_key[3]: self.pos[1]-=self.vel
			if event.key==self.move_key[2]:	self.pos[1]+=self.vel
			if event.key==self.move_key[0]:	self.pos[0]-=self.vel
			if event.key==self.move_key[1]:	self.pos[0]+=self.vel
	def eventControler(self,event,resize,move=(0,0)):
		#move=(self.pos[0]+move[0],self.pos[1]+move[1])
		innerScreen.eventControler(self,event,resize,move)#######################
		self.keyInput(event)

class toggleScreen(innerScreen):
	def __init__(self,size,color,pos,end,move,rotate=0,auto_fit=True,*itens):
		innerScreen.__init__(self,size,pos,color,*itens)
		self.move=move
		self.end_pos=end
		self.rotate=rotate
		self.init_rotation=0.0
		self.rotation=0.0
		self.auto_fit=auto_fit
		self.diff=(1 if pos[0]<end[0] else -1,
				   1 if pos[1]<end[1] else -1)
		self.moving=False
		self.turned_on=False
		self.hide=True
		self.lock=False
	def setAngle(self,rotate):
		self.rotation=rotate
		self.init_rotation=rotate
	def hideTurnedOff(self, hide=True):
		self.hide=hide
	def lockOnOff(self,lock=True):
		self.lock=lock
	def turnOn(self,boolean=True): 
		if not self.lock:
			self.turned_on=boolean
	def toggleOnOff(self):
		if not self.lock:
			self.turned_on=not self.turned_on
	def actived(self): return self.turned_on or self.moving or self.hide==False
	def posEvents(self):
		self.rotation=self.init_rotation
		self.pos=[self.init_pos[0],self.init_pos[1]]
		
	def moveScreen(self, o_dest, direction):
		pos=(self.pos[0]*self.diff[0]*direction,
			 self.pos[1]*self.diff[1]*direction)
		dest=(o_dest[0]*self.diff[0]*direction,
			  o_dest[1]*self.diff[1]*direction)
		if pos[0]<dest[0] or pos[1]<dest[1]:
			self.pos[0]+=self.move[0]*direction
			self.pos[1]+=self.move[1]*direction
			self.rotation+=self.rotate*direction
			self.moving=True
		else:
			if self.auto_fit:
				if self.pos[0]!=o_dest[0] or self.pos[0]!=o_dest[0]:
					self.pos=[o_dest[0],o_dest[1]]
					
			self.moving=False
			#self.turned_on=False
	def blitOn(self,display):
		if self.turned_on:
			self.moveScreen(self.end_pos,1)
		else:
			self.moveScreen(self.init_pos,-1)
		if self.actived():
	
			#self.display.fill((123,132,231))
			#self.display.set_colorkey((123,132,231))
			self.display=pygame.Surface(self.display.get_size(),pygame.SRCALPHA,32)
			motherScreen.blitOn(self,self.display)
	
			#self.display.blit(display,(-self.pos[0],-self.pos[1]))
			#self.display.blit(rotateCenter(temp,self.rotation),(0,0))
	
			#temp.blit(rotateCenter(self.display,self.rotation),(0,0) )
			if self.rotation>0:
				display.blit(rotateCenter(self.display,self.rotation),self.pos)
			else:
				display.blit(self.display,self.pos)
	def eventControler(self,event,resize,move):
		if self.actived(): innerScreen.eventControler(self,event,resize,move)
	def screenManipulation(self, screen):
		if self.actived(): motherScreen.screenManipulation(self, screen)
	def screenCall(self):
		if self.actived(): return motherScreen.screenCall(self)

class renderList(object):
	display_list=[]
	empty_rect=pygame.Rect(-1,-1,-1,-1)
	def setZero(self):
		self.display_list=[]
	def fill(self,color,rect=pygame.Rect(-1,-1,-1,-1),flag=0):
		self.display_list.append([True,color,rect,flag])
	def blit(self,img,pos,rect=None,flag=0):
		self.display_list.append([False,img,pygame.Rect(pos[0],pos[1],img.get_width(),img.get_height()),rect,flag])
	def sortList(self):
		dlist=self.display_list
		for i in range(len(dlist)-1):
			for e in range(i+1,len(dlist)):
				if dlist[i][2].bottom>dlist[e][2].bottom:
					dlist[i],dlist[e]=dlist[e],dlist[i]
		'''try:
			sorted(self.display_list,key=lambda item: (item[2].y,item[2].x))
			#sorted(self.display_list,key=lambda item: (item[2].y))
		except Exception,e:print e
		'''
	def blitOn(self,display):
		try:
			for item in self.display_list:
				if item[0]==True:
					display.fill(item[1],None if item[2]==self.empty_rect else item[2],item[3])
				else:
					display.blit(item[1],(item[2].x,item[2].y),item[3],item[4])
		except Exception,e:print e
		

class screenObject(motherScreen):
	def __init__(self, size, fps, color, *itens):
		motherScreen.__init__(self,size,color,*itens)
		self.resize_scale=(1,1)
		self.fps=fps
		self.stored_screen=None
		
		self.previous_screen=None
		
		'''
		self.previous_screen=False
		self.previous_screen_list=[]
		'''
		self.running=True
		self.full_screen=False
		self.title=""
		self.show_fps=False
		self.final_display=None
		self.stored_music=False
		self.setMusic(None,None,None,False)
		self.rotate=0
		self.setEscFunction(self.closeGame)
		self.play=False
		self.loading_image=None
	def setLoading(self,image):
		self.loading_image=image
	def setMusic(self, music, stop=False,repeat=-1,startpos=0.0):
		if music==-1:
			self.stopmusic=True
		else:
			self.music=music
			self.repeat=repeat
			self.startpos=startpos
			self.stopmusic=stop
	def startMusic(self):
		global mute_music
		if self.music:
			mixer.music.load(self.music)
		if not mute_music: 
			mixer.music.play(self.repeat,self.startpos)
	def setFullscreen(self,fullscr_bool=True):
		new_size=(int(self.size[0]*self.resize_scale[0]),int(self.size[1]*self.resize_scale[1]) )
		self.full_screen=fullscr_bool
		pygame.display.quit()
		pygame.display.init()
		self.final_display=pygame.display.set_mode(new_size,RESIZABLE if not self.full_screen else FULLSCREEN)
	def setTitle(self,title_string):
		self.title=title_string
	def showFps(self, show_fps=True):
		self.show_fps=show_fps
	def setNewSizeScale(self, new_size):
		self.resize_scale=(float(new_size[0])/self.size[0],float(new_size[1])/self.size[1])
		self.final_display=pygame.display.set_mode((int(new_size[0]),int(new_size[1])),RESIZABLE if not self.full_screen else FULLSCREEN)
	# run da tela
	def setEscFunction(self,function,*args):
		self.function=function
		self.args=list(args)
	def closeGame(self):
		self.running=False
		self.stored_screen=None
	def run(self):
		global mute_music
		if pygame.display.get_init():
			self.final_display=pygame.display.get_surface()
		elif not self.final_display: 
			new_size=(int(self.size[0]*self.resize_scale[0]),int(self.size[1]*self.resize_scale[1]) )
			self.final_display=pygame.display.set_mode(new_size,RESIZABLE if not self.full_screen else FULLSCREEN)
			debugLog('\t>>pygame.display.set_mode()')
		pre_display=pygame.Surface(self.size)
		fps_clock=pygame.time.Clock()
		pygame.display.set_caption(self.title)
		self.preEvents()
		'''###
		if android:
			cgps_hardware = autoclass("com.lab.labnavia.Hardware")
			gps_hardware = cgps_hardware()
			locationManager = gps_hardware.startLocationManager()
			gps_hardware.startLocationUpdater(locationManager,10000,1)
		'''###
		if self.play: self.startMusic()
		while self.running and not self.stored_screen:
			if android :
				if self.music: mixer.periodic()
				if android.check_pause ():
					debugLog("pause")
					mixer.music.stop()
					debugLog("\tparou musica")
					android.wait_for_resume ()
					self.startMusic()
					debugLog("\tiniciou musica")
					debugLog("unpause")
			debugLogSuper('\t\tInicio passagem')
			if self.show_fps: pygame.display.set_caption(self.title+" - "+str(int(fps_clock.get_fps()))+":"+str(self.fps))
			for event in pygame.event.get():
				if event.type==KEYUP:
					if event.key==K_q:
						self.function(*self.args)
				if event.type==QUIT and not android:
					self.closeGame()
				if event.type==VIDEORESIZE:
					self.setNewSizeScale((event.w,event.h))
					new_size=(int(self.size[0]*self.resize_scale[0]),int(self.size[1]*self.resize_scale[1]))
					self.final_display = pygame.display.set_mode(new_size,RESIZABLE)
			
				self.eventControler(event,self.resize_scale)

			self.stored_screen=self.screenCall()
			
			self.blitOn(pre_display)
			'''
			self.blitOn(self.render_list)
			self.render_list.reorderList()
			self.render_list.blitOn(pre_display)
			'''
			debugLogScreen(pre_display,str(int(fps_clock.get_fps()))+":"+str(self.fps),(0,0),(255,55,55))
			'''
			if android:
				debugLogScreen(pre_display,str(gps_hardware.location.latitude),(0,50),(0,0,0))
				debugLogScreen(pre_display,str(gps_hardware.location.longitude),(0,100),(0,0,0))
				
				#location=gps_hardware.getLocation(locationManager)
				#debugLogScreen(pre_display,str(location.getLatitude()),(120,30),(0,0,255))
				#debugLogScreen(pre_display,str(location.getLongitude()),(120,30),(0,0,255))
			'''
			pygame.transform.scale(pre_display if self.rotate==0 else pygame.transform.rotate(pre_display.convert(),self.rotate),(int(self.size[0]*self.resize_scale[0]),int(self.size[1]*self.resize_scale[1])),self.final_display)
			self.screenManipulation(self)
			'''self.render_list.setZero()'''

			pygame.display.flip()
			fps_clock.tick(self.fps)
			debugLogSuper('\t\tFim passagem')
		self.posEvents()
		if self.loading_image:
			self.blitBg(pre_display)
			try:pre_display.blit(self.loading_image,self.loading_image.get_rect(center=(self.size[0]//2,self.size[1]//2)).topleft)
			except Exception,e:print e
			pygame.transform.scale(pre_display if self.rotate==0 else pygame.transform.rotate(pre_display.convert(),self.rotate),(int(self.size[0]*self.resize_scale[0]),int(self.size[1]*self.resize_scale[1])),self.final_display)
			pygame.display.flip()
			
class simpleRect(object):
	def __init__(self,color=None,rect=None):
		self.rect=rect
		self.color=color
	def setColor(self,color):
		self.color=color
	def blitOn(self,display):
		if self.color!=None:
			display.fill(self.color,self.rect)

class simpleImage(object):
	def __init__(self,img,pos,center=False):
		self.img=img
		self.pos=pos
		self.show=True
		self.center=center
	def setImage(self,img):
		self.img=img
	def blitOn(self,display):
		if self.show: 
			display.blit(self.img,self.pos if not self.center else self.img.get_rect(center=self.pos).topleft )
	def hideImage(self):
		self.show=False
	def showImage(self):
		self.show=True

class functionImage(simpleImage):
	def __init__(self,img,pos,*args):
		self.args=list(*args)
		simpleImage.__init__(self,img,pos)
	def blitOn(self,display):
		if self.show: display.blit(self.img(*self.args),self.pos)

class movingImage(simpleImage):
	def __init__(self,img,pos,end,mov,auto_fit=True):
		pos=[pos[0],pos[1]]
		self.init_pos=[pos[0],pos[1]]
		simpleImage.__init__(self,img,pos)
		self.move=mov
		self.end_pos=end
		self.auto_fit=auto_fit
		self.diff=[1 if pos[0]<end[0] else -1,
				   1 if pos[1]<end[1] else -1]
		self.stop=False
	def posEvents(self):
		self.pos=[self.init_pos[0],self.init_pos[1]]
		self.stop=False
	def blitOn(self,display):
		if self.pos[0]*self.diff[0]<self.end_pos[0]*self.diff[0] or self.pos[1]*self.diff[1]<self.end_pos[1]*self.diff[1]:
			self.pos[0]+=self.move[0]
			self.pos[1]+=self.move[1]
		else:
			print 'fim'
			self.stop=True
			if self.auto_fit:
				if self.pos[0]!=self.end_pos[0] or self.pos[0]!=self.end_pos[0]:
					self.pos=[self.end_pos[0],self.end_pos[1]]
		display.blit(self.img,self.pos)

class loopImage(movingImage):
	def __init__(self,img,pos,end,mov,rewind=False):
		mov=[mov[0],mov[1]]
		movingImage.__init__(self,img,pos,end,mov,True)
		self.rewind=rewind
		self.first_init_pos=[self.init_pos[0],self.init_pos[1]]
		self.first_end_pos=[self.end_pos[0],self.end_pos[1]]
	def preEvents(self):
		self.init_pos=[self.first_init_pos[n] for n in range(2)]
		self.end_pos=[self.first_end_pos[n] for n in range(2)]
	def repeatEngine(self):
		if self.rewind:
			print 'ok'
			for n in range(2):
				self.move[n]*=(-1)
				self.diff[n]*=(-1)
			self.init_pos,self.end_pos=[self.end_pos[0],self.end_pos[1]],[self.init_pos[0],self.init_pos[1]]
			self.stop=False
			
			'''
			new_init=[self.end_pos[0],self.end_pos[1]]
			new_end=[self.init_pos[0],self.init_pos[1]]
			self.end_pos=new_end
			self.init_pos=new_init
			'''
			print 'ok2'
		else:
			movingImage.posEvents(self)
	def blitOn(self,display):
		movingImage.blitOn(self,display)
		if self.stop:
			self.repeatEngine()

class simpleButton(object):
	def __init__(self,img,pos,text_and_pos=None):
		self.img=img
		self.skin=[img]
		self.selected_skin=0
		self.pos=pos
		self.state=0
		self.actived=False
		self.pressed=False
		self.pressed_out=True
		self.auto_reset_state=True
		self.text=text_and_pos
		self.size=img[0].get_size()
		self.center=img[0].get_rect().center
		self.inflate=(0,0)
		self.rect=pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1] )
		self.setSound()
		self.setVibrate()
		self.hide=False
		self.lock=False
	def setLock(self,lock=True):
		self.lock=lock
	def setHide(self,hide=True):
		self.hide=hide
	def setSkin(self,selection):
		self.img=self.skin[selection]
		self.selected_skin=selection
	def addSkin(self,skin):
		self.skin.append(skin)
	def callActivation(self):
		self.actived=True
	def setImg(self,img):
		self.img=img
	def setText(self,text):
		self.text=text
	def setVibrate(self,vibrate_1=0,vibrate_2=0):
		self.vibrate=(vibrate_1,vibrate_2)
	def setSound(self,sound_3=None,sound_2=None,sound_1=None):
		self.sound=[sound_1,sound_2,sound_3]
	def inflateButton(self,x,y):
		self.inflate=(x,y)
		try:self.rect.inflate_ip(x,y)
		except Exception,e:print e
	def relocateButton(self,move):
		if self.pos[0]+move[0]!=self.rect.x or self.pos[1]+move[1]!=self.rect.y:
			self.rect=pygame.Rect(self.pos[0]+move[0],self.pos[1]+move[1],self.size[0],self.size[1] )
			self.rect.inflate_ip(self.inflate[0],self.inflate[1])
	def runEventControler(self,event,resize,move):
		self.relocateButton(move)
		mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
		button_up = event.type is MOUSEBUTTONUP and event.button is 1
		if self.rect.collidepoint(mouse_pos):
			if self.sound[1] and self.state!=2: 
				self.sound[1][0].play()
				pygame.time.wait(self.sound[1][1])
			if len(self.img)>2:self.state=2
			if event.type==MOUSEBUTTONUP and event.button==1:
				if self.vibrate[0]>0 and android:android.vibrate(self.vibrate[0])
				if self.sound[0]: 
					self.sound[0][0].play()
					pygame.time.wait(self.sound[0][1])
				self.actived=True
				self.pressed=False
				if len(self.img)>3 and self.state!=3:
					self.state=3
				else:self.state=0
			if event.type==MOUSEBUTTONDOWN and event.button==1:
				if self.vibrate[1]>0 and android:android.vibrate(self.vibrate[1])
				if self.sound[2]: 
					self.sound[2][0].play()
					pygame.time.wait(self.sound[2][1])
				if len(self.img)>1:self.state=1
				self.pressed=True
		elif button_up or self.state==2:
			if button_up: self.pressed_out=True
			self.state=0
	def eventControler(self,event,resize,move):
		if not self.lock: self.runEventControler(event,resize,move)
	def blitButton(self,display):
		image = self.img[self.state] if type(self.img[self.state])==pygame.Surface else self.img[self.state].blitOn(None)
		display.blit(image,self.pos)
	def blitText(self,display):
		if self.text: display.blit(self.text[0],self.text[1])
	def blitOn(self,display):
		if not self.hide:
			self.blitButton(display)
			self.blitText(display)

class pauseButtons(object):
	def __init__(self,pos,buttons,images):
		self.imgs=images
		self.buttons=buttons
		self.state=-1
		self.pos=pos
	def blitOn(self,display):
		try:
			state=len(self.buttons)
			for b in xrange(len(self.buttons)):
				if self.buttons[b].state==1:
					state=b
					break
			display.blit(self.imgs[state],self.pos)
		except Exception,e:print e

def playSound(sound,time=0):
	global mute_music
	if not mute_music:
		sound.play()
		pygame.time.wait(time)

class geniusButton(object):
	def __init__(self,centro,raio_menor,raio_maior,image,pos,screens,sound=None):
		print image[0].get_rect().center
		self.centro=[centro[i]+pos[i] for i in xrange(2)]
		self.raio_menor=raio_menor
		self.raio_maior=raio_maior
		self.rect=[
			pygame.Rect(self.centro[0]-raio_maior,self.centro[1]-raio_maior,raio_maior,raio_maior),
			pygame.Rect(self.centro[0],self.centro[1]-raio_maior,raio_maior,raio_maior),
			pygame.Rect(self.centro[0]-raio_maior,self.centro[1],raio_maior,raio_maior),
			pygame.Rect(self.centro[0],self.centro[1],raio_maior,raio_maior)]
		self.img=image
		self.state=0
		self.active=0
		self.pos=pos
		self.scr=screens
		self.detect=False
		self.sound=sound
	def eventControler(self,event,resize,move):
		mouse_pos=((event.pos[0]-move[0])/resize[0],(event.pos[1]-move[1])/resize[1])
	
		calc=pow(mouse_pos[0]-self.centro[0],2)+pow(mouse_pos[1]-self.centro[1],2)
		if event.type==MOUSEBUTTONDOWN and event.button==1:
			if pow(self.raio_maior,2)>calc:
				if self.raio_menor==0 or pow(self.raio_menor,2)<calc:
					for r in xrange(4):
						if self.rect[r].collidepoint(mouse_pos):
							self.state=r+1
				else:
					self.state=5
			else:
				self.state=0
		elif event.type==MOUSEBUTTONUP and event.button==1:
			self.active=self.state
			self.state=0
	def blitOn(self,display):
		try:display.blit(self.img[self.state],self.pos)
		except Exception,e:print e
		#pygame.draw.circle(display,(0 if self.state==0 else 255,0,0),self.centro,self.raio_maior)
		#pygame.draw.circle(display,(255,255,255),self.centro,self.raio_menor)
	def screenCall(self):
		retorno=None
		if self.active!=0:
			if self.sound:
				try:playSound(self.sound[0],self.sound[1])
				except Exception,e:print e
			retorno=self.scr[self.active-1]
			if type(retorno)==str:
				webbrowser.open(retorno)
				retorno=None
			self.active=0
			self.state=0
		return retorno
			
'''
#incompleto
class polygonButton(simpleButton):
	def __init__(self,pos,point_list):
		simpleButton.__init__(self,[pygame.Surface((0,0))for n in range(3)],pos,None)
		self.polygon=pylygon.Polygon(point_list)
		self.polygon.move_ip(pos[0],pos[1])
		self.rect=pylygon.Polygon(point_list)
		self.rect.move_ip(pos[0],pos[1])
		self.state=0
	def relocateButton(self,move):
		if self.pos[0]+move[0]!=self.rect.get_rect().x or self.pos[1]+move[1]!=self.rect.get_rect().y:
			try:self.rect=self.polygon.move(move[0],move[1])
			except Exception,e:print e
	###
	def eventControler(self,event,resize,move):
		self.relocateButton(move)
		mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
		if self.rect.collidepoint(mouse_pos):
			if self.sound[1] and self.state!=2: 
				self.sound[1][0].play()
				pygame.time.wait(self.sound[1][1])
			if len(self.img)>2:self.state=2
			if event.type==MOUSEBUTTONUP and event.button==1:
				if self.vibrate[0]>0 and android:android.vibrate(self.vibrate[0])
				if self.sound[0]: 
					self.sound[0][0].play()
					pygame.time.wait(self.sound[0][1])
				self.actived=True
				self.pressed=False
				if len(self.img)>3 and self.state!=3:
					self.state=3
				else:self.state=0
			if event.type==MOUSEBUTTONDOWN and event.button==1:
				if self.vibrate[1]>0 and android:android.vibrate(self.vibrate[1])
				if self.sound[2]: 
					self.sound[2][0].play()
					pygame.time.wait(self.sound[2][1])
				if len(self.img)>1:self.state=1
				self.pressed=True
		elif button_up or self.state==2:
			if button_up: self.pressed_out=True
			self.state=0
	###
	def blitOn(self,display):
		pygame.draw.polygon(display, (0,0,0) if self.state==0 else (255,255,255), self.polygon)
'''
class textButton(simpleButton):
	def __init__(self,img,pos,text_pos,text_font,text='',antialias=True,color=(0,0,0),limit=-1):
		simpleButton.__init__(self,img,pos,[pygame.Surface((0,0)),text_pos])
		self.auto_reset_state=False
		self.edit_text=text
		self.edit_font=text_font
		self.edit_antialias=antialias
		self.edit_color=color
		self.pointer_color=[255-cor for cor in color]
		self.edit_pos=0
		self.edit_limit=limit
		self.edit_actived=False
	def setPointerColor(self,color):
		self.pointer_color=color
	def eventControler(self,event,resize,move):
		if event.type==KEYDOWN and self.edit_actived:
			print 'teclado'
			if event.key==K_RIGHT:
				if self.edit_pos<len(self.edit_text):
					self.edit_pos+=1
					print 'direita'
			elif event.key==K_LEFT:
				if self.edit_pos>0:
					self.edit_pos-=1
					print 'esquerda'
			elif len(self.edit_text)<self.edit_limit or self.edit_limit==-1:
				print 'vai digitar'
				char=chr(event.key)
				if KMOD_LSHIFT or KMOD_RSHIFT or KMOD_SHIFT or KMOD_CAPS:
					char.upper()
				self.edit_text=self.edit_text[:self.edit_pos]+char+self.edit_text[self.edit_pos:]
				self.edit_pos+=1
				print 'digitou'
		simpleButton.eventControler(self,event,resize,move)
		if self.actived:
			print 'ok'
			self.edit_actived=True
			self.actived=False
	def blitText(self,display):
		self.text[0]=self.edit_font.render(self.edit_text,self.edit_antialias,self.edit_color)
		simpleButton.blitText(self,display)
		if self.edit_actived: 
			try:
				size=self.edit_font.size(self.edit_text[:self.edit_pos])
				rect=pygame.Rect(size[0]+self.text[1][0],self.text[1][1]-1,1,size[1]+2)
				display.fill(self.pointer_color,rect)
			except Exception,e:print e
			
			
class slideButton(simpleButton):
	def __init__(self,img_list,pos,text_and_pos=None):
		simpleButton.__init__(self,img_list[0],pos,text_and_pos)
		self.img_list=img_list
		self.selection=0
	def screenCall(self):
		if self.actived:
			if self.selection+1<len(self.img_list): self.selection+=1
			else: self.selection=0
			self.img=self.img_list[self.selection]
			self.actived=False
		return None

class urlButton(simpleButton):
	def __init__(self,url,img,pos,text_and_pos=None):
		self.url=url
		simpleButton.__init__(self,img,pos,text_and_pos)
	def screenCall(self):
		global open_url
		if self.actived:
			if android:open_url.press(self.url)
			else:webbrowser.open(self.url)
			self.actived=False
		return None

class linkButton(simpleButton):
	def __init__(self,link,img,pos,text_and_pos=None):
		self.link=link
		simpleButton.__init__(self,img,pos,text_and_pos)
	def setLink(self,link):
		self.link=link
	def screenCall(self):
		the_return=None
		if self.actived:
			the_return=self.link
			self.actived=False
		return the_return if not self.lock else None

class movingButton(linkButton):
	def __init__(self,link,img,pos,end,mov,rotate,auto_fit=True,text_and_pos=None):
		pos=[pos[0],pos[1]]
		self.init_pos=[pos[0],pos[1]]
		linkButton.__init__(self,link,img,pos,text_and_pos)
		self.move=mov
		self.end_pos=end
		self.rotate=rotate
		self.rotation=0.0
		self.auto_fit=auto_fit
		self.diff=(1 if pos[0]<end[0] else -1,
				   1 if pos[1]<end[1] else -1)
	def posEvents(self):
		self.pos=[self.init_pos[0],self.init_pos[1]]
		self.rotation=0.0
	def blitOn(self,display):
		if self.pos[0]*self.diff[0]<self.end_pos[0]*self.diff[0] or self.pos[1]*self.diff[1]<self.end_pos[1]*self.diff[1]:
			self.pos[0]+=self.move[0]
			self.pos[1]+=self.move[1]
			self.rotation+=self.rotate
		else:
			if self.auto_fit:
				if self.pos[0]!=self.end_pos[0] or self.pos[0]!=self.end_pos[0]:
					self.pos=[self.end_pos[0],self.end_pos[1]]
		if self.rotation>0:
			display.blit(rotateCenter(self.img[self.state],self.rotation),self.pos)
		else:
			display.blit(self.img[self.state],self.pos)
		self.blitText(display)


class functionButton(linkButton):
	def __init__(self,click_function,link,img,pos,text_and_pos=None,press_function=None,*args):
		linkButton.__init__(self,link,img,pos,text_and_pos)
		self.setFunction(click_function,press_function)
		self.setArgs1(*args)
		self.setArgs2()
	def setArgs1(self,*args):
		self.args_1=list(args)
	def setArgs2(self,*args):
		self.args_2=list(args)
	def setFunction(self,click_function,press_function=None):
		self.function=click_function
		self.press_function=press_function
	def callFunction(self,click=True):
		if click:
			self.function(*self.args_1)
		else:
			self.press_function(*self.args_2)
	def screenCall(self):
		the_return=None
		if self.press_function!=None and self.pressed:
			try:self.press_function(*self.args_2)
			except Exception, e: print e
		if self.actived:
			if self.function!=None:
				try:self.function(*self.args_1)
				except Exception, e: print e
			the_return=self.link
			self.actived=False
		return the_return if not self.lock else None

class buttonList(object):
	def __init__(self,*buttons):
		self.buttons=list(buttons)
		self.state=0
		self.limit=len(self.buttons)
	def setState(self,state):
		self.state=state
	def getPreviousState(self):
		return self.state-1 if self.state>0 else self.limit-1
	def preEvents(self):
		self.buttons[self.state].preEvents()
	def eventControler(self,event,resize,move):
		self.buttons[self.state].eventControler(event,resize,move)
	def blitOn(self,display):
		self.buttons[self.state].blitOn(display)
	def screenManipulation(self):
		self.buttons[self.state].screenManipulation()
	def posEvents(self):
		self.buttons[self.state].posEvents()
	def screenCall(self):
		actived=self.buttons[self.state].actived
		to_return=self.buttons[self.state].screenCall()
		if actived:
			self.state+=1
		if self.state>=self.limit:
			self.state=0
		return to_return

class checkButton(functionButton):
	def __init__(self,click_function,link,img,pos,text_and_pos=[None],press_function=None):
		functionButton.__init__(self,click_function,link,img[0],pos,text_and_pos[0],press_function)
		self.selection=0
		self.img_list=img
		self.text_list=text_and_pos
	def screenCall(self):
		if self.actived:
			self.selection+=1
			if self.selection>len(self.img_list): self.selection=0
			try:self.img=self.img_list[self.selection]
			except:pass
			try:self.text=self.text_list[self.selection]
			except:pass
		return functionButton.screenCall(self)

class backButton(functionButton):
	def __init__(self,img,pos,text_and_pos=None,clear=False):
		functionButton.__init__(self,None,None,img,pos,text_and_pos)
		self.clear=clear
	def clearPrevious(self,screen):
		screen.previous_screen=None
	def screenManipulation(self,screen):
		if self.link!=screen.previous_screen: 
			self.link=screen.previous_screen
			if self.clear: self.function = lambda : self.clearPrevious(screen)

'''
class backButton(functionButton):
	def __init__(self,link,img,pos,text_and_pos=None):
		functionButton.__init__(self,None,link,img,pos,text_and_pos)
	def turnOn(self,screen):
		screen.previous_screen=True
	def screenManipulation(self,screen):
		if self.link!=screen.previous_screen_list[-1]:
			self.link=screen.previous_screen_list[-1]
			self.function = lambda : self.turnOn(screen)
'''

class toggleFunctionButton(functionButton):
	turned_on=True
	def turnOn(self,boolean=True): self.turned_on=boolean
	def blitOn(self,display):
		if self.turned_on: functionButton.blitOn(self,display)
	def eventControler(self,ev,rs,mv):
		if self.turned_on: functionButton.eventControler(self,ev,rs,mv)

#class functionBackButton(functionButton,backButton):pass
#	def __init__(self,function,link,img,pos,text_and_pos=None):
#		super(self, functionBackButton).__init__()

class abstractSelection(object):
	def __init__(self,surface,movable,actived,K_keys=((K_LEFT,K_RIGHT),(K_UP,K_DOWN)) ):
		self.img=surface
		self.movable=movable
		self.actived=actived
		self.K_keys=K_keys
	def preEvents(self):
		self.called=False
		#self.grade_pos=[self.init_pos[x] for x in range(2)]
		#self.selected=0
	def selectionMove(self,i,e):pass
	def eventControler(self,event,resize,move):
		if event.type==KEYUP:
			if self.actived:
				for i in range(2):
					if self.movable[i]:
						for e in range(2):
							if event.key==self.K_keys[i][e]:self.selectionMove(i,e)
							#(i,e) tera as 4 possibilidades em dir e sentido (0,-1),(0,+1),(1,-1),(1,+1)
			else:
				for i in range(2):
					if self.movable[i]:
						for e in range(2):
							if event.key==self.K_keys[i][e]:self.actived=True
			if event.key==K_SPACE:
				self.called=True

class gradeSelection(abstractSelection):
	def __init__(self,options_matrix,surface,pos,movment=(10,10),end_pos=(1,1),init_pos=(0,0),movable=(True,True),actived=False):
		abstractSelection.__init__(self,surface,movable,actived)
		self.options=options_matrix
		self.move=movment
		self.pos=pos
		self.init_pos=init_pos
		self.grade_pos=[self.init_pos[x] for x in range(2)]
	def selectionMove(self,i,e):
		self.grade_pos[i]+=(e*2)-1
	def blitOn(self,display):
		if self.actived: display.blit(self.img,[self.pos[x]+self.grade_pos[x]*self.move[x] for x in range(2)] )
	def screenCall(self): return self.options[self.grade_pos[1]][self.grade_pos[0]] if self.called else None#retorno

def pointsDistance(a,b):		
	return pow(pow(a[0]-b[0],2)+pow(a[1]-b[1],2),0.5)
def rectsDistance(rect_1,rect_2):
	print (rect_1.x,rect_1.y)
	#listas de posições possíveis dos limites dos retangulos
	positions_1 = [(rect_1.x,rect_1.y),rect_1.topleft,rect_1.topright,rect_1.bottomleft,rect_1.bottomright,rect_1.midleft,rect_1.midright,rect_1.center]
	positions_2 = [(rect_2.x,rect_2.y),rect_2.topleft,rect_2.topright,rect_2.bottomleft,rect_2.bottomright,rect_2.midleft,rect_2.midright,rect_2.center]
	#armazenará as distancias entre as permutações das posições do retangulo
	distances=[]
	for pos_1 in positions_1:#para cara posição do rect_1
		for pos_2 in positions_2:#para cada posição do rect_2
			distances.append(pointsDistance(pos_1,pos_2))#armazena a distancia entre os dois
	return min(distances)

class freeSelection(abstractSelection):
	def __init__(self,buttons_list,surface,movable=(True,True),actived=False):
		self.options=buttons_list
		self.selected=0
		abstractSelection.__init__(self,surface,movable,actived)
	def selectionCompareOld(self,direction,xy):
		distancia=[-1,-1]
		select=self.selected
		for i in range(len(self.options)): # para cada botao na lista
			if self.options[i].pos[xy]*direction>self.options[self.selected].pos[xy]*direction: #se o botao estiver no sentido da tecla apertada
				new_dxy = abs(self.options[i].pos[xy]-self.options[self.selected].pos[xy]) # a distancia no sentido da tecla apertada
				new_dnotxy = abs(self.options[i].pos[abs(xy-1)]-self.options[self.selected].pos[abs(xy-1)]) # a distancia no outro sentido
				new_distancia=(new_dxy,new_dnotxy) if xy==0 else (new_dnotxy,new_dxy) #junta os dois numa tupla(x,y)
				if new_distancia[xy]<= distancia[xy] or distancia[xy]<0:  #se a distancia do botao for menor-igual que a menor distancia armazenada neste foreach ou se a menor distancia armazenada for menor que zero(primeira passagem)
					if new_distancia[abs(xy-1)]< distancia[abs(xy-1)] or distancia[abs(xy-1)]<0: #a mesma coisa no if acima só que no eixo perpendicular (x se y, y se x)
						distancia = new_distancia #armazena a nova menor distancia
						select = i #armazena o indice do botao
		########################-----------------------ideia: trocar tudo isso -----------------------########################
		self.selected=select

	def selectionCompare(self,direction,xy):# mesma coisa do de cima só que pela formula da distancia d(a,b)=sqrt(pow(a,2)+pow(b,2))
		distancia=-1
		select=self.selected
		for i in range(len(self.options)): # para cada botao na lista
			if self.options[i].pos[xy]*direction>self.options[self.selected].pos[xy]*direction: #se o botao estiver no sentido da tecla apertada
				#new_dxy = abs(self.options[i].pos[xy]-self.options[self.selected].pos[xy]) # a distancia no sentido da tecla apertada
				#new_dnotxy = abs(self.options[i].pos[abs(xy-1)]-self.options[self.selected].pos[abs(xy-1)]) # a distancia no outro sentido
				#new_distancia=pow(pow(new_dxy,2)+pow(new_dnotxy,2),0.5)
				rect_1=self.options[i].img[0].get_rect(x=self.options[i].pos[0],y=self.options[i].pos[1])
				rect_2=self.options[self.selected].img[0].get_rect(x=self.options[self.selected].pos[0],y=self.options[self.selected].pos[1])
				#try:print str(new_distancia)+' : '+str(rectsDistance(rect_1,rect_2))
				#except Exception,e: print e
				new_distancia=rectsDistance(rect_1,rect_2)
				if new_distancia<distancia or distancia<0:
					distancia=new_distancia
					select=i
		self.selected=select
	def selectionMove(self,i,e): self.selectionCompare((e*2)-1,i)
	def blitOn(self,display):
		if self.actived:
			button=self.options[self.selected]
			center_pos=[button.pos[x]+(button.size[x]/2)-(self.img.get_size()[x]/2) for x in range(2)]
			display.blit(self.img,center_pos)
	def screenCall(self): return self.options[self.selected].link if self.called else None

class iFreeSelection(freeSelection):#freeSelection que estica a surface para cobrir o botao inteiro
	def __init__(self,buttons_list,surface,ident,movable=(True,True),actived=False):
		freeSelection.__init__(self,buttons_list,surface,movable,actived)
		self.ident=ident
	def blitOn(self,display):
		if self.actived:
			button=self.options[self.selected]		
			new_img=pygame.transform.scale(self.img,[button.size[x]+(2*self.ident) for x in range(2)])
			display.blit(new_img,[button.pos[x]-self.ident for x in range(2)])
		

def truncline(text, font, maxwidth):
	real=len(text)       
	stext=text           
	l=font.size(text)[0]
	cut=0
	a=0                  
	done=1
	old = None
	while l > maxwidth:
		a=a+1
		n=text.rsplit(None, a)[0]
		if stext == n:
			cut += 1
			stext= n[:-cut]
		else:
			stext = n
		l=font.size(stext)[0]
		real=len(stext)               
		done=0                        
	return real, done, stext             
        
def wrapline(text, font, maxwidth): 
	done=0                      
	wrapped=[]                  
	while not done:             
		nl, done, stext=truncline(text, font, maxwidth) 
		wrapped.append(stext.strip())                  
		text=text[nl:]                                 
	return wrapped
 
from itertools import chain
def wrap_multi_line(text, font, maxwidth):
	""" returns text taking new lines into account.
	"""
	lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
	return list(lines)

def textBox(text_string,font,width,text_color=(0,0,0),limit=None,anti_alias=True,background=None):
	height=font.get_height()
	
	splited_text=text_string.splitlines()
	splited_and_wraped_text=[]
	line_width=0
	for line in text_string.splitlines():
		size=font.size(line)[0]
		if size>line_width: line_width=size
	if line_width>width: line_width=width
	for text in splited_text:
		splited_and_wraped_text+=wrap_multi_line(text,font,width)
	lines=len(splited_and_wraped_text) if not limit else limit
	if limit!=None and limit<len(splited_and_wraped_text): 
		splited_and_wraped_text[limit-1]=splited_and_wraped_text[limit-1][:-3]+'...'
	surface=pygame.Surface((line_width,lines*(height+1)), pygame.SRCALPHA, 32)
	if background:
		try: surface.blit(background,(0,0))
		except: surface.fill(background)
	
	for l in range(lines):
		surface.blit( font.render( splited_and_wraped_text[l], anti_alias, text_color), (0,height*l))
	return surface

#HARD CODE, rever futuramente.
class innerScroller(object):
	def __init__(self,innerscr,width,vel,color_1,color_2=None,pos=None):
		self.screen=innerscr
		self.width=width
		self.vel=vel
		self.color_1=color_1
		self.color_2=color_2
		self.pos= pos if pos else (self.screen.display.get_width(),0)
		self.rect_2=None
		self.rect_1=None
		self.clicked=False
		self.clicked_y=0
	def preEvents(self):
		self.rect_2=None
		self.rect_1=None
		self.screen.resetPos()
	def eventControler(self,event,resize,move):
		if self.rect_2:
			mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
			if event.type==MOUSEBUTTONDOWN:
				if self.screen.display.get_rect(x=self.screen.pos[0]+move[0],y=self.screen.pos[1]+move[1]).collidepoint(mouse_pos):
					if event.button==1:
						self.clicked=True
						self.clicked_y=mouse_pos[1]-self.screen.pos[1]#
			elif event.type==MOUSEBUTTONUP:
				self.clicked=False
				if self.screen.pos[1]>self.rect_2.y:self.screen.pos[1]=self.rect_2.y
				if self.screen.pos[1]<self.rect_2.h-self.screen.display.get_height():self.screen.pos[1]=self.rect_2.h-self.screen.display.get_height()
			elif event.type==MOUSEMOTION:
				if self.clicked:
					self.screen.pos[1]=-self.clicked_y+mouse_pos[1]
	def blitOn(self,display):
		if not self.rect_2: 
			self.rect_2=pygame.Rect(self.pos[0],self.pos[1],self.width,display.get_height())
		self.rect_1=pygame.Rect(
			self.pos[0],
			float(-self.screen.pos[1])/float(self.screen.display.get_height())*self.rect_2.h,
			self.width,
			float(self.rect_2.h)/float(self.screen.display.get_height())*self.rect_2.h)
		if self.color_2: display.fill(self.color_2,self.rect_2)
		display.fill(self.color_1,self.rect_1)

class renderText(object):
	def __init__(self,font,text,color,pos,surface_width=None):
		self.render=font.render(text,True,color)
		self.pos=(pos[0]+(surface_width//2)-(font.size(text)[0]//2),pos[1]) if surface_width else pos
	def blitOn(self,display):
		display.blit(self.render,self.pos)

def scaleImage(img,scale=0.5):
	return pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
def scaleGroup(img_list_origin,scale=0.5):
	img_list=img_list_origin[:]
	for i in range(len(img_list)):
		img_list[i]=scaleImage(img_list[i],scale)
	return img_list
def resizeGroup(img_list_origin,size):
	img_list=img_list_origin[:]
	for i in range(len(img_list)):
		img_list[i]=pygame.transform.scale(img_list[i],size)
	return img_list

class playerImage(object):
	def __init__(self,source,center_pos,scale=1):
		self.source=source
		self.pos=center_pos
		self.scale=scale
	def blitOn(self,display):
		img=self.source.img if self.scale==1 else scaleImage(self.source.img,self.scale)
		img_crop=img.subsurface(img.get_rect(width=img.get_width()/3))
		display.blit(img_crop,self.pos)

def colorizeFull(image,new_color):
	new_image=image.copy()
	new_image.fill((0,0,0,255),None,pygame.BLEND_RGBA_MULT)
	new_image.fill(new_color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
	return new_image

def colorizeFull_ip(image,new_color):
	image.fill((0,0,0,255),None,pygame.BLEND_RGBA_MULT)
	image.fill(new_color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

import colorsys
def hls2rgb(h,l,s):
	return tuple(i * 255 for i in colorsys.hls_to_rgb(h/360.0,l/100.0,s/100.0))
def rgb2hls(r,g,b):
	hsl=list(colorsys.rgb_to_hls(r/255.0,g/255.0,b/255.0))
	return tuple(hsl[i]*[360,100,100][i] for i in range(3))

class colorPickerHLS(object):
	def __init__(self,pos,button_size,bar_pos,bar_size,sample_pos,sample_size,first_color,function=None):
		#first_color=[0,50,0]
		self.function=function
		self.first_hls=[color for color in first_color]
		self.resetColor()
		self.pos=[pos,bar_pos,sample_pos]
		self.size=[button_size,bar_size,sample_size]
		self.pressed=False
		self.rect=[pygame.Rect(pos,(button_size[0]*360,button_size[1]*100)),pygame.Rect(bar_pos,(bar_size[0]*100,bar_size[1]))]
		self.color_sheet=pygame.Surface((button_size[0]*360,button_size[1]*100))
		sheet_rect=pygame.Rect(0,0,int(button_size[0]) if button_size[0]>=1 else 1,int(button_size[1]))
		for h in range(361):
			for s in range(101):
				sheet_rect.topleft=(int(h*button_size[0]),int(s*button_size[1]))
				self.color_sheet.fill(hls2rgb(h,50,s),sheet_rect)
		self.pointer=[pygame.Surface(tuple(self.size[0][1]*7 for x in range(2)), pygame.SRCALPHA, 32),pygame.Surface(tuple(bar_size[0]*6 for n in range(2)), pygame.SRCALPHA, 32)]
		self.pointer[0].fill((0,0,0),pygame.Rect(self.size[0][1]*3,0,self.size[0][1],self.size[0][1]*7))
		self.pointer[0].fill((0,0,0),pygame.Rect(0,self.size[0][1]*3,self.size[0][1]*7,self.size[0][1]))
	def resetColor(self):
		self.rgb=hls2rgb(*self.first_hls)
		self.hls=[color for color in self.first_hls]
	def eventControler(self,event,resize,move):
		if self.pressed:
			mouse_pos=(event.pos[0]/resize[0],event.pos[1]/resize[1])
			if self.rect[0].move(move[0],move[1]).collidepoint(mouse_pos):
				hs=[(mouse_pos[x]-self.pos[0][x]-move[x])/self.size[0][x]  for x in range(2)]
				self.hls[0]=hs[0]
				self.hls[2]=hs[1]
			elif self.rect[1].move(move[0],move[1]).collidepoint(mouse_pos):
				self.hls[1]=(mouse_pos[0]-self.pos[1][0]-move[0])/self.size[1][0]
			
			self.rgb=hls2rgb(*self.hls)
		if event.type==MOUSEBUTTONDOWN:
			self.pressed=True
		if event.type==MOUSEBUTTONUP:
			self.pressed=False
			if self.function!=None: self.function(self.rgb)
	def blitOn(self,display):
		size1=self.size[0]
		pos1=self.pos[0]
		display.blit(self.color_sheet,pos1)
		pointer_rect=self.pointer[0].get_rect()
		pointer_rect.center=((self.hls[0]*self.size[0][0])+self.pos[0][0],(self.hls[2]*self.size[0][1])+self.pos[0][1])
		display.blit(self.pointer[0],pointer_rect.topleft)
		#display.fill((255,255,255),pygame.Rect( (self.hls[0]*self.size[0][0])+self.pos[0][0],(self.hls[2]*self.size[0][1])+self.pos[0][1],self.size[0][0] if self.size[0][0]>=1 else 1 ,self.size[0][1] if self.size[0][1]>=1 else 1 ))
		
		'''
		for h in range(361):
			for s in range(101):
				display.fill(hls2rgb(h,50,s),pygame.Rect((h*size1[0])+pos1[0],(s*size1[1])+pos1[1],size1[0],size1[1]))
		'''
		size2=self.size[1]
		pos2=self.pos[1]
		line_rect=pygame.Rect((0,0),size2)
		for l in range(101):
			line_rect.topleft=((l*size2[0])+pos2[0],pos2[1])
			display.fill(hls2rgb(self.hls[0],l,self.hls[2]),line_rect)
		if self.pos[2]!=None and self.size[2]!=None: display.fill(self.rgb,pygame.Rect(self.pos[2],self.size[2]))
		line_rect.topleft=((self.hls[1]*self.size[1][0])+self.pos[1][0],self.pos[1][1])
		#display.fill((0,0,0),line_rect)
		color=tuple(255-self.rgb[x] for x in range(3))#tuple(255-(255*self.hls[1]/100) for x in range(3))
		pygame.draw.polygon(self.pointer[1],color,[[self.size[1][0]*3,0],[0,self.size[1][0]*6],[self.size[1][0]*6,self.size[1][0]*6] ])
		display.blit(self.pointer[1],line_rect.move(-size2[0]*3,size2[1]-self.pointer[1].get_height() ).topleft)
		display.blit(pygame.transform.flip(self.pointer[1],False,True),line_rect.move(-size2[0]*3,0).topleft)

class simpleWhiteText(object):
	def __init__(self,text,pos,font):
		self.text=text
		self.pos=pos
		self.font=font
	def blitOn(self,display):
		display.blit(self.font.render(self.text, True, (255,255,255)),self.pos)
