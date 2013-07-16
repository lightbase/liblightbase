import unittest
from datetime import datetime
from liblightbase.lbbase import Base
from liblightbase.lbbase.campos import *

class BaseTestCase(unittest.TestCase):
    """
    Unity tests for Base
    """
    def setUp(self):
        """
        Set up test data
        """
        pass
        
    def test_index(self):
        """
        Try to setup index value
        """
        indice = Indice(indice='Palavra')
    
    def test_tipo(self):
        """
        Try to setup Tipo object
        """
        tipo = Tipo(tipo='Inteiro')
        
        
    def test_campo(self):
        """
        Try to setup a campo object
        """
        indice = Indice(indice='Palavra')
        indexacao = list()
        indexacao.append(indice)
        
        tipo = Tipo(tipo='Texto')
        
        campo = Campo(nome='nome',
                      descricao='Esse é o nome da pessoa',
                      tipo=tipo,
                      indexacao=indexacao
                      )
        
    def test_objeto(self):
        """
        Try to setup objeto
        """
        indice = Indice(indice='Palavra')
        indexacao = list()
        indexacao.append(indice)
        
        tipo = Tipo(tipo='Texto')
        
        campo = Campo(nome='nome',
                      descricao='Esse é o nome da pessoa',
                      tipo=tipo,
                      indexacao=indexacao
                      )
        
        objeto = list()
        objeto.append(campo)
        
        objeto = CampoObjeto(objeto=objeto)
        
    def test_objeto_multiple(self):
        """
        Try objeto with multiple fields
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
        
        # Now create objeto        
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
        
        # Finally create <objeto>
        objeto = CampoObjeto(objeto=objeto)
        
    def test_objeto_multivalued(self):
        """
        Test multivalued fields
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
        
    def test_base(self):
        """
        Test base object creation
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
        
        base = Base(
                    nome='Pessoa',
                    descricao='Base que armazena informações de pessoas',
                    senha='@$!@#%fhbhfdh54745754',
                    objeto=objeto
                    )
        
        
    def tearDown(self):
        """
        Remove test data
        """
        pass
