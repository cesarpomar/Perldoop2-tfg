#!/usr/bin/python
# -*- coding: utf-8 -*-
from libs.Auxiliary import *
from libs.Blocks import *
from libs.Datatypes import *
from libs.Collection import *
from libs.Statements import *
from libs.Casting import to_type

hd_types={
BOOLEAN:'BooleanWritable',
INTEGER:'IntWritable',
LONG:'LongWritable',
FLOAT:'FloatWritable',
DOUBLE:'DoubleWritable',
STRING:'Text',                    
}

class Hadoop():
    
    def __init__(self):  
        super().__init__() 
        self.hadoop_type=[STRING,STRING,STRING,STRING]  #Tipo para mapper o reducer
        self.mapper_code=False     #Existe codigo de mapper
        self.reducer_op=None       #Codigo para reduccion
        self.reducer_change=None   #Codigo para cada clave
        self.reducer_vars=None     #Clave del reducer
        self.reducer_key=None      #Clave del reducer
        self.reducer_value=None    #Value actual del reducer
    
    def p_mapper_init(self,p):
        '''mapper_init : MAPPER_CODE
                        | MAPPER_CODE TYPE TYPE TYPE'''        
        if self.extend_class:
            error(self,'ALREADY_EXTENDS',Position(p,1))
        self.mapper_code=True
        if len(self.variables)>1:
            error(self,'SPECIAL_LOCAL_BLOCK',Position(p,1))
        #Si especifica tipo, cambiamos el por defecto
        if len(p)>2:
            self.hadoop_type=[STRING,var_types[p[2]],var_types[p[3]],var_types[p[4]]]
            
    def p_reducer_init(self,p):
        '''reducer_init : REDUCER_CODE
                        | REDUCER_CODE TYPE TYPE TYPE TYPE'''
        #Si especifica tipo, cambiamos el por defecto
        if len(p)>2:
            self.hadoop_type=[var_types[p[2]],var_types[p[3]],var_types[p[4]],var_types[p[5]]]
    
    def p_mapper_code(self,p):
        'statement_type : mapper_init LBRACE block_header statements RBRACE'
        #Extendemos la clase
        self.extend_class='Mapper<Object,'+hd_types[self.hadoop_type[1]]+','
        self.extend_class+=hd_types[self.hadoop_type[2]]+','+hd_types[self.hadoop_type[3]]+','+'>'
        #Notacion de sobrescritura
        header='@Override\n'
        #Cabecera del metodo
        header+='public void map(Object pd_key, '+hd_types[self.hadoop_type[1]]+' pd_value, Context pd_context) throws IOException, InterruptedException'
        #Creamos la funcion
        function=header+'{\ntry{\n'+p[4].value+'}catch(Exception e){\nSystem.out.println(e.toString());\n}\n}\n\n'
        #Creamos la funcion
        self.functions_code=function+self.functions_code
        #Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()    
        #El codigo no se propaga
        p[0]=Code()
        
    def p_mapper_loop_head(self,p):
        'loop_head : MAPPER_LOOP WHILE LPAREN var_access EQUALS STDIN RPAREN'  
        if not self.mapper_code:
            error(self,'HD_MAPPER_LOOP_ALONE',Position(p,1))
        elif self.mapper_type:
            error(self,'HD_MAPPER_MANY_LOOP',Position(p,1))
        #Cogemos el valor del mapper  
        code=equals(self, p[4], Code(type=[hd_types[self.hadoop_type[1]]],value='pd_value.get()'))    
        #Podemos las declaraciones del codigo
        code.value='{\n'+create_declare(self,code)+code.value+'}\n'
        #Las borramos
        code.declares=[]
        p[0]=code 
    
    def p_mapper_loop(self,p):
        'block : loop_head LBRACE statements RBRACE'
        if NEXT in p[3].flags or LAST in p[3].flags:
            error(self, 'HD_NEXT_LAST', Position(p,2))
        #Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()
        #Unimos las sentencias de la cabeceracon las del bloque
        p[0]=p[1]
        p[0].value+=p[3].value
        
    def p_hadoop_print(self,p):
        'function_call : HADOOP_PRINT PRINT LPAREN list RPAREN'
        if len(p[4])==4:
            #Cojemos los argumentos
            list=p[4]
            check_code(self,list[0])
            check_code(self,list[2])
            #Creamos el codigo
            p[0]=list[0]+list[2]
            p[0].type=[INTEGER]
            p[0].value='pd_context.write(new '+hd_types[self.hadoop_type[2]]+'('+to_type(self,Code(type=[self.hadoop_type[2]]),list[0])
            p[0].value+=', new '+hd_types[self.hadoop_type[3]]+'('+to_type(self,Code(type=[self.hadoop_type[3]]),list[2])+'))'
            p[0].st_value=p[0].value
        else:
            error(self, 'HD_PRINT', Position(p,2))
            p[0]=Code(type=[NONE])
        
    def p_reducer_if(self,p):
        'block : REDUCER_OP block_header LBRACE statements RBRACE'
        #Coge el campo con el codigo ejecutable
        self.reducer_op=p[4]
        #Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()
        p[0]=Code()
        
    def p_reducer_change(self,p):
        'block : REDUCER_CHANGE LBRACE block_header statements RBRACE'
        #Coge el bloque con el final del reducer
        self.reducer_change=p[4]
        #Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()
        p[0]=Code()
        
    def p_reducer_key(self,p):
        'statement_type : labels_line list post_block SEMI REDUCER_KEY line_comment '
        #Variable key
        if p[2][0].declares:
            #Cogemos la declaracion
            self.reducer_key=p[2][0].declares[0]
            #Si no ha sido inicializada, lo hacemos con null
            if not self.reducer_key.value in self.assigns[-1]:
                self.assigns[-1][self.reducer_key.value]=True
                p[2][0].declares[0]=Code(value=self.reducer_key.value+' = null',type=self.reducer_key.type)
                
        else:
            error(self,'HD_REDUCER_KEY',Position(p,5))
        p[0]=create_statement(self,p[2],p[3],p[6],Position(p,4)) 
        
    def p_reducer_value(self,p):   
        'statement_type : labels_line list post_block SEMI REDUCER_VALUE line_comment '  
        #Variable value
        if p[2][0].declares:
            self.reducer_value=p[2][0].declares[0] 
            #Si no ha sido inicializada, lo hacemos con null  
            if not self.reducer_value.value in self.assigns[-1]:
                self.assigns[-1][self.reducer_value.value]=True
                p[2][0].declares[0]=Code(value=self.reducer_value.value+' = null',type=self.reducer_key.type)
        else:
            error(self,'HD_REDUCER_VALUE',Position(p,5))  
        p[0]=create_statement(self,p[2],p[3],p[6],Position(p,4))  
            
    def p_reducer_code(self,p):
        'block : reducer_init LBRACE block_header REDUCER_VAR statements REDUCER_VAR statements RBRACE'
        #Genera el reducer con la union de los bloques
        if not(self.reducer_op and self.reducer_change and self.reducer_key and self.reducer_value) and self.reducer_vars:
            error(self,'HD_REDUCER_INCOMPLETE',Position(p,1)) 
            p[0]=Code()
            return
        if self.extend_class:
            error(self,'ALREADY_EXTENDS',Position(p,1))            
        #Extendemos la clase
        self.extend_class+='Reducer<'+hd_types[self.hadoop_type[0]]+','+hd_types[self.hadoop_type[1]]+','
        self.extend_class+=hd_types[self.hadoop_type[2]]+','+hd_types[self.hadoop_type[3]]+','+'>'
        #Notacion de sobrescritura
        header='@Override\n'
        #Cabecera del metodo
        header+='public void reduce('+hd_types[self.hadoop_type[0]]+' pd_key, Iterable<'+hd_types[self.hadoop_type[1]]        
        header+='> pd_value, Context pd_context) throws IOException, InterruptedException'
        #Cuerpo del medoto
        body=p[5].value
        #Igualizamos la clave a la del reduce
        body+=self.reducer_key.value+' = '+to_type(self, self.reducer_key, Code(type=[self.hadoop_type[0]],value='pd_key.get()'))+';\n'
        #pedimos una variable auxiliar
        aux=get_loop_var(self)
        body+=hd_types[self.hadoop_type[1]]+' '+aux+';\n'
        body+='for('+aux+':pd_value){\n'
        #Igualamos el valor al del reduce
        body+=self.reducer_value.value+' = '+to_type(self, self.reducer_value, Code(type=[self.hadoop_type[1]],value='pd_value.get()'))+';\n'
        body+=self.reducer_op.value+'}\n'
        body+=self.reducer_change.value
        #Creamos la funcion
        self.functions_code=header+'{\n'+body+'}\n\n'
        #Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()  
        #No produce codido
        p[0]=Code()
        
        
        
        
        
        
        
        
        
        
        
        