#!/usr/bin/python
# -*- coding: utf-8 -*-
from libs.Collection import create_value_var
from libs.Datatypes import Position, Code, INTEGER, STATEMENT, FILE, NONE,\
    STRING, ARRAY, HASH, BOOLEAN, LIST, Variable, var_types
from libs.Auxiliary import check_code, opt_paren, arg_ref, IDENT, create_declare
from libs.Casting import to_repr, to_string, to_type, create_type, equals_type,\
    to_integer
from libs.Messages import error
from libs.Variables import get_function_var, is_assign
from libs.Blocks import block_header
import re

perl_functions=('CHOMP', 'CHOP', 'CLOSE', 'DEFINED', 'DELETE', 'DIE', 'EACH', 'EXISTS', 'EXIT', 'JOIN', 
                'KEYS', 'LC', 'LCFIRST', 'LENGTH', 'OPEN', 'POP', 'PRINT', 'PUSH', 'SAY', 'SHIRFT', 
                'SORT', 'SPLICE', 'SPLIT', 'SUBSTR', 'SYSTEM', 'UC', 'UCFIRST', 'UNSHIFT', 'VALUES')

class PerlFunctions():
    
    def __init__(self):  
        super().__init__() 

    def p_function_print(self,p):
        '''function_call : PRINT LPAREN list RPAREN
                        |  PRINT expression %prec UNITARY
                        |  SAY LPAREN list RPAREN
                        |  SAY expression %prec UNITARY '''
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        declares=[]
        args=''
        #Argumetos
        for exp in list:
            declares+=exp.declares
            opt_paren(exp)
            args+=to_repr(exp)+', '   
        args=args[:-2]       
        #Codigo
        value='Perl.'+p[1]+'('+args+')'
        p[0]=Code(value=value,st_value=value,type=[INTEGER],declares=declares,pos=pos,flags={STATEMENT:True})
        
    def p_function_fprint(self,p):
        '''function_call : PRINT expression LPAREN list RPAREN
                        | PRINT LPAREN expression LPAREN list RPAREN RPAREN
                        | SAY expression LPAREN list RPAREN
                        | SAY LPAREN expression LPAREN list RPAREN RPAREN'''
        #Variables
        if len(p)==6:
            list=p[4]
            file=p[2]
            pos=Position(p,5)
        else:
            list=p[5]
            file=p[3]
            pos=Position(p,7)
        declares=file.declares
        args=''
        #Si no es un fichero
        if file.type[0]!=FILE:
            error(self,'NOT_FILE',list[0].pos,var=list[0].value)
        check_code(self,file)
        #Argumetos
        for exp in list:
            check_code(self,exp)
            declares+=exp.declares
            opt_paren(exp)
            args+=to_repr(exp)+', '   
        args=args[:-2]  
        #Codigo
        value=file.value+'.'+p[1]+'('+args+')'
        p[0]=Code(value=value,st_value=value,type=[INTEGER],declares=declares,pos=pos,flags={STATEMENT:True})     
        
    def p_function_split(self,p):
        'function_call : SPLIT LPAREN list RPAREN'
        #Variables
        list=p[3]
        declares=[]
        args=''
        #Argumetos        
        if len(list)!=2:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]= Code(type=[NONE])
            return 
        for exp in list:
            check_code(self,exp)
            declares+=exp.declares
            args+=to_string(exp)+', '  
        args=args[:-2]              
        #Codigo
        value='Perl.split('+args+')'
        p[0]=Code(value=value,st_value=value,type=[ARRAY,STRING],declares=declares,pos=Position(p,4),flags={STATEMENT:True})
        
    def p_function_join(self,p):
        'function_call : JOIN LPAREN list RPAREN'
        #Variables
        list=p[3]
        declares=[]
        args=''
        #Argumetos        
        if len(list)!=2:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]= Code(type=[NONE])
            return  
        #Si no es un array o lista de String, hacemos un cast para invocar un error    
        if list[1].type[1] != STRING and list[1].type[0] not in (ARRAY,LIST):
            to_type(self, Code(type=[ARRAY,STRING]), list[1])
            p[0]= Code(type=[NONE])
            return 
        check_code(self,list[0])
        check_code(self,list[1])
        declares+=list[0].declares
        declares+=list[1].declares
        #Codigo
        value='Perl.join('+to_string(list[0])+', '+list[1].value+')'
        p[0]=Code(value=value,st_value=value,type=[ARRAY,STRING],declares=declares,pos=Position(p,4),flags={STATEMENT:True})
        
    def p_function_keys_values(self,p):
        '''function_call : KEYS LPAREN list RPAREN
                        |  KEYS expression %prec UNITARY
                        |  VALUES LPAREN list RPAREN
                        |  VALUES expression %prec UNITARY'''
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        #Errores 
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1]) 
            p[0]=Code(type=[NONE])    
            return 
        #Aprovechamos la misma definicion ya que las funciones on casi identicas
        if p[1]=='keys':
            rtype=[ARRAY,STRING]
        else:
            rtype=[ARRAY]+p[3][0].type[1:]
        check_code(self,list[0])
        #Si no es un hash, forzamos un cast para lanzar un error
        if list[0].type[0]!=HASH:
            to_type(self, Code(type=[HASH]+list[0].type[1:]), list[1])
        #Codigo
        opt_paren(list[0])
        value='Perl.'+p[1]+'('+list[0].value+')'              
        p[0]=Code(value=value,st_value=value,type=rtype,declares=list[0].declares,pos=pos,flags={STATEMENT:True})
                
        
    def p_function_chomp(self,p):
        '''function_call : CHOMP LPAREN list RPAREN
                        |  CHOMP expression %prec UNITARY
                        |  CHOP LPAREN list RPAREN
                        |  CHOP expression %prec UNITARY'''
        #Aprovechamos la misma definicion ya que las funciones on casi identicas
        if p[1]=='chomp':
            rtype=[INTEGER]
        else:
            rtype=[STRING]
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        declares=[]
        args=''  
        var=list[0] 
        #Errores      
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1]) 
            p[0]=Code(type=[NONE])    
            return 
        if not list[0].variable:      
            error(self, 'FUNCTION_NATIVE_VAR', Position(p,1),n=1,function=p[1])
        #Codigo
        check_code(self,var)
        opt_paren(var)
        code=Code(type=rtype,declares=var.declares,pos=pos,flags={STATEMENT:True})   
        #Llamada sin uso de retorno
        code.st_value=var.value+' = '+to_type(self, var, Code(type=[STRING],value='Perl.chomp('+to_string(var)+')'))
        #Llamada con uso de retorno
        code.value='Perl.'+p[1]+'('
        #Realizamos la referenciacion
        update=arg_ref(self,code,[STRING],var)
        #Cerramos los parentesis dela funcion
        code.value+=')'
        #Funcion auxiliar para la actualizacion
        code.value='Pd.fe('+code.value+','+update+')'
        p[0]=code
        
    def p_function_each(self,p):
        'function_call :  LPAREN list RPAREN EQUALS EACH var_access'
        #Imports necesarios
        self.imports['Map']=True
        self.imports['Iterator']=True
        #Variables
        list=p[2]
        hash=create_value_var(p[6])
        pd_f1=get_function_var(self)
        pd_f2=get_function_var(self)
        #Errores
        if hash.type[0]!=HASH or len(list)!=2 or not list[1].variable or not list[0].variable:
            error(self,'EACH_ERROR',hash.pos) 
            p[0]=Code(type=[NONE])   
            return 
        check_code(self,hash)
        #Codigo
        code=Code(type=[NONE],pos=hash.pos,flags={STATEMENT:True})  
        #Variables para iterador y entrada
        code_entry=Code()
        code_it=Code()
        #Las inicializamos
        code_entry.value='Map.Entry<String, '+create_type(hash.type[1:])+'>'
        code_it.value='Iterator<'+code_entry.value+'> '+pd_f1+' = '+hash.value+'.entrySet().iterator()'
        code_entry.value+=' '+pd_f2
        #Comprobamos si existe siguietne
        code.value='('+pd_f1+'.hasNext())?Perl.each('
        #Cargamos la siguiente entrada
        code.value+=pd_f2+'='+pd_f1+'.next(),'
        #Preparamos la clave casteando al tipo de su variable
        code.value+=list[0].value+'='+to_type(self, list[0], Code(type=[STRING],value=pd_f2+'.getKey()'))+','
        #Preparamos el valor casteando al tipo de su variable
        code.value+=list[1].value+'='+to_type(self, list[1], Code(type=hash.type[1:],value=pd_f2+'.getValue()'))+'):false'
        code.value_opt=code.value
        #Declaraciones 
        code.declares=list[0].declares+list[1].declares+hash.declares+[code_it,code_entry]
        #Si la variable no esta asignada
        if not is_assign(self,list[0].variable.name):
            #Asignamos
            self.assigns[-1][list[0].variable.name]=True
            #Damos un valor por defecto
            code.declares.append(Code(value=list[0].value+' = null'))
        if not is_assign(self,list[1].variable.name):
            self.assigns[-1][list[1].variable.name]=True
            code.declares.append(Code(value=list[1].value+' = null'))
        p[0]=code
        
    def p_function_defined(self,p):
        '''function_call : DEFINED LPAREN list RPAREN
                        |  DEFINED expression %prec UNITARY'''
        #Variables
        if len(p)==5:
            list=p[3]
            exp=list[0]
            pos=Position(p,4)
        else:
            exp=p[2]
            list=[exp]
            pos=p[2].pos        
        #Argumetos        
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])
            p[0]=Code(type=[NONE])   
            return 
        check_code(self,exp,c_ref=False)
        #Codigo
        opt_paren(exp)
        value='Perl.defined('+exp.value+')'              
        p[0]=Code(value=value,st_value=value,type=[BOOLEAN],declares=exp.declares,pos=pos,flags={STATEMENT:True})
        
    def p_function_open(self,p):
        'function_call : OPEN LPAREN list RPAREN'
        #Variables
        list=p[3]
        declares=[]
        #Errores
        if len(list)!=3:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1]) 
            p[0]=Code(type=[NONE])  
            return 
        #Si no es un fichero
        if list[0].type[0]!=FILE or not list[0].variable:
            error(self,'NOT_FILE',list[0].pos,var=list[0].value)
            p[0]=Code(type=[NONE])  
            return
        check_code(self,list[0])
        #declaraciones
        declares=list[0].declares+list[1].declares+list[2].declares
        #crear descriptor si no existe, creamos uno
        if not is_assign(self, list[0], True):
            list[0].value+=' = new PerlFile()'
            self.assigns[-1][list[0].variable.name]=True 
        value='Perl.open('+list[0].value+', '+to_string(list[1])+', '+to_string(list[2])+')'
        p[0]=Code(value=value,st_value=value,type=[INTEGER],declares=declares,pos=Position(p,4),flags={STATEMENT:True})   
             
    def p_function_close(self,p):
        '''function_call : CLOSE LPAREN list RPAREN
                        | CLOSE expression %prec UNITARY'''
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        #Errores
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return
        check_code(self,list[0])
        #Si no es un fichero
        if list[0].type[0]!=FILE:
            error(self,'NOT_FILE',list[0].pos,var=list[0].value) 
        #cerrado del fichero
        opt_paren(list[0])
        value='Perl.close('+list[0].value+')'     
        p[0]=Code(value=value,st_value=value,type=[INTEGER],declares=list[0].declares,pos=pos,flags={STATEMENT:True})

    def p_function_sort_custom_head(self,p):
        'sort_head : SORT'
        #Creamos el contexto
        block_header(self)
        if 'a' not in self.declare_types:
            error(self, 'SORT_TYPE_A_ERROR', Position(p,1)) 
        else: 
            var=self.declare_types['a']
            #Las creamos automaticamnete
            self.variables[-1]['a']=Variable(var.type,var.pos,'a')
            self.variables[-1]['b']=Variable(var.type,var.pos,'b')
            #Las marcamos como asignadas
            self.assigns[-1]['a']=True
            self.assigns[-1]['b']=True
            #Borramos las declaraciones
            del self.declare_types['a']
            if 'b' in self.declare_types:
                del self.declare_types['b']

    def p_function_sort_custom(self,p):
        '''function_call : sort_head LBRACE expression RBRACE LPAREN list RPAREN
                        | sort_head LBRACE expression RBRACE expression %prec UNITARY'''
        #Variables
        cmp=p[3]
        if len(p)==8:
            list=p[6]
            exp=list[0]
            pos=Position(p,7)
        else:
            exp=p[5]
            list=[exp]
            pos=p[5].pos 
        #Errores
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return
        #Si no es un elemento ordenable
        if exp.type[0] not in (ARRAY,LIST):
            error(self,'SORT_ARRAY_ERROR',exp.pos)  
            p[0]=Code(type=[NONE])  
            return
        #Si el tipo no esta bien declarado
        if 'a' not in self.variables[-1] or not equals_type(exp.type[1:], self.variables[-1]['a'].type):
            error(self,'SORT_TYPE_ERROR',exp.pos,var=exp.value)  
            p[0]=Code(type=[NONE])  
            return        
        check_code(self,exp,c_ref=False)
        check_code(self,cmp)
        opt_paren(exp)
        #codigo   
        type=self.variables[-1]['a'].type
        #Creamos la funcion
        value='Perl.sort('+exp.value+', ('+create_type(type)+' a,'+create_type(type)+' b) ->'
        value+='{'+create_declare(cmp)+'return '+to_integer(cmp)+';})'
        #Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()
        #Generamos el codigo
        p[0]=Code(value=value,st_value=value,type=exp.type,declares=exp.declares,pos=pos,flags={STATEMENT:True}) 
        
    def p_function_sort(self,p):
        '''function_call : SORT LPAREN list RPAREN''' 
        #Variables
        list=p[3]
        pos=Position(p,4)
        #Errores
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return
        #Si no es un elemento ordenable
        if list[0].type[0] not in (ARRAY,LIST):
            error(self,'SORT_ARRAY_ERROR',list[0].pos)  
            p[0]=Code(type=[NONE])  
            return
        check_code(self,list[0],c_ref=False)
        opt_paren(list[0])
        #Generamos la funcion 
        value='Perl.sort('+list[0].value+')' 
        p[0]=Code(value=value,st_value=value,type=list[0].type,declares=list[0].declares,pos=pos,flags={STATEMENT:True})  
        
    def p_function_upper_lower(self,p):
        '''function_call : LC LPAREN list RPAREN
                        | LC expression %prec UNITARY
                        | LCFIRST  LPAREN list RPAREN
                        | LCFIRST  expression %prec UNITARY
                        | UC LPAREN list RPAREN
                        | UC expression %prec UNITARY
                        | UCFIRST  LPAREN list RPAREN
                        | UCFIRST  expression %prec UNITARY'''
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        #Errores
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return
        check_code(self,list[0])
        #cerrado del fichero
        opt_paren(list[0])
        value='Perl.'+p[1]+'('+to_string(list[0])+')'     
        p[0]=Code(value=value,st_value=value,type=[STRING],declares=list[0].declares,pos=pos,flags={STATEMENT:True})   
        
    def p_function_die(self,p):
        '''function_call : DIE LPAREN list RPAREN
                        | DIE expression %prec UNITARY'''
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        #Errores
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return
        check_code(self,list[0])
        #cerrado del fichero
        opt_paren(list[0])
        value='Perl.'+p[1]+'('+to_string(list[0])+')'     
        p[0]=Code(value=value,st_value=value,type=[INTEGER],declares=list[0].declares,pos=pos,flags={STATEMENT:True})     
           
    def p_function_delete(self,p):
        '''function_call : DELETE LPAREN list RPAREN
                        | DELETE expression %prec UNITARY'''
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        #Errores
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return
        #Tiene que ser una variable y la dimension accedida un hash
        if  not list[0].variable or len(list[0].type)>1 or (len(list[0].variable.type)>1 and list[0].variable.type[-2]!=HASH):
            error(self,'DELETE_NOT_HASH',list[0].pos)
            p[0]=Code(type=[NONE])  
            return        
        
        check_code(self,list[0],c_ref=False)
        #cerrado del fichero
        opt_paren(list[0])
        value=re.sub(r'(.*)\.get\((.*)\)$', r'Perl.delete(\1,\2)', list[0].value)
        p[0]=Code(value=value,st_value=value,type=list[0].type,declares=list[0].declares,pos=pos,flags={STATEMENT:True})   
        
    def p_function_exists(self,p):
        '''function_call : EXISTS LPAREN list RPAREN
                        | EXISTS expression %prec UNITARY'''
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        #Errores
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return
        check_code(self,list[0],c_ref=False)
        #cerrado del fichero
        opt_paren(list[0])
        value='('+list[0].value+' != null)'
        p[0]=Code(value=value,st_value=value,type=[BOOLEAN],declares=list[0].declares,pos=pos,flags={STATEMENT:True})          
        
    def p_function_exit(self,p):
        '''function_call : EXIT LPAREN list RPAREN
                        | EXIT expression %prec UNITARY'''
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        #Errores
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return
        check_code(self,list[0],c_ref=False)
        #cerrado del fichero
        opt_paren(list[0])
        value='Perl.exit('+to_integer(list[0])+')'
        p[0]=Code(value=value,st_value=value,type=[INTEGER],declares=list[0].declares,pos=pos,flags={STATEMENT:True})             
        
    def p_function_length_system(self,p):
        '''function_call : LENGTH LPAREN list RPAREN
                        |  LENGTH expression %prec UNITARY
                        |  SYSTEM LPAREN list RPAREN
                        |  SYSTEM expression %prec UNITARY'''
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        #Errores
        if len(list)!=1:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return
        check_code(self,list[0],c_ref=False)
        #cerrado del fichero
        opt_paren(list[0])
        value='Perl.'+p[1]+'('+to_string(list[0])+')'
        p[0]=Code(value=value,st_value=value,type=[INTEGER],declares=list[0].declares,pos=pos,flags={STATEMENT:True})        
 
    def p_function_substr(self,p):
        'function_call : SUBSTR LPAREN list RPAREN'   
        list=p[3]
        pos=p[3][-1].pos
        declares=[]
        #Errores
        if len(list) not in (2,3,4):
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return    
        check_code(self,list[0])
        check_code(self,list[1])  
        declares+=list[0].declares
        declares+=list[1].declares
        #codigo
        value=to_integer(list[1])
        #Formato de la funcion
        code=Code(type=list[0].type,declares=declares,pos=pos,flags={STATEMENT:True})  
        #Si tiene mas argumentos
        if len(p)>3:
            check_code(self,list[2])  
            declares+=list[2].declares
            value+=', '+to_integer(list[2])
            if len(p)>4:
                check_code(self,list[3])  
                declares+=list[3].declares
                value+=', '+to_string(list[2])
                #Llamada sin uso de retorno
                code.st_value=list[0].value+' = '+'Perl.substr('+to_string(list[0])+', '+value+')'
                #Llamada con uso de retorno
                code.value='Perl.substr('
                #Realizamos la referenciacion
                update=arg_ref(self,code,list[0].type,list[0])
                #Cerramos los parentesis dela funcion
                code.value+=')'
                #Funcion auxiliar para la actualizacion
                code.value='Pd.fe('+code.value+','+update+')'                
            else:
                code.value=code.st_value='Perl.substr('+to_string(list[0])+', '+value+')'
        else:
            code.value=code.st_value='Perl.substr('+to_string(list[0])+', '+value+')'
        p[0]=code
        
    def p_function_splice(self,p):
        'function_call : SPLICE LPAREN list RPAREN'   
        list=p[3]
        pos=p[3][-1].pos
        declares=[]
        #Errores
        if len(list) not in (2,3,4):
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return    
        if not list[0].variable:      
            error(self, 'FUNCTION_NATIVE_VAR', Position(p,1),n=1,function=p[1])
        #Si no es un array o list, forzamos un cast para lanzar un error
        if list[0].type[0] not in (ARRAY,LIST):
            to_type(self, Code(type=[ARRAY]+list[0].type[1:]), list[1])
        check_code(self,list[0])
        check_code(self,list[1])  
        declares+=list[0].declares
        declares+=list[1].declares
        #codigo
        value=to_integer(list[1])
        #Si tiene mas argumentos
        if len(p)>3:
            check_code(self,list[2])  
            declares+=list[2].declares
            value+=', '+to_integer(list[2])
            if len(p)>4:
                #Errores del ultimo argumento
                if list[3].type[0] not in (ARRAY,LIST):
                    #Cast para forzar un error
                    to_type(self, Code(type=[ARRAY]+list[3].type[1:]), list[1])
                elif not equals_type(list[0].type[1:], list[3].type[1:]):
                    error(self,'COLECTION_CONCAT_ERROR',list[3].pos,funct='splice')
                check_code(self,list[3])  
                declares+=list[3].declares
                value+=', '+list[2].value
        #Formato de la funcion
        code=Code(type=list[0].type,declares=declares,pos=pos,flags={STATEMENT:True})     
        #Llamada sin uso de retorno
        code.st_value=list[0].value+' = '+'Perl.splice('+list[0].value+', '+value+')'
        #Llamada con uso de retorno
        code.value='Perl.splice('
        #Realizamos la referenciacion
        update=arg_ref(self,code,list[0].type,list[0])
        #Cerramos los parentesis dela funcion
        code.value+=')'
        #Funcion auxiliar para la actualizacion
        code.value='Pd.fe('+code.value+','+update+')'
        p[0]=code
        
    def p_function_push_unshift(self,p):
        '''function_call : PUSH LPAREN list RPAREN
                        |  UNSHIFT LPAREN list RPAREN''' 
        list=p[3]
        pos=p[3][-1].pos
        declares=[]
        #Errores
        if len(list) != 2:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return    
        if not list[0].variable:      
            error(self, 'FUNCTION_NATIVE_VAR', Position(p,1),n=1,function=p[1])
        #Si no es un array o list, forzamos un cast para lanzar un error
        if list[0].type[0] not in (ARRAY,LIST):
            to_type(self, Code(type=[ARRAY]+list[0].type[1:]), list[1])
        #Para poder añadir debe ser del mismo tipo o del tipo del contenido
        if  (len(list[1].type) >1 and not equals_type(list[0].type[1:], list[1].type) and 
            not (equals_type(list[0].type[1:], list[1].type[1:]) 
            and list[0].type[0] in (ARRAY,LIST) and list[1].type[0] in (ARRAY,LIST))):
            error(self,'COLECTION_CONCAT_ERROR',list[1].pos,funct=p[1])
            p[0]=Code(type=[NONE])  
            return  
        check_code(self,list[0])
        check_code(self,list[1])  
        declares+=list[0].declares
        declares+=list[1].declares
        #Codigo
        code=Code(type=[INTEGER],declares=list[0].declares,pos=pos,flags={STATEMENT:True}) 
        #Si no concatena tiene que castear
        if len(list[0].type) > len(list[1].type):
            elem=to_type(self, Code(type=list[0].type[1:]), list[1])
        else:
            elem=list[1].value
        if list[0].type[0] == LIST:
            code.value=code.st_value='Perl.'+p[1]+'('+list[0].value+', '+elem+')'
        else:
            #Llamada sin uso de retorno
            code.st_value=list[0].value+' = '+'Perl.'+p[1]+'('+list[0].value+', '+elem+')'
            #Llamada con uso de retorno
            code.value='Perl.'+p[1]+'('
            #Realizamos la referenciacion
            update=arg_ref(self,code,list[0].type,list[0])
            #Cerramos los parentesis dela funcion
            code.value+=')'
            #Funcion auxiliar para la actualizacion
            code.value='Pd.fe('+code.value+','+update+')'
        p[0]=code
        
    def p_function_pop_shirft(self,p):
        '''function_call : POP LPAREN list RPAREN
                        |  POP expression %prec UNITARY
                        |  SHIRFT LPAREN list RPAREN
                        |  SHIRFT expression %prec UNITARY''' 
        #Variables
        if len(p)==5:
            list=p[3]
            pos=Position(p,4)
        else:
            list=[p[2]]
            pos=p[2].pos
        #Errores
        if len(list) != 2:
            error(self, 'FUNCTION_NATIVE_ERROR', Position(p,1),function=p[1])   
            p[0]=Code(type=[NONE])  
            return    
        if not list[0].variable:      
            error(self, 'FUNCTION_NATIVE_VAR', Position(p,1),n=1,function=p[1])  
        #Si no es un array o list, forzamos un cast para lanzar un error
        if list[0].type[0] not in (ARRAY,LIST):
            to_type(self, Code(type=[ARRAY]+list[0].type[1:]), list[1])      
        
        code=Code(type=list[0].type[1:],declares=list[0].declares,pos=pos,flags={STATEMENT:True})     
        #Llamada sin uso de retorno
        code.st_value=list[0].value+' = '+'Perl.'+p[1]+'('+list[0].value+')'
        #Llamada con uso de retorno
        code.value='Perl.'+p[1]+'('
        #Realizamos la referenciacion
        update=arg_ref(self,code,list[0].type,list[0])
        #Cerramos los parentesis dela funcion
        code.value+=')'
        #Funcion auxiliar para la actualizacion
        code.value='Pd.fe('+code.value+','+update+')'
        p[0]=code
 
#Funciones con mas de un argumento para que el lexer pueda emular los parentesis        
perlArgs={
'JOIN':2,
'OPEN':3,
'PRINT':-1,
'PUSH':2,
'SAY':-1,
'SPLICE':4,
'SPLIT':2,
'SUBSTR':4,
'UNSHIFT':2,
}

   

    