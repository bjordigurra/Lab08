import flet as ft

from model.nerc import Nerc
from time import time
from operator import attrgetter


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        if self._view._ddNerc.value is None:
            self._view.create_alert("Selezionare un NERC!")
            return
        elif self._view._txtYears.value == "" or self._view._txtYears.value.isdigit() is False:
            self._view.create_alert("Inserire un numero di anni valido!")
            return
        elif self._view._txtHours.value == "" or self._view._txtHours.value.isdigit() is False:
            self._view.create_alert("Inserire un numero di ore valido!")
            return

        self._view._txtOut.controls.clear()
        self._view._txtOut.controls.append(ft.Text("Elaborazione in corso..."))
        self._view.update_page()

        start_time = time()
        lista_sequenza, persone_affette, ore_totali = self._model.worstCase(self._view._ddNerc.value,
                                               int(self._view._txtYears.value),
                                               int(self._view._txtHours.value))
        # ho la lista, faccio i calcoli da mettere all'inizio e poi i singoli eventi
        end_time = time()
        print("FINITO")

        self._view._txtOut.controls.clear()

        if len(lista_sequenza) != 0:
            self._view._txtOut.controls.append(ft.Text(f"Persone affette: {persone_affette}"))
            self._view._txtOut.controls.append(ft.Text(f"Ore totali: {ore_totali}"))

            lista_sequenza.sort(key=attrgetter("_date_event_began"))

            for evento in lista_sequenza:
                self._view._txtOut.controls.append(ft.Text(evento.__str__()))
        else:
            self._view._txtOut.controls.append(ft.Text("Nessun evento trovato in base ai parametri inseriti!"))

        self._view._txtOut.controls.append(ft.Text(f"Time elapsed: {end_time-start_time}"))

        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key=n.id, text=n.value))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
