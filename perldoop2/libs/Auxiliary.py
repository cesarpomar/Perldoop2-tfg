#!/usr/bin/python
# -*- coding: utf-8 -*-
from libs.Datatypes import HASH,LIST,REF,Code,Package
from libs.Casting import create_type,to_type
from libs.Variables import is_assign,imports_path,get_function_var,packages
from libs.Messages import error
import libs.ply.yacc as yacc
import re
import logging

def debugger(parser):
	#Depurado del analizador sintactico
	if parser.parser_debug:
		#Tamaño del codigo a mostrar en la reglas
		yacc.resultlimit=parser.parser_debug_len
		if parser.parser_debug_file:
			#Nivel de detalle del depurado
			if parser.parser_debug_details:
				level=logging.DEBUG
			else:
				level=logging.INFO
			#Formato del depurado
			logging.basicConfig(
		    level = level,
		    filename = parser.parser_debug_file,
		    filemode = "w",
		    format = "%(filename)10s:%(lineno)4d:%(message)s"
			)
			#Filtro para depurado en fichero
			return logging.getLogger()	
		else:
			#Depurado en pantalla
			return True
	else:
		#Sin depurado
		return False

#Funcion para identar el codigo java
IDENT=' '*4
def identer(text):
	#Partimos el codigo en lineas
	lines=text.splitlines(1)
	pretty=''			#codigo identado
	tam_ident=len(IDENT)#Tamaño de una identacion
	ident=''			#Tamaño de la identacion actual
	open_block=re.compile(r'.*\{$')	#Linea que termina con una llave
	close_block=re.compile(r'^\}.*')#Linea que empieza con una llave
	for line in lines:
		#reducimos identacion
		if close_block.match(line):
			ident=ident[0:-tam_ident]
		pretty+=ident+line
		#aumentamos identacion
		if open_block.match(line):
			ident+=IDENT
	return pretty

def check_unreachable(parser,code):
	#Partimos el codigo en lineas
	lines=code.value.splitlines(1)
	#Palabras que generan codigo muerto
	code_stop=re.compile("^(break|continue|return)")	
	#Apertura de bloque
	open_block=re.compile(r'.*\{$')		
	#Apertura de bloque que propaga codigo muerto	
	open_block_prop=re.compile(r'^(do)?\{$')
	#Cierre de bloque
	close_block=re.compile(r'^\}.*')
	#Pilas para comprobaciones
	st_control=[False]
	st_propague=[False]
	for line in lines:
		#Si abrimos bloque
		if open_block.match(line):
			#Las sentencias son alcanzables
			st_control.append(False)
			#Añadimos si propaga o no
			if open_block_prop.match(line):
				st_propague.append(True)
			else:
				st_propague.append(False)
		#Si cerramos bloque
		elif close_block.match(line): 
			#Si propagamos
			if st_propague.pop():
				#Pasamos el valor al bloque anterior
				st_control[-2]=st_control[-1]
			st_control.pop()
		#Si la bandera de codigo muerto esta activada
		if st_control[-1]:
			error(parser,'UNREACHABLE_STATEMENT',code.pos)	
			#Paramos para solo generar un error
			parser.unreachable_code=False
			break
		#Si es una sentecia de ruptura, luego sera codigo muerto
		if code_stop.match(line):
			st_control[-1]=True
			continue
	
#Crea la declaracion de tipo de una variable
def create_declare(code):
	value=''
	#Para cada variable que haya que declarar
	for var in code.declares:
		#Creamos la sentencia de declaracion
		if var.type:
			#Si tiene tipo lo usamos
			value+=create_type(var.type)+' '+var.value+';\n'
		else:
			#Si no asumimos que ya forma parte de la codena
			value+=var.value+';\n'					
	return value

#Comprobar si el codigo es valido
def check_code(parser,code,c_ref=True):
	if code.variable and not is_assign(parser,code.variable.name):
		error(parser, 'READ_BEFORE_ASSIGN', code.pos,var=code.value)
	if c_ref and (code.type[0]==REF or  code.ref):
		error(parser,'REF_OPERATION',code.pos)	

#Crea los imports de la clase
def create_imports(parser):
	imports='import perldoop.*;\n'
	for (key,value) in parser.imports.items():
		if value:
			imports+='import '+imports_path[key]+';\n'
	return imports+'\n'

#Declara un paquete
def declare_package(parser,name,pos):
	if parser.atributes or parser.functions:
		error(parser, 'PACK_DIF_NAME', pos)
	elif parser.class_name!=name:
		error(parser,'PACK_AFTER_CODE', pos)
	else:
		parser.is_package=True

#crea un paquete
def create_package(parser):
	variables={}
	#Para todaslas variables
	for var,value in parser.variables[0].items():
		#Añadimos solo las compartidas
		if not value.private:
			variables[var]=value
	#Añadimos el paquete
	packages[parser.class_name]=Package(parser.class_name,variables,parser.functions)
	
def access_package(parser,name,pos):
	#Buscamos el paquete
	if name in packages:
		return packages[name]
	else:
		#Damos error y lo cremos para continuar el analisis
		error(parser,'PACK_NOT_EXIST',pos,pack=name)
		return Package(name,{},{})

#Elimina el acceso a un puntero recien creado
def opt_get(value):
	return re.sub(r'^new Ref(<[^\(]*>)?\((.*)\)\.get\(\)$', r'\2', value)

#Usar notacion diamante en cado de igualar
def opt_eq(value):
	return re.sub(r'^(new [^<]*)<[^\(]*(\(.*)$', r'\1<>\2', value)

#Evita dobles parentesis
def opt_paren(code):
	if code.value and code.value[0]=='(' and code.value[-1]==')':
		code.value=code.value[1:-1]

#Crea un paso por referencia a una variable
def arg_ref(parser,code,f_type,var):     
	#Pide una variable reservada
	var_f=get_function_var(parser)
	#Solicita su declaracion 
	code.declares.append(Code(value=var_f,type=[REF]+var.type))
	#Añade el argumento a la funcion usando la referencia
	code.value+=var_f+'=new Ref<>('+to_type(parser,Code(type=f_type),var)+')'
	#Retorna el codigo que debe ser usado en la actualizacion de la variable
	return readToEqual(var,to_type(parser,var,Code(type=f_type,value=var_f+'.get()')))

#Transformar lecturas de colecciones en escrituras
def readToEqual(code,exp):
	if code.variable.type[0]==HASH:
		return re.sub(r'(.*)get\((.*)\)$', r'\1put(\2,'+exp+')', code.value)
	elif code.variable.type[0]==LIST:
		return re.sub(r'(.*)get\((.*)\)$', r'\1set(\2,'+exp+')', code.value)
	else:
		return code.value+'='+exp 
	

