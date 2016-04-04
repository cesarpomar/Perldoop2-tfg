#!/usr/bin/python
# -*- coding: utf-8 -*-
from libs.Auxiliary import check_code,readToEqual
from libs.Casting import to_long,to_string,to_integer,to_double,to_boolean,to_type,to_floor,to_number,equals_type
from libs.Datatypes import BOOLEAN,INTEGER,FLOAT,LONG,DOUBLE,STRING,ARRAY,HASH,LIST,type_order,Code,STATEMENT,\
    REF, FILE
from libs.Messages import error
from libs.Variables import is_assign
from libs.Collection import create_value_var
from libs.Statements import equals
    

#Para suma, resta y multiplicacion
def op_basic(parser,op,exp1,exp2):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)
    #Componemos transformando los operandos si hace falta
    code.value=to_number(exp1)+' '+op+' '+to_number(exp2)
    #Calculamos el tipo, cogiendo el mas amplio
    if type_order[exp1.type[0]] > type_order[exp2.type[0]]:
        code.type=exp1.type
    else:
        code.type=exp2.type    
    return code

def op_divide(parser,op,exp1,exp2):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)
    #Transformamos los operando en numeros
    to_number(exp1)
    to_number(exp2)     
    #Calculamos el tipo, cogiendo el mas amplio
    if type_order[exp1.type[0]] > type_order[exp2.type[0]]:
        code.type=exp1.type
    else:
        code.type=exp2.type  
    #Obligamos a java a realizar siempre la division flotante
    if type_order[code.type[0]]<type_order[FLOAT]:
        code.type=[FLOAT]
        #Transformamos el segundo a flotante
        exp2.value="(float)"+exp2.value    
    ##Componemos la operacion
    code.value=exp1.value+' / '+exp2.value 
    return code
    
def op_pow(parser,op,exp1,exp2):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)
    #La operacion en java es de tipo double
    code.type=[DOUBLE]
    code.value='Math.pow('+to_number(exp1)+','+to_number(exp2)+')'
    return code

def op_mod(parser,op,exp1,exp2):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)
    #Transformamos los operando en numeros
    to_number(exp1)
    to_number(exp2)
    #Forzamos ambos sean enteros
    if type_order[exp1.type[0]] > type_order[LONG]:
        exp1.type=[LONG]
        exp1.value=to_long(exp1)
    if type_order[exp2.type[0]] > type_order[LONG]:
        exp2.type=[LONG]
        exp2.value=to_long(exp2)
    #El tipo depende del primer operador
    code.type=exp1.type 
    #Componemos la operacion
    code.value=exp1.value+' % '+exp2.value    
    return code

def op_period(parser,op,exp1,exp2):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)
    #Perl ya obliga a que el primer operador sea string y el resto al igual que en java no importa
    code.type=[STRING]
    code.value=exp1.value+' + '+exp2.value
    return code

def op_repeat(parser,op,exp1,exp2):
    code=exp1+exp2  
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)
    code.type=[STRING] 
    #Se repite una cadena un numero entero de veces
    code.value='Pd.repeat('+to_string(exp1)+', '+to_integer(exp2)+')'
    return code 

def op_opposite(parser,exp):
    #Comprobamos la expresion
    check_code(parser,exp)
    #Convertimos la expresion a numero y la negamos
    exp.value="-"+to_number(exp)  
    
def plusplus_var(parser,var,check=True):
    #Reutilizar en codigo sin las comprobaciones
    if check:
        check_code(parser,var.var)
    #El operador no funciona sobre colecciones
    if var.type[0] in (ARRAY,HASH,LIST):
        error(parser,'INC_DEC_COLECTION',var.pos)
        return var.var    
    #Creamos el codigo
    code=var.var+Code()   
    code.type=var.type
    code.declares+=var.declares
    #Empezamos por el valor de lectura
    code.value=var.value+var.read_value+var.end_value
    #Si el tipo es entero, la operacion es directa
    if code.type[0] in (INTEGER,LONG):
        code.value='++'+code.value
    else:
        #Guardamos el tipo de la varaible
        code_type=Code(type=code.type)
        #Comvertimos en numero y sumamos 1
        code.value=to_double(code)+' + 1'
        code.type=[DOUBLE]
        #Devolvemos el codigo a su tipo
        code.value=var.value+var.store_value+to_type(parser, code_type, code)+var.end_value
        code.type=code_type.type
    #La operacion es una sentencia
    code.st_value=code.value
    return code

def minusminus_var(parser,var,check=True):   
    #Reutilizar en codigo sin las comprobaciones
    if check:
        check_code(parser,var.var)
    #El operador no funciona sobre colecciones
    if var.type[0] in (ARRAY,HASH,LIST):
        error(parser,'INC_DEC_COLECTION',var.pos)
        return var.var    
    #Creamos el codigo
    code=var.var+Code()   
    code.type=var.type
    code.declares+=var.declares
    #Empezamos por el valor de lectura
    code.value=var.value+var.read_value+var.end_value
    #Si el tipo es entero, la operacion es directa
    if code.type[0] in (INTEGER,LONG):
        code.value='--'+code.value
    else:
        #Guardamos el tipo de la varaible
        code_type=Code(type=code.type)
        #Comvertimos en numero y sumamos 1
        code.value=to_double(code)+' - 1'
        code.type=[DOUBLE]
        #Devolvemos el codigo a su tipo
        code.value=var.value+var.store_value+to_type(parser, code_type, code)+var.end_value
        code.type=code_type.type
    #La operacion es una sentencia
    code.st_value=code.value
    return code

def var_plusplus(parser,var): 
    check_code(parser,var.var)
    #El operador no funciona sobre colecciones
    if var.type[0] in (ARRAY,HASH,LIST):
        error(parser,'INC_DEC_COLECTION',var.pos)
        return var    
    #Creamos el codigo
    code=var.var+Code()   
    code.type=var.type
    code.declares+=var.declares
    #Empezamos por el valor de lectura
    code.value=var.value+var.read_value+var.end_value
    #Si el tipo es entero, la operacion es directa
    if code.type[0] in (INTEGER,LONG):
        code.value=code.value+'++'
        code.st_value=code.value       
    else:
        #La primera parte es como el otro incremento
        code.value=plusplus_var(parser,var).value    
        code.st_value=code.value        
        #Guardamos el tipo de la varaible
        code_type=Code(type=code.type)
        #Aunque la variable incremente, muestra el valor anterior
        #Comvertimos en numero y restamos 1
        code.value=to_double(code)+' - 1' 
    return code

def var_minusminus(parser,var):
    check_code(parser,var.var)
    #El operador no funciona sobre colecciones
    if var.type[0] in (ARRAY,HASH,LIST):
        error(parser,'INC_DEC_COLECTION',var.pos)
        return var    
    #Creamos el codigo
    code=var.var+Code()   
    code.type=var.type
    code.declares+=var.declares
    #Empezamos por el valor de lectura
    code.value=var.value+var.read_value+var.end_value
    #Si el tipo es entero, la operacion es directa
    if code.type[0] in (INTEGER,LONG):
        code.value=code.value+'--'
        code.st_value=code.value       
    else:
        #La primera parte es como el otro incremento
        code.value=plusplus_var(parser,var).value    
        code.st_value=code.value        
        #Guardamos el tipo de la varaible
        code_type=Code(type=code.type)
        #Aunque la variable incremente, muestra el valor anterior
        #Comvertimos en numero y restamos 1
        code.value=to_double(code)+' + 1'
        code.type=[DOUBLE]    
    return code

def num_compare(parser,op,num1,num2):
    code=num1+num2
    #Comprobamos las expresiones
    check_code(parser,num1)
    check_code(parser,num2)
    #Transformamos los operando en numeros y componemos la expresion
    code.value=to_number(num1)+' '+op+' '+to_number(num2)
    code.value_opt=code.value
    #La funcion es Booleana
    code.type=[BOOLEAN]
    return code

def cmp_num(parser,num1,num2):
    code=num1+num2
    #Comprobamos las expresiones
    check_code(parser,num1)
    check_code(parser,num2)
    #Transformamos los operando en numeros y componemos la expresion
    code.value='Pd.cmp('+to_number(num1)+', '+to_number(num2)+')'
    #La funcion es Entera
    code.type=[INTEGER]
    return code

def cmp_string(parser,str1,str2,compare):
    code=str1+str2
    #Comprobamos las expresiones
    check_code(parser,str1)
    check_code(parser,str2)   
    #Componemos la expresion 
    code.value='Pd.cmp('+to_string(str1)+', '+to_string(str2)+') '+compare+' '
    code.value_opt=code.value
    code.type=[INTEGER]
    return code

def string_compare(parser,str1,str2,compare):
    code=str1+str2
    #Comprobamos las expresiones
    check_code(parser,str1)
    check_code(parser,str2)   
    #Componemos la expresion 
    code.value=to_string(str1)+'.compareTo('+to_string(str2)+') '+compare+' '
    code.value_opt=code.value
    code.type=[BOOLEAN]
    return code

def m_regex(parser,exp,regex,pos,negate=False):
    code=exp+Code(pos=pos)
    #Comprobamos la expresion
    check_code(parser,exp)
    #Componemos la operacion
    code.value='Regex.match('+to_string(exp)+', "'+regex+'")'
    if negate:
        code.value='!'+code.value
    #El tipo de la operacion es Booleano
    code.type=[BOOLEAN]
    code.value_opt=code.value
    return code

def s_regex(parser,var,regex,pos):
    code=var+Code(pos=pos,flags={STATEMENT:True})
    #Comprobamos la expresion
    check_code(parser,var)
    #Tiene que ser una variable
    if not var.variable:
        error(parser,'VAR_REQUIRES',var.pos)
    #No puede ser una coleccion
    if len(var.type)>1:
        error(parser,'SCALAR_REQUIRES',var.pos) 
    value=Code(value='Regex.s('+to_string(var)+', "'+regex+'")',type=[STRING])    
    code.value=readToEqual(var,to_type(parser, var, value))
    return code

def y_regex(parser,var,regex,pos):
    code=var+Code(pos=pos,flags={STATEMENT:True})
    #Comprobamos la expresion
    check_code(parser,var)
    #Tiene que ser una variable
    if not var.variable:
        error(parser,'VAR_REQUIRES',var.pos)
    #No puede ser una coleccion
    if len(var.type)>1:
        error(parser,'SCALAR_REQUIRES',var.pos) 
    value=Code(value='Regex.tr('+to_string(var)+',v"'+regex+'")',type=[STRING])    
    code.value=readToEqual(var,to_type(parser, var, value))
    return code

def smart_compare(parser,exp1,exp2,opPos):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)   
    #Operador no soportado
    error(parser, 'SMART_EQ', opPos)
    return Code()

def binary_op(parser,op,exp1,exp2):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)
    #Componemos la operacion
    code.value=to_floor(exp1)+' '+op+' '+to_floor(exp2)
    code.type=exp1.type
    return code

def binary_not(parser,exp):
    #Comprobamos la expresion
    check_code(parser,exp)
    #Componemos la operacion
    exp.value='~'+to_floor(exp)
    return exp

def logic_or(parser,op,exp1,exp2,low=False):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)
    #Si el operador es de baja precedencia, a�adimos parentesis a sus expresiones  
    if low:
        b_value='('+to_boolean(exp1)+') || ('++to_boolean(exp2)+')'
    else:
        b_value=to_boolean(exp1)+' || '+to_boolean(exp2)    
    #Si los operandos dos operandos booleanos o no son del mismo tipo
    if (exp1.type[0]==BOOLEAN and exp2.type[0]==BOOLEAN) or not equals_type(exp1.type,exp2.type):
        #El codigo es booleano
        code.value=b_value
        code.type=[BOOLEAN]   
    else:
        #El tipo es el mismo de los datos
        code.type=exp1.type 
        code.value='Pd.or('+exp1.value+', '+exp2.value+')'
        #El booleano se guarda como secundario
        code.value_opt=b_value
    return code

def logic_and(parser,op,exp1,exp2,low=False):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)
    #Si el operador es de baja precedencia, a�adimos parentesis a sus expresiones  
    if low:
        b_value='('+to_boolean(exp1)+') && ('++to_boolean(exp2)+')'
    else:
        b_value=to_boolean(exp1)+' && '+to_boolean(exp2)    
    #Si los operandos dos operandos booleanos o no son del mismo tipo
    if (exp1.type[0]==BOOLEAN and exp2.type[0]==BOOLEAN) or not equals_type(exp1.type,exp2.type):
        #El codigo es booleano
        code.value=b_value
        code.type=[BOOLEAN]   
    else:
        #El tipo es el mismo de los datos
        code.type=exp1.type 
        code.value='Pd.and('+exp1.value+', '+exp2.value+')'
        #El booleano se guarda como secundario
        code.value_opt=b_value
    return code

def logic_not(parser,exp,low=False):
    #Comprobamos la expresion
    check_code(parser,exp)
    #Si el operador es de baja precedencia, a�adimos parentesis a sus expresiones  
    if low:    
        b_value='!('+to_boolean(exp)+')'
    else:
        b_value='!'+to_boolean(exp)
    #Si el valor es booleano el codigo es boobleano   
    if exp.type[0]==BOOLEAN:    
        exp.value=b_value
        exp.value_opt=exp.value
        exp.type=[BOOLEAN]
    #En caso contrario el valor es Entero
    else:
        exp.value='('+to_boolean(exp)+')?0:1'
        exp.value_opt=b_value 
        exp.type=[INTEGER]
    return exp    

def logic_xor(parser,op,exp1,exp2):
    code=exp1+exp2
    #Comprobamos las expresiones
    check_code(parser,exp1)
    check_code(parser,exp2)    
    #Componemos la operacion
    code.st_value='Pd.xor('+to_boolean(exp1)+', '+to_boolean(exp2)+')'
    #Si se vuelve a usar tiene que tener su tipo correcto
    code.value='('+code.st_value+')?0:1'
    #El Tipo de la funcion es Entero
    code.type=[INTEGER]
    if exp1.st_value or exp2.st_value:
        code.st_value=code.value
    return code   

def condicional_equals(parser,cond,exp1,exp2):
    code=exp1+exp2+cond
    #Comprobamos las expresiones
    check_code(parser,cond)
    check_code(parser,exp1)
    check_code(parser,exp2)   
    #Componemos la operacion
    code.value='('+to_boolean(cond)+')?'+exp1.value+':'
    #Si no tienen el mismo tipo, casteamos el segundo
    if equals_type(exp1.type,exp2.type):
        code.value+=exp2.value
    else:
        code.value+=to_type(parser, exp1, exp2)
    #El tipo es el del primer operador
    code.type=exp1.type
    return code

def check_op_equals(parser,var):
    #Si la parte izquierda no es una variable
    if not var.var.variable:
        error(parser,'VAR_REQUIRES',var.pos)  
    elif not is_assign(parser,var.var.variable.name):
        error(parser, 'READ_BEFORE_ASSIGN', var.pos,var=var.var.value)
    elif var.type[0]==REF:
        error(parser,'REF_OPERATION',var.pos) 
    elif len(var.type)>1 or var.type[0]==FILE:
        error(parser,'SCALAR_REQUIRES',var.pos,var=var.var.value) 
    else:
        return True
 
#Realiza la operacion de asignacion de forma nativa o cambianando ambas funciones
def op_equals(parser,var,exp,op,opf,ntypes=[],types=[],native=True): 
    #Comprobamos la expresion
    check_code(parser,exp)
    #Si no es posible abortamos
    if not check_op_equals(parser,var):
        return Code(type=[None])
    #Comprobamos la traduccion nativa
    if (native and (len(var.var.type) == 1 or (len(var.var.type)>1 and var.var.type[-2] == ARRAY)) 
        and (var.type[0] not in ntypes or var.type[0] in types)):
        #Creamos la variable
        var=create_value_var(var)
        #Creamos el codigo
        code=var+exp
        code.value=var.value+' '+op+' '+to_type(parser, var, exp)
        code.st_value=code.value
        return code
    #Si no se realiza uniendo la funcion con la operacion igual
    else:
        return equals(parser, var, opf(parser,op[1], Code(type=var.type,value=var.value+var.read_value+var.end_value), exp))
 