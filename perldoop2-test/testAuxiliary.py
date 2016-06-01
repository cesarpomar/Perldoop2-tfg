#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import unittest.mock as Mock
from libs import Auxiliary as Aux
from libs import DataType as Dtp
from libs import Parser
from libs import Lexer
from libs import Code
from libs import Variable
from doublex.pyDoubles import method_returning, method_raising
from Utils import *



class TestAuxiliary(unittest.TestCase):


    def setUp(self):
        self.parser = Parser()
        
    def called(self):
        if self.call:
            self.call+=1
        else:
            self.call=1

    def test_identer(self):
        # Comprbar si identa
        input = "{\n{\na++;\n}\n}"
        expected = "{\n    {\n        a++;\n    }\n}"
        output = Aux.identer(input)
        self.assertEqual(expected, output, "La identancion no es correcta")

    @Mock.patch('libs.Messages.error', method_returning(None))
    def test_check_unreachable(self):
        # Casos a detectar
        input = '''
        {
        return 1;
        i++;
        }
        '''
        self.parser.unreachable_code = True
        Aux.check_unreachable(self.parser, Code(value=input))
        self.assertFalse(self.parser.unreachable_code, "Codigo inalcanzable no detectado")
        input = '''
        {
        break;
        i++;
        }
        '''
        self.parser.unreachable_code = True
        Aux.check_unreachable(self.parser, Code(value=input))
        self.assertFalse(self.parser.unreachable_code, "Codigo inalcanzable no detectado")
        input = '''
        {
        continue;
        i++;
        }
        '''
        self.parser.unreachable_code = True
        Aux.check_unreachable(self.parser, Code(value=input))
        self.assertFalse(self.parser.unreachable_code, "Codigo inalcanzable no detectado")
        input = '''
        {
        {
        return 1;
        }
        i++;
        }
        '''
        self.parser.unreachable_code = True
        Aux.check_unreachable(self.parser, Code(value=input))
        self.assertFalse(self.parser.unreachable_code, "Codigo inalcanzable no detectado")
        input = '''
        {
        do{
        return 1;
        }
        i++;
        }
        '''
        self.parser.unreachable_code = True
        Aux.check_unreachable(self.parser, Code(value=input))
        self.assertFalse(self.parser.unreachable_code, "Codigo inalcanzable no detectado")
        input = '''
        {
        do{
        break;
        return 1;
        }
        }
        '''
        self.parser.unreachable_code = True
        Aux.check_unreachable(self.parser, Code(value=input))
        self.assertFalse(self.parser.unreachable_code, "Codigo inalcanzable no detectado")        
        # Posibles falsos positivos
        input = '''
        {
        if(true){
        return 1;
        }
        i++;
        }
        '''
        self.parser.unreachable_code = True
        Aux.check_unreachable(self.parser, Code(value=input))
        self.assertTrue(self.parser.unreachable_code, "Codigo inalcanzable falso positivo")

    @Mock.patch('libs.Casting.create_type', method_returning("String"))
    def test_create_declare(self):
        declare=Code(value="x",type=[Dtp.STRING])
        code=Code(declares=[declare])
        expected=Aux.create_declare(code)
        self.assertEqual(expected, "String x;\n", "la varaible no se declara correctamente con tipo")
        declare=Code(value="String x")
        code=Code(declares=[declare])
        expected=Aux.create_declare(code)
        self.assertEqual(expected, "String x;\n", "la varaible no se declara correctamente sin tipo")
     
    @Mock.patch('libs.Messages.error', fake_error)   
    @Mock.patch('libs.Variables.is_assign', method_returning(False))     
    def test_check_code(self):
        code=Code(type=[Dtp.STRING])
        code.variable=Variable()
        #Variable sin asignar usada        
        try:
            Aux.check_code(self.parser, code)  
            self.fail("Variable sin asignar no detectada")
        except Called as called:
            self.assertEqual(called.message, 'READ_BEFORE_ASSIGN', "mensaje errroneo")  
        code=Code(type=[Dtp.REF])
        try:
            Aux.check_code(self.parser, code, c_ref=True)  
            self.fail("Chequeo de puntero erroneo")
        except Called as called:
            self.assertEqual(called.message, 'REF_OPERATION', "mensaje errroneo")  
        code=Code(type=[Dtp.STRING],ref=True)
        try:
            Aux.check_code(self.parser, code, c_ref=True)  
            self.fail("Chequeo de puntero erroneo por colecion")
        except Called as called:
            self.assertEqual(called.message, 'REF_OPERATION', "mensaje errroneo")  
    
    def test_create_imports(self):
        parser=self.parser
        parser.imports["Map"]=True
        expected="import perldoop.*;\nimport java.util.Map;\n\n"
        self.assertEqual(expected, Aux.create_imports(parser), "Los import se han creado incorrectamente")
    
    @Mock.patch('libs.Messages.error', fake_error)     
    def test_declare_package(self):
        parser=Parser()
        try:
            Aux.declare_package(parser, None, None)
            self.fail("Chequeo de puntero erroneo")
        except Called as called:
            self.assertEqual(called.message, 'REF_OPERATION', "mensaje errroneo") 
        
        
    
        

