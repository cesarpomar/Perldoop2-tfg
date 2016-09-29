#!/usr/bin/python
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
from libs import Messages as Msg
from libs import DataType as Dtp
from libs import Type

class Casting:
	
	@classmethod
	def to_number(Cst, code):
		# Si es una coleccion o un booleano usamos su transformacion entera
		if code.type[0] == Dtp.VOID or len(code.type) > 1 or code.type[0] == Dtp.BOOLEAN:
			code.value = Cst.to_integer(code)
			code.type = [Dtp.INTEGER]
		# Si es una cadena combertimos a double
		elif code.type[0] == Dtp.STRING:
			code.value = Cst.to_double(code)
			code.type = [Dtp.DOUBLE]
		return code.value
	
	@classmethod
	def to_floor(Cst, code):
		# Si no es entero, lo combertimos
		if code.type[0] not in (Dtp.INTEGER, Dtp.LONG):
			code.type = [Dtp.INTEGER]
			code.value = Cst.to_integer(code)
		return code.value
	
	@classmethod
	def to_boolean(Cst, code):
		# Si ya tenemos un valor booleano
		if code.value_opt:
			return code.value_opt
		# Si no tiene un solo tipo usamos su tamaño
		elif code.type[0] == Dtp.VOID:
			return 'Pd.len(' + code.value + ') != 0'
		elif code.type[0] == Dtp.BOOLEAN:
			return code.value
		elif code.type[0] == Dtp.FILE:
			return 'true'
		elif re.match("^\d*$", code.value):
			if(code.value=='0'):
				return "false"
			else:
				return "true"
		else:
			return 'Pd.eval(' + code.value + ')'
	
	@classmethod
	def to_integer(Cst, code):
		# Si no es un tipo basico
		if len(code.type) > 1:
			if code.type[0] == Dtp.ARRAY:
				return code.value + '.length'
			elif code.type[0] == Dtp.LIST:
				return code.value + '.size()'
			# Tanto si es un hash o una referencia
			else:
				# Como no existe un valor usable ponemos uno por defecto para evitar errores
				return '1'
		# Si es un numero de mayor rango
		elif code.type[0] in [Dtp.LONG, Dtp.FLOAT, Dtp.DOUBLE]:
			if re.match("^(\d*(\.\d*)?eE\d*)|(\d*\.\d*)$", code.value):	
				return '(int)' + code.value
			else:
				return 'Pd.toInteger(' + code.value + ')'
		# Si hay que interpretar una cadena
		elif code.type[0] == Dtp.STRING:
			return 'Integer.parseInt(' + code.value + ')'
		# Si sale de un boleano
		elif code.type[0] == Dtp.BOOLEAN:
			return '(' + code.value + ')?1:0'
		# Si no tiene un solo tipo
		elif code.type[0] == Dtp.VOID:
			return 'Pd.len(' + code.value + ')'
		elif code.type[0] == Dtp.FILE:
			return '1'
		# Opcion para errores sin tipo
		else:
			return code.value
	
	@classmethod
	def to_long(Cst, code):
		# Si no es un tipo basico
		if len(code.type) > 1:
			if code.type[0] == Dtp.ARRAY:
				return '((long)' + code.value + '.length)'
			elif code.type[0] == Dtp.LIST:
				return '((long)' + code.value + '.size())'
			# Tanto si es un hash o una referencia
			else:
				# Como no existe un valor usable ponemos uno por defecto para evitar errores
				return '1l'
		# Si es un numero de otro rango
		elif code.type[0]  in [Dtp.INTEGER, Dtp.FLOAT, Dtp.DOUBLE]:
			# Si es un numero, para ahorrar el cast añadimos l
			if re.match("^(0[xbXB])?[\d]+$", code.value):
				return code.value + 'l'
			else:
				return 'Pd.toLong(' + code.value + ')'
		# Si hay que interpretar una cadena
		elif code.type[0] == Dtp.STRING:
			return 'Long.parseLong(' + code.value + ')'
			# Si sale de un boleano
		elif code.type[0] == Dtp.BOOLEAN:
			return '(' + code.value + ')?1l:0l'
		# Si no tiene un solo tipo
		elif code.type[0] == Dtp.VOID:
			return '((long)Pd.len(' + code.value + '))'
		elif code.type[0] == Dtp.FILE:
			return '1l'
		# Opcion para errores sin tipo
		else:
			return code.value
	
	@classmethod	
	def to_float(Cst, code):
		# Si no es un tipo basico
		if len(code.type) > 1:
			if code.type[0] == Dtp.ARRAY:
				return '((float)' + code.value + '.length)'
			elif code.type[0] == Dtp.LIST:
				return '((float)' + code.value + '.size())'
			# Tanto si es un hash o una referencia
			else:
				# Como no existe un valor usable ponemos uno por defecto para evitar errores
				return '1f'
		# Si es numero de otro rango
		elif code.type[0] in [Dtp.INTEGER, Dtp.LONG]:
			# Si es un numero, para ahorrar el cast añadimos f
			if re.match("^(0[xbXB])?[\d]+$", code.value):
				return code.value + 'f'
			else:
				return 'Pd.toFloat(' + code.value + ')'
		elif code.type[0] == Dtp.DOUBLE:	
			# Si es un numero, para ahorrar el cast añadimos f
			if re.match("^(\d*(\.\d*)?eE\d*)|(\d*\.\d*)$", code.value):
				return code.value + 'f'
			else:
				return 'Pd.toFloat(' + code.value + ')'		
		# Si hay que interpretar una cadena
		elif code.type[0] == Dtp.STRING:
			return 'Float.parseFloat(' + code.value + ')'
			# Si sale de un boleano
		elif code.type[0] == Dtp.BOOLEAN:
			return '(' + code.value + ')?1f:0f'
		# Si no tiene un solo tipo
		elif code.type[0] == Dtp.VOID:
			return '((float)Pd.len(' + code.value + '))'
		elif code.type[0] == Dtp.FILE:
			return '1f'
		# Opcion para errores sin tipo
		else:
			return code.value
	
	@classmethod			
	def to_double(Cst, code):		
		# Si no es un tipo basico
		if len(code.type) > 1:
			if code.type[0] == Dtp.ARRAY:
				return '((double)' + code.value + '.length)'
			elif code.type[0] == Dtp.LIST:
				return '((double)' + code.value + '.size())'
			# Tanto si es un hash o una referencia
			else:
				# Como no existe un valor usable ponemos uno por defecto para evitar errores
				return '1d'
		# Si es un entero
		elif code.type[0] in [Dtp.INTEGER, Dtp.LONG, Dtp.FLOAT]:
			# Si es un numero, para ahorrar el cast añadimos l
			if re.match("^(0[xbXB])?[\d]+$", code.value):
				return code.value + 'd'
			else:
				return 'Pd.toDouble(' + code.value + ')'
		# Si hay que interpretar una cadena
		elif code.type[0] == Dtp.STRING:
			return 'Double.parseDouble(' + code.value + ')'
			# Si sale de un boleano
		elif code.type[0] == Dtp.BOOLEAN:
			return '(' + code.value + ')?1d:0d'
		# Si no tiene un solo tipo
		elif code.type[0] == Dtp.VOID:
			return '((double)Pd.len(' + code.value + '))'
		elif code.type[0] == Dtp.FILE:
			return '1d'
		# Opcion para errores sin tipo
		else:
			return code.value	
	
	@classmethod	
	def to_string(Cst, code):
		# Si no es un tipo basico
		if len(code.type) > 1:
			if code.type[0] == Dtp.ARRAY:
				return 'String.valueOf(' + code.value + '.length)'
			elif code.type[0] == Dtp.LIST:
				return 'String.valueOf(' + code.value + '.size())'
			# Tanto si es un hash o una referencia
			else:
				# Como no existe un valor usable ponemos uno por defecto para evitar errores
				return '"1"'
		# Si ya es una cadena queda tal cual
		elif code.type[0] == Dtp.STRING:
			return code.value
		elif code.type[0] == Dtp.FILE:
			return '"1"'
		# En caso contrario transformamos
		else:
			return 'String.valueOf(' + code.value + ')'	
	
	# Representacion de una variable al ser impresa(distinto de to_string)		
	@classmethod	
	def to_repr(Cst, code):
		# Si es un tipo basico, no hacemos nada
		if len(code.type) == 1:
			# Si es un fichero imprimimos una constante
			if code.type[0] == Dtp.FILE:
				return 'GLOB(0x1)'
			else:
				return code.value
		# Si es interpretado como referencia
		elif code.ref and not code.type[0] == Dtp.REF:	
			if code.type[0] == Dtp.HASH:
				type = 'HASH'
			else:
				type = 'ARRAY'	
			return '"' + type + '(0x1)"'	
		else:
			# Si es una referencia, imitamos a perl para fines de depuracion
			if code.type[0] == Dtp.REF:
				if code.type[1] == Dtp.REF or code.ref:
					type = 'REF'
				elif code.type[1] == Dtp.HASH:
					type = 'HASH'
				elif code.type[1] in [Dtp.ARRAY, Dtp.LIST]:
					type = 'ARRAY'
				else:
					type = 'SCALAR'
				return '"' + type + '(0x1)"'
			# En caso contrario usamos una funcion	
			else:
				return 'Pd.repr(' + code.value + ')'
			
	@classmethod		
	def to_list(Cst, array):
		if array.type[0] == Dtp.ARRAY:
			# cambiamos el tipo
			array.type = [Type(Dtp.LIST)] + array.type[1:]
			# Si era una variable ya no lo es
			array.variable = None
			# Llama a la funcion
			array.value = 'Pd.list(' + array.value + ')'
		return array.value
	
	@classmethod
	def to_array(Cst, list):
		if list.type[0] == Dtp.LIST:
			# cambiamos el tipo
			list.type = [Type(Dtp.ARRAY)] + list.type[1:]
			# Si era una variable ya no lo es
			list.variable = None
			# Llama a la funcion
			list.value=list.value+".toArray("+Cst.creare_inicialize(list.type,[])+"{})"
		return list.value
	
	@classmethod		
	def to_type(Cst, parser, c_type, code):
		# Si es un tipo basico
		if len(c_type.type) == 1:
			# Segun el tipo llama a la funcion
			if c_type.type[0] == Dtp.BOOLEAN:
				return Cst.to_boolean(code)
			elif c_type.type[0] == Dtp.INTEGER:
				return Cst.to_integer(code)
			elif c_type.type[0] == Dtp.LONG:
				return Cst.to_long(code)
			elif c_type.type[0] == Dtp.FLOAT:
				return Cst.to_float(code)
			elif c_type.type[0] == Dtp.DOUBLE:
				return Cst.to_double(code)
			elif c_type.type[0] == Dtp.STRING:
				return Cst.to_string(code)
			elif c_type.type[0] == Dtp.FILE and c_type.type[0] != Dtp.FILE:
				Msg.error(parser, 'IMPOSIBLE_CAST', code.pos, type=Cst.type_string(code), cast=Cst.type_string(c_type))
			else:
				return code.value
		else:
			if c_type.type[0] == Dtp.LIST:
				Cst.to_list(code)
			elif c_type.type[0] == Dtp.ARRAY:
				Cst.to_array(code)
			elif code.ref:
				return 'new Ref<' + Cst.create_type(code.type) + '>(' + code.value + ')'
			# El tipo debe ser ahora el mismo
			if not Cst.equals_type(c_type.type, code.type):
				Msg.error(parser, 'IMPOSIBLE_CAST', code.pos, type=Cst.type_string(code), cast=Cst.type_string(c_type))
			return code.value
	
	# Muestra el tipo como una cadena
	@classmethod
	def type_string(Cst, code):
		string = '('
		for dim in code.type:
			string += str(dim) + ', '
		return string[:-2] + ')'
	
	# Compara si dos tipos son iguales
	@classmethod
	def equals_type(Cst, type1, type2):
		if len(type1) == len(type2):
			for dim1, dim2 in zip(type1, type2):
				if dim1 != dim2:
					return False
		else:
			return False
		return True
	
	# Crea el tipo de la variable
	@classmethod
	def create_type(Cst, code_type):
		declare = '%t'
		for type in code_type:
			if type == Dtp.ARRAY:
				declare = declare.replace('%t', '%t[]')
			elif type == Dtp.LIST:
				declare = declare.replace('%t', 'List<%t>')
			elif type == Dtp.HASH:
				declare = declare.replace('%t', 'Map<String,%t>')
			elif type == Dtp.REF:
				declare = declare.replace('%t', 'Ref<%t>')
			else:
				declare = declare.replace('%t', type)
		return declare
	
	# Reserva de memoria para una coleccion
	@classmethod
	def creare_inicialize(Cst, types, sizes):
		# Si es un hash la declaracion es directa
		if types[0] == Dtp.HASH:
			if sizes and sizes[0]:
				return 'new HashPerl<>(' + sizes[0] + ')'
			else:
				return 'new HashPerl<>()'
		# Si es una lista igual
		elif types[0] == Dtp.LIST:
			if sizes and sizes[0]:
				return 'new PerlList<>(' + sizes[0] + ')'
			else:
				return 'new PerlList<>()'
	
		# El caso contrario añadimos los corchetes de cada array
		declare = '%t'
		for type in types:
			if type == Dtp.ARRAY:
				declare = declare.replace('%t', '%t[%size]')
			elif type == Dtp.HASH:
				declare = declare.replace('%t', 'Map')
				break
			elif type == Dtp.HASH:
				declare = declare.replace('%t', 'List')
				break
			elif type == Dtp.REF:
				declare = declare.replace('%t', 'Ref')
				break
			else:
				declare = declare.replace('%t', types[-1])
				break
		# Añadimos los tamaños a cada array
		for size in sizes:
			if size:
				declare = declare.replace('%size', size, 1)	
			else:
				break
		# Los que no tienen tamaño los dejamos vacios
		declare = declare.replace('%size', '',)	
		return 'new ' + declare
