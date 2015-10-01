import cPickle

def saveItens(save_file,*itens):
	opened_file=open(save_file,'wb')
	for item in itens:
		try:cPickle.dump(item,opened_file)
		except Exception,e:print e
	opened_file.close()
def loadItens(load_file,*itens):
	opened_file=open(load_file,'rb')
	for item in itens:
		try:item=cPickle.load(opened_file)
		except Exception,e:print e
	opened_file.close()
def clearFile(data_file):
	opened_file=open(data_file,'wb')
	opened_file.truncate()
	opened_file.close()
	

class saveSystem(object):
	def __init__(self,save_file,*itens):
		self.save_file=save_file
		self.itens=list(itens)
		self.setUpdateFunctions()
		self.setClearFunctions()
		self.setLoadFunctions()
		self.setSaveFunctions()
	
	def setUpdateFunctions(self,*functions):
		self.update_functions=list(functions)
	def setClearFunctions(self,*functions):
		self.clear_functions=list(functions)
	def setLoadFunctions(self,*functions):
		self.load_functions=list(functions)
	def setSaveFunctions(self,*functions):
		self.save_functions=list(functions)
	def callFunctions(self,*many_functions_lists):
		for functions_list in many_functions_lists:
			for function_n_args_list in functions_list:
				function_n_args_list[0](*function_n_args_list[1:])
	
	def saveItens(self):
		saveItens(self.save_file,*self.itens)
		self.callFunctions(self.save_functions,self.update_functions)
	
	def loadItens(self):
		loadItens(self.save_file,*self.itens)
		self.callFunctions(self.load_functions,self.update_functions)
	
	def clearItens(self):
		clearFile(self.save_file)
		self.callFunctions(self.clear_functions,self.update_functions)
