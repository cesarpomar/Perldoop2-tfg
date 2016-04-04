#!/usr/bin/python
# -*- coding: utf-8 -*-
#Tipos de datos
BOOLEAN='Boolean'
INTEGER='Integer'
LONG='Long'
FLOAT='Float'
DOUBLE='Double'
STRING='String'
OBJECT='Object'
FILE='PerlFile'
#Tipos codigo
NONE='None'
VOID='void'

#Tipo etiquetas
LABEL_TYPE='label_type'
LABEL_DECLARE='label_declare'

#Flags del codigo
NEXT='next'
LAST='last'
RETURN='return'
VARIABLE='variable'
STATEMENT='statement'

#Orden de tipos
type_order={
NONE:0,
INTEGER:1,
LONG:2,
FLOAT:3,
DOUBLE:4,				
}

#Tipos de las etiquetas a java
var_types={
'boolean':BOOLEAN,
'integer':INTEGER,
'long':LONG,
'float':FLOAT,
'double':DOUBLE,
'string':STRING,
'file':FILE,
}

#Tipos de variables
ARRAY='ARRAY'
HASH='HASH'
LIST='LIST'
REF='REF'

#Clase para almacenar variables
class Variable():
	def __init__(self,type=None,pos=None,name=None,multi_type=None,private=False):
		self.name=name				#Nombre java de la variable
		self.type=type				#Tipo de la variable
		self.multi_type=multi_type	#Tipos en caso de multitipo
		self.pos=pos				#Posicion de la variable en el codigo
		self.private=private		#Indica si una variable puede ser accedida fuera del paquete	

#Guardar posicion para mostrar errores		
class Position():
	def __init__(self,p=None,pos=None,line=None,lexpos=None):
		if line!=None and lexpos!=None:
			self.line=line				#Linea del lexema
			self.lexpos=lexpos			#Posicion en el texto
		elif p!=None and pos!=None:
			self.line=p.lineno(pos)		
			self.lexpos=p.lexpos(pos)
		else:
			self.line=0
			self.lexpos=0			
			
	def column(self,parser):
		return parser.lexer.find_column(self.lexpos)

#Clase para almacenar el codigo segun se genera		
class Code():
	def __init__(self,value=None,type=None,st_value=None,value_opt=None,pos=None,declares=None,variable=None,multi_type=None,flags=None,ref_var=None,var_assing=None,ref=None):

		#Valores por defecto
		if value is None: value=""
		if declares is None: declares=[]
		if pos is None: pos=Position(line=1,lexpos=1)
		if flags is None: flags=dict()
		
		self.value=value				#Expresion en codigo java
		self.value_opt=value_opt		#Expresion java alternativa con operaciones logicas, mas eficiente si puede aplicarse
		self.st_value=st_value			#Expresion completa del campo value sin el codigo muerto asociado
		self.multi_type=multi_type		#Array de retorno posible en el uso de funciones multiretorno
		self.type=type					#Tipo de la expresion
		self.declares=declares			#Declaraciones dentro de la sentencia
		self.variable=variable			#Si el codigo es SOLO una variable aqui esta su entrada
		self.ref_var=ref_var			#Campo para obviar declaraciones en caso de usar st_value
		self.pos=pos					#posicion del codigo analizado basado en el ultimo token
		self.flags=flags				#Marcas para hacer comprobaciones sobre el codigo
		self.var_assing=var_assing		#Variables asignadas dentro del codigo (solo se usa en los if)
		self.ref=ref					#Marca que la coleccion debera ser refenciada en caso de una operacion que lo requiera
	
	#Al sumar dos codigos	
	def __add__(self,other):		
		r=Code()
		#Se suman las declaraciones
		r.declares=self.declares+other.declares
		#Las banderas
		r.flags.update(self.flags)
		r.flags.update(other.flags)
		#Y se coge la posicion mas alta
		if(self.pos.lexpos>other.pos.lexpos):
			r.pos=self.pos
		else:
			r.pos=other.pos
		return r
	
	def __repr__(self):
		return self.value
			

#Clase para almacenar las declaraciones		
class Declare():
	def __init__(self,value,pos,variable=False):
		self.value=value		#Valor de la declaracion
		self.variable=variable	#Contiene una variable
		self.pos=pos			#Posicion de la declaracion
		
		
class Type():
	def __init__(self,type,size=None):
		self.type=type		#Tipo puede ser Array o Hash
		self.size=size		#Tamaño si se quiere memoria
			
	def __eq__(self,type):
		return self.type==type	
	
	def __ne__(self,type):
		return self.type!=type	
	
	def __str__(self):
		return self.type

	def __repr__(self):
		return self.type
		
#Clase para almacenar los accesos a array y hash
class Access():
	def __init__(self,var):
		self.var=var			#Variable a la que se accede
		self.value=var.value	#Valor desde que es accedido
		self.type=var.type[:]	#Tipo del valor
		self.pos=var.pos		#Posicion en el codigo fuente
		self.read_value=''		#Codigo a añadir al valor si el acceso es de lectura
		self.store_value=' = '	#Codigo a añadir al valor si el acceso es de escritura
		self.end_value=''		#Codigo a añadir al final, tanto en lectura como escritura
		self.declares=[]		#Declaraciones en el acceso
		self.ref=None			#Marca que la coleccion debera ser refenciada en caso de una operacion que lo requiera
		
	def __repr__(self):
		return self.value
		
class Function():
	def __init__(self,args,returns,pos=None):
		if args is None: args=[]
		if returns is None: returns=[]
		
		self.args=args			#Tipos de los argumentos de la funcion
		self.returns=returns	#Tipos de los retornos de la funcion
		self.pos=pos		  	#Posicion en el codigo
		
class Package():
	def __init__(self,name,variables,functions):
		self.name=name				#Nombre del paquete
		self.variables=variables	#Variables del paquete
		self.functions=functions	#Funciones del paquete

	
	
	