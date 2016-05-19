#!/usr/bin/python
# -*- coding: utf-8 -*-

from libs import Messages as Msg
from libs import Casting as Cst
from libs import Auxiliary as Aux
from libs import DataType as Dtp
from libs import Variables as Var
from libs import Code
from libs import Access
from libs import Type 

class Collection:    
       
    # Acceder a una coleccion
    @classmethod
    def access_colection(Coll, parser, var, key, pos, type, ref=False):
        # Comprobamos la clave
        Aux.check_code(parser, key)
        # Si no es una variable no lo permitimos
        if not var.var.variable:
            Msg.error(parser, 'DECLARE_ACCESS', pos)
            return var
        # Si la variable no ha sido asgianda
        if not Var.is_assign(parser, var.var.variable.name):
            Msg.error(parser, 'READ_BEFORE_ASSIGN', pos, var=var.var.value)
            # Evitar que se replique el error    
            var.var.variable.assign = True
        # Si el acceso es de tipo referencia
        if ref:
            # tamaño del tipo
            tl = len(var.type)
            # Primero accedemos a la referencia
            var = Coll.access_pointed(parser, var, pos)
            # Si tiene el mismo tipo, ya dio error al acceder y abortamos
            if tl == len(var.type):
                return var;   
        # Actualizamos la posicion
        var.pos = pos;
        # Copiamos las declaraciones
        var.declares += key.declares 
        # Cogemos el tipo a acceder
        type_check = var.type[0]
        # Si es una lista, lo cambiamos por array para simplificar
        if type_check == Dtp.LIST:
            type_check = Dtp.ARRAY
        # Si el tipo no coincide con el acceso
        if type != type_check:
            Msg.error(parser, 'VAR_ERROR_ACCESS', pos, type=type, find=str(var.type[0]))
            return var
        # Unimos el valor del acceso para lectura
        var.value += var.read_value + var.end_value
        # Si tenemos optimizacion
        if parser.optimize_code:
            # Eliminamos los accesos contrarios
            var.value = Aux.opt_get(var.value)
        # Para un array
        if var.type[0] == Dtp.ARRAY:
            var.read_value = ''
            var.store_value = ' = '
            var.end_value = ''
            var.value += '[' + Cst.to_integer(key) + ']'
        # Para una lista
        elif var.type[0] == Dtp.LIST:
            var.read_value = '.get(' + key.value
            var.store_value = '.set(' + Cst.to_integer(key) + ','
            var.end_value = ')'    
        # Para un hash        
        elif var.type[0] == Dtp.HASH:
            var.read_value = '.get(' + Cst.to_string(key)
            var.store_value = '.put(' + Cst.to_string(key) + ','
            var.end_value = ')'
        # Quitamos la dimension accedida
        var.type = var.type[1:]
        var.ref = True
        return var
    
    # Accede a un puntero
    @classmethod
    def access_pointed(Coll, parser, var, pos):
        # Actualizamos la posicion
        var.pos = pos;
        # Si no es una referencia damos error
        if var.type[0] != Dtp.REF and not var.ref:
            Msg.error(parser, 'VAR_ERROR_ACCESS', pos, type=Dtp.REF, find=str(var.type[0]))
            return var    
        if var.type[0] == Dtp.REF:
            # Unimos el valor del acceso para lectura
            var.value += var.read_value + var.end_value
            # Podemos los valores de acceso
            var.read_value = '.get('
            var.store_value = '.set('
            var.end_value = ')'
            # Quitamos la referencia del tipo
            var.type = var.type[1:]
        var.ref = False
        return var
        
    # Crea una expresion como puntero a variable 
    @classmethod   
    def create_pointer_var(Coll, parser, var):
        # Solo punteros a colecciones
        if not var.var.variable or var.type[0] not in (Dtp.ARRAY, Dtp.HASH, Dtp.LIST):
            Msg.error(parser, 'VAR_REF_SCAlAR', var.pos)
        # Unimos el valor del acceso para lectura
        var.value += var.read_value + var.end_value
        # Creamos la clase referencia
        var.value = 'new Ref<' + Cst.create_type(var.type) + '>(' + var.value + ')'
        var.read_value = ''
        var.store_value = ''
        var.end_value = ''
        # Añadimos la referencia al tipo
        var.type = [Dtp.REF, ] + var.type
    	# Si es una coleccion deberia ser referenciada
        var.ref = var.type[0] in (Dtp.ARRAY, Dtp.HASH, Dtp.LIST)
        return var
    
    # Crea una expresion con el valor de una variable
    @classmethod
    def create_value_var(Coll, var):
        # Cogemos la varaible
        code = var.var
        code.ref = var.ref
        # Copiamos el tipo despues de los accesos
        code.type = var.type
        # Actualizamos la posicion con los acceos
        code.pos = var.pos
        # Actualizamos el valor con un acceso de lectura
        code.value = var.value + var.read_value + var.end_value
        # Cogemos las declaraciones de los accesos
        code.declares += var.declares
        return code
    
    # Crea un array basado en una lista de elementos
    @classmethod
    def create_array_value(Coll, parser, list):
        # El tipo del array es el del primer elemento
        if len(list[0].type) == 1:
            # Si es un escalar cogemos su tipo
            c_type = list[0].type   
            scalar = True
        # Si es una referencia 
        elif list[0].type[0] == Dtp.REF:
            # Si la referencia es a un escalar
            if len(list[0].type) == 2:
                # cogemos su tipo
                c_type = list[0].type 
                scalar = True
            else:
                # Si es una coleccion eliminamos la referencia
                c_type = list[0].type[1:]
                scalar = False
        else:
            # En ultimo caso, cogemos lo que sea y luego daremos un error
            c_type = list[0].type  
            scalar = True
        # Creamos el codigo del array
        code = Code(type=[Dtp.REF, Dtp.ARRAY] + c_type)
        # Creamos la inicializacion
        code.value = Cst.creare_inicialize(code.type[1:], []) + '{'
        for exp in list:
            # Comprobamos el codigo y añadimos las declaraciones
            code.declares += exp.declares
            Aux.check_code(parser, exp, c_ref=False)
            # Si un valor es una sentencia, el array lo sera
            if Dtp.STATEMENT in exp.flags:
                code.flags[Dtp.STATEMENT] = True
            # Si no es un array de scalar, primero eliminamos las referencias
            if not scalar:
                # Tiene que ser una referencia
                if exp.type[0] == Dtp.REF:
                    # Accedemos a la referencia
                    access = Coll.access_pointed(parser, Access(exp), exp.pos)
                    exp.value = access.value + access.read_value + access.end_value 
                    if parser.optimize_code:
                        exp.value = Aux.opt_get(exp.value) 
                    # Cogemos el tipo accedido
                    exp.type = access.type  
                else:
                    Msg.error(parser, 'VAR_REF_REQUIRES', exp.pos, var=exp.value)
            # Añadimos la expresion casteada al tipo del array   
            code.value += Cst.to_type(parser, Code(type=c_type), exp) + ',' 
        # Quitamos la ultima coma y cerramos la llava            
        code.value = code.value[:-1] + '}'  
        # Transformamos el codigo en referencia
        code.value = 'new Ref<>(' + code.value + ')'    
        return code  
    
    @classmethod
    def create_hash_value(Coll, parser, list):
        # Si el numero de elementos no es par una clave no tiene valor
        if len(list) % 2 != 0:
            Msg.error(parser, 'HASH_NOT_VALUE', list[-1].pos)
            return Code(type=[Dtp.NONE])
        # El tipo del hash es el de la primera clave
        if len(list[1].type) == 1:
            # Si es un escalar cogemos su tipo
            c_type = list[1].type   
            scalar = True
        # Si es una referencia 
        elif list[1].type[0] == Dtp.REF:
            # Si la referencia es a un escalar
            if len(list[1].type) == 2:
                # cogemos su tipo
                c_type = list[1].type 
                scalar = True
            else:
                # Si es una coleccion eliminamos la referencia
                c_type = list[1].type[1:]
                scalar = False
        else:
            # En ultimo caso, cogemos lo que sea y luego daremos un error
            c_type = list[1].type  
            scalar = True    
        # Creamos el codigo del hash
        code = Code(type=[Dtp.REF, Dtp.HASH] + c_type)        
        # Llamada a la funcion que crea los hash
        code.value = 'Pd.hash('        
        # Las claves siempre son strings
        keys = 'new String[]{'        
        # Los valores son del tipo del hash
        values = Cst.creare_inicialize([Type(Dtp.ARRAY)] + code.type[2:], []) + '{'        
        # Bandera para alternar entre clave y valor
        flag = True        
        for exp in list:    
            # Comprobamos el codigo y añadimos las declaraciones
            code.declares += exp.declares
            Aux.check_code(parser, exp, c_ref=False)
            # Si un valor es una sentencia, el hash lo sera
            if Dtp.STATEMENT in exp.flags:
                code.flags[Dtp.STATEMENT] = True
            # Es es clave, nos aseguramos de que valla como string
            if flag:
                keys += Cst.to_string(exp) + ','    
            else: 
                # Si no es un hash de scalar, primero eliminamos las referencias
                if not scalar:        
                    # Tiene que ser una referencia
                    if exp.type[0] == Dtp.REF:
                        # Accedemos a la referencia
                        access = Coll.access_pointed(parser, Access(exp), exp.pos)
                        exp.value = access.value + access.read_value + access.end_value
                        if parser.optimize_code:
                            exp.value = Aux.opt_get(exp.value) 
                        # Cogemos el tipo accedido
                        exp.type = access.type  
                    else:
                        Msg.error(parser, 'VAR_REF_REQUIRES', exp.pos, var=exp.value)
                # Añadimos la expresion casteada al tipo del array   
                values += Cst.to_type(parser, Code(type=c_type), exp) + ',' 
            # Cambio
            flag = not flag
        # El valor final debe ser: Pd.hash(new String[]{...},new T[]{...})
        code.value += keys[:-1] + '}, ' + values[:-1] + '})'    
        # Lo convertimos en referencia
        code.value = 'new Ref<>(' + code.value + ')'
        return code    
    
    @classmethod
    def create_array_range(Coll, parser, exp1, exp2):
        # Comprobamos las expresiones
        Aux.check_code(parser, exp1)
        Aux.check_code(parser, exp2)
        # Creamos el codigo
        code = exp1 + exp2
        # Si alguno es String, creamos String
        if exp1.type[0] == Dtp.STRING or  exp1.type[0] == Dtp.STRING:
            code.type = [Dtp.ARRAY, Dtp.STRING]
            code.value = 'Pd.range(' + Cst.to_string(exp1) + ',' + Cst.to_string(exp2) + ')'
        else:
            code.type = [Dtp.ARRAY, Dtp.INTEGER]
            code.value = 'Pd.range(' + Cst.to_integer(exp1) + ',' + Cst.to_integer(exp2) + ')'
        return code
