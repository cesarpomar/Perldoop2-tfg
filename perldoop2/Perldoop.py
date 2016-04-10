#!/usr/bin/python
# -*- coding: utf-8 -*-
from libs.Parser import Parser
from libs.Auxiliary import identer
from libs.Messages import error,get_message
import argparse
import sys
import os.path
import re

#sys.argv=[sys.argv[0],"-out","D:\\",'-m','-oc','D:\\manual\\MultiAsignacion.pl',]
#sys.argv=[sys.argv[0],"-h"]

def analyzer(files,args,output,main=False):
	#Para cada fichero
	for file in files:
		#Comprobamos si existe
		if not os.path.exists(file):
			error(error='FILE_NOT_FOUND',file=file)
			quit()
		
		#Comprobamos si tenemos acceso a el
		if not os.access(file, os.R_OK):
			error(error='FILE_NOT_ACCESS',file=file)
			quit()
		
		#Creamosel parses
		parser=Parser()
		
		#Opciones basicas del parser
		parser.main_class=main
		parser.file_name=os.path.basename(file)
		parser.class_name=re.sub(r'(.*)\..*$', r'\1', parser.file_name)
		
		#Argumentos
		if args.read_comments:
			parser.read_comments=True
		if args.emulate_parens:
			parser.emulate_parens=True
		if args.optimize_code:
			parser.optimize_code=True
		if args.unreachable_code:
			parser.unreachable_code=True
		if args.error_abort:
			parser.error_abort=True
		if args.debug_lexer:
			parser.lexer_debug=True
		if args.debug_parser:
			parser.parser_debug=True
			#Solo si se tienen permisos de escritura
			if args.debug_file and os.access(args.debug_file, os.W_OK):
				if args.debug_details:
					parser.parser_debug_details=True
			if args.debug_size:
				#Solo si es un numero positivo
				if args.debug_size > 0:
					parser.parser_debug_len=args.debug_size
		#Ejecucion
		input=open(file, 'r')
		perl=input.read()
		input.close()
			
		java=parser.parse(perl)
		#Si no hay errores
		if not parser.code_error:
			#Identamos el codigo
			java=identer(java)
			#Escribimos el codigo
			output = open(os.path.join(output,parser.class_name+'.java'), 'w')
			output.write(java)
			output.close()
	

if __name__=='__main__':
	#Opciones del analizador
	argp = argparse.ArgumentParser(description=get_message('HELP_TOOL_DESCRIPTION'))
	argp.add_argument('files', nargs='+', action='store', metavar='infile'  , help=get_message('HELP_FILES'))
	argp.add_argument('-m','-main', action='store_true', dest='main', help=get_message('HELP_MAIN'))
	argp.add_argument('-out', action='store', dest='out', default=os.getcwd(), metavar='dir', help=get_message('HELP_OUT'))
	argp.add_argument('-c','--comments', action='store_true', dest='read_comments', help=get_message('HELP_COMMENTS'))
	argp.add_argument('-ep','--emulate-parens', action='store_true', dest='emulate_parens', help=get_message('HELP_EMULATE_PAREN'))
	argp.add_argument('-oc','--optimize-code', action='store_true', dest='optimize_code', help=get_message('HELP_OPTIMIZE_CODE'))
	argp.add_argument('-uc','--unreachable-code', action='store_true', dest='unreachable_code', help=get_message('HELP_UNRECHEABLE_CODE'))
	argp.add_argument('-ea','--error-abort', action='store_true', dest='error_abort', help=get_message('HELP_ERROR_ABORT'))
	#Opciondes de depuracion
	debug=argp.add_argument_group('debugger arguments', get_message('HELP_DEBUGGER'))
	debug.add_argument('-dl','--debug-lexer', action='store_true', dest='debug_lexer', help=get_message('HELP_DEBUGGER_LEXER'))
	debug.add_argument('-dp','--debug-parser', action='store_true', dest='debug_parser', help=get_message('HELP_DEBUGGER_PARSER'))
	debug.add_argument('-df','--debug-file', action='store',type=str, dest='debug_file', metavar='file', help=get_message('HELP_DEBUGGER_FILE'))
	debug.add_argument('-ds','--debug-size', action='store',type=int, dest='debug_size', metavar='size',help=get_message('HELP_DEBUGGER_SIZE'))
	debug.add_argument('-dd','--debug-details', action='store_true', dest='debug_details',help=get_message('HELP_DEBUGGER_DETAILS'))
	
	args=argp.parse_args()
	
	#Comprobamos si existe el directorio de salida
	if not os.path.exists(args.out):
		error(error='OUT_NOT_FOUND')
		quit()	
	
	#Comprobamos si tiene permido para escribir la salida
	if not os.access(args.out, os.W_OK):
		error(error='OUT_NOT_ACCESS')
		quit()
	#Si necesita main
	if args.main:
		analyzer(args.files[:-1], args, args.out)
		analyzer(args.files[-1:], args, args.out, True)
	else:
		analyzer(args.files, args, args.out)

