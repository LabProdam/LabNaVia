import urllib
import json
from datetime import datetime

def buscarSpaceEvent(lat,lng):
    paginaSpace = urllib.urlopen("http://spcultura.prefeitura.sp.gov.br/api/space/find?@select=id,%20name,%20location&@order=id%20ASC&_geoLocation=GEONEAR("+str(lng)+","+str(lat)+",1500)")
    space= paginaSpace.read()
    spaceJson = json.loads(space)
    spaceId = []
    spaceLoc = []
    '''
    for i in range (0, len(spaceJson)):
        print spaceJson[i]["id"]'''
    
    for i in range (0, len(spaceJson)):
        spaceId.append(spaceJson[i]["id"])
        spaceLoc.append(spaceJson[i]["location"])

    spaceIdStr = "EQ("+str(spaceId[0])+"),"

    for i in range (1, len(spaceId)):
        spaceIdStr = spaceIdStr+"EQ("+str(spaceId[i])+"),"

    spaceIdStr = spaceIdStr[:-1]
    
    #print spaceIdStr

    now = datetime.now()
    dateNow = str(now.year)+"-"+str(now.month)+"-"+str(now.day)
    dateLimit = str(now.year)+"-"+str(now.month+2)+"-"+str(now.day)
    #print dateNow
    #print dateLimit
    paginaEventOcc = urllib.urlopen("http://spcultura.prefeitura.sp.gov.br/api/eventoccurrence/find?@select=id, eventId, startson,spaceId&_startsOn=AND(GT("+dateNow+"), LT("+dateLimit+"))&spaceId=OR("+spaceIdStr+")")
    eventOcc= paginaEventOcc.read()
    eventOccJson = json.loads(eventOcc)
    eventId = []

    for i in range (0, len(eventOccJson)):
        eventId.append(eventOccJson[i]["eventId"])

    eventIdStr = "EQ("+str(eventId[0])+"),"

    for i in range (1, len(eventId)):
        eventIdStr = eventIdStr+"EQ("+str(eventId[i])+"),"

    eventIdStr = eventIdStr[:-1]

    
    paginaEvent = urllib.urlopen("http://spcultura.prefeitura.sp.gov.br/api/event/find?@select=id,%20name&@order=id%20ASC&id=OR("+eventIdStr+")")
    event= paginaEvent.read()
    eventJson = json.loads(event)

    #print eventJson

    print "Lista de Locais\n"
    for i in range (0, len(spaceJson)):
        print spaceJson[i]["name"]
    print "\n\n"

    print "Lista de Eventos\n"
    for i in range (0, len(eventJson)):
        print eventJson[i]["name"]
        for e in range(len(spaceLoc)):
        	if spaceId[e]==eventJson[i]['id']:
        		print spaceLoc[e]
        		break
	

    return "Algo Util"


    '''
        
    print "http://spcultura.prefeitura.sp.gov.br/api/eventoccurrence/find?@select=id, eventId, startson,spaceId&_startsOn=AND(GT("+dateNow+"), LT("+dateLimit+"))&spaceId=OR("+spaceIdStr+")"

    "http://spcultura.prefeitura.sp.gov.br/api/event/find?@select=id,%20name&@order=id%20ASC&id=OR("+eventIdStr+")"  '''
        


print "Metodo de busca de locais e eventos por Georeferencia"
lat = input("Entre com a Latitude: ")
lng = input("Entre com a Longitude: ")

buscarSpaceEvent(lat, lng)

