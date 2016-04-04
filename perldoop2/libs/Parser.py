
#!/usr/bin/python
# -*- coding: utf-8 -*-

from libs.Lexer import Lexer
import libs.ply.yacc as yacc
from libs.Options import Options
from libs.Functions import PerlFunctions
from libs.Hadoop import Hadoop
from libs.Messages import error
from libs.Datatypes import Position, var_types, Code, NEXT, LAST, LABEL_TYPE,\
	LABEL_DECLARE, Type, LIST, Declare, REF, INTEGER, Access, VARIABLE, STRING,\
	DOUBLE, ARRAY, HASH, BOOLEAN, LONG
from libs.Auxiliary import debugger , create_package, declare_package,\
	access_package
from libs.Blocks import create_class, check_st, function_header, create_function,\
	block_empty, block_header, block_if_concat, block_while, block_until,\
	block_dowhile, block_dountil, create_for_declare, block_foreach_head,\
	foreach_declare_init, foreach_declare_end, block_foreach_var, block_foreach,\
	block_if, block_unless, block_elif_concat, block_else, block_elif,\
	post_block_if, post_block_unless, post_block_while, post_block_until,\
	post_block_for
from libs.Statements import statements_concat, create_statement,\
	advanced_declare, create_return, equals, equals_declare, equals_input,\
	equals_read, multi_equals_single, multi_equals_multi, function_call, read_var,\
	create_var, value_cmd
from libs.Collection import create_value_var, create_array_value,\
	create_hash_value, create_array_range, access_colection, access_pointed,\
	create_pointer_var
from libs.Operations import op_basic, op_divide, op_pow, op_repeat, op_opposite,\
	op_mod, plusplus_var, minusminus_var, var_plusplus, var_minusminus, op_period,\
	num_compare, string_compare, smart_compare, m_regex, s_regex, y_regex,\
	binary_op, binary_not, logic_or, logic_and, logic_not, logic_xor,\
	condicional_equals, op_equals, cmp_string, cmp_num


class Parser(Options,PerlFunctions,Hadoop):

	def __init__(self):
		#Inicializamos los atributos padres
		super(). __init__()
		#Declaraciones del analizador
		self.__package__='libs'								#Indica que la clase esta dentro del paquete
		self.parser=yacc.yacc(module=self,start = 'file')	#Declara en analizador

		
	def parse(self,text):
		self.lexer=Lexer()
		self.lexer.debug_mode=self.lexer_debug
		self.lexer.parser=self
		return self.parser.parse(input=text,lexer=self.lexer,debug=debugger(self))
		
	def p_error(self,p):
		if p:
			error(self,'SYNTAX_ERROR_TOKEN',Position(line=p.lineno,lexpos=p.lexpos),token=p.value,type=p.type)
		else:
			error(self,'SYNTAX_ERROR_EOF')
		
	#Tokens
	tokens=Lexer.tokens
	
	#Precedencias
	precedence =(
		('left','LLOR','LLXOR'),
		('left','LLAND'),
		('left','LLNOT'),
		#nonassoc list operators (rightward),
		('left','COMMA'),
		('right','EQUALS','TIMESEQUAL','DIVEQUAL','MODEQUAL','PLUSEQUAL','MINUSEQUAL',
		'LSHIFTEQUAL','RSHIFTEQUAL','ANDEQUAL','OREQUAL','XOREQUAL','POWEQUAL',
		'LANDEQUAL','LOREQUAL','PERIODEQUAL','XEQUAL'),
		('right','COLON','QUEST_CLOSE'),
		('nonassoc','TWO_PERIOD'),
		('left','LOR'),
		('left','LAND'),
		('left','OR','XOR'),
		('left','AND'),
		('nonassoc','NUM_EQ','NUM_NE','STR_EQ','STR_NE','CMP','CMP_NUM','SMART_EQ'),
		('nonassoc','NUM_LT','NUM_LE','NUM_GT','NUM_GE','STR_LT','STR_LE','STR_GT','STR_GE'),
		#nonassoc named unary operators
		('left','LSHIFT','RSHIFT'),
		('left','PLUS','MINUS','PERIOD'),
		('left','TIMES','DIVIDE','PERCENTAGE','X'),
		('left','STR_REX','STR_NO_REX'),
		('left','LNOT','NOT','UNITARY'),
		('right','POW'),
		('nonassoc','PLUSPLUS','MINUSMINUS'),
		('right','LPAREN','RPAREN','LBRACKET','RBRACKET','LBRACE','RBRACE'),
		#left terms and list operators(leftward)
	)
	##
	## Reglas
	##
	
	### Regla inicial ###	
	def p_file(self,p):
		'file : code'
		p[0]=create_class(self)
		if self.is_package:
			create_package(self)
		
	### Code ###
	def p_code(self,p):
		'code : statements function'
		check_st(self,p[1])
		self.functions_code=p[2]+self.functions_code
		self.global_code=p[1].value+self.global_code
		
	### function ###	
	def p_function_empty(self,p):
		'function : '
		p[0]=''	
	
	def p_function(self,p):
		'function : function_body code'
		p[0]=p[1]
	
	### function header ###
	def p_function_header(self,p):
		'function_header : args_opt returns_opt SUB ID'
		function_header(self,p[1],p[2],p[4],Position(p,4))
		p[0]=p[4]
	
	### function body ###	
	def p_function_body(self,p):
		'function_body : function_header LBRACE statements RBRACE'
		p[0]=create_function(self,p[1],p[3])
		
	### ARGS ###
	def p_args_opt_empty(self,p):
		'args_opt : '	
		p[0]=None

	def p_args_opt(self,p):
		'args_opt : ARGS function_types'	
		p[0]=p[2]

	### RETURNS ###
	def p_returns_opt_empty(self,p):
		'returns_opt : '	
		p[0]=None

	def p_returns_opt(self,p):
		'returns_opt : RETURNS function_types'	
		p[0]=p[2]
	
	### function type ###
	def p_function_types_empty(self,p):
		'function_types : '	
		p[0]=[]
	
	def p_function_types(self,p):
		'function_types : function_types TYPE'	
		p[0]=p[1]+[[var_types[p[3]]]]
		
	def p_function_types_ref(self,p):
		'function_types : function_types REF dimension TYPE'	
		p[0]=p[1]+[[Type(REF)]+p[3]+[var_types[p[4]]]]
		
	### Statements ###
	def p_statements_empty(self,p):
		'statements : '	
		p[0]=Code()
	
	def p_statements(self,p):
		'statements : statements statement_type'
		p[0]=statements_concat(self,p[1],p[2])
	
	### Statement type ###	
	def p_statement_type_simple(self,p):
		'statement_type : labels_line list post_block SEMI line_comment'
		p[0]=create_statement(self,p[2],p[3],p[5],Position(p,4))
		
	def p_statement_type_multi_equals(self,p):
		'statement_type : labels_line multi_equals post_block SEMI line_comment'
		p[0]=create_statement(self,p[2],p[3],p[5],Position(p,4))	
		
	def p_statement_type_special_statement(self,p):
		'statement_type : special_statement SEMI'
		p[0]=p[1]
		p[0].pos=Position(p,2)
		p[0].value+=';\n'
		
	def p_statement_type_block(self,p):
		'statement_type : block_header block '
		p[0]=p[2]	
		
	def p_statement_type_block_empty(self,p):
		'statement_type : LBRACE block_header statements RBRACE'
		p[0]=block_empty(self,p[3],Position(p,4))
		
	def p_statement_advanced_declare(self,p):
		'statement_type : declare TYPE'
		p[0]=advanced_declare(self,p[1],[var_types[type]],Position(p,2))
		
	def p_statement_advanced_declare_dim(self,p):
		'statement_type : declare dimension TYPE'
		p[0]=advanced_declare(self,p[1],p[2]+[var_types[p[3]]],Position(p,3))
		
	def p_statement_advanced_declare_ref(self,p):
		'statement_type : declare REF dimension TYPE'
		p[0]=advanced_declare(self,p[1],[Type(REF)]+p[3]+[var_types[p[4]]],Position(p,4))
			
	def p_statement_comment(self,p):
		'statement_type : COMMENT'
		p[0]=Code(value='/*'+p[1]+'*/\n')
				
	def p_statement_line_comment(self,p):
		'statement_type : SEMI line_comment'
		p[0]=p[2]	
		
	def p_statement_package(self,p):
		'statement_type : PACKAGE ID SEMI '
		declare_package(self,p[2],Position(p,2))
		p[0]=Code()
		
	def p_statement_java_line(self,p):
		'statement_type : JAVA_LINE'
		p[0]=Code(value=p[1])
		
	def p_statement_java_import(self,p):
		'statement_type : JAVA_IMPORT'
		self.package_code+=p[1]
		p[0]=Code()
						
	def p_statement_error(self,p):
		'statement_type : error SEMI '
		p[0]=Code()
		
	### Special Statement ###
	def p_special_statement_break(self,p):
		'special_statement : LAST'
		p[0]=Code(value='break')
		p[0].flags[LAST]=True
			
	def p_special_statement_next(self,p):
		'special_statement : NEXT'
		p[0]=Code(value='continue')
		p[0].flags[NEXT]=True
		
	def p_special_statement_return_paren(self,p):
		'special_statement : RETURN LPAREN list RPAREN' 
		p[0]=create_return(self,p[3],Position(p,4))
		
	def p_special_statement_return(self,p):
		'special_statement : RETURN list' 
		p[0]=create_return(self,p[2],p[2][-1].pos)
		
	def p_special_statement_return_empty(self,p):
		'special_statement : RETURN' 
		p[0]=create_return(self,[],Position(p,1))
		
		
	### line_comment ###
	def p_line_comment_empthy(self,p):
		'line_comment : '
		p[0]=None

	def p_line_comment(self,p):
		'line_comment : COMMENT_LINE'
		p[0]=Code(value='//'+p[1],pos=Position(p,1))	

	### labels_type ###
	def p_labels_line_empthy(self,p):
		'labels_line : '
		p[0]=None	
	
	def p_labels_type_type(self,p):
		'labels_line : TYPE'
		self.labels_line[LABEL_TYPE]=[var_types[p[1]]]
		
	def p_labels_type_dim(self,p):
		'labels_line : dimension TYPE'
		self.labels_line[LABEL_TYPE]=p[1]+[var_types[p[2]]]
		
	def p_labels_type_ref(self,p):
		'labels_line : REF dimension TYPE'
		self.labels_line[LABEL_TYPE]=[Type(REF)]+p[2]+[var_types[p[3]]]

	def p_labels_declare(self,p):
		'labels_line : declare'
		self.labels_line[LABEL_DECLARE]=p[1]

	### Dimension ###
	def p_dimension_hash(self,p):
		'dimension : L_HASH size_opt'
		self.imports['Map']=True
		p[0]=[Type(HASH,p[2])]
		
	def p_dimension_array(self,p):
		'dimension : L_ARRAY size_opt'
		p[0]=[Type(ARRAY,p[2])]
	
	def p_dimension_list(self,p):
		'dimension : L_LIST size_opt'
		self.imports['List']=True
		p[0]=[Type(LIST,p[2])]
		
	def p_dimension_hash_more(self,p):
		'dimension : dimension L_HASH size_opt'
		self.imports['Map']=True
		p[0]=p[1]+[Type(HASH,p[3])]
		
	def p_dimension_array_more(self,p):
		'dimension : dimension L_ARRAY size_opt'
		p[0]=p[1]+[Type(ARRAY,p[3])]
	
	def p_dimension_list_more(self,p):
		'dimension : dimension L_LIST size_opt'
		self.imports['List']=True
		p[0]=p[1]+[Type(LIST,p[3])]
		
	### SIZE ###
	def p_size_opt_emtpy(self,p):
		'size_opt : '
		p[0]=None
		
	def p_size_opt(self,p):
		'size_opt : SIZE'
		p[0]=p[1]
		
	### Declare ###
	def p_declare_var(self,p):
		'declare : VAR'
		p[0]=[Declare(p[1],Position(p,1),True)]
		
	def p_declare_size(self,p):
		'declare : SIZE'
		p[0]=[Declare(p[1],Position(p,1))]
	
	def p_declare_more_var(self,p):
		'declare : declare VAR'
		p[0]=p[1]
		p[0].append(Declare(p[2],Position(p,2),True))
		
	def p_declare_more_size(self,p):
		'declare : declare SIZE'
		p[0]=p[1]
		p[0].append(Declare(p[2],Position(p,2)))		
					
	### Vars init ###
	def p_change_init(self,p):
		'change_init : '
		self.init_var=not self.init_var
		
	### Block header ###
	def p_block_header(self,p):
		'block_header : '
		block_header(self)
		
	### Block ###		
	def p_block_if(self,p):
		'block : if_block elif'
		p[0]=block_if_concat(self,p[1],p[2])
		
	def p_block_while(self,p):
		'block : WHILE change_init LPAREN expression RPAREN change_init LBRACE statements RBRACE'
		p[0]=block_while(self,p[4],p[8],Position(p,9))
		
	def p_block_until(self,p):
		'block : UNTIL change_init LPAREN expression RPAREN change_init LBRACE statements RBRACE'
		p[0]=block_until(self,p[4],p[8],Position(p,9))				
		
	def p_block_do_while(self,p):
		'block : DO LBRACE statements RBRACE WHILE change_init LPAREN expression RPAREN change_init SEMI'
		p[0]=block_dowhile(self,p[8],p[3],Position(p,11))	
		
	def p_block_do_until(self,p):
		'block : DO LBRACE statements RBRACE UNTIL change_init LPAREN expression RPAREN change_init SEMI'
		p[0]=block_dountil(self,p[8],p[3],Position(p,11))	
		
	def p_block_for(self,p):
		'block : FOR LPAREN opt_list change_init SEMI opt_list SEMI opt_list RPAREN change_init LBRACE statements RBRACE'
		p[0]=create_for_declare(self,p[3],p[6],p[8],p[12],Position(p,13))	
		
	def p_block_foreach(self,p):
		'block : for_each LBRACE statements RBRACE'
		p[0]=block_foreach_head(self, p[1], p[3], Position(p,4))
		
	## for type ##
	def p_for_type(self,p):
		'for_type :'
		foreach_declare_init(self)
		
	## for variable ##
	def p_for_variable(self,p):
		'for_variable : variable'
		p[0]=foreach_declare_end(self,p[1])	
		
	### opt List ###
	def p_opt_list_empty(self,p):
		'opt_list :'
		p[0]=None
	
	def p_opt_list(self,p):
		'opt_list : list'
		p[0]=p[1]
		
	### Foreach block ###
	def p_foreach_var(self,p):
		'for_each : FOR for_type for_variable LPAREN expression RPAREN'
		p[0]=block_foreach_var(self,p[3],p[5])

	def p_foreach(self,p):
		'for_each : FOR  LPAREN expression RPAREN'
		p[0]=block_foreach(self,p[3])	
		
	### IF block ###
	def p_if_block_if(self,p):
		'if_block : IF LPAREN expression RPAREN LBRACE statements RBRACE'	
		p[0]=block_if(self,p[3],p[6],Position(p,7))

	def p_if_block_unless(self,p):
		'if_block : UNLESS LPAREN expression RPAREN LBRACE statements RBRACE'	
		p[0]=block_unless(self,p[3],p[6],Position(p,7))
	
	### ELIF ###		
	def p_elif_empty(self,p):
		'elif :'		
		p[0]=None
	
	def p_elif_elif(self,p):
		'elif : block_header elif_block elif'
		p[0]=block_elif_concat(self,p[2],p[3])
		
	def p_elif_else(self,p):
		'elif : block_header ELSE LBRACE statements RBRACE'
		p[0]= block_else(self,p[4],Position(p,5))	
		
	### ELIF block ###
	def p_elif_block(self,p):
		'elif_block : ELSIF change_init LPAREN expression RPAREN change_init LBRACE statements RBRACE'
		p[0]=block_elif(self,p[4],p[8],Position(p,9))
				
	### POST Block ###
	def p_post_block_empty(self,p):
		'post_block : '
		p[0]=None
	
	def p_post_block_if(self,p):
		'post_block : IF expression'
		p[0]=post_block_if(self,p[2])
		
	def p_post_block_unless(self,p):
		'post_block : UNLESS expression'
		p[0]=post_block_unless(self,p[2])
	
	def p_post_block_while(self,p):
		'post_block : WHILE expression'
		p[0]=post_block_while(self,p[2])
		
	def p_post_block_until(self,p):
		'post_block : UNTIL expression'
		p[0]=post_block_until(self,p[2])
		
	def p_post_block_for(self,p):
		'post_block : FOR expression'
		p[0]=post_block_for(self,p[2])
					
	### Expression###			
	def p_expression_paren(self,p):
		'expression : LPAREN expression RPAREN'
		p[0]=p[2]
		p[0].pos=Position(p,3)
		p[0].value=p[1]+p[2].value+p[3]		
				
	def p_expression_assignment(self,p):
		'expression : assignment'
		p[0]=p[1]
		
	def p_expression_arithmetic(self,p):
		'expression : arithmetic'
		p[0]=p[1]
		
	def p_expression_comparations(self,p):
		'expression : comparations'
		p[0]=p[1]
		
	def p_expression_regex(self,p):
		'expression : regex'
		p[0]=p[1]
		
	def p_expression_binary(self,p):
		'expression : binary'
		p[0]=p[1]
		
	def p_expression_logical(self,p):
		'expression : logical'
		p[0]=p[1]
		
	def p_expression_value(self,p):
		'expression : value'
		p[0]=p[1]	
		
	def p_expression_function(self,p):
		'expression : function_call'
		p[0]=p[1]	
		
	def p_expression_variable(self,p):
		'expression : var_access'
		p[0]=create_value_var(p[1])
		
	### List ###
	def p_list_comma(self,p):
		'list : expression COMMA list'
		p[0]=[p[1]]+p[3]
		
	def p_list_expression(self,p):
		'list : expression'
		p[0]=[p[1],]
		
	def p_list_expression_comma(self,p):
		'list : expression COMMA'
		p[0]=[p[1],]
				
	### Assignment ###
	def p_assignment_equals(self,p):
		'assignment : var_access EQUALS expression'
		p[0]=equals(self,p[1],p[3])
			
	def p_assignment_declare_colection(self,p):
		'assignment : var_access EQUALS LPAREN RPAREN'		
		p[0]=equals_declare(self,p[1])
		
	def p_assignment_declare_var(self,p):
		'assignment : var_access EQUALS UNDEF'		
		p[0]=equals_declare(self,p[1])
		
	def p_assignment_input(self,p):
		'assignment : var_access EQUALS STDIN'
		p[0]=equals_input(self,p[1],Position(p,3))
		
	def p_assignment_read(self,p):
		'assignment : var_access EQUALS NUM_LT var_access NUM_GT'
		p[0]=equals_read(self,p[1],p[4],Position(p,5))
		
	def p_assignment_plusequal(self,p):
		'assignment : var_access PLUSEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],op_basic,(BOOLEAN,STRING))
		
	def p_assignment_minusequal(self,p):
		'assignment : var_access MINUSEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],op_basic,(BOOLEAN,STRING))
		
	def p_assignment_timesequal(self,p):
		'assignment : var_access TIMESEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],op_basic,(BOOLEAN,STRING))
		
	def p_assignment_divequal(self,p):
		'assignment : var_access DIVEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],op_divide,(BOOLEAN,STRING))
		
	def p_assignment_modequal(self,p):
		'assignment : var_access MODEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],op_mod,(BOOLEAN,STRING))
		
	def p_assignment_powequal(self,p):
		'assignment : var_access POWEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],op_pow,native=False)
		
	def p_assignment_andequal(self,p):
		'assignment : var_access ANDEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],binary_op,types=(INTEGER,LONG))
		
	def p_assignment_orequal(self,p):
		'assignment : var_access OREQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],binary_op,types=(INTEGER,LONG))
		
	def p_assignment_xorequal(self,p):
		'assignment : var_access XOREQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],binary_op,types=(INTEGER,LONG))
		
	def p_assignment_lshiftequal(self,p):
		'assignment : var_access LSHIFTEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],binary_op,types=(INTEGER,LONG))
		
	def p_assignment_rshiftequal(self,p):
		'assignment : var_access RSHIFTEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],binary_op,types=(INTEGER,LONG))
		
	def p_assignment_landequal(self,p):
		'assignment : var_access LANDEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],logic_and,types=(BOOLEAN,))
		
	def p_assignment_lorequal(self,p):
		'assignment : var_access LOREQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],logic_or,types=(BOOLEAN,))
		
	def p_assignment_xequal(self,p):
		'assignment : var_access XEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],p[2],logic_xor,types=(BOOLEAN,))
		
	def p_assignment_periodequal(self,p):
		'assignment : var_access PERIODEQUAL expression'
		p[0]=op_equals(self,p[1],p[3],'+=',op_period,types=(STRING,))
		
	### Multi equals ###
	def p_multi_equals_single(self,p):
		'multi_equals : LPAREN list RPAREN EQUALS expression'
		p[0]=multi_equals_single(self,p[2],p[5])	
		
	def p_multi_equals_multi(self,p):
		'multi_equals : LPAREN list RPAREN EQUALS LPAREN list RPAREN'
		p[0]=multi_equals_multi(self,p[2],p[6])
		
	### Arithmetic ###
	def p_arithmetic_plus(self,p):
		'arithmetic : expression PLUS expression'
		p[0]=op_basic(self,p[2],p[1],p[3])
	
	def p_arithmetic_minus(self,p):
		'arithmetic : expression MINUS expression'
		p[0]=op_basic(self,p[2],p[1],p[3])
							
	def p_arithmetic_times(self,p):
		'arithmetic : expression TIMES expression'
		p[0]=op_basic(self,p[2],p[1],p[3])
							
	def p_arithmetic_divide(self,p):
		'arithmetic : expression DIVIDE expression'
		p[0]=op_divide(self,p[2],p[1],p[3])
		
	def p_arithmetic_pow(self,p):
		'arithmetic : expression POW expression'
		p[0]=op_pow(self,p[2],p[1],p[3])
		
	def p_arithmetic_x(self,p):
		'arithmetic : expression X expression'
		p[0]=op_repeat(self,p[2],p[1],p[3])
							
	def p_arithmetic_plus_unitary(self,p):
		'arithmetic : PLUS expression %prec UNITARY'
		p[0]=p[2]
							
	def p_arithmetic_minus_unitary(self,p):
		'arithmetic : MINUS expression %prec UNITARY'
		p[0]=op_opposite(self,p[2])
							
	def p_arithmetic_mod(self,p):
		'arithmetic : expression PERCENTAGE expression'
		p[0]=op_mod(self,p[2],p[1],p[3])
							
	def p_arithmetic_plusplus_var(self,p):
		'arithmetic : PLUSPLUS var_access'
		p[0]=plusplus_var(self,p[2])
		
	def p_arithmetic_minusminus_var(self,p):
		'arithmetic : MINUSMINUS var_access'
		p[0]=minusminus_var(self,p[2])
							
	def p_arithmetic_var_plusplus(self,p):
		'arithmetic : var_access PLUSPLUS'
		p[0]=var_plusplus(self,p[1])
							
	def p_arithmetic_var_minusminus(self,p):
		'arithmetic : var_access MINUSMINUS'
		p[0]=var_minusminus(self,p[1])
							
	def p_arithmetic_period(self,p):
		'arithmetic : expression PERIOD expression'
		p[0]=op_period(self,p[2],p[1],p[3])
		
	### Comparations ###
	def p_expression_num_eq(self,p):
		'comparations : expression NUM_EQ expression'
		p[0]=num_compare(self,p[2],p[1],p[3])
		
	def p_expression_num_ne(self,p):
		'comparations : expression NUM_NE expression'
		p[0]=num_compare(self,p[2],p[1],p[3])
		
	def p_expression_num_lt(self,p):
		'comparations : expression NUM_LT expression'
		p[0]=num_compare(self,p[2],p[1],p[3])
		
	def p_expression_num_le(self,p):
		'comparations : expression NUM_LE expression'
		p[0]=num_compare(self,p[2],p[1],p[3])
		
	def p_expression_num_gt(self,p):
		'comparations : expression NUM_GT expression'
		p[0]=num_compare(self,p[2],p[1],p[3])
		
	def p_expression_num_ge(self,p):
		'comparations : expression NUM_GE expression'
		p[0]=num_compare(self,p[2],p[1],p[3])
		
	def p_expression_cmp_num(self,p):
		'comparations : expression CMP_NUM expression'
		p[0]=cmp_num(self,p[1],p[3])
		
	def p_expression_str_eq(self,p):
		'comparations : expression STR_EQ expression'
		p[0]=string_compare(self,p[1],p[3],'==0')
		
	def p_expression_str_ne(self,p):
		'comparations : expression STR_NE expression'
		p[0]=string_compare(self,p[1],p[3],'!=0')
		
	def p_expression_str_lt(self,p):
		'comparations : expression STR_LT expression'
		p[0]=string_compare(self,p[1],p[3],'<0')
		
	def p_expression_str_le(self,p):
		'comparations : expression STR_LE expression'
		p[0]=string_compare(self,p[1],p[3],'<=0')
		
	def p_expression_str_gt(self,p):
		'comparations : expression STR_GT expression'
		p[0]=string_compare(self,p[1],p[3],'>0')
		
	def p_expression_str_ge(self,p):
		'comparations : expression STR_GE expression'
		p[0]=string_compare(self,p[1],p[3],'>=0')
		
	def p_expression_cmp_str(self,p):
		'comparations : expression CMP expression'
		p[0]=cmp_string(self,p[1],p[3])
		
	def p_expression_smart(self,p):
		'comparations : expression SMART_EQ expression'
		p[0]=smart_compare(self,p[1],p[3],Position(p,2))
		
	### Regex ###	
	def p_not_m_regex(self,p):
		'regex : expression STR_NO_REX M_REGEX'	
		p[0]=m_regex(self,p[1],p[3],Position(p,3),negate=True)
	
	def p_m_regex(self,p):
		'regex : expression STR_REX M_REGEX'	
		p[0]=m_regex(self,p[1],p[3],Position(p,3))
	
	def p_s_regex(self,p):
		'regex : expression STR_REX S_REGEX'	
		p[0]=s_regex(self,p[1],p[3],Position(p,3))
	
	def p_y_regex(self,p):
		'regex : expression STR_REX Y_REGEX'	
		p[0]=y_regex(self,p[1],p[3],Position(p,3))	
		
	### Binary ###
	def p_binary_or(self,p):
		'binary : expression OR expression'
		p[0]=binary_op(self,'|',p[1],p[3])
		
	def p_binary_and(self,p):
		'binary : expression AND expression'
		p[0]=binary_op(self,'&',p[1],p[3])
		
	def p_binary_not(self,p):
		'binary : NOT expression'
		p[0]=binary_not(self,p[2])
		
	def p_binary_xor(self,p):
		'binary : expression XOR expression'
		p[0]=binary_op(self,'^',p[1],p[3])
		
	def p_binary_lshift(self,p):
		'binary : expression LSHIFT expression'
		p[0]=binary_op(self,'<<',p[1],p[3])
		
	def p_binary_rshift(self,p):
		'binary : expression RSHIFT expression'
		p[0]=binary_op(self,'>>',p[1],p[3])

	### Logical ###
	def p_logical_lor(self,p):
		'logical : expression LOR expression'
		p[0]=logic_or(self,p[2], p[1], p[3], False)
		
	def p_logical_land(self,p):
		'logical : expression LAND expression'
		p[0]=logic_and(self,p[2], p[1], p[3], False)
		
	def p_logical_lnot(self,p):
		'logical : LNOT expression'
		p[0]=logic_not(self,p[2], False)
		
	def p_logical_llor(self,p):
		'logical : expression LLOR expression'
		p[0]=logic_or(self,p[2], p[1], p[3], True)
		
	def p_logical_lland(self,p):
		'logical : expression LLAND expression'
		p[0]=logic_and(self,p[2], p[1], p[3], True)
		
	def p_logical_llnot(self,p):
		'logical : LLNOT expression'
		p[0]=logic_not(self,p[2], True)
		
	def p_logical_llxor(self,p):
		'logical : expression LLXOR expression'
		p[0]=logic_xor(self,p[2],p[1], p[3])

	def p_logical_equals(self,p):
		'logical : expression QUEST_CLOSE expression COLON expression'
		p[0]=condicional_equals(self,p[1],p[3],p[5])
		
	### function call ###
	def p_function_call_empty_paren(self,p):
		'function_call : ID LPAREN RPAREN'
		p[0]=function_call(self,p[1],Position(p,3))
		
	def p_function_call_list(self,p):
		'function_call : ID LPAREN list RPAREN'
		p[0]=function_call(self,p[1],Position(p,4),p[3])
		
	def p_function_call_exp(self,p):
		'function_call : ID expression %prec UNITARY'
		p[0]=function_call(self,p[1],p[2].pos,[p[2]])
		
	def p_function_call_empty(self,p):
		'function_call : ID %prec UNITARY'
		p[0]=function_call(self,p[1],Position(p,1))
		
	def p_function_call_pack_empty_paren(self,p):
		'function_call : package ID LPAREN RPAREN'
		p[0]=function_call(self,p[2],Position(p,4),package=p[1])
		
	def p_function_call_pack_list(self,p):
		'function_call : package ID LPAREN list RPAREN'
		p[0]=function_call(self,p[2],Position(p,5),p[4],package=p[1])
		
	def p_function_call_pack_exp(self,p):
		'function_call : package ID expression %prec UNITARY'
		p[0]=function_call(self,p[2],p[3].pos,[p[3]],package=p[1])
		
	def p_function_call_pack_empty(self,p):
		'function_call : package ID %prec UNITARY'
		p[0]=function_call(self,p[2],Position(p,2),package=p[1])
		
	### Package ###	
	def p_package(self,p):
		'package : ID TWO_COLON'
		p[0]=access_package(self,p[1],Position(p,1))
				
	### Variable Access ###
	def p_var_access(self,p):
		'var_access : variable'		
		p[0]=Access(p[1])
		p[1].flags[VARIABLE]=True
		
	def p_var_array(self,p):
		'var_access : LBRACKET list RBRACKET'
		p[0]=Access(create_array_value(self,p[2]))
		
	def p_var_hash(self,p):
		'var_access : LBRACE list RBRACE'
		p[0]=Access(create_hash_value(self,p[2]))
		
	def p_var_array_range(self,p):
		'var_access : LPAREN expression TWO_PERIOD expression RPAREN'
		p[0]=create_array_range(self,p[1],p[3])
		
	def p_var_access_array(self,p):
		'var_access : var_access LBRACKET expression RBRACKET'
		p[0]=access_colection(self,p[1],p[3],Position(p,4),ARRAY)
		
	def p_var_access_hash(self,p):
		'var_access : var_access LBRACE expression RBRACE '
		p[0]=access_colection(self,p[1],p[3],Position(p,4),HASH)
		
	def p_var_access_array_pointed(self,p):
		'var_access : var_access POINTED LBRACKET expression RBRACKET'
		p[0]=access_colection(self,p[1],p[4],Position(p,5),ARRAY,ref=True)
		
	def p_var_access_hash_pointed(self,p):
		'var_access : var_access POINTED LBRACE expression RBRACE '
		p[0]=access_colection(self,p[1],p[4],Position(p,5),HASH,ref=True)
		
	def p_var_access_pointed_scalarB(self,p):
		'var_access : DOLLAR LBRACE var_access RBRACE'
		p[0]=access_pointed(self,p[3],Position(p,4))
		
	def p_var_access_pointed_arrayB(self,p):
		'var_access : AT LBRACE var_access RBRACE'
		p[0]=access_pointed(self,p[3],Position(p,4))
		
	def p_var_access_pointed_hashB(self,p):
		'var_access : PERCENTAGE LBRACE var_access RBRACE'
		p[0]=access_pointed(self,p[3],Position(p,4))

	def p_var_access_pointed_scalar(self,p):
		'var_access : DOLLAR var_access %prec UNITARY'
		p[0]=access_pointed(self,p[2],p[2].var.pos)
		
	def p_var_access_pointed_array(self,p):
		'var_access : AT var_access %prec UNITARY'
		p[0]=access_pointed(self,p[2],p[2].var.pos)
		
	def p_var_access_pointed_hash(self,p):
		'var_access : PERCENTAGE var_access %prec UNITARY'
		p[0]=access_pointed(self,p[2],p[2].var.pos)		
		
	def p_var_access_variable_ref(self,p):
		'var_access : BACKSLASH var_access %prec UNITARY'
		p[0]=create_pointer_var(self,p[2])	
				
	### Variable ###
	def p_variable_scalar(self,p):
		'variable : DOLLAR ID'
		p[0]=read_var(self,p[2],pos=Position(p,2))
		
	def p_variable_array(self,p):
		'variable : AT ID'
		p[0]=read_var(self,p[2],pos=Position(p,2))
		
	def p_variable_hash(self,p):
		'variable : PERCENTAGE ID'
		p[0]=read_var(self,p[2],pos=Position(p,2))
		
	def p_variable_pack_scalar(self,p):
		'variable : DOLLAR package ID'
		p[0]=read_var(self,p[3],pos=Position(p,3),package=p[2])
		
	def p_variable_pack_array(self,p):
		'variable : AT package ID'
		p[0]=read_var(self,p[3],pos=Position(p,3),package=p[2])
		
	def p_variable_pack_hash(self,p):
		'variable : PERCENTAGE package ID'
		p[0]=read_var(self,p[3],pos=Position(p,3),package=p[2])
		
	def p_variable_variable_new(self,p):
		'variable : variable_my'
		p[0]=p[1]
		
	### Variable my ###
	def p_variable_my_scalar(self,p):
		'variable_my : MY DOLLAR ID'
		p[0]=create_var(self,p[3],Position(p,3))
		
	def p_variable_my_array(self,p):
		'variable_my : MY AT ID'
		p[0]=create_var(self,p[3],Position(p,3))
		
	def p_variable_my_hash(self,p):
		'variable_my : MY PERCENTAGE ID'
		p[0]=create_var(self,p[3],Position(p,3))
		
	def p_variable_our_scalar(self,p):
		'variable_my : OUR DOLLAR ID'
		p[0]=create_var(self,p[3],Position(p,3),shared=True)
		
	def p_variable_our_array(self,p):
		'variable_my : OUR AT ID'
		p[0]=create_var(self,p[3],Position(p,3),shared=True)
		
	def p_variable_our_hash(self,p):
		'variable_my : OUR PERCENTAGE ID'
		p[0]=create_var(self,p[3],Position(p,3),shared=True)
		
	### Value ###		
	def p_value_int(self,p):
		'value : INT_NUMBER'
		p[0]=Code(value=p[1],type=[INTEGER],pos=Position(p,1))
		
	def p_value_float(self,p):	
		'value : FLOAT_NUMBER'
		p[0]=Code(value=p[1],type=[DOUBLE],pos=Position(p,1))
		
	def p_value_string_quote(self,p):	
		'value : STRING_QUOTE'
		p[0]=Code(value='"'+p[1]+'"',type=[STRING],pos=Position(p,1))
		
	def p_value_string_double_quote(self,p):	
		'value : STRING_DOUBLE_QUOTE'
		p[0]=Code(value='"'+p[1]+'"',type=[STRING],pos=Position(p,1))
		
	def p_value_cmd(self,p):	
		'value : CMD'
		p[0]=value_cmd(self,p[1],Position(p,1))
		
		
		
		
#