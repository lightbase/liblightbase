
from xml.dom import minidom
from liblightbase.lbbase import Base
from liblightbase.lbbase import campos
import webob.multidict
from webob.multidict import MultiDict
import json
import ast

def base_to_json(base):
    """
    Convert Base object to JSON
    Receives an lbbase Base object
    """

    def create_campo_json(doc, field):
        """
        function to parse campo object.
        
        return: An JSON object containing campo attributes
        """
        if isinstance(field, campos.Campo):
            campo_elm = dict()
            attr_elm = dict()
            attr_elm_c = dict()
            objetos_2 = list()
            for value in field.__dict__.keys():
                if isinstance(field.__dict__.get(value), campos.Tipo):
                    tipo = field.__dict__.get(value)
                    attr_elm['tipo'] = tipo.tipo
                elif value == '_indexacao':
                    indice_elm = list()
                    for indice in field.__dict__.get(value):
                        if isinstance(indice, campos.Indice):
                            text = indice.indice
                            indice_elm.append(text)
                            attr_elm['indexacao'] = indice_elm
                elif value == 'objeto':
                    objeto_2 = field.__dict__.get(value)
                    for elm in objeto_2.objeto:
                        campo_2 = create_campo_json(doc, elm)
                        attr_elm_c['campo'] = campo_2
                        attr_elm['objeto'] = dict()
                        attr_elm['objeto']['campo'] = attr_elm_c['campo']
                        objetos_2.append(attr_elm['objeto'])
                else:
                    attr_elm[value] = field.__dict__.get(value)

                if objetos_2:
                    attr_elm['objeto'] = objetos_2

            return attr_elm
        else:
            raise Exception('TypeError this should be an instance of Campo. Instead it is %s' % campo)

    doc = dict()
    base_elm = dict()
    objeto_elm = dict()
    objetos = list()

    for elm in base.__dict__.keys():
        if isinstance(base.__dict__.get(elm), campos.CampoObjeto):
            objeto = base.__dict__.get(elm)
        else:
            base_elm[elm] = base.__dict__.get(elm)

    for field in objeto.objeto:
        campo = create_campo_json(doc, field)
        objeto_elm['campo'] = campo
        base_elm['objeto'] = dict()
        base_elm['objeto']['campo'] = objeto_elm['campo']
        objetos.append(base_elm['objeto'])

    if objetos:
        base_elm['objeto'] = objetos

    doc['base'] = base_elm

    jdoc = json.dumps(doc)
    return jdoc


def json_to_base(doc):
    """
    Receives an JSON object and parse it to base object
    """
    #base_elm = doc.getElementsByTagName('base')
    base_elm = ast.literal_eval(doc)
    
    def parse_campo_json(field):
        """
        Create and parse a Campo object
        """
        print('777777777777777777777')
        print(field)
        # Now open campos
        field_dict = dict()
        #for campo_elm in field.childNodes:
        for campo_elm in field:
            #if campo_elm.nodeName == 'indexacao' and campo_elm.nodeName != '#text':
            if campo_elm == 'indexacao' and campo_elm != '#text':
                # This is a list
                indexacao = list()
                #for indice in campo_elm.childNodes:
                for indice in field.get(campo_elm):
                    #if indice.nodeName != '#text':
                    if indice != '#text':
                        # Create the index object
                        #indice_obj = campos.Indice(indice=indice.firstChild.nodeValue)
                        indice_obj = campos.Indice(indice=field.get(campo_elm).get(indice))
                        #--------------PAREI AQUI-----------------------------------------#
                        # Add it to indice list
                        indexacao.append(indice_obj)
                field_dict['indexacao'] = indexacao
            elif campo_elm.nodeName == 'tipo' and campo_elm.nodeName != '#text':
                tipo = campos.Tipo(tipo=campo_elm.firstChild.nodeValue)
                field_dict['tipo'] = tipo
            elif campo_elm.nodeName == 'objeto' and campo_elm.nodeName != '#text':
                objeto_elm2 = list()
                for field_elm in campo_elm.childNodes:
                    if field_elm.nodeName != '#text':
                        campo2 = parse_campo(field_elm)
                        objeto_elm2.append(campo2)
                
                # Add this new objeto to campo dict
                field_dict['objeto'] = campos.CampoObjeto(objeto=objeto_elm2)
            elif campo_elm.nodeName != '#text':
                field_dict[campo_elm.nodeName] = campo_elm.firstChild.nodeValue
                
        campo3 = campos.Campo(**field_dict)
        
        return campo3 
                        
    base_dict = dict()
    #for elm in base_elm[0].childNodes:
    for elm in base_elm['base']:
        # Now open and parse every element individually
        #if elm.nodeName == 'objeto':
        if elm == 'objeto':
            # now open <objeto>
            objeto_elm = list()
            #for field in elm.childNodes:
            for field in base_elm['base']['objeto']:
                #if field.nodeName != '#text':
                if field != '#text':
                    campo = parse_campo_json(base_elm['base']['objeto'][field])
                    # Add campo to objeto
                    objeto_elm.append(campo)
                
            base_dict['objeto'] = campos.CampoObjeto(objeto=objeto_elm)
        #elif elm.nodeName != '#text':
        elif elm != '#text':
            # Add this elm and value do base dict
            #base_dict[elm.nodeName] = elm.firstChild.nodeValue
            base_dict[elm] = base_elm.get(elm)
                    
                    
    # Create base object
    base = Base(**base_dict)
    
    return base
