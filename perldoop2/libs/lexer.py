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
from libs.ply.lex import TOKEN, LexToken
import libs.ply.lex as lex
from libs import Messages as Msg
from libs import Variables as Var
from libs import Functions as Ftn
from libs import Position


class Lexer():

	def __init__(self):
		self.lexer = lex.lex(object=self)  # Analizador lexico
		self.debug_mode = False  # Modo depuracion
		self.parser = None  # Analizador sintactico
		self.comment = None  # Token del comentario actual sin etiquetas
		self.perl_line = -1  # Linea del ultimo componente perl
		self.buffer = []  # Buffer de tokens
		self.t = None  # Token actual
		
	def input(self, text):	
		self.lexer.input(text)
		self.input = text	
		self.t = self.lexer.token()
		
	def token(self):
		token = self.token_buffer()
		if self.debug_mode:
			print(token)
		return token	
		
	# Busca la columna correspondiente a un token, mas eficiente que calcularlo para todos
	def find_column(self, lexpos):
		last_cr = self.input.rfind('\n', 0, lexpos)
		if last_cr < 0:
			last_cr = -1
		column = (lexpos - last_cr)
		return column
	
	def t_ANY_error(self, t):
		Msg.error(self.parser, 'ILEGAL_TOKEN', Position(line=t.lineno, lexpos=t.lexpos), c=t.value[0])
		t.lexer.skip(1)

	
	# #
	# # Palabras reservadas
	# #
	
	reserved_map = {}
	
	reserved = (
	# Declaraciones		
	'MY', 'SUB', 'OUR', 'PACKAGE',
	
	# Control de Flujo
	'WHILE', 'DO', 'FOR', 'UNTIL',
	'IF', 'ELSIF', 'ELSE', 'UNLESS',
	'LAST', 'NEXT', 'RETURN',
	
	# Funciones de Perl
	'CMP', 'X', 'UNDEF'
	) + Ftn.perl_functions
	
	# Asignamos palabras a los tokens
	for reserved_word in reserved:
		reserved_map[reserved_word.lower()] = reserved_word
		
	# Casos en que la palabra difiere del token
	reserved_map['foreach'] = 'FOR' 
	reserved_map['and'] = 'LLAND' 
	reserved_map['or'] = 'LLOR' 
	reserved_map['xor'] = 'LLXOR' 
	reserved_map['not'] = 'LLNOT' 
	reserved_map['le'] = 'STR_LE'
	reserved_map['gt'] = 'STR_GT'
	reserved_map['lt'] = 'STR_LT'
	reserved_map['ge'] = 'STR_GE'
	reserved_map['eq'] = 'STR_EQ'
	reserved_map['ne'] = 'STR_NE'

	
	# #
	# # Etiquetas perldoop
	# #
	
	labels_maps = {}
	
	# Etiquetas de tipo
	labels_type = ('BOOLEAN', 'INTEGER', 'LONG', 'FLOAT', 'DOUBLE', 'STRING', 'FILE')
	
	for label in labels_type:
		labels_maps[label.lower()] = 'TYPE'
	
	# Etiquetas que no tienen la misma palabra que token
	labels_value = ('VAR', 'TYPE', 'SIZE', 'L_ARRAY', 'L_HASH', 'L_LIST')	
	
	# Las colecciones estan para no entrar en conflicto con la propia variable
	labels_maps['array'] = 'L_ARRAY'
	labels_maps['hash'] = 'L_HASH'
	labels_maps['list'] = 'L_LIST'	
	
	# Etiquetas que tienen la misma palabra como token	
	labels_key = ('REF', 'ARGS', 'RETURNS',
			# Hadoop
			'MAPPER_CODE', 'MAPPER_LOOP', 'HADOOP_PRINT',
			'REDUCER_CODE', 'REDUCER_OP', 'REDUCER_CHANGE',
			'REDUCER_KEY', 'REDUCER_VALUE', 'REDUCER_VAR',
	)
	
	# Asignamos palabras a los tokens
	for label in labels_key:
		labels_maps[label.lower()] = label
		
	# ## Etiquetas que se mueven a principio de linea
	
	labels_moved = {}
	
	# No se mueven
	for label in labels_key:
		labels_moved[label] = False
		
	# Se mueven
	for label in labels_value + ('REF',):
		labels_moved[label] = True
		
	# #
	# # Estado para etiquetas
	# #
	
	states = (('labels', 'exclusive'),)
	
	# #
	# # Tokens
	# #
	
	tokens = reserved + labels_key + labels_value + (
		# Identificadores						
		'DOLLAR', 'AT', 'PERCENTAGE', 'ID',

		# Constantes
		'INT_NUMBER', 'FLOAT_NUMBER', 'STRING_QUOTE', 'STRING_DOUBLE_QUOTE', 'CMD',

		# Operadores
		'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POW',
		'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
		'LOR', 'LAND', 'LNOT', 'LLAND', 'LLOR', 'LLNOT', 'LLXOR',
		'NUM_LT', 'NUM_LE', 'NUM_GT', 'NUM_GE', 'NUM_EQ', 'NUM_NE',
		'STR_LT', 'STR_LE', 'STR_GT', 'STR_GE', 'STR_EQ', 'STR_NE',
		'STR_REX', 'STR_NO_REX', 'SMART_EQ', 'CMP_NUM',

		# Asignacion
		'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'POWEQUAL',
		'PLUSEQUAL', 'MINUSEQUAL',
		'LSHIFTEQUAL', 'RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL',
		'OREQUAL', 'LANDEQUAL', 'LOREQUAL', 'PERIODEQUAL', 'XEQUAL',

		# Incremento/decremento
		'PLUSPLUS', 'MINUSMINUS',

		# Delimitadores
		'LPAREN', 'RPAREN',  # ( )
		'LBRACKET', 'RBRACKET',  # [ ]
		'LBRACE', 'RBRACE',  # { }
		'COMMA', 'PERIOD',  # , .
		'SEMI', 'COLON',  # ; :
		'BACKSLASH', 'POINTED',  # \	->
		'QUEST_CLOSE', 'TWO_PERIOD',  # ? ..
		'TWO_COLON',  # ::
		
		# Expresiones regualres
		'M_REGEX', 'S_REGEX', 'Y_REGEX',

		# Entrada/Salida
		'STDIN',
		
		# Comentarios
		'COMMENT', 'COMMENT_LINE', 'JAVA_LINE', 'JAVA_IMPORT'		
	)
	
	# #
	# # Expresiones
	# #
	
	# Identificadores
	ID					 = r'[A-Za-z_][\w_]*'
	t_DOLLAR			 = r'\$'
	t_AT				 = r'@'
	t_PERCENTAGE		 = r'%'

	# Constantes
	INT_NUMBER			 = r'(([1-9]\d*)|(o[xX][a-fA-F\d]+)|(o[bB][01]+)|(0[0-7]*))'
	FLOAT		 		 = r'((\d*\.\d+)|(\d+\.\d*))'
	SCIENTIFIC		 	 = r'(' + INT_NUMBER + '|' + FLOAT + ')[eE](\+-)?' + INT_NUMBER
	FLOAT_NUMBER		 = r'('+FLOAT+'|'+SCIENTIFIC+')'
	STRING_QUOTE		 = r'\'([^\'\\\n]|(\\.))*\''
	STRING_DOUBLE_QUOTE	 = r'"([^"\\\n]|(\\.))*"'
	CMD					 = r'`.+`'
	
	# Operadores
	t_PLUS				 = r'\+'
	t_MINUS				 = r'-'
	t_TIMES				 = r'\*'
	t_DIVIDE			 = r'/'
	t_POW				 = r'\*\*'
	t_OR				 = r'\|'
	t_AND				 = r'&'
	t_NOT				 = r'~'
	t_XOR				 = r'\^'
	t_LSHIFT			 = r'<<'
	t_RSHIFT			 = r'>>'
	t_LOR				 = r'\|\|'
	t_LAND				 = r'&&'
	t_LNOT				 = r'!'
	t_NUM_LT			 = r'<'
	t_NUM_GT			 = r'>'
	t_NUM_LE			 = r'<='
	t_NUM_GE			 = r'>='
	t_NUM_EQ			 = r'=='
	t_NUM_NE			 = r'!='
	t_STR_REX			 = r'=~'
	t_STR_NO_REX		 = r'!~'
	t_SMART_EQ			 = r'~~'
	t_CMP_NUM			 = r'<=>'
	
	# Assignment operators
	t_EQUALS			 = r'='
	t_TIMESEQUAL		 = r'\*='
	t_DIVEQUAL			 = r'/='
	t_MODEQUAL			 = r'%='
	t_POWEQUAL			 = r'\*\*='
	t_PLUSEQUAL			 = r'\+='
	t_MINUSEQUAL		 = r'-='
	t_LSHIFTEQUAL		 = r'<<='
	t_RSHIFTEQUAL		 = r'>>='
	t_ANDEQUAL			 = r'&='
	t_OREQUAL			 = r'\|='
	t_XOREQUAL			 = r'\^='
	t_LANDEQUAL			 = r'&&='
	t_LOREQUAL			 = r'\|\|='
	t_PERIODEQUAL		 = r'\.='
	XEQUAL				 = r'x='
	
	# Incremento/decremento
	t_PLUSPLUS			 = r'\+\+'
	t_MINUSMINUS		 = r'--'
	
	# Delimeters
	t_LPAREN			 = r'\('
	t_RPAREN			 = r'\)'
	t_LBRACKET			 = r'\['
	t_RBRACKET			 = r'\]'
	t_COMMA				 = r'(,|=>)'
	t_PERIOD			 = r'\.'
	t_TWO_PERIOD		 = r'\.\.'
	t_QUEST_CLOSE		 = r'\?'
	t_SEMI				 = r';'
	t_COLON				 = r':'
	t_TWO_COLON			 = r'::'
	t_LBRACE			 = r'\{'
	t_RBRACE			 = r'\}'
	t_BACKSLASH			 = r'\\'
	t_POINTED			 = r'->'
	
	# Expresiones regualares
	REGEX_MOD			 = '(i|s|m|x|o|p|d|a|u|l|g|cg|e)?'
	M_REGEX				 = r'm/([^\n\\/]*(\\.)?)*/' + REGEX_MOD
	S_REGEX				 = r's/([^\n\\/]*(\\.)?)*/([^\n\\/]*(\\.)?)*/' + REGEX_MOD
	Y_REGEX				 = r'(y|tr)/([^\n\\/]*(\\.)?)*/([^\n\\/]*(\\.)?)*/' + REGEX_MOD

	# Entrada/Salida
	t_STDIN				 = r'<STDIN>'
	
	# Ignorar	
	t_ignore					 = ' \t\r'
	t_labels_ignore 			 = ''
	
	# Comentarios
	COMMENT				 = r'\#'
	COMMENT_SPECIAL		 = r'\#!.*'
	COMMENT_SCAPE		 = r'.'
	COMMENT_EXIT		 = r'\n'
	COMMENT_IGNORE_LINE = r'.*\#<ignore-line>.*'
	COMMENT_IGNORE_BLOCK = r'\#<ignore-block>\n(.|\n)*\#<ignore-block>.*'
	COMMENT_CODE_IMPORT = r'\#<java-import>.*'
	COMMENT_CODE_LINE	 = r'\#<java-line>.*'
	
	# Etiquetas
	LABEL_ID			 = r'<' + ID + '>'
	LABEL_SIZE			 = r'<[1-9][0-9]*>'
	LABEL_VAR			 = r'<(\$|@|%)' + ID + '>'
	
	# Regla para cambiar de linea
	def t_newline(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)
	
	# Ignora la importacion de paquetes	
	def t_ignore_pack(self, t):	
		r'(use .*;)|(require .*;)'
		pass
		
	# Regla para flotantes
	@TOKEN(FLOAT_NUMBER)
	def t_FLOAT_NUMBER(self, t):
		return t
	
	# Regla para enteros
	@TOKEN(INT_NUMBER)
	def t_INT_NUMBER(self, t):
		return t	
	
	# Regla para devolver una cadena sin las comillas simples
	@TOKEN(STRING_QUOTE)
	def t_STRING_QUOTE(self, t):
		t.value = t.value[1:-1]
		return t
	
	# Regla para devolver una cadena sin las comillas dobles
	@TOKEN(STRING_DOUBLE_QUOTE)
	def t_STRING_DOUBLE_QUOTE(self, t):
		t.value = t.value[1:-1]
		return t	
	
	# Regla para ejecutar comandos 
	@TOKEN(CMD)
	def t_CMD(self, t):
		t.value = t.value[1:-1]
		return t	
	
	# Expresion regular m
	@TOKEN(M_REGEX)
	def t_M_REGEX(self, t):
		return t	
	
	# Expresion regular m
	@TOKEN(S_REGEX)
	def t_S_REGEX(self, t):
		return t	
	
	# Expresion regular m
	@TOKEN(Y_REGEX)
	def t_Y_REGEX(self, t):
		return t		
	
	# Regla para los comentarios especiales
	@TOKEN(COMMENT_SPECIAL)
	def t_COMMENT_SPECIAL(self, t):
		pass
	
	# Regla para ignorar una linea
	@TOKEN(COMMENT_IGNORE_LINE)
	def t_COMMENT_IGNORE_LINE(self, t):
		pass
	
	# Regla para ignorar un bloque de lineas	
	@TOKEN(COMMENT_IGNORE_BLOCK)
	def t_COMMENT_IGNORE_BLOCK(self, t):
		label='#<ignore-block>'
		ln=len(label)
		blocks=t.value.split(label)
		if len(blocks)>3:
			tam=ln+len(blocks[1])+ln
			self.lexer.lexpos = self.lexer.lexpos - (len(t.value)-tam)
			t.value=t.value[0:tam]		
		t.lexer.lineno += t.value.count('\n')
	
	# Regla para linea nativa java para importar
	@TOKEN(COMMENT_CODE_IMPORT)
	def t_COMMENT_CODE_IMPORT(self, t):
		t.type = 'JAVA_IMPORT'
		t.value = t.value[14:] + '\n'
		return t	
	
	# Regla para linea nativa java
	@TOKEN(COMMENT_CODE_LINE)
	def t_COMMENT_CODE_LINE(self, t):
		t.type = 'JAVA_LINE'
		t.value = t.value[12:] + '\n'
		return t
	
	
	# Regla que inicia la entrada en un comentario
	@TOKEN(COMMENT)
	def t_COMMENT(self, t):
		self.comment = t
		t.value = ''
		t.lexer.push_state('labels') 
	
	# Regla para etiquetas de las variables
	@TOKEN(LABEL_VAR)		
	def t_labels_var(self, t):
		t.value = t.value[2:-1]
		t.type = 'VAR'
		return t
	
	# Regla para las etiquetas de tipos de datos, si no es se incluye como comentario
	@TOKEN(LABEL_ID)
	def t_labels_id(self, t):
		t.value = t.value[1:-1]
		if t.value in self.labels_maps:
			t.type = self.labels_maps[t.value]
			return t	
		else:
			self.comment.value += '<' + t.value + '>'
			Msg.error(self.parser, 'LABEL_UNKNOWN_IGNORE', Position(line=t.lineno, lexpos=t.lexpos), label=t.value)
		
	# Regla que incluye las etiquetes de los tamaños para arrays
	@TOKEN(LABEL_SIZE)
	def t_labels_size(self, t):
		t.value = t.value[1:-1]
		t.type = 'SIZE'
		return t		
		
	# Regla para añadir como comentario todo lo que no sea etiqueta
	@TOKEN(COMMENT_SCAPE)
	def t_labels_scape(self, t):
		self.comment.value += t.value
	
	# Regla con la que terminamos el comentario
	@TOKEN(COMMENT_EXIT)
	def t_labels_exit(self, t):
		# Devolvemos el \n para no duplicar la regla de numero de lineas	 
		self.lexer.lexpos -= 1
		t.lexer.pop_state() 	
		t.type = 'COMMENT'
		return t
	
	# Operador x=	
	@TOKEN(XEQUAL)	
	def t_XEQUAL(self, t):
		return t
		
	# Nombres de funciones o palabras reservadas
	@TOKEN(ID)
	def t_ID(self, t):
		# Hay que evitar varaibles con nombre de funciones
		if not self.buffer or self.buffer[-1].value not in ('$', '@', '%'):
			t.type = self.reserved_map.get(t.value, 'ID')
		return t
	
	# ##
	# ##Funciones Auxiliares del analizador
	# ##
	def token_buffer(self, ready=False):	
		# Emular parentesis al terminar
		if ready and self.parser.emulate_parens:
			self.emulate_parens()
		if self.buffer:
			return self.buffer.pop(0)
		stack = [0]  # Principio de la sentencia
		end = False  # Se ha terminado de leer codigo perl
		# Si hay un token
		if self.t:
			while True:
				# Si no hay token
				if not self.t:
					return self.token_buffer(True)
				# Si el token es una etiqueta
				if self.t.type in self.labels_moved:
					# Si esta en distinta linea
					if self.perl_line != self.t.lineno:
						self.perl_line = self.t.lineno
						return self.token_buffer(True)
					# Si la etiqueta se tiene que mover
					if self.labels_moved[self.t.type]:
						end = True
						self.buffer.insert(stack[-1], self.t)
						stack[-1] += 1
						self.t = self.lexer.token()
					# Si no paramos
					else:
						self.buffer.append(self.t)				
						self.t = self.lexer.token()
						return self.token_buffer(True)
				else:
					# Si no se pude leer mas perl
					if end:
						return self.token_buffer(True)
					# Si esun comentario
					elif self.t.type == 'COMMENT' :
						# Si hay que leer comentario y este contiene algo
						if self.parser.read_comments and not re.match("^[^ \t]*$", self.t.value):
							if self.perl_line == self.t.lineno:
								self.comment.type = 'COMMENT_LINE'
								self.buffer.append(self.t)				
						self.t = self.lexer.token()
						return self.token_buffer(True)		
					# Si es la llamada a una funcion				
					elif (self.t.type == 'ID' and len(self.buffer) > 0 and self.buffer[-1].type == 'SUB'):
						self.buffer.append(self.t)				
						self.t = self.lexer.token()
						return self.token_buffer(True)
					# Si es un punto y coma
					elif self.t.type == 'SEMI':
						end = True
					# Si se abren llaves
					elif self.t.type == 'LBRACE':
						stack.append(len(self.buffer) + 1)
					# Si se cierran llaves
					elif self.t.type == 'RBRACE':
						# Si se abrieron llaves y hay algo dentro
						if len(stack) > 1 and (len(self.buffer) > 0 and self.buffer[-1].type != 'LBRACE'):
							stack.pop()
						else:
							self.buffer.append(self.t)				
							self.t = self.lexer.token()
							return self.token_buffer(True)	
					self.buffer.append(self.t)	
					self.perl_line = self.t.lineno			
					self.t = self.lexer.token()
		return None			

	# Emular unos parentesis despues de las funciones
	def emulate_parens(self):
		stack = []  # Pila de argumentos
		last = None  # Ultimo token leido
		next = None  # Siguiente token a leer
		index = 0  # Posicion dentro del buffer
		# Buscamos en todo el buffer
		while index < len(self.buffer):
			token = self.buffer[index]  # Cogemos el token actual
			if len(self.buffer) != index + 1:
				next = self.buffer[index + 1]  # Si hay siguiente lo cogemos
			# Si encontramos una llamada a una funcion definida en el codigo y esta no esta precedida de parentesis
			if (((token.type == 'ID' and token.value in self.parser.functions) or token.type in Ftn.perlArgs) 
			and (not last or last.type != 'SUB') 	and next and next.type != 'LPAREN' and next.type != 'TWO_COLON'):
				# Guardamos en la pila el numero de argumentos
				if token.type == 'ID':
					# Si pertenece a un paquete
					if index - 2 > -1 and last.type == 'TWO_COLON' and self.buffer[index - 2].type == 'ID':
						# Token del paquete
						last2 = self.buffer[index - 2]
						# Si el paquete existe y contiene la funcion
						if last2.value in Var.packages and token.value in Var.packages[last2.value].functions:
							stack.append(len(Var.packages[last2.value].functions[token.value].args))
						else:
							continue
					stack.append(len(self.parser.functions[token.value].args))
				else:
					stack.append(Ftn.perlArgs[token.type])
				# Creamos el token del parentesis
				t = LexToken()
				t.lineno = token.lineno
				t.lexpos = token.lexpos
				t.type = 'LPAREN'
				t.value = '('
				# Lo añadimos
				self.buffer.insert(index + 1, t)
				# Para que no analice el parentesis
				index += 1
			# Si estamos dentro de una lista, las comas no cuentan y lo marcamos con una bandera
			elif token.type in ('LBRACKET', 'LBRACE', 'LPAREN'):
				stack.append(token.type)
			# Si la lista termino quitamos la bandera de la pila				
			elif (stack and ((token.type == 'RBRACKET' and stack[-1] == 'LBRACKET') or 
			(token.type == 'RBRACE'  and stack[-1] == 'LBRACE') or 
			(token.type == 'RPAREN'  and stack[-1] == 'LPAREN'))):
				stack.pop()
			# Si encontramos una compa fuera de una lista
			elif token.type == 'COMMA' and stack and stack[-1] not in ('LBRACKET', 'LBRACE', 'LPAREN'):
				if stack[-1] > 0:  # Funcion sin argumentos
					stack[-1] -= 1  # Quitamos un argumento a la funcion actual
				if stack[-1] == 0:  # Si no quedan arugmentos
					stack.pop()  # Quitamos la funcion de la pila
					# Creamos el token del parentesis
					t = LexToken()
					t.lineno = token.lineno
					t.lexpos = token.lexpos
					t.type = 'RPAREN'
					t.value = ')'
					# insertamos en el buffer
					self.buffer.insert(index, t)
					# Para que no analice el parentesis
					index += 1
			# Al llegar a un ;
			elif token.type == 'SEMI':
				for f in stack:  # Por cada funcion
					if f not in ('LBRACKET', 'LBRACE', 'LPAREN'):  # Que no sea bandera
						# Cerramos todos los parentesis
						t = LexToken()
						t.lineno = token.lineno
						t.lexpos = token.lexpos
						t.type = 'RPAREN'
						t.value = ')'
						self.buffer.insert(index, t)
				stack = []  # limpiamos la pila
			last = token  # ponemos el anterior
			next = None  # limpiamos siguiente
			index += 1  # siguiente posicion
				
	
