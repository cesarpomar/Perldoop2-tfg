#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright 2016 César Pomar <cesarpomar18@gmail.com>
#
#This file is part of Perldoop.
#
#Perldoop is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Perldoop is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Perldoop.  If not, see <http://www.gnu.org/licenses/>.

from libs import Auxiliary as Aux
from libs import Casting as Cst
from libs import DataType as Dtp
from libs import Messages as Msg
from libs import Variables as Var
from libs import Collection as Coll
from libs import Statements as Sts  
from libs import Position
from libs import Code


class Hadoop():
    
    hd_types = {
    Dtp.BOOLEAN:'BooleanWritable',
    Dtp.INTEGER:'IntWritable',
    Dtp.LONG:'LongWritable',
    Dtp.FLOAT:'FloatWritable',
    Dtp.DOUBLE:'DoubleWritable',
    Dtp.STRING:'Text',
    }    
    def __init__(self):  
        super().__init__() 
        self.hadoop_type = [Dtp.STRING, Dtp.STRING, Dtp.STRING, Dtp.STRING]  # Tipo para mapper o reducer
        self.mapper_code = False  # Existe codigo de mapper
        self.mapper_loop = False  # Existe un loop mapper
        self.reducer_op = None  # Codigo para reduccion
        self.reducer_change = None  # Codigo para cada clave
        self.reducer_key = None  # Clave del reducer
        self.reducer_value = None  # Value actual del reducer
    
    def p_mapper_init(self, p):
        '''mapper_init : MAPPER_CODE
                        | MAPPER_CODE TYPE TYPE TYPE'''        
        if self.extend_class:
            Msg.error(self, 'ALREADY_EXTENDS', Position(p, 1))
        self.mapper_code = True
        if len(self.variables) > 1:
            Msg.error(self, 'SPECIAL_LOCAL_BLOCK', Position(p, 1))
        # Si especifica tipo, cambiamos el por defecto
        if len(p) > 2:
            self.hadoop_type = [Dtp.STRING, Dtp.var_types[p[2]], Dtp.var_types[p[3]], Dtp.var_types[p[4]]]
        self.imports['Mapper'] = True
        self.imports['HadoopIO'] = True
        self.imports['HadoopContext'] = True
        self.imports['IOException'] = True
            
    def p_reducer_init(self, p):
        '''reducer_init : REDUCER_CODE
                        | REDUCER_CODE TYPE TYPE TYPE TYPE'''
        # Si especifica tipo, cambiamos el por defecto
        if len(p) > 2:
            self.hadoop_type = [Dtp.var_types[p[2]], Dtp.var_types[p[3]], Dtp.var_types[p[4]], Dtp.var_types[p[5]]]
    
    def p_mapper_code(self, p):
        'statement_type : mapper_init LBRACE block_header statements RBRACE'
        # Extendemos la clase
        self.extend_class = 'Mapper<Object,' + self.hd_types[self.hadoop_type[1]] + ','
        self.extend_class += self.hd_types[self.hadoop_type[2]] + ',' + self.hd_types[self.hadoop_type[3]] + '>'
        # Notacion de sobrescritura
        header = '@Override\n'
        # Cabecera del metodo
        header += 'public void map(Object pd_key, ' + self.hd_types[self.hadoop_type[1]] + ' pd_value, Context pd_context) throws IOException, InterruptedException'
        # Creamos la funcion
        function = header + '{\ntry{\n' + p[4].value + '}catch(Exception e){\nSystem.out.println(e.toString());\n}\n}\n\n'
        # Creamos la funcion
        self.functions_code = function + self.functions_code
        # Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()    
        # El codigo no se propaga
        p[0] = Code()
        
    def p_mapper_loop_head(self, p):
        'loop_head : MAPPER_LOOP WHILE LPAREN var_access EQUALS STDIN RPAREN'  
        if not self.mapper_code:
            Msg.error(self, 'HD_MAPPER_LOOP_ALONE', Position(p, 1))
        elif self.mapper_loop:
            Msg.error(self, 'HD_MAPPER_MANY_LOOP', Position(p, 1))
        # Cogemos el valor del mapper  
        if self.hadoop_type[1] == Dtp.STRING:
            code = Sts.equals(self, p[4], Code(type=[self.hadoop_type[1]], value='pd_value.toString()'))    
        else:
            code = Sts.equals(self, p[4], Code(type=[self.hadoop_type[1]], value='pd_value.get()'))    
        # Podemos las declaraciones del codigo
        code.value = Aux.create_declare(code) + code.value + ';\n'
        # Las borramos
        code.declares = []
        p[0] = code 
    
    def p_mapper_loop(self, p):
        'block : loop_head LBRACE statements RBRACE'
        self.mapper_loop = True
        if Dtp.NEXT in p[3].flags or Dtp.LAST in p[3].flags:
            Msg.error(self, 'HD_NEXT_LAST', Position(p, 2))
        # Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()
        # Unimos las sentencias de la cabeceracon las del bloque
        p[0] = p[1]
        p[0].value = '{\n' + p[0].value + p[3].value + '}\n'
        
    def p_hadoop_print(self, p):
        'function_call : HADOOP_PRINT PRINT LPAREN list RPAREN'
        if len(p[4]) == 4:
            # Cojemos los argumentos
            list = p[4]
            Aux.check_code(self, list[0])
            Aux.check_code(self, list[2])
            # Creamos el codigo
            p[0] = list[0] + list[2]
            p[0].type = [Dtp.INTEGER]
            p[0].value = 'pd_context.write(new ' + self.hd_types[self.hadoop_type[2]] + '(' + Cst.to_type(self, Code(type=[self.hadoop_type[2]]), list[0]) + ')'
            p[0].value += ', new ' + self.hd_types[self.hadoop_type[3]] + '(' + Cst.to_type(self, Code(type=[self.hadoop_type[3]]), list[2]) + '))'
            p[0].st_value = p[0].value
        else:
            Msg.error(self, 'HD_PRINT', Position(p, 2))
            p[0] = Code(type=[Dtp.NONE])
        
    def p_reducer_if(self, p):
        'block : REDUCER_OP block_header LBRACE statements RBRACE'
        # Coge el campo con el codigo ejecutable
        self.reducer_op = p[4]
        # Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()
        p[0] = Code()
        self.imports['Reducer'] = True
        
    def p_reducer_change(self, p):
        'block : REDUCER_CHANGE LBRACE block_header statements RBRACE'
        # Coge el bloque con el final del reducer
        self.reducer_change = p[4]
        # Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()
        p[0] = Code()
        self.imports['Reducer'] = True
        
    def p_reducer_key(self, p):
        'statement_type : labels_line list post_block SEMI REDUCER_KEY line_comment '
        # Variable key
        if p[2][0].declares:
            var = p[2][0].declares[0] 
            self.reducer_key = Code(value = var.variable.name, type = var.type)
            # Si no ha sido inicializada, lo hacemos con null
            if not self.reducer_key.value in self.assigns[-1]:
                self.assigns[-1][self.reducer_key.value] = True
                p[2][0].declares[0] = Code(value=self.reducer_key.value + ' = null', type=self.reducer_key.type)
                
        else:
            Msg.error(self, 'HD_REDUCER_KEY', Position(p, 5))
        p[0] = Sts.create_statement(self, p[2], p[3], p[6], Position(p, 4)) 
        
    def p_reducer_value(self, p):   
        'statement_type : labels_line list post_block SEMI REDUCER_VALUE line_comment '  
        # Variable value
        if p[2][0].declares:
            var = p[2][0].declares[0] 
            self.reducer_value = Code(value = var.variable.name, type = var.type)
            # Si no ha sido inicializada, lo hacemos con null  
            if not self.reducer_value.value in self.assigns[-1]:
                self.assigns[-1][self.reducer_value.value] = True
                p[2][0].declares[0] = Code(value=self.reducer_value.value + ' = null', type=self.reducer_value.type)
        else:
            Msg.error(self, 'HD_REDUCER_VALUE', Position(p, 5))  
        p[0] = Sts.create_statement(self, p[2], p[3], p[6], Position(p, 4))  
            
    def p_reducer_code(self, p):
        'block : reducer_init LBRACE block_header REDUCER_VAR statements REDUCER_VAR statements RBRACE'
        self.imports['HadoopTypes'] = True
        # Genera el reducer con la union de los bloques
        if not(self.reducer_op and self.reducer_change and self.reducer_key and self.reducer_value):
            Msg.error(self, 'HD_REDUCER_INCOMPLETE', Position(p, 4)) 
            p[0] = Code()
            return
        if self.extend_class:
            Msg.error(self, 'ALREADY_EXTENDS', Position(p, 1))            
        # Extendemos la clase
        self.extend_class += 'Reducer<' + self.hd_types[self.hadoop_type[0]] + ',' + self.hd_types[self.hadoop_type[1]] + ','
        self.extend_class += self.hd_types[self.hadoop_type[2]] + ',' + self.hd_types[self.hadoop_type[3]] + ',' + '>'
        # Notacion de sobrescritura
        header = '@Override\n'
        # Cabecera del metodo
        header += 'public void reduce(' + self.hd_types[self.hadoop_type[0]] + ' pd_key, Iterable<' + self.hd_types[self.hadoop_type[1]]        
        header += '> pd_value, Context pd_context) throws IOException, InterruptedException'
        # Cuerpo del medoto
        body = p[5].value
        # Igualizamos la clave a la del reduce
        body += self.reducer_key.value + ' = ' + Cst.to_type(self, self.reducer_key, Code(type=[self.hadoop_type[0]], value='pd_key.get()')) + ';\n'
        # pedimos una variable auxiliar
        aux = Var.get_loop_var(self)
        body += 'for(' + self.hd_types[self.hadoop_type[1]] + ' ' + aux + ' : pd_value){\n'
        # Igualamos el valor al del reduce
        body += self.reducer_value.value + ' = ' + Cst.to_type(self, self.reducer_value, Code(type=[self.hadoop_type[1]], value=aux+'.get()')) + ';\n'
        body += self.reducer_op.value + '}\n'
        body += self.reducer_change.value
        # Creamos la funcion
        self.functions_code = header + '{\n' + body + '}\n\n'
        # Borramos todo sobre las variables dentro del bloque
        self.assigns.pop()
        self.variables.pop()  
        # No produce codido
        p[0] = Code()
        
        
        
        
        
        
        
        
        
        
        
        
