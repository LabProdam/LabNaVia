import pygame
from pygame.locals import*

class popUpTimer(object):
	def __init__(self,time,popup_call,popup_time,popup_render):
		self.popup_call=popup_call
		self.time=time
		self.popup_time=popup_time
		self.popup_render=popup_render
	def preEvents(self):
		pygame.time.set_timer(USEREVENT+5,self.time)
	def eventControler(self,event,resize,move):
		if event.type==USEREVENT+5:
			self.popup_call(self.popup_render,self.popup_time)
			pygame.time.set_timer(USEREVENT+5,0)

class popUp(object):
	def __init__(self,pos,final_pos,move,background,ident ):
		self.background=background#uma superficie, pode ser imagem ou surface preenchida com cor
		self.init_pos=pos
		self.final_pos=final_pos
		self.ident=ident
		self.move=move
		self.setZero()
	def setZero(self):
		self.pos=[self.init_pos[0],self.init_pos[1]]
		self.text=None
		self.pop_up=False
		self.time=0
	def callMasterPopup(self,pos,final_pos,move,background,ident,rendered_text,time):pass#ideia profuturo
	def callPopup(self,rendered_text,time):
		self.text=rendered_text
		self.time=time
		self.pop_up=True
	def eventControler(self,event,resize,move):
		if event.type==USEREVENT+4:
			pygame.time.set_timer(USEREVENT+4,0)
			self.time=0
	def popupEngine(self):
		if self.time==0:
			#voltando
			if self.pos[0]!=self.init_pos[0] or self.pos[1]!=self.init_pos[1]:
				self.pos[0]-=self.move[0]
				self.pos[1]-=self.move[1]
			else:
				self.pop_up=False
		else:
			#indo
			if self.pos[0]!=self.final_pos[0] or self.pos[1]!=self.final_pos[1]:
				self.pos[0]+=self.move[0]
				self.pos[1]+=self.move[1]
			elif self.time>0:
				pygame.time.set_timer(USEREVENT+4,self.time)
				self.time=(-1)
	def blitPopup(self,display):
		self.popupEngine()
		display.blit(self.background,self.pos)#desenha o background
		idented_pos=(self.pos[0]+self.ident[0],self.pos[1]+self.ident[1])#identa a posicao
		display.blit(self.text,idented_pos)#desenha o texto identado
	def blitOn(self,display):
		if self.pop_up: self.blitPopup(display)
