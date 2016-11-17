# -*- coding: utf-8 -*-

#Copyright 2016 César Pomar <cesarpomar18@gmail.com>
#
#This file is part of Perldoop.
#
#Perldoop is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Perldoop is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Perldoop.  If not, see <http://www.gnu.org/licenses/>.

import re
import logging
import libs.ply.yacc as yacc
from libs import Messages as Msg
from libs import Casting as Cst
from libs import DataType as Dtp
from libs import Variables as Var
from libs import Package
from libs import Code

class Auxiliary:
	
	@classmethod
	def debugger(Aux, parser):
		# Depurado del analizador sintactico
		if parser.parser_debug:
			# Tamaño del codigo a mostrar en la reglas
			yacc.resultlimit = parser.parser_debug_len
			if parser.parser_debug_file:
				# Nivel de detalle del depurado
				if parser.parser_debug_details:
					level = logging.DEBUG
				else:
					level = logging.INFO
				# Formato del depurado
				logging.basicConfig(
			    level=level,
			    filename=parser.parser_debug_file,
			    filemode="w",
			    format="%(filename)10s:%(lineno)4d:%(message)s"
				)
				# Filtro para depurado en fichero
				return logging.getLogger()	
			else:
				# Depurado en pantalla
				return True
		else:
			# Sin depurado
			return False
	
	# Funcion para identar el codigo java
	@classmethod
	def identer(Aux, text):
		IDENT = ' ' * 4
		# Partimos el codigo en lineas
		lines = text.splitlines(1)
		pretty = ''  # codigo identado
		tam_ident = len(IDENT)  # Tamaño de una identacion
		ident = ''  # Tamaño de la identacion actual
		open_block = re.compile(r'.*\{$')  # Linea que termina con una llave
		close_block = re.compile(r'^\}.*')  # Linea que empieza con una llave
		for line in lines:
			# reducimos identacion
			if close_block.match(line):
				ident = ident[0:-tam_ident]
			pretty += ident + line
			# aumentamos identacion
			if open_block.match(line):
				ident += IDENT
		return pretty
	
	@classmethod
	def check_unreachable(Aux, parser, code):
		# Partimos el codigo en lineas
		lines = code.value.splitlines(1)
		# Palabras que generan codigo muerto
		code_stop = re.compile("^[ ]*(break|continue|return)")	
		# Apertura de bloque
		open_block = re.compile(r'.*\{$')		
		# Apertura de bloque que propaga codigo muerto	
		open_block_prop = re.compile(r'^[ ]*(do)?\{$')
		# Cierre de bloque
		close_block = re.compile(r'^[ ]*\}.*')
		# Sentencias no ejecutables
		no_st = re.compile(r'^[ ]*(//|/\*)')
		# Pilas para comprobaciones
		st_control = [False]
		st_propague = [False]
		for line in lines:
			# Si abrimos bloque
			if open_block.match(line):
				# Las sentencias son alcanzables
				st_control.append(False)
				# Añadimos si propaga o no
				if open_block_prop.match(line):
					st_propague.append(True)
				else:
					st_propague.append(False)
			# Si cerramos bloque
			elif close_block.match(line): 
				# Si propagamos
				if st_propague.pop():
					# Pasamos el valor al bloque anterior
					st_control[-2] = st_control[-1]
				st_control.pop()
			# Si la bandera de codigo muerto esta activada y aparece codigo ejecutable
			elif st_control[-1] and not no_st.match(line):
				Msg.error(parser, 'UNREACHABLE_STATEMENT', code.pos)	
				# Paramos para solo generar un error
				parser.unreachable_code = False
				return True
			# Si es una sentecia de ruptura, luego sera codigo muerto
			elif code_stop.match(line):
				st_control[-1] = True
		return False
		
	# Crea la declaracion de tipo de una variable
	@classmethod
	def create_declare(Aux, code):
		value = ''
		# Para cada variable que haya que declarar
		for var in code.declares:
			# Creamos la sentencia de declaracion
			if var.type:
				# Si tiene tipo lo usamos
				value += Cst.create_type(var.type) + ' ' + var.value + ';\n'
			else:
				# Si no asumimos que ya forma parte de la codena
				value += var.value + ';\n'					
		return value
	
	# Comprobar si el codigo es valido
	@classmethod
	def check_code(Aux, parser, code, c_ref=True):
		if code.variable and not Var.is_assign(parser, code.variable.name):
			Msg.error(parser, 'READ_BEFORE_ASSIGN', code.pos, var=code.value)
		if c_ref and code.type[0] == Dtp.REF:
			Msg.error(parser, 'REF_OPERATION', code.pos)	
	
	# Crea los imports de la clase
	@classmethod
	def create_imports(Aux, parser):
		imports = 'import perldoop.*;\n'
		for (key, value) in parser.imports.items():
			if value:
				imports += 'import ' + Var.imports_path[key] + ';\n'
		return imports + '\n'
	
	# Declara un paquete
	@classmethod
	def declare_package(Aux, parser, name, pos):
		if parser.atributes or parser.functions or parser.global_code or parser.package_code:
			Msg.error(parser, 'PACK_AFTER_CODE', pos)
		elif parser.class_name != name:
			Msg.error(parser, 'PACK_DIF_NAME', pos)
		else:
			parser.is_package = True
	
	# crea un paquete
	@classmethod
	def create_package(Aux, parser):
		variables = {}
		# Para todaslas variables
		for var, value in parser.variables[0].items():
			# Añadimos solo las compartidas
			if not value.private:
				variables[var] = value
		# Añadimos el paquete
		Var.packages[parser.class_name] = Package(parser.class_name, variables, parser.functions)
	
	@classmethod	
	def access_package(Aux, parser, name, pos):
		# Buscamos el paquete
		if name in Var.packages:
			return Var.packages[name]
		else:
			# Damos error y lo cremos para continuar el analisis
			Msg.error(parser, 'PACK_NOT_EXIST', pos, pack=name)
			return Package(name, {}, {})
	
	# Elimina el acceso a un puntero recien creado
	@classmethod
	def opt_get(Aux, value):
		return re.sub(r'^new Ref(<[^\(]*>)?\((.*)\)\.get\(\)$', r'\2', value)
	
	# Usar notacion diamante en cado de igualar
	@classmethod
	def opt_eq(Aux, value):
		return re.sub(r'^(new [^<]*)<[^\(]*(\(.*)$', r'\1<>\2', value)
	
	# Evita dobles parentesis
	@classmethod
	def opt_paren(Aux, code):
		if code.value and code.value[0] == '(' and code.value[-1] == ')':
			code.value = code.value[1:-1]
	
	# Crea un paso por referencia a una variable
	@classmethod
	def arg_ref(Aux, parser, code, f_type, var):     
		# Pide una variable reservada
		var_f = Var.get_function_var(parser)
		# Solicita su declaracion 
		code.declares.append(Code(value=var_f, type=[Dtp.REF] + var.type))
		# Añade el argumento a la funcion usando la referencia
		code.value += var_f + '=new Ref<>(' + Cst.to_type(parser, Code(type=f_type), var) + ')'
		# Retorna el codigo que debe ser usado en la actualizacion de la variable
		return Aux.readToEqual(var, Cst.to_type(parser, var, Code(type=f_type, value=var_f + '.get()')))
	
	# Transformar lecturas de colecciones en escrituras
	@classmethod
	def readToEqual(Aux, code, exp):
		if code.variable.type[0] == Dtp.HASH:
			return re.sub(r'(.*)get\((.*)\)$', r'\1put(\2,' + exp + ')', code.value)
		elif code.variable.type[0] == Dtp.LIST:
			return re.sub(r'(.*)get\((.*)\)$', r'\1set(\2,' + exp + ')', code.value)
		else:
			return code.value + ' = ' + exp 

	# Interpola las variables en el código
	@classmethod
	def interpolateVar(Aux, parser, string):
		vars=re.findall("\$[a-zA-Z_][a-zA-Z_0-9]*",string)
		for var in vars:
			entry = Var.get_var(parser, var[1:])
			if entry and len(entry.type) == 1:
				string=string.replace(var,"\"+"+var[1:]+"+\"")		
	
		vars=re.findall("\$\{[a-zA-Z_][a-zA-Z_0-9]*\}",string)
		for entry in vars:
			entry = Var.get_var(parser,var[2:-1])
			if var and len(entry.type) == 1:					
				string=string.replace(var,"\"+\""+var[2:-1]+"\"+\"")
		return string		
	
	# Arregla los escapes
	@classmethod
	def fixScapes(Aux, string, regex=False):
		scapesRex={'.': True, '^': True, '$': True, '*': True, '+': True, '-': True, '?': True, 
			'(': True, ')': True, '[': True, ']': True, '{': True, '}': True, '|': True,'/': True}
		scapesJava={"t":True,"b":True,"n":True,"r":True,"f":True,'"':True}
		fixstring=""
		last=""
		for c in string:
			if last == "\\":
				if c in scapesJava:
					fixstring=fixstring+"\\"+c
				elif regex and (c in scapesRex or c.isalpha()):
					fixstring=fixstring+"\\\\"+c
				elif regex and c == "\\":
					fixstring=fixstring+"\\\\\\\\"
				elif c == "\\":
					fixstring=fixstring+"\\\\"
				else:
					fixstring=fixstring+c
				last = ""
				continue
			elif c != "\\":
				fixstring=fixstring+c
			last=c
		return fixstring
	
	# Escapa un caracter eb toda la cadena
	@classmethod
	def scapeChar(Aux, string, chars):
		newstring=""
		scapes=0
		for c in string:		
			if c in chars and scapes % 2 == 0:
				newstring = newstring + "\\"
			newstring = newstring + c
			if c == '\\':
				scapes=scapes+1
			else:
				scapes=0
			
		return newstring

