#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import unittest.mock as Mock
from libs import Auxiliary as Aux
from libs import Parser
from libs import Code
from doublex.pyDoubles import method_returning


class TestAuxiliary(unittest.TestCase):


    def setUp(self):
        self.parser = Parser()

    def test_identer(self):
        # Comprbar si identa
        input = "{\n{\na++;\n}\n}"
        expected = "{\n    {\n        a++;\n    }\n}"
        output = Aux.identer(input)
        self.assertEqual(expected, output, "La identancion no es correcta")

    @Mock.patch('libs.messages.Messages.error', method_returning(None))
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


        

