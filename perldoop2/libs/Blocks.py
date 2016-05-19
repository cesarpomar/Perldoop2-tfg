#!/usr/bin/python
# -*- coding: utf-8 -*-

from libs import Messages as Msg
from libs import Auxiliary as Aux
from libs import DataType as Dtp
from libs import Casting as Cst
from libs import Variables as Var
from libs import Code
from libs import Function

class Blocks:
    
    # Crea la cabecera de un bloque
    @classmethod
    def block_header(Bks, parser):
        # Añade un nivel para guardar las variables del bloque
        parser.variables.append(dict())
        # Añade un nivel para las asignaciones del bloque
        parser.assigns.append(dict())
    
    # Bloque compuesto solo por llaves 
    @classmethod 
    def block_empty(Bks, parser, block, pos):
        # Creamos el bloque con su posicion y las flags se mantienen
        code = Code(value='{\n' + block.value + '}\n', pos=pos, flags=block.flags)
        # Eliminamos las variables declaradas en el propio bloque
        for var in parser.variables[-1].keys():
            if var in parser.assigns[-1]:
                del parser.assigns[-1][var]
        # El resto permaneceran asignadas en el bloque superior
        parser.assigns[-2].update(parser.assigns[-1])
        parser.assigns.pop()
        # Borramos las varaibles del bloque
        parser.variables.pop()
        return code
    
    @classmethod
    def block_while(Bks, parser, exp, block, pos):
        # Verificamos la expresion de la condicion
        Aux.check_code(parser, exp)
        # Creamos el bloque y ponemos la posicion de final del codigo
        code = Code(value='while(' + Cst.to_boolean(exp) + '){\n' + block.value + '}\n', pos=pos)
        # Si hay declaraciones creamos un bloque externo y las declaramos
        if exp.declares:
            code.value = '{\n' + Aux.create_declare(exp) + code.value + '}\n'
        # Borramos las variables del bloque y asignaciones
        parser.variables.pop()  
        parser.assigns.pop()
        return code  
    
    @classmethod
    def block_until(Bks, parser, exp, block, pos):
        # Verificamos la expresion de la condicion
        Aux.check_code(parser, exp)
        # Creamos el bloque y ponemos la posicion de final del codigo
        code = Code(value='while(!(' + Cst.to_boolean(exp) + ')){\n' + block.value + '}\n', pos=pos)
        # Si hay declaraciones creamos un bloque externo y las declaramos
        if exp.declares:
            code.value = '{\n' + Aux.create_declare(parser, exp) + code.value + '}\n'
        # Borramos las variables del bloque y asignaciones
        parser.variables.pop()  
        parser.assigns.pop()
        return code  
    
    # Comprueba las propagaciones en un bloque do
    @classmethod
    def do_block_checks(Bks, parser, code, block):
        # Eliminamos las variables declaradas en el propio bloque
        for var in parser.variables[-1].keys():
            if var in parser.assigns[-1]:
                del parser.assigns[-1][var]
        # El resto permaneceran asignadas en el bloque superior
        parser.assigns[-2].update(parser.assigns[-1])
        parser.assigns.pop()
        # Propaga el return de la funcion
        if Dtp.RETURN in block.flags:
            code.flags[Dtp.RETURN] = True 
    
    @classmethod
    def block_dowhile(Bks, parser, exp, block, pos):
        # Verificamos la expresion de la condicion
        Aux.check_code(parser, exp)
        # Creamos el bloque y ponemos la posicion de final del codigo
        code = Code(value='do{\n' + block.value + '}while(' + Cst.to_boolean(exp) + ');\n', pos=pos)
        # Si hay declaraciones creamos un bloque externo y las declaramos
        if exp.declares:
            code.value = '{\n' + Aux.create_declare(exp) + code.value + '}\n'
        Bks.do_block_checks(Bks, parser, code, block)
        # Borramos las variables del bloque
        parser.variables.pop()  
        return code
    
    @classmethod
    def block_dountil(Bks, parser, exp, block, pos):
        # Verificamos la expresion de la condicion
        Aux.check_code(parser, exp)
        # Creamos el bloque y ponemos la posicion de final del codigo
        code = Code(value='do{\n' + block.value + '}while(!(' + Cst.to_boolean(exp) + '));\n', pos=pos)
        # Si hay declaraciones creamos un bloque externo y las declaramos
        if exp.declares:
            exp.value = '{\n' + Aux.create_declare(parser, exp) + code.value + '}\n'
        Bks.do_block_checks(Bks, parser, code, block)   
        # Borramos las variables del bloque
        parser.variables.pop()  
        return code
    
    @classmethod
    def block_if(Bks, parser, exp, block, pos):
        # Verificamos la expresion de la condicion
        Aux.check_code(parser, exp)
        # Guardamos los flags, las declaraciones en la expresion y la posicion
        code = Code(flags=block.flags, declares=exp.declares, pos=pos)
        # Creamos el bloque
        code.value = 'if(' + Cst.to_boolean(exp) + '){\n' + block.value + '}'    
        # Guardamos las asignaciones para comprobar despues de las clausulas elsif y else
        code.var_assing = parser.assigns.pop()
        # Eliminamos las variables declaradas en el propio bloque
        for var in parser.variables[-1].keys():
            if var in code.var_assing:
                del  code.var_assing[var]
        # Borramos las variables del bloque
        parser.variables.pop()    
        return code
    
    @classmethod
    def block_unless(Bks, parser, exp, block, pos):
        # Verificamos la expresion de la condicion
        Aux.check_code(parser, exp)
        # Guardamos los flags, las declaraciones en la expresion y la posicion
        code = Code(flags=block.flags, declares=exp.declares, pos=pos)
        # Creamos el bloque
        code.value = 'if(!(' + Cst.to_boolean(exp) + ')){\n' + block.value + '}'    
        # Guardamos las asignaciones para comprobar despues de las clausulas elsif y else
        code.var_assing = parser.assigns.pop()
        # Eliminamos las variables declaradas en el propio bloque
        for var in parser.variables[-1].keys():
            if var in code.var_assing:
                del  code.var_assing[var]
        # Borramos las variables del bloque
        parser.variables.pop()    
        return code
    
    @classmethod
    def block_elif(Bks, parser, exp, block, pos):
        # Verificamos la expresion de la condicion
        Aux.check_code(parser, exp)
        # Guardamos los flags, las declaraciones en la expresion y la posicion
        code = Code(flags=block.flags, declares=exp.declares, pos=pos)
        # Creamos el bloque
        code.value = 'else if(!(' + Cst.to_boolean(exp) + ')){\n' + block.value + '}'    
        # Guardamos las asignaciones para comprobar despues de las clausulas elsif y else
        code.var_assing = parser.assigns.pop()
        # Eliminamos las variables declaradas en el propio bloque
        for var in parser.variables[-1].keys():
            if var in code.var_assing:
                del  code.var_assing[var]
        # Borramos las variables del bloque
        parser.variables.pop()    
        return code
    
    @classmethod
    def block_else(Bks, parser, block, pos):
        # Guardamos los flags y la posicion
        code = Code(flags=block.flags, pos=pos)
        # Creamos el bloque
        code.value = 'else{\n' + block.value + '}\n'    
        # Guardamos las asignaciones para comprobar despues de las clausulas elsif y else
        code.var_assing = parser.assigns.pop()
        # Eliminamos las variables declaradas en el propio bloque
        for var in parser.variables[-1].keys():
            if var in code.var_assing:
                del  code.var_assing[var]
        # Borramos las variables del bloque
        parser.variables.pop()    
        return code
    
    # Une los bloques elsif hasta el else
    @classmethod
    def block_elif_concat(Bks, parser, block1, block2):
        # Si no hay bloque dos usamos directamente el uno
        if block2 is None:
            # Añadimos el salto de linea despues de cerrar la llava
            block1.value += '\n'
            return block1
        # Unimos los dos bloques
        code = Code(value=block1.value + block2.value, pos=block2.pos)
        code.var_assing = dict()
        # Si las variables estan asignadas en ambos bloques la propagamos
        for var in block1.var_assing.keys():
            if var in block2.var_assing:
                code.var_assing[var] = True
        # Las declaraciones de propagan hasta el if
        code.declares = block1.declares + block2.declares
        # Si ambos tienen un return entonces lo propagamos
        if Dtp.RETURN in block1.flags and Dtp.RETURN in block2.flags:
            code.flags[Dtp.RETURN] = True
        return code    
    
    # Une el bloque if con los elsif
    @classmethod
    def block_if_concat(Bks, parser, block1, block2):
        # Realizamos las mismas tareas que con los elif
        code = Bks.block_elif_concat(parser, block1, block2)
        # Las variables asignadas en todos los bloques las propagamos
        parser.assigns[-1].update(code.var_assing)  
        # Añadimos todas las declaraciones de las expresiones de los bloques if e elsif
        if code.declares:
            code.value = '{\n' + Aux.create_declare(code) + code.value + '}\n'
        return code
    
    # Comprueba si hace falta crear un bloque externo o se puede usar el bloque de inicializacion del for
    @classmethod
    def external_for(Bks, list):                
        declare = False  # Formado por declaraciones
        type_for = None  # Tipo de las declaraciones
        sts = False  # Formado por sentencias sin declaraciones
        # Paratodas las sentencias
        for st in list:
            # Si es una declaracion
            if st.declares:
                declare = True
                # Si ya hay una sentencia, hace falta un boque externo
                if sts:
                    return True
                # Cogemos el tipo de la asginacion
                if not type_for:
                    type_for = Cst.create_type(st.declares[0].type)
                # Recorremos todas las declaraciones
                for declare in st.declares:
                    type = Cst.create_type(declare.type)
                    # Si hay una declaracio de tipo direfente se necesita un bloque esterno
                    if type != type_for:
                        return True
            # Si es una sentencia sin declaraciones
            if st.st_value:
                sts = True
                # Si en el anteror las habia, hace falta un boque externo
                if declare:
                    return True
        # Si se cumplen todos los requisitos podemos ahorrarnos el bloque externo
        return False
    
    @classmethod
    def create_for_declare(Bks, parser, list1, list2, list3, block, pos):
        code = Code(pos=pos)  # Codigo del for
        external_code = ''  # Codigo externo si llega a ser necesario
        # Campos del bucle
        for_head1 = ''
        for_head2 = ''
        for_head3 = ''
        # Campos de incrementos,empezamos por el final por eficiencia
        if list3:
            # para todos las sentencias del tercer bloque
            for st in list3:
                for_head3 += st.st_value + ','
                if st.declares:
                    external_code += Aux.create_declare(st)  
            # Quitamos la coma 
            for_head3 = for_head3[:-1]
        # Campo condicional
        if list2:
            # Para todas las expresiones realizamos el and
            for exp in list2:
                for_head2 = Cst.to_boolean(exp) + '&&'
                if st.declares:
                    external_code += Aux.create_declare(exp)
            # Quitamos la coma 
            for_head2 = for_head2[:-2]
        # Campo de inicializacion
        if list1:
            # Si hay declaraciones de otros bloques nos ahorramos la llamada a la funcion de comprobacion
            external = external_code or Bks.external_for(list1)
        # Si hay un bloque externo
        if external:
            # Añadimos todas las declaracion
            for st in list1:
                if st.declares:
                    external_code += Bks.create_declare(st)
                if st.st_value:
                    external_code += st.st_value + ';\n'
        # Si usamos el bloque interno del for
        else:
            # Para todas las sentencias
            for st in list1: 
                # Si hay declaraciones
                if st.declares:
                    # Cogemos el tipo de la primera que encontramos
                    if not for_head1: for_head1 = Cst.create_type(st.declares[0].type) + ' '
                    # Añadimos todas las declaraciones
                    for declare in st.declares:
                        for_head1 += declare.value + ','
                # O si son sin declaracion de tipo
                else:
                    for_head1 += st.value + ','
            for_head1 = for_head1[:-1]
        # Unimos toda la cabecera en el codigo
        code.value = 'for(' + for_head1 + '; ' + for_head2 + '; ' + for_head3 + '){\n' + block.value + '}\n'
        # Si hay codido externo creamos el bloque
        if external_code:
            code.value = '{\n' + external_code + code.value + '}\n'
        # Borramos las variables del bloque y asignaciones
        parser.variables.pop()  
        parser.assigns.pop()    
        return code
    
    # Inicia la declaracion para leer una variable sin tipo
    @classmethod
    def foreach_declare_init(Bks, parser):
        parser.foreach_flag = True    
        
    # Marca la variable del for como asignada y apagana la declaracion sin tipo
    @classmethod
    def foreach_declare_end(Bks, parser, var):
        parser.foreach_flag = False
        parser.assigns[-1][var.variable.name] = True 
        return var
    
    @classmethod
    def block_foreach_var(Bks, parser, var, exp):
        # Creamos el codigo y ponemos las declaraciones
        code = Code(value='for(', declares=exp.declares)
        # Comprobamos el codigo, las refencias las obviamos porque se comprueban luego
        Aux.check_code(parser, exp, c_ref=False)
        # Si el codigo no es una coleccion damos un error
        if exp.type[0] not in (Dtp.ARRAY, Dtp.HASH, Dtp.LIST):
            Msg.error(parser, 'FOREACH_ERROR', exp.pos)
            return exp    
        # El tipo es el de la coleccion sin incluirla
        var_type = exp.type[1:]
        # Le damos el tipo a la variable
        var.variable.type = var_type
        # Creamos el tipo de la variable a usar como iterador
        code.value += Cst.create_type(var_type) + ' '
        # Java requiere iterar sobre una variable recien declarada
        block_st = ''
        # Si la varaible ya estaba declarada
        if not var.declares:
            # Pedimos una varaible resevada para bucles
            l_var = Var.get_loop_var(parser)
            # La añadimos a la declaracion
            code.value += l_var
            # Añadimos al inicio del bloque la igualacion del la varaible orignal a la recien declarada
            block_st = '\n' + var.value + ' = ' + Cst.to_type(parser, var , Code(type=var_type, value=l_var)) + ';'
        # Si la varaible no esta declarada, la ponemos despues del tipo
        else:
            code.value += var.value
        # Terminamos el resto de la cabeza del for 
        code.value += ' : ' + exp.value + '){' + block_st
        return code
    
    @classmethod
    def block_foreach(Bks, parser, exp):
        # Comprobamos el codigo, las refencias las obviamos porque se comprueban luego
        Aux.check_code(parser, exp, c_ref=False)
        # Si el codigo no es una coleccion damos un error
        if exp.type[0] not in (Dtp.ARRAY, Dtp.HASH, Dtp.LIST):
            Msg.error(parser, 'FOREACH_ERROR', exp.pos)
            return exp   
        # Necesitamos algo para recorrer asi que pedimos una varaible resevada para bucles
        l_var = Var.get_loop_var(parser)
        # Creamos el codigo y ponemos las declaraciones
        code = Code(value='for(Integer ' + l_var + '=0; ' + l_var + '<' + Cst.to_integer(exp) + '; ' + l_var + '++){', declares=exp.declares)
        return code
    
    @classmethod
    def block_foreach_head(Bks, parser, head, block, pos):
        # Actualizamos la posicion
        head.pos = pos
        # juntamos ambas partes del codigo
        head.value += '\n' + block.value + '}\n'
        # Borramos las variables del bloque y asignaciones
        parser.assigns.pop()
        parser.variables.pop()
        # Añadimos las declaraciones de las expresion si las tiene
        if head.declares:
            head.value = '{\n' + Aux.create_declare(head) + head.value + '}\n'
        return head
    
    @classmethod
    def post_block_if(Bks, parser, exp):
        # Comprobamos el codigo
        Aux.check_code(parser, exp)
        # Creamos el bloque y su posicion
        code = Code(value='if(' + Cst.to_boolean(exp) + '){', pos=exp.pos)
        # Añadimos las declaraciones
        code.declares = exp.declares
        return code
    
    @classmethod 
    def post_block_unless(Bks, parser, exp):
        # Comprobamos el codigo
        Aux.check_code(parser, exp)
        # Creamos el bloque y su posicion
        code = Code(value='if(!(' + Cst.to_boolean(exp) + ')){', pos=exp.pos)
        # Añadimos las declaraciones
        code.declares = exp.declares
        return code
    
    @classmethod 
    def post_block_while(Bks, parser, exp):
        # Comprobamos el codigo
        Aux.check_code(parser, exp)
        # Creamos el bloque y su posicion
        code = Code(value='while(' + Cst.to_boolean(exp) + '){', pos=exp.pos)
        # Añadimos las declaraciones
        code.declares = exp.declares
        return code
    
    @classmethod 
    def post_block_until(Bks, parser, exp):
        # Comprobamos el codigo
        Aux.check_code(parser, exp)
        # Creamos el bloque y su posicion
        code = Code(value='while(!(' + Cst.to_boolean(exp) + ')){', pos=exp.pos)
        # Añadimos las declaraciones
        code.declares = exp.declares
        return code
    
    @classmethod
    def post_block_for(Bks, parser, exp):
        # Reutilizamos la funcion
        return Bks.block_foreach(parser, exp)
    
    # Declara el tipo de la funcion
    @classmethod
    def function_header(Bks, parser, args, returns, name, pos):
        # Si el nombre esta resevado, se dan error
        if Var.is_reserver(parser, name):
            Msg.error(parser, 'WORD_NATIVE_DECLARE', pos, word=name)
        # Si existe una entrada con el nombre de la funcion 
        if name in parser.functions:
            # Obtenemos sus datos
            parser.function_head = parser.functions[name]
            entry = parser.function_head
            Msg.error(parser, 'FUNCTION_ALREADY_DECLARE', position=pos, funct=name, line=entry.pos.line)
        else:
            # En caso contrario creamos la cabecera y la añadimos
            parser.function_head = Function(args, returns, pos)    
            parser.functions[name] = parser.function_head    
        # Creamos el contexto del bloque
        Bks.block_header(parser)
        # Verificamos que en los argumetos las colecciones se pasen como puntero
        if args:
            for arg in args:
                if len(arg) > 1 and arg[0] != Dtp.REF:
                    Msg.error(parser, 'REF_REQUIRES', pos)
                    break
        # Creamos la variable argumento usando la cabecera
        Var.function_vars(parser, parser.function_head)
        
    # Comprueba que no llega una instruccion de bucle a una funcion     
    @classmethod       
    def check_st(Bks, parser, code):
        if Dtp.NEXT in code.flags:
            Msg.error(parser, 'NEXT_ERROR', code.pos)
            del code.flags[Dtp.NEXT]
        if Dtp.LAST in code.flags:
            Msg.error(parser, 'LAST_ERROR', code.pos)
            del code.flags[Dtp.LAST]
    
    # Crea la clase para el codigo
    @classmethod
    def create_class(Bks, parser):
        # Gestionalos el codigo global
        if parser.main_class:
            parser.atributes = 'private static String[] ARGV;\n' + parser.atributes
            parser.global_code = parser.class_name + '.ARGV=ARGV;\n' + parser.global_code
            init_code = 'public static void main(String[] ARGV){\n' + parser.global_code + '}\n\n'
        elif parser.global_code:
            init_code = 'static{\n' + parser.global_code + '}\n\n' 
        else:
            init_code = ''
        # Empezamos creando los imports y el codigo externo si existiera
        class_code = parser.package_code + Aux.create_imports(parser) + '\n\n'
        # Cabecera de la clase
        class_code += 'public class ' + parser.class_name
        # Si la clase extiende de otra
        if parser.extend_class:
            class_code += ' extends ' + parser.extend_class
        # Atributos de la clase
        class_code += '{\n' + parser.atributes + '\n\n'
        # Funciones de la clase
        class_code += parser.functions_code
        # Añadimos el codigo de inicio
        class_code += init_code
        # Cerramos la clase y retornamos
        return class_code + '}'
    
    @classmethod       
    def create_function(Bks, parser, name, code):
        # Quitamos los contextos de variables y asignaciones
        parser.variables.pop()
        parser.assigns.pop()
        # Comprobamos si las sentencias son validas
        Bks.check_st(parser, code)
        # Si no hay retorno se crea de tipo Object
        if not parser.function_head.returns:
            function = 'public static Object ' + name + '(Object... pd_argv)'
        # Si tiene un retorno se crea de ese tipo
        elif len(parser.function_head.returns) == 1:
            function = 'public static ' + Cst.create_type(parser.function_head.returns[0]) + ' ' + name + '(Object... pd_argv)'
        # Si tiene varios, se crea de array de Object
        else:
            function = 'public static Object[] ' + name + '(Object... pd_argv)'
        # Quitamos la cabecera del analizador
        parser.function_head = None
        # Añadimos el codigo a la funcion
        function += '{\n' + code.value
        # Si no podemos asegurar que se retorne siempre, a�adimos un return al final
        if not Dtp.RETURN in code.flags:
            function += 'return null;\n'
        # Cerramos la funcion y retornamos
        return function + '}\n\n'
