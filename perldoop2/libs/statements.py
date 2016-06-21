#!/usr/bin/python
# -*- coding: utf-8 -*-

from libs import Auxiliary as Aux
from libs import DataType as Dtp
from libs import Variables as Var
from libs import Casting as Cst
from libs import Messages as Msg
from libs import Collection as Coll
from libs import Code
from libs import Variable
from libs import Access

class Statements:
    
    # Crea una sentencia acabada en ;
    @classmethod
    def create_statement(Sts, parser, list, control, comment, pos):
        # Borramos las etiquetas de la linea
        parser.labels_line = {}  
        # Si hay un comentario cogemos su valor y su posicion
        if comment:
            pos = comment.pos
            comment = comment.value
        else:
            comment = ''
        # Creamos el codigo
        code = Code(pos=pos)
        # Recorremos todas las sentencias
        for st in list:
            # Copiamos las flags
            code.flags.update(st.flags)
            l = len(st.declares) - 1
            # Nos movemos en las declaraciones
            for i, var in enumerate(st.declares):
                # Creamos la sentencia de declaracion
                if var.type:
                    # Si tiene tipo lo usamos
                    declare = Cst.create_type(var.type) + ' ' + var.value + ';'
                else:
                    # Si no asumimos que ya forma parte de la codena
                    declare = var.value + ';'
                # Si la varaible es reservada
                if Var.is_reserver(parser, var.value):
                    # Se escriben siempre en el codigo y si es la ultima se mira si al final la funcion la usa
                    if l != i or (l == i and not st.ref_var):
                        code.value += Cst.create_type(var.type) + ' ' + var.value + ';\n'
                # Si es una variable normal
                else:
                    # Si estamos en el contexto global
                    if len(parser.variables) == 1:
                        # Añadimos la declaracion como atributo
                        parser.atributes += 'private static ' + declare + comment + '\n'
                    else:
                        # Añadimos la variable al codigo
                        code.value += declare + comment + '\n'
                    comment = ''
            # Si el codigo almacena una sentencia la escribimos en el codigo
            if st.st_value:
                code.value += st.st_value + ';\n' 
            # Si la expresion contiene sentencias, forzamos su ejecucion
            elif Dtp.STATEMENT in st.flags:
                code.value += 'Pd.eval(' + st.value + ');\n' 
        # Si la linea tiene un bloque de control metemos el codigo en su interior
        if control:
            code.value = control.value + comment + '\n' + code.value + '}\n'
        return code              
      
    @classmethod  
    def advanced_declare(Sts, parser, vars, type, pos):
        # Verificamos y añadimos los tipos a las variables
        for var in vars:
            # Tienen que ser variables, la sintaxis permite numeros para otros usos
            if var.variable:
                if Var.var_exist(parser, var.value):
                    Msg.error(parser, 'VAR_ALREADY_TYPED', pos, var=var.value)
                else:
                    # Añadimos para cada variable el tipo
                    parser.declare_types[var.value] = Variable(type=type, pos=pos)  
        # Genera un codigo vacio sin efecto       
        return  Code()       
    
    # Concatena las sentencias
    @classmethod
    def statements_concat(Sts, parser, sts, st):
        # Añadimos la nueva sentencia
        sts.value += st.value
        # Actualizamos las flags
        sts.flags.update(st.flags)
        # Comprobamos codigo inalcanzable si esta activado
        if parser.unreachable_code:
            Aux.check_unreachable(parser, sts)
        return sts
        
    # Crea una nueva variable
    @classmethod
    def create_var(Sts, parser, var, pos, shared=False):
        # Cresmos el codigo
        code = Code(value=var, pos=pos)
        # Situamos el contexto de la variable en el mas bajo
        context_var = parser.variables[-1]
        # Si ha sido declarada damos un error
        if Var.var_exist(parser, var):
            entry = Var.get_var(parser, var)
            Msg.error(parser, 'VAR_ALREADY_DECLARE', pos, var=var, line=entry.pos.line)
        # Si es reservada tambien damos error
        elif Var.is_reserver(parser, var):
            Msg.error(parser, 'WORD_NATIVE_DECLARE', pos, word=var)
        entry = Variable(pos=pos, name=var, private=not shared)
        # Si el tipo ha sido declarado con las etiquetas avanzadas
        if var in parser.declare_types:
            # Si estamos en un foreach, damos un error
            if parser.foreach_flag:
                Msg.error(parser, 'VAR_FOR_TYPED', pos, var=var, line=parser.declare_types[var].pos.line)
            # Copiamos el tipo
            entry.type = parser.declare_types[var].type
            # Lo borramos de las declaraciones
            del parser.declare_types[var]
        # Si el tipo esta declarado en la propia linea
        elif Dtp.LABEL_TYPE in parser.labels_line:
            entry.type = parser.labels_line[Dtp.LABEL_TYPE]
        # Si no es ninguno de los casos damos un error
        else:
            # Si no estamos en un for each, el tipo es obligatorio
            if not parser.foreach_flag:
                Msg.error(parser, 'VAR_NOT_TYPE', pos, var=var)
            entry.type = [Dtp.NONE]  # Tipo por defecto para poder continuar el analisis
        # Le damos el tipo al codigo
        code.type = entry.type[:]
        context_var[var] = entry    
        # Guardamos el codigo como que contiene una variable
        code.variable = entry
        # Si la variable no es compartida
        if not shared:
            # Guardamos el codigo para luego declararlo
            code.declares.append(code)    
        else:
            # Añadimos directamente como atributo
            parser.atributes += 'public static ' + Cst.create_type(code.type) + ' ' + code.value + ';\n'
        return code
    
    # Accedemos a una variable que debio ser declarada    
    @classmethod
    def read_var(Sts, parser, var, pos=None, package=None):
        code = Code(pos=pos)
        # Si pertenece a un paquete
        if package:
            # Miramos si existe y la leemos
            if var in package.variables:
                variable = package.variables[var]
            else:
                variable = None
        else:
            # Buscamos la varaible en todos los niveles
            variable = Var.get_var(parser, var)
        # Si la varaible no existe damos error
        if variable is None:
            if package:
                Msg.error(parser, 'PACK_VAR_NOT_EXIST', pos, var=var, pack=package.name)
            elif var in parser.declare_types:
                Msg.error(parser, 'VAR_NOT_DECLARE', pos, var=var)
            else:
                Msg.error(parser, 'VAR_NOT_EXIST', pos, var=var)
            # Podemos datos por defecto
            code.type = [Dtp.NONE]
            code.value = var
            variable = Variable()
            parser.assigns[-1][var] = True
        else:
            # Cargamos el tipo en la variable
            code.type = variable.type[:]    
            if variable.multi_type:
                code.multi_type = variable.multi_type[:]
            # Cogemos el nombre java de la variable que normalmente sera el mismo y la situamos en su contexto
            if package:
                code.value = package.name + '.' + variable.name
            else:
                code.value = variable.name
        # Guardamos el codigo como que contiene una variable
        code.variable = variable
        return code      
    
    @classmethod    
    def equals(Sts, parser, var, exp, casting=False):
        # Comprobamos la expresion
        Aux.check_code(parser, exp, c_ref=False)
        # Si la parte izquierda no es una variable
        if not var.var.variable:
            Msg.error(parser, 'VAR_REQUIRES', var.pos)   
            return exp 
        # Ajustamos las dimensiones
        if exp.type[0] == Dtp.REF and var.ref:
            exp = Coll.create_value_var(Sts.access_pointed(parser, Access(exp), exp.pos))
        # Si estan activadas aplicamos las optimizaciones
        if parser.optimize_code:
            exp.value = Aux.opt_get(exp.value)
        # Si se requiere se añade un cast al tipo
        if casting:
            exp.value = '((' + Cst.create_type(exp.type) + ')' + exp.value + ')'
        # Creamos el codigo usando los anteriores
        code = var.var + exp
        # Marcamos la variable como asignada en el contexto actual
        parser.assigns[-1][var.var.variable.name] = True
        # Copiamos el tipo
        code.type = var.type
        code.declares += var.declares
        # Preparamos el valor
        value = Cst.to_type(parser, code, exp)    
        # Si no es una variable o es un tipo basico
        if not exp.variable or exp.type[0] not in (Dtp.HASH, Dtp.LIST, Dtp.ARRAY) or exp.value != exp.variable.name or var.ref:
            code.value = var.value + var.store_value + value + var.end_value
        # Si es una coleccion se debe hacer una copia superficial
        else:
            code.value = var.value + var.store_value + 'Pd.copy(' + value + ')' + var.end_value
        # Si hay declaraciones, no estamos en el contexto global, no hemos accedido en caso de una coleccion y el parser lo permite
        if var.var.declares and len(parser.variables) > 1 and len(var.type) == len(var.var.type) and parser.init_var:
            # Añadimos el codigo a la declaracion y dejamos solo la variable
            tmp = var.var.value    
            var.var.value = code.value
            code.value = tmp  
            # Si el codigo era un estamento, ya esta asegura su ejecucion entonces quitamos la bandera      
            if Dtp.STATEMENT in code.flags:
                del code.flags[Dtp.STATEMENT]
        else:
            # El codigo ya es una sentencia
            code.st_value = code.value
            # El codigo contiene una sentencia
            code.flags[Dtp.STATEMENT] = True
        return code
    
    @classmethod
    def equals_declare(Sts, parser, var):
        # Si la parte izquierda no es una variable
        if not var.var.variable:
            Msg.error(parser, 'VAR_REQUIRES', var.pos) 
        # Si no es una coleccion la igualamos a null
        if var.type[0] not in [Dtp.ARRAY, Dtp.HASH, Dtp.LIST]:
            return Sts.equals(parser, var, Code(type=var.type, value='null'))    
        # Obtenermos una referencia directa a la variable
        variable = var.var.variable
        # Tamaños para la declaracion, solo se usara mas de uno en caso de arrays multidimensionales
        sizes = []
        # Si en la linea tenemos tamaños declarados usamos esos
        if Dtp.LABEL_DECLARE in parser.labels_line:
            # para cada etiqueta
            for label in parser.labels_line[Dtp.LABEL_DECLARE]:
                # Si la etiqueta es de una variable, esta debe existir y estar inicializada
                if label.variable:
                    # Bascamos la variable
                    var_size = Var.get_var(parser, label.value)
                    # Si no existe
                    if not var_size:
                        Msg.error(parser, 'VAR_NOT_EXIST', label.pos, var=label.value)
                    # Si no esta asignada
                    elif not Var.is_assign(parser, var_size.name):
                        Msg.error(parser, 'READ_BEFORE_ASSIGN', label.pos, var=label.value)
                    # En caso contrario podemos usar la variable en su forma entera
                    else:
                        label.value = Cst.to_integer(Code(value=label.value, type=var_size.type))
                # Añadimos como tamaño
                sizes.append(label.value)
        # Si no se indica ningun tamaño por defecto cogemos los almacenados en la declaracion
        else:
            # vamos de una en una copiando el tamaño
            for dim in variable.type[:-1]:
                sizes.append(dim.size)
        # Creamos el codigo de la inicializacion
        exp = Code(type=var.type)
        # Si estammos inicializando un array es obligatorio que al menos se tenga un tamaño
        if not sizes and exp.type[0] == Dtp.ARRAY:
            Msg.error(parser, 'SIZE_REQUIRED', var.pos, var=var.value)
        # Creamos la inicializacion
        exp.value = Cst.creare_inicialize(exp.type, sizes)
        return Sts.equals(parser, var, exp)
    
    @classmethod
    def equals_read(Sts, parser, var, file, pos):
        # Convierte la variable
        file = Coll.create_value_var(file)
        # Comprobamos la expresion
        Aux.check_code(parser, file)
        # Creamos el codigo
        code = Code(pos=pos) + file
        # Si no es un fichero
        if file.type[0] != Dtp.FILE:
            Msg.error(parser, 'NOT_FILE', file.pos, var=file.value)
        # Si el contenedor es una coleccion
        if len(var.type) > 1:
            # Esta debe ser un array o una lista de Strings
            if len(var.type) != 2 or var.type[1] != Dtp.STRING or var.type[0] not in (Dtp.ARRAY, Dtp.LIST):
                Msg.error(parser, 'FILE_ARRAY_ERROR', var.pos)
            # Cambiamos el tipo a array de String
            code.type = [Dtp.ARRAY, Dtp.STRING]
            # Usamos la funcion de lectura
            code.value = file.value + '.readLines()'
            # Realizamos la asignacion
            return Sts.equals(parser, var, code)
        else:
            # Esta debe ser un String
            if var.type[0] != Dtp.STRING:
                Msg.error(parser, 'FILE_STRING_ERROR', var.pos)
            code.type = [Dtp.STRING]
            # Usamos la funcion de lectura
            code.value = file.value + '.read()'          
            # Realizamos la asignacion
            code = Sts.equals(parser, var, code)
            return code
    
    @classmethod    
    def equals_input(Sts, parser, var, pos):
        # Si el contenedor es una coleccion
        if len(var.type) > 1:
            # Esta debe ser un array o una lista de Strings
            if len(var.type) != 2 or var.type[0] == Dtp.STRING or var.type[1] not in (Dtp.ARRAY, Dtp.LIST):
                Msg.error(parser, 'FILE_ARRAY_ERROR', var.pos)
            return Sts.equals(parser, var, Code(type=[Dtp.ARRAY, Dtp.STRING], value='Pd.readLines()'))
        else:
            # Esta debe ser un String
            if var.type[0] != Dtp.STRING:
                Msg.error(parser, 'FILE_STRING_ERROR', var.pos)
            return Sts.equals(parser, var, Code(type=[Dtp.STRING], value='Pd.read()'))
    
    # Igualar varias variables de una unica fuente
    @classmethod
    def multi_equals_single(Sts, parser, list, exp):
        # Comprobamos la expresion
        Aux.check_code(parser, exp, c_ref=False)
        # Creamos un array para las sentencia con una varia para mandar las declaraciones
        sts = [Code()]
        # Si hay declaracione en la expression
        if exp.declares:
            # Las añadimos y las borramos de la expresion
            sts[0].declares = exp.declares
            exp.declares = []
        # Comprobar que todas son variables
        for var in list:
            if var.declares:
                # hacemos los mismo con con la expresion
                sts[0].declares += var.declares
                var.declares = []
            if not var.variable:
                Msg.error(parser, 'VAR_REQUIRES', var.pos)    
                return sts
        # La fuente no es una variable, usamos una para almacenar el resultado dentro de un contexto de llaves
        if not exp.variable:
            # Si es mutitipo creamos un array generico
            if exp.multi_type:
                sts.append(Code(st_value='{\nObject[] pd_me=' + exp.value))
            # En caso contrario creamos una variable del tipo apropiado
            else:
                sts.append(Code(st_value='{\n' + Cst.create_type(exp.type) + ' pd_me=' + exp.value))
            # A partir de ahora la fuente sera la variable
            exp.value = 'pd_me'
        # Variables igualadas a un array
        if exp.type[0] == Dtp.ARRAY:
            # El tipo lo sacamos del array
            type = exp.type[1:]
            for n, var in enumerate(list):
                sts.append(Sts.equals(parser, Access(var), Code(type=type, value=exp.value + '[' + str(n) + ']')))    
        # Variables igualadas a una lista
        elif exp.type[0] == Dtp.LIST:
            # El tipo lo sacamos de la lista
            type = exp.type[1:]
            for n, var in enumerate(list):
                sts.append(Sts.equals(parser, Access(var), Code(type=type, value=exp.value + '.get(' + str(n) + ')')))    
        # Variables igualadas a un array multitipo
        elif exp.type[0] == Dtp.VOID and exp.multi_type:
            # Recorremos las n posiciones de tipo type para almacenarlo en var
            for n, (var, type) in enumerate(zip(list, exp.multi_type)):
                # Nos servimos de la funcion equals para realizar la asignacion pidiendo un casting dado que el array era generico
                sts.append(Sts.equals(parser, Access(var), Code(type=type, value=exp.value + '[' + str(n) + ']'), casting=True))
        # En caso de otra operacion como usar un hash de fuente, damos un error
        else:        
            Msg.error(parser, 'INVALID_MULTI_EQUALS', exp.pos)
        # Si la fuente no fue una varaible tenemos que cerrar el contexto
        if not exp.variable:
            sts.append(Code(st_value='}'))
        return sts
    
    # Igualamos un conjunto de varaibles a un conjunto de valores
    @classmethod
    def multi_equals_multi(Sts, parser, listI, listD):
        # Creamos un array para las sentencia con una varia para mandar las declaraciones
        sts = [Code()]
        # Variable para almacenar valores temporales en caso de igualar una variable a otra
        sts.append(Code(st_value='{\nObject[] pd_me=new Object[]{'))
        # Bandera que indica si hay variables como fuente de datos
        no_vars = True
        # Para todas las expresiones del lado derecho
        for exp in listD:
            # Si hay declaraciones las quitamos
            if exp.declares:
                # Las a�adimos y las borramos de la expresion
                sts[0].declares += exp.declares
                exp.declares = []
            # Si son variables
            if Dtp.VARIABLE in exp.flags:
                # Las metemos en el array de temporales
                sts[1].st_value += exp.value + ','
                # Marcamos como que hay varaibles temporales
                no_vars = False
        # Si no hubo varaibles no hace falta el array temporal y lo borramos
        if no_vars:
            sts.pop(1)
        # En caso contrario cerramos la lista con la llave final y quitamos la coma final
        else:
            sts[1].st_value = sts[1].st_value[:-1] + '}' 
        # Posicion de variable temporal   
        n = 0
        for var, exp in zip(listI, listD):
            # Si la parte izquierda no es una variable damos error
            if not var.variable:
                Msg.error(parser, 'VAR_REQUIRES', var.pos)
            # Si se igualan dos variables le quitamos la declaracion  
            if var.declares and Dtp.VARIABLE in exp.flags:
                # Las a�adimos y las borramos de la variable
                sts[0].declares += var.declares
                var.declares = []    
            # Si la parte derecha no es una variable igualamos directamente
            if Dtp.VARIABLE not in exp.flags:
                sts.append(Sts.equals(parser, Access(var), exp)) 
            # Si la parte derecha es una varaible igualamos y recuperamos el tipo mediante casting 
            else:    
                sts.append(Sts.equals(parser, Access(var), Code(type=exp.type, value='pd_me[' + str(n) + ']'), casting=True))        
                n = n + 1
            # Si por el contrario se igualo una variable a una expresion sacamos las declaraciones despues
            if sts[-1].declares:
                # Las a�adimos y las borramos de la variable
                sts[0].declares += sts[-1].declares
                sts[-1].declares = []                  
        # Si hubo variables hay que cerrar el bloque creado como contexto de la declaracion      
        if not no_vars:    
            sts.append(Code(st_value='}'))    
        return sts
    
    @classmethod
    def function_call(Sts, parser, name, pos, list=[], package=None):
        # Si hay un paquete
        if package:
            # Si la funcion no existe damos error y devolvemos un codigo para continuar el analisis
            if name not in package.functions:
                Msg.error(parser, 'PACK_FUNCTION_NOT_EXIST', position=pos, funct=name, pack=package.name)
                return Code(type=Dtp.NONE) 
            head = package.functions[name]
        else:
            # Si la funcion no existe damos error y devolvemos un codigo para continuar el analisis
            if name not in parser.functions:
                Msg.error(parser, 'FUNCTION_NOT_EXIST', position=pos, funct=name)
                return Code(type=Dtp.NONE)    
            # Obtenemos la cabecera de la funcion
            head = parser.functions[name]
        # Codigo de la llamada
        code = Code(pos=pos)   
        # Si la funcion no tiene los mismos argumentos que necesita damos error
        if len(list) != len(head.args):
            Msg.error(parser, 'FUNCTION_ARGS_ERROR', position=pos, funct=name, exp=len(head.args), find=len(list))
            return Code(type=Dtp.NONE)    
        # Recorremos los argumentos
        args = ''
        for exp, type in zip(list, head.args):
            code.declares += exp.declares
            Aux.check_code(parser, exp, c_ref=False)
            Aux.opt_paren(exp)
            args += Cst.to_type(parser, Code(type=type), exp) + ', '
        # Quitamos el espacio y la coma final
        if len(args) > 2:
            args = args[:-2]
        # Construimos la funcion
        if package:
            code.st_value = code.value = package.name + '.' + name + '(' + args + ')'
        else:
            code.st_value = code.value = name + '(' + args + ')'    
        # Preparamos su retorno    
        # Si la funcion devuelve solo un tipo
        if head.returns and len(head.returns) == 1:
            # Copiamos ese tipo al codigo
            code.type = head.returns[0][:]              
        else:
            # Si no retorna parametros o retorna multiples tipos,marcamos el codigo como void 
            code.type = [Dtp.VOID]
            code.multi_type = head.returns 
        code.flags[Dtp.STATEMENT] = True    
        return code
    
    @classmethod
    def create_return(Sts, parser, list, pos):
        code = Code()
        # El return debe estar dentro de una funcion
        if not parser.function_head:
            Msg.error(parser, 'RETURN_ERROR', pos)
            return code
        # Sacamos su tipo de la cabecera de la funcion actual
        r_types = parser.function_head.returns
        # El numero de elementos retornados debe coincidir
        if len(r_types) != len(list):
            Msg.error(parser, 'RETURN_PARAM_ERROR', pos, num=len(r_types), find=len(list))
        # Si la funcion no retorna nada ponemos null
        if len(r_types) == 0:
            code.value = 'return null'
            return code
        # Para cada elemento a retornar
        for exp, type in zip(list, r_types):
            Aux.check_code(parser, exp, c_ref=False)
            code.declares += exp.declares
            code.value += Cst.to_type(parser, Code(type=type), exp) + ', '
        # Quitamos la coma y espacio final
        code.value = code.value[:-2]
        # Si son mas de uno se crea un array generico
        if len(r_types) > 1:
            code.value = 'return new Object[]{' + code.value + '}'
        else:
            code.value = 'return ' + code.value
        # Usamos la bandera return
        code.flags[Dtp.RETURN] = True
        return code    
    
    # Coge el valor de una llamada al sistema
    @classmethod
    def value_cmd(Sts, parser, value, pos):
        if value[0] == '$':
            var = Var.get_var(parser, value[1:])
            if var and len(var.type) == 1:
                return Code(value='Pd.cmd(' + Cst.to_string(Code(type=var.type, value=var.name)) + ')', type=[Dtp.STRING], pos=pos)
        return Code(value='Pd.cmd("' + value.replace("\"", "\\\"") + '")', type=[Dtp.STRING], pos=pos)

