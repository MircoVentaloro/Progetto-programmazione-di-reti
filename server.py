# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Script Python per la realizzazione di un server multithread
per connessione CHAT asincrone.
"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accetta_connessioni_in_entrata():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)
        #al client che si connette per la prima volta fornisce alcune indicazioni di utilizzo
        client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto INVIO", "utf8"))
        #ci serviamo di un dizionario per registrare i client
        indirizzi[client] = client_address
        #diamo inizio all'attività del Thread - uno per ciascun client
        Thread(target=gestisce_client, args=(client,)).start()

"""Creazione funzione gestisce_client
gestisce la connessione di un singolo client"""
def gestisce_client(client): #prende il socket del client come argomento della funzione
    nome = client.recv(BUFSIZ).decode("utf8")
    #da il benvenuto al client e gli indica come fare per uscire dalla chat quando ha terminato
    benvenuto = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi (quit) per uscire.' % nome
    client.send(bytes(benvenuto, "utf8"))
    msg = "%s si è unito alla Chat!" % nome
    #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x entrato
    broadcast(bytes(msg, "utf8"))
    #aggiorna il dizionario clients creato all'inizio
    clients[client] = nome
    
#si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita della Chat
    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg != bytes("quit", "utf8"):
                broadcast(msg, nome+": ")
            else:
                client.send(bytes("quit", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf"))
                break
        except Exception as e:
            print("Errore durante la gestione del client:", e)
            client.close()
            del clients[client]
            broadcast(bytes("Connessione con %s persa." % nome, "utf8"))
            break
        

"""Creazione funzione broadcast
invia un messaggio in broadcast a tutti i client"""
def broadcast(msg, prefisso=""): #il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        utente.send(bytes(prefisso, "utf8")+msg)
"""Chiamata per inviare messaggi a tutti gli utenti della Chat
ciclando dentro al dizionario dei clients e inviando sul loro
socket il messaggio accompagnato dal prefisso corrispondente
al nome dell'utente che ha inviato il messaggio"""

clients = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__=="__main__":
#riga utilizzata per far capire al codice se verrà eseguito come script o se sarà invocato come modulo da qualche programma
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    
