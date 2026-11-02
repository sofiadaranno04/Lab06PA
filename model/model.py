import mysql
from mysql.connector import errorcode

from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        """restitiosce il nome del deposito"""
        return self._nome

    @nome.setter
    def nome(self, nome):
        """imposta il nome del deposito"""
        self._nome = nome

    @property
    def responsabile(self):
        """restituisce il nome del responsabile"""
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        """imposta il nome del responabile del deposito"""
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """funzione che legge tutti gli strumenti dal database.

        Una lista vuota indica che la query è riuscita ma non ci sono righe;
        None indica che non è stato possibile interrogare il database.
        """
        # Recupera una connessione usando le impostazioni di connector.cnf.
        conn = get_connection()
        if conn is None:
            raise ConnectionError("impossibile connettersi al database")

        cursor = conn.cursor()
        try:
            # Il cursore esegue la query SQL e riceve le righe restituite, esegue la query per ottenere tutti gli elementi ordinati per codice
            query ="""
                       SELECT *
                       FROM strumento
                   """
            cursor.execute(query)
            lista_strumenti =[]
            for row in cursor:
                lista_strumenti.append(Strumento(row[0],
                                                 row[1],
                                                 row[2],
                                                 row[3],
                                                 row[4],
                                                 row[5])
                                       )
            return lista_strumenti

            # Trasforma ogni riga in un oggetto Strumento del nostro modello.
            return [
                Strumento(*row[:5], disponibile=bool(row[5]))
                for row in cursor.fetchall()
            ]
        except Exception:
            # Il controller distingue un errore da una ricerca valida senza risultati.
            return None
        finally: # comunque devo chiudere la connessiome a prescindere dal try
            # Rilascia sempre le risorse, anche se la query genera un errore.
            if cursor is not None:
                cursor.close()
            conn.close()

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """Restituisce tutti gli strumenti del tipo richiesto, oppure None in caso di errore.
        :param tipo: tipo di strumento(es."Chitarra")
        :return: lista di strumento per tipo richiesto oppure None
        """
        # Un input vuoto non deve avviare una ricerca nel database.

        if not isinstance(tipo, str) or not tipo.strip():
            return []

        # Se non esiste una connessione, segnala l'errore al controller.
        conn = get_connection() #stabilisce la connessione
        if conn is None:
            raise ConnectionError("impossibile connettersi al database")

        cursor = conn.cursor()
        try:
            query = """
                        SELECT *
                        FROM strumento
                        WHERE TIPO = %s
                    """
            # %s è un parametro: l'input non viene concatenato alla query SQL.
            cursor.execute(query, (tipo,)) #parametro {tipo <--> %s}

            # Il risultato può contenere più strumenti dello stesso tipo.
            strumenti_per_tipo = []
            for row in cursor:
                strumenti_per_tipo.append(Strumento(row[0],
                                                    row[1],
                                                    row[2],
                                                    row[3],
                                                    row[4],
                                                    row[5])
                                          )
            return strumenti_per_tipo
        except Exception:
            return None
        finally:
            # Chiude cursore e connessione dopo la ricerca.
            if cursor is not None:
                cursor.close()
            conn.close()
