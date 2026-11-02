import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        # Il controller legge il campo della View e rimuove spazi superflui.
        responsabile = (self._view.input_responsabile.value or "").strip()
        if not responsabile:
            self._view.show_alert("Inserisci il nome del responsabile.")
            return

        # Aggiorna il dato nel Model e poi il testo mostrato nella View.
        self._model.responsabile = responsabile
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    def mostra_strumenti(self, e):
        # Chiede al Model di recuperare tutti gli strumenti dal database.
        strumenti = self._model.get_strumenti()
        # Cancella i risultati di un eventuale clic precedente.
        self._view.lista_strumenti.controls.clear()

        if strumenti is None:
            self._view.show_alert(
                "Impossibile leggere gli strumenti. Verifica che il database "
                "deposito_strumenti esista e che il server sia avviato."
            )
        elif not strumenti:
            self._view.lista_strumenti.controls.append(
                ft.Text("Nessuno strumento presente nel deposito.")
            )
        else:
            self._view.lista_strumenti.controls.extend(
                ft.Text(str(strumento)) for strumento in strumenti
            )
        self._view.update()

    def cerca_strumenti_per_tipo(self, e):
        # Legge e pulisce il tipo inserito dall'utente.
        tipo = (self._view.input_tipo_strumento.value or "").strip()
        self._view.lista_strumenti_ricerca.controls.clear()
        if not tipo:
            self._view.show_alert("Inserisci il tipo di strumento da cercare.")
            self._view.update()
            return

        # Il Model esegue la query; la View riceverà poi i risultati da mostrare.
        strumenti = self._model.cerca_strumenti_per_tipo(tipo)
        if strumenti is None:
            self._view.show_alert(
                "Impossibile cercare gli strumenti. Verifica che il database "
                "deposito_strumenti esista e che il server sia avviato."
            )
        elif not strumenti:
            self._view.lista_strumenti_ricerca.controls.append(
                ft.Text(f"Nessuno strumento trovato per il tipo: {tipo}.")
            )
        else:
            self._view.lista_strumenti_ricerca.controls.extend(
                ft.Text(str(strumento)) for strumento in strumenti
            )
        self._view.update()
