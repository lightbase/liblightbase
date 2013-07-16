import unittest
from datetime import datetime
from liblightbase.lbbase import Base
from liblightbase.lbbase.campos import *
from liblightbase.lbbase.xml import *
from liblightbase.lbbase.json import *
import os.path
from xml.dom.minidom import parse, parseString

class XMLTestCase(unittest.TestCase):
    """
    Unity tests for Base
    """
    def setUp(self):
        """
        Set up test data
        """
        objeto = list()
                        
        # First <campo>
        indice = Indice(indice='Palavra')
        indexacao = list()
        indexacao.append(indice)
        
        tipo = Tipo(tipo='Texto')
        
        campo = Campo(nome='nome',
                      descricao='Esse é o nome da pessoa',
                      tipo=tipo,
                      indexacao=indexacao
                      )
        
        objeto.append(campo)
        
        # Second <campo>
        indice = Indice(indice='Unico')
        indexacao = list()
        indexacao.append(indice)
        
        tipo = Tipo(tipo='Inteiro')
        
        campo = Campo(nome='cpf',
                      descricao='Esse é o CPF da pessoa',
                      tipo=tipo,
                      indexacao=indexacao
                      )

        objeto.append(campo)
        
        # Now add a multivalued field
        indice = Indice(indice='Palavra')
        indexacao = list()
        indexacao.append(indice)
        
        tipo = Tipo(tipo='Texto')
        
        dependente_nome = Campo(nome='nome',
                      descricao='Esse é o nome do dependente',
                      tipo=tipo,
                      indexacao=indexacao
                      )
        
        indice = Indice(indice='Ordenado')
        indexacao = list()
        indexacao.append(indice)
        
        tipo = Tipo(tipo='Data')
        
        dependente_nasc = Campo(nome='datanascimento',
                      descricao='Essa é a data de nascimento do dependente',
                      tipo=tipo,
                      indexacao=indexacao
                      )
        
        objeto_dep = list()
        objeto_dep.append(dependente_nome)
        objeto_dep.append(dependente_nasc)
        objeto_dep = CampoObjeto(objeto=objeto_dep)
        
        # Add this objeto to a regular <campo>
        campo = Campo(
                      nome='dependentes',
                      descricao='Dependentes da pessoa',
                      objeto=objeto_dep
                      )
        
        objeto.append(campo)
        
        # Finally create <objeto>
        objeto = CampoObjeto(objeto=objeto)
        
        self.base = Base(
                    nome='Pessoa',
                    descricao='Base que armazena informações de pessoas',
                    senha='@$!@#%fhbhfdh54745754',
                    objeto=objeto
                    )
        
        self.base_file = os.path.join(os.path.join(os.path.dirname(__file__), 'static'), 'base.xml')        

    def test_json(self):
        print ('llllllllllllllllllllllllllll')
        j = base_to_json(self.base)
        print (j)

    def test_create(self):
        """
        Test base XML creation
        """
        # Create base object to test
        base = self.base
        xml = base_to_xml(base)
        
        # Write it to a test file
        fd = open('/tmp/xml_base.xml', 'w+')
        fd.write(str(xml, encoding='utf-8'))
        fd.close()
        
    def test_parse_self(self):
        """
        Test receiving an XML object and parse it to a base object
        """
        # Create an XML object to test
        base = self.base
        xml = base_to_xml(base)
        
        xml_object = parseString(xml)
        
        # Now we do it the other way
        base = xml_to_base(xml_object)
        
    def test_parse_file(self):
        """
        Test opening a test multivalued XML file and creating an object
        """
        # Open XML file
        xml_object = parse(self.base_file)
        
        # Parse it as a base
        base = xml_to_base(xml_object)
        
    def tearDown(self):
        """
        Remove test data
        """
        pass
