from liblightbase.lbbase import campos

class Base():
    """
    Defining a LB Base object
    """

    def __init__(self, nome, descricao, senha, objeto, exportar_indice, url_indice,
		    tempo_indice, extrair_doc, tempo_extrator, **entries):
        """
        Base attributes
        """
        self.nome = nome
        self.descricao = descricao
        self.senha = senha
        self.exportar_indice = exportar_indice
        self.url_indice = url_indice
        self.tempo_indice = tempo_indice
        self.extrair_doc = extrair_doc
        self.tempo_extrator = tempo_extrator
        self.objeto = objeto

        if entries:
            self.__dict__.update(entries)
