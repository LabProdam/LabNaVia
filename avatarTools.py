# -*- coding: utf-8 -*-
import pygame,os, cPickle
from pygame.locals import *
from screenTools import colorizeFull
dir_avatar='images'+str(os.sep)+'avatar'+str(os.sep)
dir_data='data'+str(os.sep)
try:font=pygame.font.Font(None,22)
except:font=None
class avatarTools(object):
	def __init__(self,player,shoes,pants,shirt,hair,head,pos=None,ident=0):
		self.bike=pygame.image.load(dir_avatar+'bike0.png').convert_alpha()
		self.skin=pygame.image.load(dir_avatar+'skinN.png').convert_alpha()
		self.skin_color=(0,0,0)
		self.avatar=[
					[0,shoes],
					[0,pants],
					[0,shirt],
					[0,hair],
					[0,head]
					]
		self.icons=[pygame.image.load(dir_avatar+'icon'+str(av)+'0.png').convert_alpha() for av in range(5)]
		self.player=player
		self.focus_avatar=5
	def clearSave(self):
		try:
			save_file=open(dir_data+"avatar_data.lab",'wb')
			save_file.truncate()
			save_file.close()
		except Exception,e:print e
		for avatar in self.avatar:
			avatar[0]=0
		self.skin_color=(191,143,88)
		self.updateAvatar()
		print 'cleared avatar'
	def preEvents(self):
		try:
			save_file=open(dir_data+"avatar_data.lab",'rb')
			for avatar in self.avatar:
				avatar[0]=cPickle.load(save_file)
			self.skin_color=cPickle.load(save_file)
			save_file.close()
		except Exception,e:print e
		self.updateAvatar()
	def posEvents(self):
		try:
			save_file=open(dir_data+"avatar_data.lab",'wb')
			for avatar in self.avatar:
				cPickle.dump(avatar[0],save_file)
			cPickle.dump(self.skin_color,save_file)
			save_file.close()
		except Exception,e:print e
	def setSkinColor(self,new_color):
		self.skin_color=new_color
		self.updateAvatar()
	def updateAvatar(self):
		img_size=(237,194)
		new_avatar=pygame.Surface(img_size, pygame.SRCALPHA, 32)
		new_avatar.convert_alpha()
		new_avatar.blit(self.bike,(0,0))
		new_avatar.blit(colorizeFull(self.skin,self.skin_color).convert_alpha(),(0,0))
		for item in self.avatar:
			new_avatar.blit(item[1][item[0]][0] , (0,0))
		self.player.setImg(new_avatar)
	def focusAvatar(self,av):
		self.focus_avatar=av
	def setSelection(self,av,pos):
		self.avatar[av][0]=pos
		self.updateAvatar()
	def moveFocus(self,move):
		self.moveSelection(self.focus_avatar,move)
	def moveSelection(self,av,move):	
		self.avatar[av][0]+=move
		avatar_len=len(self.avatar[av][1])
		if self.avatar[av][0]<0:
			self.avatar[av][0]=avatar_len-1
		elif self.avatar[av][0]>=avatar_len:
			self.avatar[av][0]=0
		self.updateAvatar()
	def blitOnOld(self,display):#_Old0
		global font
		if font:
			pos=[350,25]
			for av in range(4,-1,-1):
				try:
					text=font.render(self.avatar[av][1][self.avatar[av][0]][1],True,(0,0,0))
					display.blit(text,pos)
					display.blit(self.icons[4-av],(0,pos[1]-15))
					pos[1]+=72
				except Exception,e:print e
	def blitOn(self,display):
		global font
		if font:
			pos_center=(
						((250+50)/2)#metade da (distancia entre as setas, mais a largura da segunda)
						+220#mais a posição em x da primeira
						,330)
			av=self.focus_avatar
			if av<len(self.avatar) and av>=0:
				text=font.render(self.avatar[av][1][self.avatar[av][0]][1],True,(255,255,255))
				try:display.blit(text,text.get_rect(center=pos_center).topleft )
				except Exception,e:print e
