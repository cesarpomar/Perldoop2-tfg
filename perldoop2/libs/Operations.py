#!/usr/bin/python
# -*- coding: utf-8 -*-
from libs import Auxiliary as Aux
from libs import Casting as Cst
from libs import DataType as Dtp
from libs import Messages as Msg
from libs import Variables as Var
from libs import Collection as Coll
from libs import Statements as Sts  
from libs import Code

class Operations:
    
    # Para suma, resta y multiplicacion
    @classmethod
    def op_basic(Ops, parser, op, exp1, exp2):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        # Componemos transformando los operandos si hace falta
        code.value = Cst.to_number(exp1) + ' ' + op + ' ' + Cst.to_number(exp2)
        # Calculamos el tipo, cogiendo el mas amplio
        if Dtp.type_order[exp1.type[0]] > Dtp.type_order[exp2.type[0]]:
            code.type = exp1.type
        else:
            code.type = exp2.type    
        return code
    
    @classmethod
    def op_divide(Ops, parser, op, exp1, exp2):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        # Transformamos los operando en numeros
        Cst.to_number(exp1)
        Cst.to_number(exp2)     
        # Calculamos el tipo, cogiendo el mas amplio
        if Dtp.type_order[exp1.type[0]] > Dtp.type_order[exp2.type[0]]:
            code.type = exp1.type
        else:
            code.type = exp2.type  
        # Obligamos a java a realizar siempre la division flotante
        if Dtp.type_order[code.type[0]] < Dtp.type_order[Dtp.FLOAT]:
            code.type = [Dtp.FLOAT]
            # Transformamos el segundo a flotante
            exp2.value = "(float)" + exp2.value    
        # #Componemos la operacion
        code.value = exp1.value + ' / ' + exp2.value 
        return code
        
    @classmethod    
    def op_pow(Ops, parser, op, exp1, exp2):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        # La operacion en java es de tipo double
        code.type = [Dtp.DOUBLE]
        code.value = 'Math.pow(' + Cst.to_number(exp1) + ',' + Cst.to_number(exp2) + ')'
        return code
    
    @classmethod
    def op_mod(Ops, parser, op, exp1, exp2):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        # Transformamos los operando en numeros
        Cst.to_number(exp1)
        Cst.to_number(exp2)
        # Forzamos ambos sean enteros
        if Dtp.type_order[exp1.type[0]] > Dtp.type_order[Dtp.LONG]:
            exp1.type = [Dtp.LONG]
            exp1.value = Cst.to_long(exp1)
        if Dtp.type_order[exp2.type[0]] > Dtp.type_order[Dtp.LONG]:
            exp2.type = [Dtp.LONG]
            exp2.value = Cst.to_long(exp2)
        # El tipo depende del primer operador
        code.type = exp1.type 
        # Componemos la operacion
        code.value = exp1.value + ' % ' + exp2.value    
        return code
    
    @classmethod
    def op_period(Ops, parser, op, exp1, exp2):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        # Perl ya obliga a que el primer operador sea string y el resto al igual que en java no importa
        code.type = [Dtp.STRING]
        code.value = exp1.value + ' + ' + exp2.value
        return code
    
    @classmethod
    def op_repeat(Ops, parser, op, exp1, exp2):
        code = exp1 + exp2  
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        code.type = [Dtp.STRING] 
        # Se repite una cadena un numero entero de veces
        code.value = 'Pd.repeat(' + Cst.to_string(exp1) + ', ' + Cst.to_integer(exp2) + ')'
        return code 
    
    @classmethod
    def op_opposite(Ops, parser, exp):
        # Comprobamos la expresion
        Aux.check_code(parser, exp)
        # Convertimos la expresion a numero y la negamos
        exp.value = "-" + Cst.to_number(exp)  
    
    @classmethod    
    def plusplus_var(Ops, parser, var, check=True):
        # Reutilizar en codigo sin las comprobaciones
        if check:
            Aux.check_code(parser, var.var)
        # El operador no funciona sobre colecciones
        if var.type[0] in (Dtp.ARRAY, Dtp.HASH, Dtp.LIST):
            Msg.error(parser, 'INC_DEC_COLECTION', var.pos)
            return var.var    
        # Creamos el codigo
        code = var.var + Code()   
        code.type = var.type
        code.declares += var.declares
        # Empezamos por el valor de lectura
        code.value = var.value + var.read_value + var.end_value
        # Si el tipo es entero, la operacion es directa
        if code.type[0] in (Dtp.INTEGER, Dtp.LONG):
            code.value = '++' + code.value
        else:
            # Guardamos el tipo de la varaible
            code_type = Code(type=code.type)
            # Comvertimos en numero y sumamos 1
            code.value = Cst.to_double(code) + ' + 1'
            code.type = [Dtp.DOUBLE]
            # Devolvemos el codigo a su tipo
            code.value = var.value + var.store_value + Cst.to_type(parser, code_type, code) + var.end_value
            code.type = code_type.type
        # La operacion es una sentencia
        code.st_value = code.value
        return code
    
    @classmethod
    def minusminus_var(Ops, parser, var, check=True):   
        # Reutilizar en codigo sin las comprobaciones
        if check:
            Aux.check_code(parser, var.var)
        # El operador no funciona sobre colecciones
        if var.type[0] in (Dtp.ARRAY, Dtp.HASH, Dtp.LIST):
            Msg.error(parser, 'INC_DEC_COLECTION', var.pos)
            return var.var    
        # Creamos el codigo
        code = var.var + Code()   
        code.type = var.type
        code.declares += var.declares
        # Empezamos por el valor de lectura
        code.value = var.value + var.read_value + var.end_value
        # Si el tipo es entero, la operacion es directa
        if code.type[0] in (Dtp.INTEGER, Dtp.LONG):
            code.value = '--' + code.value
        else:
            # Guardamos el tipo de la varaible
            code_type = Code(type=code.type)
            # Comvertimos en numero y sumamos 1
            code.value = Cst.to_double(code) + ' - 1'
            code.type = [Dtp.DOUBLE]
            # Devolvemos el codigo a su tipo
            code.value = var.value + var.store_value + Cst.to_type(parser, code_type, code) + var.end_value
            code.type = code_type.type
        # La operacion es una sentencia
        code.st_value = code.value
        return code
    
    @classmethod
    def var_plusplus(Ops, parser, var): 
        Aux.check_code(parser, var.var)
        # El operador no funciona sobre colecciones
        if var.type[0] in (Dtp.ARRAY, Dtp.HASH, Dtp.LIST):
            Msg.error(parser, 'INC_DEC_COLECTION', var.pos)
            return var    
        # Creamos el codigo
        code = var.var + Code()   
        code.type = var.type
        code.declares += var.declares
        # Empezamos por el valor de lectura
        code.value = var.value + var.read_value + var.end_value
        # Si el tipo es entero, la operacion es directa
        if code.type[0] in (Dtp.INTEGER, Dtp.LONG):
            code.value = code.value + '++'
            code.st_value = code.value       
        else:
            # La primera parte es como el otro incremento
            code.value = Ops.plusplus_var(parser, var).value    
            code.st_value = code.value        
            # Guardamos el tipo de la varaible
            code_type = Code(type=code.type)
            # Aunque la variable incremente, muestra el valor anterior
            # Comvertimos en numero y restamos 1
            code.value = Cst.to_double(code) + ' - 1' 
        return code
    
    @classmethod
    def var_minusminus(Ops, parser, var):
        Aux.check_code(parser, var.var)
        # El operador no funciona sobre colecciones
        if var.type[0] in (Dtp.ARRAY, Dtp.HASH, Dtp.LIST):
            Msg.error(parser, 'INC_DEC_COLECTION', var.pos)
            return var    
        # Creamos el codigo
        code = var.var + Code()   
        code.type = var.type
        code.declares += var.declares
        # Empezamos por el valor de lectura
        code.value = var.value + var.read_value + var.end_value
        # Si el tipo es entero, la operacion es directa
        if code.type[0] in (Dtp.INTEGER, Dtp.LONG):
            code.value = code.value + '--'
            code.st_value = code.value       
        else:
            # La primera parte es como el otro incremento
            code.value = Ops.plusplus_var(parser, var).value    
            code.st_value = code.value        
            # Guardamos el tipo de la varaible
            code_type = Code(type=code.type)
            # Aunque la variable incremente, muestra el valor anterior
            # Comvertimos en numero y restamos 1
            code.value = Cst.to_double(code) + ' + 1'
            code.type = [Dtp.DOUBLE]    
        return code
    
    @classmethod
    def num_compare(Ops, parser, op, num1, num2):
        code = num1 + num2
        # Comprobamos las expresiones
        Aux.check_code(parser, num1)
        Aux.check_code(parser, num2)
        # Transformamos los operando en numeros y componemos la expresion
        code.value = Cst.to_number(num1) + ' ' + op + ' ' + Cst.to_number(num2)
        code.value_opt = code.value
        # La funcion es Booleana
        code.type = [Dtp.BOOLEAN]
        return code
    
    @classmethod
    def cmp_num(Ops, parser, num1, num2):
        code = num1 + num2
        # Comprobamos las expresiones
        Aux.check_code(parser, num1)
        Aux.check_code(parser, num2)
        # Transformamos los operando en numeros y componemos la expresion
        code.value = 'Pd.cmp(' + Cst.to_number(num1) + ', ' + Cst.to_number(num2) + ')'
        # La funcion es Entera
        code.type = [Dtp.INTEGER]
        return code
    
    @classmethod
    def cmp_string(Ops, parser, str1, str2, compare):
        code = str1 + str2
        # Comprobamos las expresiones
        Aux.check_code(parser, str1)
        Aux.check_code(parser, str2)   
        # Componemos la expresion 
        code.value = 'Pd.cmp(' + Cst.to_string(str1) + ', ' + Cst.to_string(str2) + ') ' + compare + ' '
        code.value_opt = code.value
        code.type = [Dtp.INTEGER]
        return code
    
    @classmethod
    def string_compare(Ops, parser, str1, str2, compare):
        code = str1 + str2
        # Comprobamos las expresiones
        Aux.check_code(parser, str1)
        Aux.check_code(parser, str2)   
        # Componemos la expresion 
        code.value = Cst.to_string(str1) + '.compareTo(' + Cst.to_string(str2) + ') ' + compare + ' '
        code.value_opt = code.value
        code.type = [Dtp.BOOLEAN]
        return code
    
    @classmethod
    def m_regex(Ops, parser, exp, regex, pos, negate=False):
        code = exp + Code(pos=pos)
        # Comprobamos la expresion
        Aux.check_code(parser, exp)
        # Componemos la operacion
        code.value = 'Regex.match(' + Cst.to_string(exp) + ', "' + regex + '")'
        if negate:
            code.value = '!' + code.value
        # El tipo de la operacion es Booleano
        code.type = [Dtp.BOOLEAN]
        code.value_opt = code.value
        return code
    
    @classmethod
    def s_regex(Ops, parser, var, regex, pos):
        code = var + Code(pos=pos, flags={Dtp.STATEMENT:True})
        # Comprobamos la expresion
        Aux.check_code(parser, var)
        # Tiene que ser una variable
        if not var.variable:
            Msg.error(parser, 'VAR_REQUIRES', var.pos)
        # No puede ser una coleccion
        if len(var.type) > 1:
            Msg.error(parser, 'SCALAR_REQUIRES', var.pos) 
        value = Code(value='Regex.s(' + Cst.to_string(var) + ', "' + regex + '")', type=[Dtp.STRING])    
        code.value = Aux.readToEqual(var, Cst.to_type(parser, var, value))
        return code
    
    @classmethod
    def y_regex(Ops, parser, var, regex, pos):
        code = var + Code(pos=pos, flags={Dtp.STATEMENT:True})
        # Comprobamos la expresion
        Aux.check_code(parser, var)
        # Tiene que ser una variable
        if not var.variable:
            Msg.error(parser, 'VAR_REQUIRES', var.pos)
        # No puede ser una coleccion
        if len(var.type) > 1:
            Msg.error(parser, 'SCALAR_REQUIRES', var.pos) 
        value = Code(value='Regex.tr(' + Cst.to_string(var) + ',v"' + regex + '")', type=[Dtp.STRING])    
        code.value = Aux.readToEqual(var, Cst.to_type(parser, var, value))
        return code
    
    @classmethod
    def smart_compare(Ops, parser, exp1, exp2, opPos):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)   
        # Operador no soportado
        Msg.error(parser, 'SMART_EQ', opPos)
        return Code()
    
    @classmethod
    def binary_op(Ops, parser, op, exp1, exp2):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        # Componemos la operacion
        code.value = Cst.to_floor(exp1) + ' ' + op + ' ' + Cst.to_floor(exp2)
        code.type = exp1.type
        return code
    
    @classmethod
    def binary_not(Ops, parser, exp):
        # Comprobamos la expresion
        Aux.check_code(parser, exp)
        # Componemos la operacion
        exp.value = '~' + Cst.to_floor(exp)
        return exp
    
    @classmethod
    def logic_or(Ops, parser, op, exp1, exp2, low=False):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        # Si el operador es de baja precedencia, a�adimos parentesis a sus expresiones  
        if low:
            b_value = '(' + Cst.to_boolean(exp1) + ') || (' + +Cst.to_boolean(exp2) + ')'
        else:
            b_value = Cst.to_boolean(exp1) + ' || ' + Cst.to_boolean(exp2)    
        # Si los operandos dos operandos booleanos o no son del mismo tipo
        if (exp1.type[0] == Dtp.BOOLEAN and exp2.type[0] == Dtp.BOOLEAN) or not Cst.equals_type(exp1.type, exp2.type):
            # El codigo es booleano
            code.value = b_value
            code.type = [Dtp.BOOLEAN]   
        else:
            # El tipo es el mismo de los datos
            code.type = exp1.type 
            code.value = 'Pd.or(' + exp1.value + ', ' + exp2.value + ')'
            # El booleano se guarda como secundario
            code.value_opt = b_value
        return code
    
    @classmethod
    def logic_and(Ops, parser, op, exp1, exp2, low=False):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        # Si el operador es de baja precedencia, a�adimos parentesis a sus expresiones  
        if low:
            b_value = '(' + Cst.to_boolean(exp1) + ') && (' + +Cst.to_boolean(exp2) + ')'
        else:
            b_value = Cst.to_boolean(exp1) + ' && ' + Cst.to_boolean(exp2)    
        # Si los operandos dos operandos booleanos o no son del mismo tipo
        if (exp1.type[0] == Dtp.BOOLEAN and exp2.type[0] == Dtp.BOOLEAN) or not Cst.equals_type(exp1.type, exp2.type):
            # El codigo es booleano
            code.value = b_value
            code.type = [Dtp.BOOLEAN]   
        else:
            # El tipo es el mismo de los datos
            code.type = exp1.type 
            code.value = 'Pd.and(' + exp1.value + ', ' + exp2.value + ')'
            # El booleano se guarda como secundario
            code.value_opt = b_value
        return code
    
    @classmethod
    def logic_not(Ops, parser, exp, low=False):
        # Comprobamos la expresion
        Aux.check_code(parser, exp)
        # Si el operador es de baja precedencia, a�adimos parentesis a sus expresiones  
        if low:    
            b_value = '!(' + Cst.to_boolean(exp) + ')'
        else:
            b_value = '!' + Cst.to_boolean(exp)
        # Si el valor es booleano el codigo es boobleano   
        if exp.type[0] == Dtp.BOOLEAN:    
            exp.value = b_value
            exp.value_opt = exp.value
            exp.type = [Dtp.BOOLEAN]
        # En caso contrario el valor es Entero
        else:
            exp.value = '(' + Cst.to_boolean(exp) + ')?0:1'
            exp.value_opt = b_value 
            exp.type = [Dtp.INTEGER]
        return exp    
    
    @classmethod
    def logic_xor(parser, op, exp1, exp2):
        code = exp1 + exp2
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)    
        # Componemos la operacion
        code.st_value = 'Pd.xor(' + Cst.to_boolean(exp1) + ', ' + Cst.to_boolean(exp2) + ')'
        # Si se vuelve a usar tiene que tener su tipo correcto
        code.value = '(' + code.st_value + ')?0:1'
        # El Tipo de la funcion es Entero
        code.type = [Dtp.INTEGER]
        if exp1.st_value or exp2.st_value:
            code.st_value = code.value
        return code   
    
    @classmethod
    def condicional_equals(Ops, parser, cond, exp1, exp2):
        code = exp1 + exp2 + cond
        # Comprobamos las expresiones
        Aux.check_code(parser, cond)
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)   
        # Componemos la operacion
        code.value = '(' + Cst.to_boolean(cond) + ')?' + exp1.value + ':'
        # Si no tienen el mismo tipo, casteamos el segundo
        if Cst.equals_type(exp1.type, exp2.type):
            code.value += exp2.value
        else:
            code.value += Cst.to_type(parser, exp1, exp2)
        # El tipo es el del primer operador
        code.type = exp1.type
        return code
    
    @classmethod
    def check_op_equals(Ops, parser, var):
        # Si la parte izquierda no es una variable
        if not var.var.variable:
            Msg.error(parser, 'VAR_REQUIRES', var.pos)  
        elif not Var.is_assign(parser, var.var.variable.name):
            Msg.error(parser, 'READ_BEFORE_ASSIGN', var.pos, var=var.var.value)
        elif var.type[0] == Dtp.REF:
            Msg.error(parser, 'REF_OPERATION', var.pos) 
        elif len(var.type) > 1 or var.type[0] == Dtp.FILE:
            Msg.error(parser, 'SCALAR_REQUIRES', var.pos, var=var.var.value) 
        else:
            return True
     
    # Realiza la operacion de asignacion de forma nativa o cambianando ambas funciones
    @classmethod
    def op_equals(Ops, parser, var, exp, op, opf, ntypes=[], types=[], native=True): 
        # Comprobamos la expresion
        Aux.check_code(parser, exp)
        # Si no es posible abortamos
        if not Ops.check_op_equals(parser, var):
            return Code(type=[None])
        # Comprobamos la traduccion nativa
        if (native and (len(var.var.type) == 1 or (len(var.var.type) > 1 and var.var.type[-2] == Dtp.ARRAY)) 
            and (var.type[0] not in ntypes or var.type[0] in types)):
            # Creamos la variable
            var = Coll.create_value_var(var)
            # Creamos el codigo
            code = var + exp
            code.value = var.value + ' ' + op + ' ' + Cst.to_type(parser, var, exp)
            code.st_value = code.value
            return code
        # Si no se realiza uniendo la funcion con la operacion igual
        else:
            return Sts.equals(parser, var, opf(parser, op[1], Code(type=var.type, value=var.value + var.read_value + var.end_value), exp))
     
