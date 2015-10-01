class animatedSprite(object):
	def __init__(self,sprite_sheet,sprite_rect,pos,timer_event,rewind=True,repeat=-1):
		self.sprite_sheet=sprite_sheet
		self.sprite_rect=sprite_rect
		self.timer_event=timer_event
		self.rewind=rewind
		self.init_repeat=repeat
		self.direction=1
		self.pos=pos
		self.preEvents()
	def preEvents(self):
		self.repeat=self.init_repeat
	def setLine(self,line):
		rect=self.sprite_rect
		if rect.h*(line+1)<self.sprite_sheet.get_width():
			rect.y=rect.h*line
	def eventControler(self,event,resize,move):
		if event.type==self.timer_event:
			if self.repeat!=0:
				rect=self.sprite_rect
				sheet_width=self.sprite_sheet.get_width()
				rect.x+=rect.w*self.direction
				if self.rewind:
					if rect.right==sheet_width or rect.left==0:
						self.direction*=(-1)
						if self.repeat>0:self.repeat-=1
				else:
					if rect.right>sheet_width: 
						if self.repeat>0:self.repeat-=1
						rect.x-=rect.w if self.repeat==0 else rect.x
	def blitOn(self,display):
		display.blit(self.sprite_sheet.subsurface(self.sprite_rect),self.pos)
	def getImage(self):
		return self.sprite_sheet.subsurface(self.sprite_rect)
