from xml.dom import minidom
from liblightbase.lbbase import Base
from liblightbase.lbbase import campos

def base_to_xml(base):
    """
    Convert Base object to XML
    Receives an lbbase Base object
    """
    # create XML document
    doc = minidom.Document()
    
    # Create base elm
    base_elm = doc.createElement('base')
    
    def create_campo(doc, field):
        """
        function to parse campo object.
        
        return: An XML object containing campo attributes
        """
        if isinstance(field, campos.Campo):
            # Adding <campo> element
            campo_elm = doc.createElement('campo')
            campo_elm2 = doc.createElement('campo')
            if 'multi' in field.__dict__.keys():
                multi = True
                campo_elm = doc.createElement('grupo')
                campo_elm.setAttribute('multivalued','True')
            else:
                multi = False
            if 'objeto' in field.__dict__.keys():
                obj = True
            else:
                obj = False
            if 'objeto' in field.__dict__.keys() and not 'multi' in field.__dict__.keys():
                campo_elm = doc.createElement('grupo')
            for value in field.__dict__.keys():
                # Here we have campo attributes
                    
                # Add every campo attribute to XML. Ex.: <nome>                    
                if isinstance(field.__dict__.get(value), campos.Tipo):
                    # This is a XML <tipo>. Add its value.
                    attr_elm = doc.createElement('tipo')
                    tipo = field.__dict__.get(value)
                    text = doc.createTextNode(tipo.tipo)
                    attr_elm.appendChild(text)
                elif value == '_indexacao':
                    attr_elm = doc.createElement('indexacao')
                    # There can be more than one indice
                    for indice in field.__dict__.get(value):
                        # Make sure we are adding an <indice> element
                        if isinstance(indice, campos.Indice):
                            indice_elm = doc.createElement('indice')
                            # Now add this index to element
                            text = doc.createTextNode(indice.indice)
                            indice_elm.appendChild(text)
                            # Add it as a child to <indexacao>
                            attr_elm.appendChild(indice_elm)
                elif value == 'multi':
                    pass
                elif value == 'objeto':
                    #attr_elm = doc.createElement('grupo')
                    # there's a new field inside the field.
                    objeto_2 = field.__dict__.get(value)
                    for elm in objeto_2.objeto:
                        # Now we parse the <campo> ocurrencies                        
                        campo_2 = create_campo(doc, elm)
                        #attr_elm.appendChild(campo_2)
                        campo_elm.appendChild(campo_2)
                else:
                    # Just add text value to the element
                    valor = doc.createElement(value)
                    #text = doc.createTextNode(field.__dict__.get(value))
                    # Encapsulate text in CData
                    cdata = doc.createCDATASection(field.__dict__.get(value))
                    valor.appendChild(cdata)
                    campo_elm.appendChild(valor)
                    if obj == False and multi == True:
                        campo_elm2.appendChild(valor)

                name = doc.createElement('nome')
                nametxt = doc.createCDATASection(field.__dict__.get('nome'))
                name.appendChild(nametxt)
                desc = doc.createElement('descricao')
                desctxt = doc.createCDATASection(field.__dict__.get('descricao'))
                desc.appendChild(desctxt)

                if obj == False and multi == True:
                    if len(campo_elm.childNodes) < 1:
                        campo_elm.appendChild(name)
                        campo_elm.appendChild(desc)
                    if 'attr_elm' in vars():
                        campo_elm2.appendChild(attr_elm)
                    campo_elm.appendChild(campo_elm2)

                # Add child elements to <campo> object
                elif obj == True and multi == False:
                    #Group of fields not multivalued
                    pass
                elif 'attr_elm' in vars():
                    campo_elm.appendChild(attr_elm)


            # Return <campo> object
            return campo_elm
        else:
            # Raise type error
            raise Exception('TypeError this should be an instance of Campo. Instead it is %s' % campo)

    objeto_elm = doc.createElement('grupo')
    # Now add base elements 
    for elm in base.__dict__.keys():
        if isinstance(base.__dict__.get(elm), campos.CampoObjeto):
            #  This is a field definition elements and it will have childs
            objeto = base.__dict__.get(elm)
        else:
            # Add elements to XML
            b_elm = doc.createElement(elm)
            #text = doc.createTextNode(base.__dict__.get(elm))
            # Encapsulate it in CDATA
            text = doc.createCDATASection(base.__dict__.get(elm))
            b_elm.appendChild(text)
            
            # Add them to base
            base_elm.appendChild(b_elm)
            if elm != 'senha':
                new_b_elm = b_elm.cloneNode(True)
                objeto_elm.appendChild(new_b_elm)
    
    # Now add fields to the document
        
    # Now we add the fields
    for field in objeto.objeto:
        campo = create_campo(doc, field)
        objeto_elm.appendChild(campo)
            
    # Add <objeto> element to <base>
    base_elm.appendChild(objeto_elm)
    
    # Add <base> element do document
    doc.appendChild(base_elm)
    
    # Now return XML
    return doc.toprettyxml(encoding='utf-8',newl='',indent='')

def xml_to_base(doc):
    """
    Receives an XML object and parse it to base object
    """
    base_elm = doc.getElementsByTagName('base')

    def parse_campo(field):
        """
        Create and parse a Campo object
        """
        # Now open campos
        field_dict = dict()
        if field.nodeName == 'descricao':
            return False
        elif field.nodeName == 'nome':
            return False
        elif field.nodeName == 'campo':
            for campo_elm in field.childNodes:
                if campo_elm.nodeName == 'indexacao' and campo_elm.nodeName != '#text':
                    # This is a list
                    indexacao = list()
                    for indice in campo_elm.childNodes:
                        if indice.nodeName != '#text':
                            # Create the index object
                            indice_obj = campos.Indice(indice=indice.firstChild.nodeValue)
                            # Add it to indice list
                            indexacao.append(indice_obj)
                    field_dict['indexacao'] = indexacao
                elif campo_elm.nodeName == 'tipo' and campo_elm.nodeName != '#text':
                    tipo = campos.Tipo(tipo=campo_elm.firstChild.nodeValue)
                    field_dict['tipo'] = tipo
                elif campo_elm.nodeName != '#text':
                    field_dict[campo_elm.nodeName] = campo_elm.firstChild.nodeValue

        elif field.nodeName == 'grupo':
            objeto_elm2 = list()
            for campo_elm in field.childNodes:
                if field.getAttribute('multivalued') == 'True':
                    field_dict['multivalued'] = 'True'
                if campo_elm.nodeName == 'nome' or campo_elm.nodeName == 'descricao':
                    field_dict[campo_elm.nodeName] = campo_elm.firstChild.nodeValue
                elif campo_elm.nodeName != '#text':
                    campo2 = parse_campo(campo_elm)
                    if campo2:
                        objeto_elm2.append(campo2)
            if len(objeto_elm2)>0:
                field_dict['objeto'] = campos.CampoObjeto(objeto=objeto_elm2)

        if len(field_dict)>0:
            campo3 = campos.Campo(**field_dict)
        else:
            campo3 = False

        return campo3

    base_dict = dict()
    for elm in base_elm[0].childNodes:
        # Now open and parse every element individually
        if elm.nodeName == 'grupo':
            # now open <objeto>
            objeto_elm = list()
            for field in elm.childNodes:
                if field.nodeName != '#text':
                    campo = parse_campo(field)
                    # Add campo to objeto
                    if campo:
                        objeto_elm.append(campo)

            if len(objeto_elm)>0:
                base_dict['objeto'] = campos.CampoObjeto(objeto=objeto_elm)
            else:
                raise Exception('No fields supplied')
        elif elm.nodeName != '#text':
            # Add this elm and value do base dict
            base_dict[elm.nodeName] = elm.firstChild.nodeValue


    #Create base object
    base = Base(**base_dict)

    return base
