# -*- coding: utf-8 -*-
        
class Standard():
    def __repr__(self):
        return "'%s'" % self.__class__.__name__

class Texto(Standard):
    def __call__(self, value):
        return value

class AlfaNumerico(Standard):
    def __call__(self, value):
        return value

class Documento(Standard):
    def __call__(self, value):
        return value

class Inteiro(Standard):
    def __call__(self, value):
        return value

class Decimal(Standard):
    def __call__(self, value):
        return value

class Moeda(Standard):
    def __call__(self, value):
        return value

class AutoEnumerado(Standard):
    def __call__(self, value):
        return value

class Data(Standard):
    def __call__(self, value):
        return value

class Hora(Standard):
    def __call__(self, value):
        return value

class DataHora(Standard):
    def __call__(self, value):
        return value

class Imagem(Standard):
    def __call__(self, value):
        return value

class Som(Standard):
    def __call__(self, value):
        return value

class Video(Standard):
    def __call__(self, value):
        return value

class URL(Standard):
    def __call__(self, value):
        return value

class VerdadeiroFalso(Standard):
    def __call__(self, value):
        return value

class Arquivo(Standard):
    def __call__(self, value):
        return value

class HTML(Standard):
    def __call__(self, value):
        return value

class Email(Standard):
    def __call__(self, value):
        return value

class JSON(Standard):
    def __call__(self, value):
        return value
