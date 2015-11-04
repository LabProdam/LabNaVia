# -*- coding: utf-8 -*-
import urllib
import json
import math
from datetime import datetime,date


#usado anteriorment
#latlng=(-46.6875639,-23.5759547,1000)
#mapscult_instance=urllib.urlopen('http://spcultura.prefeitura.sp.gov.br/api/space/find?@select=id,%20name,%20location,%20horario,%20site,%20acessibilidade&@order=name%20ASC&_geoLocation=GEONEAR'+str(latlng))
#mapscult_str=mapscult_instance.read()
#mapscult_list= json.loads(mapscult_str)



#VÁRIÁVEIS QUE PODEM VIR A SER INCREMENTADAS
#shortDescription
#createTimeStamp
#owner
#emailPublico
#emailPrivado
#telefonePublico
#telefone1(ou 2)
#endereco

#Essenciais
	#name
	#location
	#horario
	#site
	#acessibilidade

class findUrl(object):
	def __init__(self,url,latlng,*args):
		self.latlng=latlng
		self.args=list(args)
		self.params=""
		self.url=url
		self.completeUrl=''
		self.url_list=[]
		self.eventJson=[]
		self.localsFromMaps=[]
		self.distances=[]
		self.distM=[]
		self.text=''
	def run(self,latlng):
		self.latlng=latlng
		self.putParams()
		self.calcLocalDistance()
		self.putUrl()
		self.listUrl()
	def runText(self,latlng):
		self.putParams()
		self.calcLocalDistance()
		self.putUrl()
		self.listUrlText()
		return self.text
	def putParams(self):
		for i in range (0,len(self.args)):
			self.params+="%20"+str(self.args[i])+","
		
		self.completeUrl=self.url[0]+self.params+self.url[1]
		self.completeUrl=self.completeUrl+str(self.latlng)
	
	def putUrl(self):
		url_instance=urllib.urlopen(self.completeUrl)
		url_str=url_instance.read()
		url_list= json.loads(url_str)
		self.url_list=url_list
	
	def addArgs(self, *new_args):
		for new_arg in new_args:
			self.args.append(new_arg)
			#nao usado ;)

	def checkUrl(self,latlng):
		self.latlng=latlng
		self.putParams()
		self.calcLocalDistance()
		self.putUrl()
		return True if len(self.url_list)>0 else False
	def listUrl(self):
		print 'listUrl()'
		spaceId = []

		spaceIdStr = ""
		print '1º for'
		for i in range (0, len(self.url_list)):
			spaceIdStr = spaceIdStr+"EQ("+str(self.url_list[i]["id"])+"),"
		
		spaceIdStr = spaceIdStr[:-1]#depois ele come a ultima virgula
		
		dateNow = str(date.today())
		print dateNow
		dateLimit = str(date.fromordinal(date.today().toordinal()+30))
		print dateLimit

		url_debug="http://spcultura.prefeitura.sp.gov.br/api/eventoccurrence/find?@select=id, eventId, startson,spaceId&_startsOn=AND(GT("+dateNow+"), LT("+dateLimit+"))&spaceId=OR("+spaceIdStr+")"
		print url_debug
		print '1º acesso ao spcultura'
		paginaEventOcc_instance = urllib.urlopen(url_debug)
		print 'lendo...'
		eventOcc_str= paginaEventOcc_instance.read()
		print eventOcc_str
		print 'eu carregando json...'

		eventOccJson_list = json.loads(eventOcc_str)
		
		eventIdStr = ""
		print '2º for'
		for i in range (0, len(eventOccJson_list)):
			eventIdStr +="EQ("+str(eventOccJson_list[i]["eventId"])+"),"

		eventIdStr = eventIdStr[:-1]#remove ultima virugla
		
		try:url_debug_2="http://spcultura.prefeitura.sp.gov.br/api/event/find?@select=id,%20name&@order=id%20ASC&id=OR("+eventIdStr+")"
		except Exception,e:print e
		print '2º acesso ao spcultura'
		paginaEvent = urllib.urlopen(url_debug_2)
		print 'lendo...'
		event=paginaEvent.read()
		print 'carregando json'
		self.eventJson = json.loads(event)
		print 'retornando...'
		return True if len(self.url_list)>0 else False
	def listUrlText(self):
		self.text= "\n \nLOCAIS\n "
		'''
		1º for
		'''
		for i in range(0,len(self.url_list)):
			for arg in self.args:
				self.text+= '\n'+unicode(self.url_list[i][arg])
			self.localsFromMaps.append(self.url_list[i])
			self.text+= "\n-----------------------------------------"
		
		spaceId = []
		'''
		2º for
		'''
		for i in range (0, len(self.url_list)):
			spaceId.append(self.url_list[i]["id"])

		spaceIdStr = "EQ("+str(spaceId[0])+"),"
		'''
		3º for
		'''
		for i in range (1, len(spaceId)):	
			spaceIdStr = spaceIdStr+"EQ("+str(spaceId[i])+"),"

		spaceIdStr = spaceIdStr[:-1]
		
		now = datetime.now()
		dateNow = str(now.year)+"-"+str(now.month)+"-"+str(now.day)
		dateLimit = str(now.year)+"-"+str(now.month+2)+"-"+str(now.day)

		url_debug="http://spcultura.prefeitura.sp.gov.br/api/eventoccurrence/find?@select=id, eventId, startson,spaceId&_startsOn=AND(GT("+dateNow+"), LT("+dateLimit+"))&spaceId=OR("+spaceIdStr+")"
		#print url_debug
		paginaEventOcc_instance = urllib.urlopen(url_debug)
		eventOcc_str= paginaEventOcc_instance.read()
		eventOccJson_list = json.loads(eventOcc_str)
		eventId = []
		'''
		4º for
		'''
		for i in range (0, len(eventOccJson_list)):
			eventId.append(eventOccJson_list[i]["eventId"])

		if eventId != []:
			eventIdStr = "EQ("+str(eventId[0])+"),"
		'''
		5º for
		'''
		for i in range (1, len(eventId)):
			eventIdStr = eventIdStr+"EQ("+str(eventId[i])+"),"

		eventIdStr = eventIdStr[:-1]
		try:url_debug_2="http://spcultura.prefeitura.sp.gov.br/api/event/find?@select=id,%20name&@order=id%20ASC&id=OR("+eventIdStr+")"
		except Exception,e:print e
		#print url_debug_2
		paginaEvent = urllib.urlopen(url_debug_2)
		event= paginaEvent.read()
		self.eventJson = json.loads(event)
		
		self.text+= "\n \nEVENTOS\n "
		'''
		6º for
		'''
		for i in range (0, len(self.eventJson)):
			self.text+= "\n"+unicode(self.eventJson[i]["name"])
			self.text+=  "\n-----------------------------------------"
		return self.text
	def calcLocalDistance(self):
		print 'calculando distancias'
		latA=math.radians(self.latlng[1])
		lngA=math.radians(self.latlng[0])
		localist=[]
		radiusEarth=6371	#6372.795477598 #ou 6371 #ou 6381,4616755 # outros: 6378,1 6231,34
		print '1º for'
		for i in range(0,len(self.url_list)):
			localist.append((float(self.url_list[i]["location"]["latitude"]),float(self.url_list[i]["location"]["longitude"])))
		print '2º for'
		for l in range (0,len(localist)):
			plngB=localist[l][1]
			platB=localist[l][0]
			lngB=math.radians(plngB)
			latB=math.radians(platB)
			distKm=radiusEarth*math.acos(math.sin(latA)*math.sin(latB)+math.cos(latA)*math.cos(latB)*math.cos(lngA-lngB))
			self.distM.append(distKm*1000)
	def getEvents(self):
		return self.eventJson
	def getLocals(self):
		return self.url_list
	def getDistances(self):
		return self.distM
