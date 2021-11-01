import re

class Dte:

    def __init__(self, tiempo = None, referencia = None, nit_emisor = None, nit_receptor = None, valor = None, iva = None, total = None):
        self.tiempo = tiempo
        self.fecha = tiempo
        self.referencia = referencia
        self.nit_emisor = nit_emisor
        self.nit_receptor = nit_receptor
        self.valor = valor
        self.iva = iva
        self.total = total

    def save_date(self, tiempo):
        match = re.search('(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}', tiempo)
        if match:
            self.fecha = match.group(0)