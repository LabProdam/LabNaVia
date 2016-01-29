# -*- coding: utf-8 -*-
import urllib2
import json
import math
from debugLog import *
from datetime import datetime,date
import sys


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

'''
	Lista de códigos de erros previstos:
		P7500 : Tudo ok (nunca aparecerá, afinal não é erro)
		P7510 : SP Cultura está no ar, mas nosso aplicativo não foi capaz de retornar a lista de locais/eventos.
		P7501 : Mapas Culturais está no ar, mas nosso aplicativo não foi capaz de retornar a lista de locais/eventos.
		P7511 : SP Cultura e Mapas Culturais estão no ar, mas nosso aplicativo não foi capaz de retornar a lista de locais/eventos, de nenhum dos dois.
		P8510 : SP Cultura fora do ar, não foi possível acessar a home do site.
		P7601 : Mapas Culturais fora do ar, não foi possível acessar a home do site.
		P8611 : SP Cultura e Mapas Culturais fora do ar, não foi possível acessar a home dos dois sites.
	Como funciona o código de erros:
		P de Problema
		7+(1 se sp cultura fora do ar, senão 0)
		5+(1 se mapas culturais fora do ar, senão 0)
		1 se sp cultura inascessível, senão 0
		1 se mapas culturais inascessível, senão 0
'''

def isNetworkConnected(ping="http://www.google.com/"):
	try:
		data=urllib2.urlopen(ping)
		return True
	except Exception,e:
		debugGps(e)
	return False
	

class findUrl(object):
	def __init__(self,url,urlBr,latlng,*args):
		self.latlng=latlng
		self.args=list(args)
		self.params=""
		self.url=url
		self.urlBr=urlBr
		self.completeUrl=''
		self.url_list_sp=[]
		self.url_list_br=[]
		self.eventJson=[]
		self.localsFromMaps=[]
		self.distances=[]
		self.distM=[]
		self.distMbr=[]
		self.listObjSp=[]
		self.listObjBr=[]
		self.listObj=[]
		self.url_sp_off=False
		self.url_br_off=False
		self.sp_ping=True
		self.br_ping=True
		self.web_on=True
		self.len_events=0
		self.len_locals=0
	def run(self,latlng):
		self.web_on=isNetworkConnected()
		self.sp_ping=isNetworkConnected("http://spcultura.prefeitura.sp.gov.br/")
		self.br_ping=isNetworkConnected("http://mapas.cultura.gov.br/")
		if self.web_on:
			self.startRun(latlng)
		self.len_locals=len(self.listObj)
		self.len_events=len(self.eventJson)
	def startRun(self,latlng):
		self.latlng=latlng
		self.putParams()
		self.putUrl()
		self.calcLocalDistance()
		self.addObj()
		self.listUrl()
		self.comparaLista()
		self.listObj.sort(key = lambda listObj: listObj["distancia"])
		self.listLimit()
	def putParams(self):
		for i in range (0,len(self.args)):
			self.params+=str(self.args[i])+","
		
		self.completeUrl=self.url[0]+self.params+self.url[1]
		self.completeUrl=self.completeUrl+'('+str(self.latlng[0])+','+str(self.latlng[1])+','+str(self.latlng[2])+')'
		
		#fazendo a url dos mapas da cultura
		for i in range (0,len(self.args)):
			self.params+=str(self.args[i])+","
		
		self.completeUrlBr=self.urlBr[0]+self.params+self.urlBr[1]
		self.completeUrlBr=self.completeUrlBr+'('+str(self.latlng[0])+','+str(self.latlng[1])+','+str(self.latlng[2])+')'

	def returnUrl(self,url):
		url_instance=urllib2.urlopen(url)
		url_str=url_instance.read()
		url_instance.close()
		return json.loads(url_str)
	def putUrl(self):
		try:
			self.url_list_sp=self.returnUrl(self.completeUrl)
		except Exception,e:
			self.url_sp_off=True
			debugGps('SP CULTURA FORA DO AR')
			debugGps(e)
		debugGps(self.completeUrl)
		try:
			self.url_list_br=self.returnUrl(self.completeUrlBr)
		except Exception,e:
			self.url_br_off=True
			debugGps('BR CULTURA FORA DO AR')
			debugGps(e)
		debugGps(self.completeUrlBr)
	def checkUrl(self,latlng):
		self.latlng=latlng
		self.putParams()
		self.calcLocalDistance()
		self.putUrl()
		return True if len(self.url_list_sp)>0 else False
	def listUrl(self):
		debugGps('listUrl()')
		spaceId = []

		spaceIdStr = ""
		debugGps('1 for')
		if len(self.listObjSp)>0:
			for i in range (0, len(self.listObjSp)): 
				spaceIdStr = spaceIdStr+"EQ("+str(self.listObjSp[i]["id"])+"),"

			spaceIdStr = spaceIdStr[:-1]#depois ele come a ultima virgula
		
			dateNow = str(date.today())
			debugGps(dateNow)
			dateLimit = str(date.fromordinal(date.today().toordinal()+30))
			debugGps(dateLimit)

			url_debug="http://spcultura.prefeitura.sp.gov.br/api/eventoccurrence/find?@select=id,eventId,startson,spaceId&_startsOn=AND(GT("+dateNow+"),LT("+dateLimit+"))&spaceId=OR("+spaceIdStr+")"
			debugGps(url_debug)
			debugGps('1 acesso ao spcultura')
			paginaEventOcc_instance = urllib2.urlopen(url_debug)
			debugGps('lendo...')
			eventOcc_str= paginaEventOcc_instance.read()
			debugGps(eventOcc_str)
			debugGps('eu carregando json...')

			eventOccJson_list = json.loads(eventOcc_str)
					
			eventIdStr = ""
			debugGps('2 for')
			if len(eventOccJson_list)>2:
				for i in range (0, len(eventOccJson_list)):
					eventIdStr +="EQ("+str(eventOccJson_list[i]["eventId"])+"),"

				eventIdStr = eventIdStr[:-1]#remove ultima virugla
				
				try:url_debug_2="http://spcultura.prefeitura.sp.gov.br/api/event/find?@select=id,name&@order=id%20ASC&id=OR("+eventIdStr+")"
				except Exception,e:debugGps(e)
				debugGps('2 acesso ao spcultura')
				paginaEvent = urllib2.urlopen(url_debug_2)
				debugGps('lendo...')
				event=paginaEvent.read()
				debugGps('carregando json')
				self.eventJson = json.loads(event)
				debugGps(self.eventJson)
				debugGps('retornando...')
		return True if len(self.listObj)>0 else False
	
	def returnLocalDistance(self,url):
		localist=[]
		latA=math.radians(self.latlng[1])
		lngA=math.radians(self.latlng[0])
		radiusEarth=6371	#6372.795477598 #ou 6371 #ou 6381,4616755 # outros: 6378,1 6231,34
		for i in range(0,len(url)):
			localist.append((float(url[i]["location"]["latitude"]),float(url[i]["location"]["longitude"])))
		sys.stdout.flush()
		for l in range (0,len(localist)):
			plngB=localist[l][1]
			platB=localist[l][0]
			lngB=math.radians(plngB)
			latB=math.radians(platB)
			distKm=radiusEarth*math.acos(math.sin(latA)*math.sin(latB)+math.cos(latA)*math.cos(latB)*math.cos(lngA-lngB))
			localist[l]=distKm*1000
		return localist
	def calcLocalDistance(self):
		debugGps('calculando distancias')
		if not self.url_sp_off:
			self.distM=self.returnLocalDistance(self.url_list_sp)
		if not self.url_br_off:
			self.distMBr=self.returnLocalDistance(self.url_list_br)
		debugGps('distancias calculadas')
	def returnObj(self,url):
		listObj=[]
		for i in range(len(url)):
			listObj.append(
				{
					"id": self.url_list_sp[i]["id"],
					"nome": self.url_list_sp[i]["name"],
					"distancia": self.distM[i],
					"belongList":"spCult"
				}
			)
		return listObj
	def addObj(self):
		if not self.url_sp_off:
			self.listObjSp=self.returnObj(self.url_list_sp)
		if not self.url_br_off:
			self.listObjBr=self.returnObj(self.url_list_br)
	def comparaLista(self):
		listObjTemp=[]
		for el in self.listObjBr:
			match = False
			for spel in self.listObjSp:
				if spel['nome'].upper() == el['nome'].upper():
					match = True
					break
			if not match:
				listObjTemp.append(el)
		self.listObj = self.listObjSp+listObjTemp
	
	def listLimit(self):
		limite = 30
		
		if len(self.listObj)> limite:
			del self.listObj[limite:]
			debugGps('limitado')
	
	def emptyList(self):
		
		self.url_list_sp=[]
		self.url_list_br=[]
		self.listObjBr=[]
		self.listObjSp=[]
		#self.listObj=[]
		
	def getEvents(self):
		return self.eventJson
	'''
	def getLocals(self):
		return self.url_list
	def getDistances(self):
		return self.distM
		'''
