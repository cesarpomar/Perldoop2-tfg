#!/usr/bin/python
# -*- coding: utf-8 -*-
from libs.Datatypes import BOOLEAN,INTEGER,LONG,FLOAT,DOUBLE,STRING,VOID,ARRAY,HASH,LIST,Type,REF,FILE
from libs.Messages import error
import re

def to_number(code):
	#Si es una coleccion o un booleano usamos su transformacion entera
	if code.type[0]==VOID or len(code.type)>1 or code.type[0]==BOOLEAN:
		code.type=[INTEGER]
		code.value=to_integer(code)
	#Si es una cadena combertimos a double
	elif code.type[0]==STRING:
		code.value=to_double(code)
		code.type=[DOUBLE]
	return code.value

def to_floor(code):
	#Si no es entero, lo combertimos
	if code.type[0] not in (INTEGER, LONG):
		code.type=[INTEGER]
		code.value=to_integer(code)
	return code.value

def to_boolean(code):
	#Si ya tenemos un valor booleano
	if code.value_opt:
		return code.value_opt
	#Si no tiene un solo tipo usamos su tamaño
	elif code.type[0]==VOID:
		return 'Pd.len('+code.value+') != 0'
	elif code.type[0]==BOOLEAN:
		return code.value
	elif code.type[0]==FILE:
		return 'true'
	else:
		return 'Pd.eval('+code.value+')'

def to_integer(code):
	#Si no es un tipo basico
	if len(code.type)>1:
		if code.type[0]==ARRAY:
			return code.value+'.length'
		elif code.type[0]==LIST:
			return code.value+'.size()'
		#Tanto si es un hash o una referencia
		else:
			#Como no existe un valor usable ponemos uno por defecto para evitar errores
			return '1'
	#Si es un numero de mayor rango
	elif code.type[0] in [LONG,FLOAT,DOUBLE]:
		return '(int)('+code.value+')'
	#Si hay que interpretar una cadena
	elif code.type[0] == STRING:
		return 'Integer.parseInt('+code.value+')'
	#Si sale de un boleano
	elif code.type[0] == BOOLEAN:
		return '('+code.value+')?1:0'
	#Si no tiene un solo tipo
	elif code.type[0]==VOID:
		return 'Pd.len('+code.value+')'
	elif code.type[0]==FILE:
		return '1'
	#Opcion para errores sin tipo
	else:
		return code.value

def to_long(code):
	#Si no es un tipo basico
	if len(code.type)>1:
		if code.type[0]==ARRAY:
			return '((long)'+code.value+'.length)'
		elif code.type[0]==LIST:
			return '((long)'+code.value+'.size())'
		#Tanto si es un hash o una referencia
		else:
			#Como no existe un valor usable ponemos uno por defecto para evitar errores
			return '1l'
	#Si es un numero de otro rango
	elif code.type[0]  in [INTEGER,FLOAT,DOUBLE]:
		#Si es un numero, para ahorrar el cast añadimos l
		if re.match("^(0[xbXB])?[\d]+$", code.value):
			return code.value+'l'
		else:
			return '((long)'+code.value+')'
	#Si hay que interpretar una cadena
	elif code.type[0] == STRING:
		return 'Long.parseLong('+code.value+')'
		#Si sale de un boleano
	elif code.type[0] == BOOLEAN:
		return '('+code.value+')?1l:0l'
	#Si no tiene un solo tipo
	elif code.type[0]==VOID:
		return '((long)Pd.len('+code.value+'))'
	elif code.type[0]==FILE:
		return '1l'
	#Opcion para errores sin tipo
	else:
		return code.value
	
def to_float(code):
	#Si no es un tipo basico
	if len(code.type)>1:
		if code.type[0]==ARRAY:
			return '((float)'+code.value+'.length)'
		elif code.type[0]==LIST:
			return '((float)'+code.value+'.size())'
		#Tanto si es un hash o una referencia
		else:
			#Como no existe un valor usable ponemos uno por defecto para evitar errores
			return '1f'
	#Si es numero de otro rango
	elif code.type[0] in [INTEGER,LONG]:
		#Si es un numero, para ahorrar el cast añadimos f
		if re.match("^(0[xbXB])?[\d]+$", code.value):
			return code.value+'f'
		else:
			return '((float)'+code.value+')'
	elif code.type[0] == DOUBLE:	
		#Si es un numero, para ahorrar el cast añadimos f
		if re.match("^\d*\.\d*eE\d*$", code.value):
			return code.value+'d'
		else:
			return '((float)'+code.value+')'		
	#Si hay que interpretar una cadena
	elif code.type[0] == STRING:
		return 'Float.parseFloat('+code.value+')'
		#Si sale de un boleano
	elif code.type[0] == BOOLEAN:
		return '('+code.value+')?1f:0f'
	#Si no tiene un solo tipo
	elif code.type[0]==VOID:
		return '((float)Pd.len('+code.value+'))'
	elif code.type[0]==FILE:
		return '1f'
	#Opcion para errores sin tipo
	else:
		return code.value
			
def to_double(code):		
	#Si no es un tipo basico
	if len(code.type)>1:
		if code.type[0]==ARRAY:
			return '((double)'+code.value+'.length)'
		elif code.type[0]==LIST:
			return '((double)'+code.value+'.size())'
		#Tanto si es un hash o una referencia
		else:
			#Como no existe un valor usable ponemos uno por defecto para evitar errores
			return '1d'
	#Si es un entero
	elif code.type[0] == [INTEGER,LONG,FLOAT]:
		#Si es un numero, para ahorrar el cast añadimos l
		if re.match("^(0[xbXB])?[\d]+$", code.value):
			return code.value+'d'
		else:
			return '((double)'+code.value+')'
	#Si hay que interpretar una cadena
	elif code.type[0] == STRING:
		return 'Double.parseDouble('+code.value+')'
		#Si sale de un boleano
	elif code.type[0] == BOOLEAN:
		return '('+code.value+')?1d:0d'
	#Si no tiene un solo tipo
	elif code.type[0]==VOID:
		return '((double)Pd.len('+code.value+'))'
	elif code.type[0]==FILE:
		return '1d'
	#Opcion para errores sin tipo
	else:
		return code.value	
	
def to_string(code):
	#Si no es un tipo basico
	if len(code.type)>1:
		if code.type[0]==ARRAY:
			return 'String.valueOf('+code.value+'.length)'
		elif code.type[0]==LIST:
			return 'String.valueOf('+code.value+'.size())'
		#Tanto si es un hash o una referencia
		else:
			#Como no existe un valor usable ponemos uno por defecto para evitar errores
			return '"1"'
	#Si ya es una cadena queda tal cual
	elif code.type[0] == STRING:
		return code.value
	elif code.type[0]==FILE:
		return '"1"'
	#En caso contrario transformamos
	else:
		return 'String.valueOf('+code.value+')'	

#Representacion de una variable al ser impresa(distinto de to_string)			
def to_repr(code):
	#Si es un tipo basico, no hacemos nada
	if len(code.type)==1:
		#Si es un fichero imprimimos una constante
		if code.type[0]==FILE:
			return 'GLOB(0x1)'
		else:
			return code.value
	#Si es interpretado como referencia
	elif code.ref and not code.type[0]==REF:	
		if code.type[0] == HASH:
			type='HASH'
		else:
			type='ARRAY'	
		return '"'+type+'(0x1)"'	
	else:
		#Si es una referencia, imitamos a perl para fines de depuracion
		if code.type[0]==REF:
			if code.type[1] == REF or code.ref:
				type='REF'
			elif code.type[1] == HASH:
				type='HASH'
			elif code.type[1] in [ARRAY,LIST]:
				type='ARRAY'
			else:
				type='SCALAR'
			return '"'+type+'(0x1)"'
		#En caso contrario usamos una funcion	
		else:
			return 'Pd.repr('+code.value+')'
		
def to_list(array):
	if array.type[0]==ARRAY:
		#cambiamos el tipo
		array.type=[Type(LIST)]+array.type[1:]
		#Si era una variable ya no lo es
		array.variable=None
		#Llama a la funcion
		array.value='Pd.list('+array.value+')'
	return array.value

def to_array(list):
	if list.type[0]==LIST:
		#cambiamos el tipo
		list.type=[Type(ARRAY)]+list.type[1:]
		#Si era una variable ya no lo es
		list.variable=None
		#Llama a la funcion
		list.value='Pd.array('+list.value+')'
	return list.value
		
def to_type(parser,c_type,code):
	#Si es un tipo basico
	if len(c_type.type) == 1:
		#Segun el tipo llama a la funcion
		if c_type.type[0] == BOOLEAN:
			return to_boolean(code)
		elif c_type.type[0] == INTEGER:
			return to_integer(code)
		elif c_type.type[0] == FLOAT:
			return to_float(code)
		elif c_type.type[0] == DOUBLE:
			return to_double(code)
		elif c_type.type[0] == STRING:
			return to_string(code)
		elif c_type.type[0] == FILE and c_type.type[0] != FILE:
			error(parser,'IMPOSIBLE_CAST',code.pos,type=type_string(code),cast=type_string(c_type))
		else:
			return code.value
	else:
		if c_type.type[0] == LIST:
			to_list(code)
		elif c_type.type[0] == ARRAY:
			to_array(code)
		elif code.ref:
			return 'new Ref<'+create_type(code.type)+'>('+code.value+')'
		#El tipo debe ser ahora el mismo
		if not equals_type(c_type.type, code.type):
			error(parser,'IMPOSIBLE_CAST',code.pos,type=type_string(code),cast=type_string(c_type))
		return code.value

#Muestra el tipo como una cadena
def type_string(code):
	string='('
	for dim in code.type:
		string+=str(dim)+', '
	return string[:-2]+')'

#Compara si dos tipos son iguales
def equals_type(type1,type2):
	if len(type1)==len(type2):
		for dim1,dim2 in zip(type1,type2):
			if dim1!=dim2:
				return False
	else:
		return False
	return True

#Crea el tipo de la variable
def create_type(code_type):
	declare='%t'
	for type in code_type:
		if type==ARRAY:
			declare=declare.replace('%t','%t[]')
		elif type==LIST:
			declare=declare.replace('%t','List<%t>')
		elif type==HASH:
			declare=declare.replace('%t','Map<String,%t>')
		elif type==REF:
			declare=declare.replace('%t','Ref<%t>')
		else:
			declare=declare.replace('%t',type)
	return declare

#Reserva de memoria para una coleccion
def creare_inicialize(types,sizes):
	#Si es un hash la declaracion es directa
	if types[0]==HASH:
		if sizes and sizes[0]:
			return 'new HashPerl<>('+sizes[0]+')'
		else:
			return 'new HashPerl<>()'
	#Si es una lista igual
	elif types[0]==LIST:
		if sizes and sizes[0]:
			return 'new PerlList<>('+sizes[0]+')'
		else:
			return 'new PerlList<>()'

	#El caso contrario añadimos los corchetes de cada array
	declare='%t'
	for type in types:
		if type==ARRAY:
			declare=declare.replace('%t','%t[%size]')
		elif type==HASH:
			declare=declare.replace('%t','Map')
			break
		elif type==HASH:
			declare=declare.replace('%t','List')
			break
		elif type==REF:
			declare=declare.replace('%t','Ref')
			break
		else:
			declare=declare.replace('%t',types[-1])
			break
	#Añadimos los tamaños a cada array
	for size in sizes:
		if size:
			declare=declare.replace('%size',size,1)	
		else:
			break
	#Los que no tienen tamaño los dejamos vacios
	declare=declare.replace('%size','',)	
	return 'new '+declare



	




