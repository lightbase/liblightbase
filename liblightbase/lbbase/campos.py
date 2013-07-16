class CampoObjeto():
    """
    this class defines a collection of fields
    """
    def __init__(self, objeto):
        """
        Base attributes for this object
        """
        self.objeto = objeto
        
    @property
    def objeto(self):
        """
        Define this as a property
        """
        return self._objeto
    
    @objeto.setter
    def objeto(self, o):
        """
        Validate this attribute
        """
        out = list()
        if type(o) is list:
            # Now we check if the indexes are valid fields
            for value in o:
                if isinstance(value, Campo):
                    # Add this instance to the list
                    out.append(value)
                else:
                    # if there's an error it'll throw an exception
                    raise Exception('InstanceError This must be an instance of Campo. Instead it is %s' % value)
                
            # Now register all objects in this list
            self._objeto = out
        else:
            raise Exception('TypeError Wrong data type for objeto. you supplied %s' % o)
            self._objeto = None
        
class Campo():
    """
    This is the filed description
    """ 
    def __init__(self, nome=None, descricao=None, tipo=None, indexacao=None, objeto=None, multi=None, **entries):
        """
        Field options
        """
        self.nome = nome
        self.descricao = descricao
        
        if entries:
            self.__dict__.update(entries)
        
        if tipo:
            self.tipo = tipo
                    
        if indexacao:        
            self.indexacao = indexacao
                
        # This define multivalued fields and it's an option attribute
        if objeto:
            self.objeto = objeto

        if multi:
            self.multi = multi
        
    @property
    def indexacao(self):
        """
        Define this attribute
        """
        return self._indexacao
    
    @indexacao.setter
    def indexacao(self, i):
        """
        Validate the value for this field
        """
        out = list()
        if type(i) is list:
            # This value must be a list, and every index is an indice type
            for value in i:
                if isinstance(value, Indice):
                    # If this is a not valid index, there will be an exception here
                    out.append(value)
                else: 
                    # Raise exception
                    raise Exception('InstanceError This should be an instance of Indice. instead it is %s' % value)
                #indice = Indice(value)
                # add this to return list
                #out.append(indice)
            
            self._indexacao = out
        else:
            # Invalid type. Raise exception
            raise Exception('Type Error: indexacao field must be a list instead of %s' % i)
            self._indexacao = None


    @property
    def multivalue(self):
        """
        Define this attribute
        """
        return self._multi
    
    @multivalue.setter
    def multivalue(self, m):
        """
        Validate the value for this field
        """
        out = list()
        if type(m) is list:
            # This value must be a list, and every index is an indice type
            for value in m:
                if isinstance(value, Multi):
                    # If this is a not valid index, there will be an exception here
                    out.append(value)
                else: 
                    # Raise exception
                    raise Exception('InstanceError This should be an instance of Multi. instead it is %s' % value)
                #indice = Indice(value)
                # add this to return list
                #out.append(indice)
            
            self._multi = out
        else:
            # Invalid type. Raise exception
            raise Exception('Type Error: multi field must be a list instead of %s' % m)
            self._multi = None
            
    @property
    def tipo(self):
          """
          Define this as a property
          """
          return self._tipo
      
    @tipo.setter
    def tipo(self, t):
        """
        check this attribute properties
        """
        if isinstance(t, Tipo):
            self._tipo = t
        else:
            # It must be an instance
            raise Exception('TypeError This must be a instance of Tipo. Instead it is %s' % t)
            self._tipo = None
        
class Indice():
    """
    This is the indice object.
    """
    def __init__(self, indice):
        self.indice = indice
        
    def valid_indices(self):
        """
        Returns a list of valid values for indices
        """
        # TODO: Get this list of values from somewhere else
        valid_indices = ['SemIndice',
                         'Textual',
                         'Ordenado',
                         'Unico',
                         'Fonetico',
                         'Fuzzy',
                         'Vazio',
                         ]
        
        return valid_indices
        
    @property
    def indice(self):
        """
        Define this attribute
        """
        return self._indice
    
    @indice.setter
    def indice(self, i):
        """
        Validate attribute
        """
        valid = self.valid_indices()
        if i not in valid:
            # invalid value for indices. Raise exception
            raise Exception('IndexError violation. Supplied value for index %s is not valid' % i)
            self._indice = None
            
        self._indice = i
        
        
class Tipo():
    """
    Define valid data type
    """
    def __init__(self, tipo):
        self.tipo = tipo
        
        
    def valid_tipos(self):
        """
        Get valid instances of tipos
        """ 
        # TODO: Get these valid data types from somewhere else
        valid_tipos = ['AlfaNumerico',
                       'Documento',
                       'Inteiro',
                       'Decimal',
                       'Moeda',
                       'AutoEnumerado',
                       'Data',
                       'Hora',
                       'Imagem',
                       'Som',
                       'Video',
                       'URL',
                       'Verdadeiro/Falso',
                       'Texto',
                       'Arquivo',
                       'HTML',
                       'Email'
                       ]
        
        return valid_tipos 
    
    @property
    def tipo(self):
        """
        Define this as a property
        """
        return self._tipo
    
    @tipo.setter
    def tipo(self, t):
        """
        Check if this tipo is valid
        """
        if t in self.valid_tipos():
            self._tipo = t
        else:
            raise Exception('TypeError Wrong tipo. The value you supllied for tipo is not valid: %s' % t)
            self._tipo = None


class Multi():
    """
    Define valid data type
    """
    def __init__(self, multi):
        self.multi = multi
        
        
    def valid_multi(self):
        """
        Get valid instances of tipos
        """ 
        # TODO: Get these valid data types from somewhere else
        valid_multi = ['True']
        
        return valid_multi
    
    @property
    def multi(self):
        """
        Define this as a property
        """
        return self._multi
    
    @multi.setter
    def multi(self, m):
        """
        Check if this tipo is valid
        """
        if m in self.valid_multi():
            self._multi = m
        else:
            raise Exception('TypeError Wrong multi. The value you supllied for multi is not valid: %s' % m)
            self._multi = None
