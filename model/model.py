from database.impianto_DAO import ImpiantoDAO
from model.impianto_DTO import Impianto

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti() #sono tutti gli impianti presenti

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        risultati=[]
        lst_consumi=[]
        for i in self._impianti:
            consumo_impianto=i.get_consumi()
            for c in consumo_impianto:
                anno,mese_c,giorno=str(c.data).split('-')
                if int(mese_c) == mese:
                    lst_consumi.append(c.kwh)
            media=(sum(lst_consumi)/len(lst_consumi))
            risultati.append((i.nome,media))
        return risultati



    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        #A
        if giorno>7:
            if self.__costo_ottimo==-1 or costo_corrente<self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima=list(sequenza_parziale)
            return
        #B
        for id_i, consumi in consumi_settimana.items():
            costo_giorno=consumi[giorno-1]
            costo_spostamento=0
            if ultimo_impianto is not None and ultimo_impianto!= id_i:
                costo_spostamento=5
            nuovo_costo=costo_corrente+costo_giorno+costo_spostamento
            if self.__costo_ottimo!=-1 and nuovo_costo>=self.__costo_ottimo:
                continue
            sequenza_parziale.append(id_i)
            self.__ricorsione(sequenza_parziale,
                              giorno+1,
                              id_i,
                              nuovo_costo,
                              consumi_settimana)
            sequenza_parziale.pop()
    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        diz_consumi = {}
        for i in self._impianti:
            kwh_settimana=[0]*7
            for c in i.get_consumi():
                anno,mese_c,giorno=str(c.data).split('-')
                if int(mese_c) == mese and 1<=int(giorno)<=7:
                    kwh_settimana[int(giorno)-1]=c.kwh
            diz_consumi[i.id]=kwh_settimana
        return diz_consumi








