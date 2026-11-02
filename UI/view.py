import flet as ft
from UI.alert import AlertManager

'''
    VIEW:
    - Rappresenta l'interfaccia utente
    - Riceve i dati dal MODELLO e li presenta senza modificarli
'''

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab06"
        self.page.horizontal_alignment = "center"
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

        # Elementi UI
        self.txt_titolo = None
        self.txt_responsabile = None

        # Non obbligatorio mettere già qui tutti gli elementi UI

    def show_alert(self, messaggio):
        """mostra un popup di avvios /errore all'utente"""
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        """ Imposta il controller alla pagina """
        self.controller = controller

    def update(self):
        """aggiorna ala schermata di Flet"""
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge Elementi di UI alla pagina e la aggiorna. """
        #intestazione con il nome del deposito
        self.txt_titolo = ft.Text(value=self.controller.get_nome(), size=38, weight=ft.FontWeight.BOLD)
        #etichetta del resposnabile
        self.txt_responsabile = ft.Text(
            value=f"Responsabile: {self.controller.get_responsabile()}",
            size=16,
            weight=ft.FontWeight.BOLD
        )

        # TextField per responsabile, campo di testo per modificae il nome del responabile
        self.input_responsabile = ft.TextField(value=self.controller.get_responsabile(), label="Responsabile")

        # ListView dove il Controller inserirà gli strumenti caricati dal Model, elenco completo degli stumenti aggiornata.(Sezione 3)
        self.lista_strumenti = ft.ListView(
            height=180, spacing=5, padding=10, auto_scroll=False
        )

        # TextField per ricerca strumento per tipo, campo di testo per inserire il tipo di strumento da cercare. (Sezione 4)
        self.input_tipo_strumento = ft.TextField(label="Tipo")

        # Lista separata per mostrare i risultati della ricerca per tipo.
        self.lista_strumenti_ricerca = ft.ListView(
            height=180, spacing=5, padding=10, auto_scroll=False
        )

        # --- PULSANTI e TOGGLE associati a EVENTI ---
        # Gli handler del Controller vengono chiamati quando l'utente clicca.
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)
        pulsante_conferma_responsabile = ft.Button("Conferma", on_click=self.controller.conferma_responsabile)

        pulsante_mostra_strumenti = ft.Button("Mostra", on_click=self.controller.mostra_strumenti)
        pulsante_cerca_per_tipo = ft.Button("Cerca", on_click=self.controller.cerca_strumenti_per_tipo)

        # --- LAYOUT ---
        # Gli elementi sono aggiunti dall'alto verso il basso come richiesto.
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            self.txt_responsabile,
            ft.Divider(),

            # Sezione 2
            ft.Text("Modifica Informazioni", size=20),
            ft.Row(spacing=200,
                   controls=[self.input_responsabile, pulsante_conferma_responsabile],
                   alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),

            # Sezione 3: lista degli strumenti
            ft.Text(spacing=200,
                    controls=[self.input_responsabile,pulsante_mostra_strumenti],
                    alignment=ft.MainAxisAlignment.START),
            self.lista_strumenti,#appendo la ListaView
            ft.Divider(),

            # Sezione 4: ricerca strumento per tipo
            ft.Text("Cerca Strumento per Tipo", size=20),
            ft.Row(spacing=10,
                   controls=[self.input_tipo_strumento, pulsante_cerca_per_tipo],
                   alignment=ft.MainAxisAlignment.START),
            self.lista_strumenti_ricerca

        )


    def cambia_tema(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
