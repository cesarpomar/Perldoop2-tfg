# -*- coding: utf-8 -*-

class Messages:
	# idioma por defecto
	DEFAULT_LANG = 'spanish'
	LANGUAGE = DEFAULT_LANG
	
	# Errores que no generan codigo erroneo
	not_fatal = {
	'VAR_FOR_TYPED',
	'LABEL_UNKNOWN_IGNORE',
	}
	
	# Definicion de los idiomas
	spanish = {
	# Descripciones Interfaz		
	'HELP_TOOL_DESCRIPTION':'Perldoop 2.0: Un compilador fuente-a-fuente Perl-Java.', 	
	'HELP_FILES':'Ficheros Perl para ser analizados.', 	
	'HELP_MAIN':'Crea una función de inicio "main" en el último fichero para poder ejecutar el código directamente.', 	
	'HELP_OUT':'Carpeta donde se guardará los ficheros generados, por defecto es el directorio actual.', 	
	'HELP_COMMENTS':'Los comentarios dentro del código Perl, se mantendrán en el código java.', 	
	'HELP_EMULATE_PAREN':'Añade automáticamente los paréntesis a las funciones, si el código es sintácticamente correcto, debería hacerlo correctamente.', 	
	'HELP_OPTIMIZE_CODE':'Mejora el código de salida haciéndolo más visible y eliminado redundancias dando lugar a un mayor rendimiento.', 	
	'HELP_UNRECHEABLE_CODE':'Comprueba la existencia de código muerto, si existe, el código resultante no podrá ser copilado.', 	
	'HELP_ERROR_ABORT':'Para el análisis en caso de encontrar un error.', 	
	'HELP_DEBUGGER':'Opciones para la depuración del análisis.', 	
	'HELP_DEBUGGER_LEXER':'Activa la impresión de tokens para el analizador léxico.', 	
	'HELP_DEBUGGER_PARSER':'Activa la impresión de reglas para el analizador sintáctico.', 	
	'HELP_DEBUGGER_SIZE':'Tamaño del código mostrado para cada regla durante la depuración.', 	
	'HELP_DEBUGGER_FILE':'Fichero para almacenar la depuración de reglas para mejorar su visibilidad y compresión.', 	
	'HELP_DEBUGGER_DETAILS':'Si se usa un fichero, podrán mostrarse más detalles sobre las reglas al analizar.', 			
	# Errores Interfaz	
	'FILE_NOT_FOUND':'No se ha encontrado el fichero %file.',
	'FILE_NOT_ACCESS':'No se ha podido acceder al fiero %file.',
	'OUT_NOT_FOUND':'El directorio de salida no existe.',
	'OUT_NOT_ACCESS':'No tienes permiso de escritura en el directorio de salida.', 		
	# Errores Generales
	'ERROR':'Error',
	'WARNING':'Aviso',
	'ILEGAL_TOKEN':'El carácter %c no está permitido',
	'LABEL_UNKNOWN_IGNORE':'La etiqueta %label ha sido ignorada.',
	'SYNTAX_ERROR_TOKEN':'No se esperaba el componente %type "%token".',
	'SYNTAX_ERROR_EOF':'Error sintactico, final de fichero inexperado.',
	'VAR_NOT_DECLARE':'La variable "%var" tiene definido un tipo pero no ha sido declarada.',
	'VAR_NOT_TYPE':'La variable "%var" no tiene asignado un tipo',
	'VAR_NOT_EXIST':'La variable "%var" no ha sido declarada.', 	
	'VAR_ERROR_ACCESS':'Se esperaba acceder a %type pero se encontro %find',
	'VAR_ALREADY_DECLARE':'La variable %var ya habia sido declarada en la linea %line', 	
	'WORD_NATIVE_DECLARE':'La palabra %word es una palabra reservada, no se puede usar.', 	
	'VAR_REQUIRES':'No se puede asignar un valor a algo que no sea una variable.',
	'VAR_ALREADY_TYPED':'Definicion de tipo sobre %var despues de ser declarada.',
	'VAR_FOR_TYPED':'La variable %var tiene un tipo declarado en la linea %line que sera ignorado.', 	
	'VAR_REF_REQUIRES':'Se esperaba una referencia a %var.',
	'VAR_REF_SCAlAR':'Solo se pueden crear punteros a variables colecciones.',
	'COLECTION_REQUIRES':'La variable %var no es una coleccion.',
	'SCALAR_REQUIRES':'La variable %var debe ser un escalar.',
	'READ_BEFORE_ASSIGN':'La variable "%var" fue leida antes de asignarle un valor.',
	'IMPOSIBLE_CAST':'No se puede castear %type a %cast',
	'SIZE_REQUIRED':'La declaracion de "%var" requiere al menos una etiqueta de tamaño.',
	'FUNCTION_NOT_EXIST':'La funcion %funct no existe.',
	'FUNCTION_ALREADY_DECLARE':'La funcion %funct ya habia sido declarada en la linea %line',
	'FUNCTION_ARGS_ERROR':'La funcion %funct espera %exp argumentos en vez de %find',
	'FUNCTION_NATIVE_ERROR':'La funcion %funct tiene un numero incorrecto de parametros.',
	'FUNCTION_NATIVE_VAR':'El argumento %n de %funct debe ser una variable.',
	'INVALID_MULTI_EQUALS':'El tipo de la parte derecha de la multi asignacion no es valido.',
	'HASH_NOT_VALUE':'La ultima clave del hash no tiene un valor.',
	'REF_OPERATION':'No se puede realizar operaciones sobre referencias.',
	'REF_REQUIRES':'Las colecciones solo pueden pasarse como referencia a las funciones.',
	'RETURN_PARAM_ERROR':'Return esperaba %num argumentos pero recibio %find',
	'NEXT_ERROR':'No puedes usar next fuera de un bucle.',
	'LAST_ERROR':'No puedes usar last fuera de un bucle.',
	'RETURN_ERROR':'No puedes usar return fuera de una funcion.',
	'FOREACH_ERROR':'Foreach solo puede usarse sobre colecciones.',
	'SMART_EQ':'El operador ~~ no esta soportado por razones de eficiencia.',
	'INC_DEC_COLECTION':'Los operadores de incremento y decremento no pueden usarse en colecciones.',
	'UNREACHABLE_STATEMENT':'El codigo despues de un LAST, NEXT o RETURN nunca sera ejecutado.',
	'DECLARE_ACCESS':'Acceder a una coleccion que no esta guardada en una variable no esta permitido.',
	'ALREADY_EXTENDS':'Solo puede haber un bloque especial(MAPPER,REDUCER,...) en el codigo.',
	'SPECIAL_LOCAL_BLOCK':'Los bloques especiales no pueden estar dentro de otro bloque.',
	'PACK_NOT_EXIST':'El paquete %pack no existe.',
	'PACK_VAR_NOT_EXIST':'La variable "%var" no existe en el paquete %pack',
	'PACK_FUNCTION_NOT_EXIST':'La funcion "%funct no existe en el paquete %pack"',
	'PACK_DIF_NAME':'El nombre del paquete debe coincidir con el nombre del fichero.',
	'PACK_AFTER_CODE':'La directiva package debe ser la primera en el codigo.',
	'FILE_ARRAY_ERROR':'No puedes leer todo un fichero en algo que no sea un array o una lista de Strings.',
	'FILE_STRING_ERROR':'No puedes leer un fichero en una variable que no es un String.',
	'NOT_FILE':'La variable "%var" no es un fichero.',
	'NOT_STRING_CONCAT':'El operador . debe estar precedido por una cadena',
	# Errores Funciones
	'EACH_ERROR':'La funcion each necesita dos variables a la izquierda y un hash a la derecha.',
	'SORT_TYPE_A_ERROR':'La funcion sort necesita la declaracion de tipo de a.',
	'SORT_TYPE_ERROR':'El tipo de a no coincide con el tipo de %var.',
	'FUN_ARRAY_ERROR':'La funcion %fun solo funciona sobre arrays o listas.',
	'DELETE_NOT_HASH':'La funcion delete solo puede usarse sobre variables de tipo hash que contengan escalares.',
	'COLECTION_CONCAT_ERROR':'La funcion %funct no puede concatenar dos colecciones de distinto tipo.',
	# Errores Hadoop
	'HD_MAPPER_MANY_LOOP':'Solo se puede usar una vez la etiqueta <mapper_loop>.',
	'HD_MAPPER_LOOP_ALONE':'La etiqueta <mapper_loop> debe usarse en un bloque <mapper_code>.',
	'HD_NEXT_LAST':'No se pueden usar modificadores NEXT o LAST en un bucle <mapper_loop>.',
	'HD_PRINT':'El print de Hadoop debe constar de 4 argumentos (key,separador1,valor,separador2).',
	'HD_REDUCER_KEY':'No se ha encontrado la variable key para el reducer.',
	'HD_REDUCER_VALUE':'No se ha encontrado la variable value para el reducer.',
	'HD_REDUCER_INCOMPLETE':'No se han especificado todos los bloques del reducer.'
	}
	
	english = {}
	
	# Idiomas disponibles
	languages = {'spanish':spanish, 'english':english}

	# Obtiene un mensaje
	@classmethod
	def get_message(Msg, id):
		# Si el idioma existe y contiene el id del mensaje
		if Msg.LANGUAGE in Msg.languages and id in Msg.languages[Msg.LANGUAGE]:
			return Msg.languages[Msg.LANGUAGE][id]
		else:
			return Msg.languages[Msg.DEFAULT_LANG][id]	
	
	@classmethod
	def error(Msg, parser=None, error=None, position=None, **names):
		# Sin error no hacemos nada
		if error == None:
			return
		# Obtenemos el mensaje de error
		msg = Messages.get_message(error)
		# Posicion del error, cuando se tenga
		msg_pos = ' '
		# Remplazamos las claves por sus valores
		for key in names.keys():
			msg = msg.replace('%' + key, str(names[key]))	
		# Si esta definida la posicion y la linea
		if position and position.line:
			# Si existe calculamos la columna
			if position.lexpos:	
				msg_pos = str(position.column(parser)) + ':' + msg_pos	
			msg_pos = str(position.line) + ':' + msg_pos
		# Si tenemos analizador
		if parser:	
			# Si solo es un aviso
			if error in Msg.not_fatal:
				# Imprimimos el mensaje como aviso
				print(parser.file_name + ':' + msg_pos + Messages.get_message('WARNING') + ': ' + msg)
				Messages.show_code(parser, position)
			else:
				# Imprimimos el mensaje como error
				print(parser.file_name + ':' + msg_pos + Messages.get_message('ERROR') + ': ' + msg)
				Messages.show_code(parser, position)
				# Marcamos el codigo como erroneo en el analizador
				parser.code_error = True
				# Terminamos el programa si la opcion lo permite
				if parser.error_abort:
					quit()
		else:
			if error in Msg.not_fatal:
				# Imprimimos el mensaje como aviso
				print(Messages.get_message('WARNING') + ': ' + msg)
			else:
				# Imprimimos el mensaje como error
				print(Messages.get_message('ERROR') + ': ' + msg)		
				
	@classmethod	
	def show_code(Msg, parser, pos):	
		# Si sabemos la posicion
		if pos and pos.lexpos:
			# TamaÃ±o maximo a ambos lados del error
			TAM = 40
			# Codigo de ambos lados
			lcode = parser.lexer.input[pos.lexpos - TAM:pos.lexpos]
			rcode = parser.lexer.input[pos.lexpos:pos.lexpos + TAM]
			# Si hay fin de linea, cortamos por ahÃ­
			init = lcode.rfind("\n") + 1
			end = rcode.find("\n")
			if end == -1: end = TAM * 2
			# Cogemos el codigo sin saltos de linea
			lcode = lcode[init:]
			rcode = rcode[:end]
			# Identamos y mostramos el error
			print (" "*8 + lcode + rcode)
			# Identamos y mostramos la marca de posicion
			print (" "*(8 + len(lcode)) + '^')

		
		
		
		
		
