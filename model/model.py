import copy

from database.DAO import DAO
import datetime
import time


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self._persone_affette_max = 0
        self._ore_totali = 0
        self._numero_anni = 1

    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []
        self._persone_affette_max = 0
        self._ore_totali = 0
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, 0, self._listEvents)
        return self._solBest, self._persone_affette_max, self._ore_totali

    def ricorsione(self, parziale, maxY, maxH, pos, rimanenti):
        print(f"sono alla posizione: {pos}")
        # condizione terminale
        if pos != 0:
            if pos > len(self._listEvents) or self.parziale_ammissibile(parziale, maxY, maxH) is False:
                return

            if self.parziale_ammissibile(parziale, maxY, maxH) is True:
                # print(parziale)
                persone_affette = self.calcola_persone_affette(parziale)
                if persone_affette > self._persone_affette_max:
                    print(parziale)
                    self._persone_affette_max = persone_affette
                    self._solBest = copy.deepcopy(parziale)
                    self._ore_totali = self.calcola_ore_totali(self._solBest)

        for evento in rimanenti:
            parziale.append(evento)
            nuovi_rimanenti = copy.deepcopy(rimanenti)
            nuovi_rimanenti.remove(evento)
            self.ricorsione(parziale, maxY, maxH, pos + 1, nuovi_rimanenti)
            parziale.pop()

    def calcola_persone_affette(self, parziale):
        persone_affette = 0
        for evento in parziale:
            persone_affette += evento.customers_affected
        return persone_affette

    def parziale_ammissibile(self, parziale, maxY, maxH):
        # Vincolo 1) ore
        ore_parziale = self.calcola_ore_totali(parziale)
        #print(evento)
        #print(evento.durata)
        #print(evento.durata.days)
        #print(evento.durata.seconds)

        #print(ore_evento)
        if ore_parziale > maxH:
            return False

        # Vincolo 2) anni
        if len(parziale) > 0:
            anni = self.get_anni(parziale)
            max_anno = max(anni)
            min_anno = min(anni)

            if (max_anno - min_anno) > maxY:
                return False

        return True # se passa tutti i controlli

    def calcola_ore_totali(self, parziale):
        secondi = 0
        for evento in parziale:
            secondi += evento.durata.total_seconds()

        return (secondi/60)/60

    def get_anni(self, parziale): # set con gli anni
        anni = set()
        for evento in parziale:
            anni.add(evento.date_event_finished.year)
        return anni

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc
