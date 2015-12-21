Lightbase database library
===================

Biblioteca para utilização do módulo Lightbase em aplicações python. A hierarquia fornece os seguintes módulos

* Criação de bases com campos e tipos de dados
* Integração com interface REST

Modelo de documento LighBase
----------------------------

*documento*

    { membros }

*membros*

    estrutura
    estrutura, membros

*estrutura*

    campo
    campo_multivalorado
    grupo
    grupo_multivalorado

*campo*

    string: valor

*campo_multivalorado*

    string: []
    string: [elementos]

*elementos*

    valor
    valor, elementos

*grupo*

    string: documento

*grupo_multivalorado*

    string: []
    string: [documentos]

*documentos*

    documento
    documento, documentos

*string*

    "caracteres"
