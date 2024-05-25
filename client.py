# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter.
IMPORT"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

"""creazione funzione che gestisce ricezione di messaggi"""
def receive():
    while True:
        try:
            #ascolto messaggi che arrivano al socket
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            #visualizzazione messaggi su schermo
            msg_list.insert(tkt.END, msg) #END corrisponde alla posizione del cursore subito dopo l'ultimo carattere nel buffer
            #nel caso di errore e' probabile che il client abbia abbandonato la chat
        except OSError:
            break
        except ConnectionError:
            print("Connsessione persa con il server.")
            break

"""creazione funzione che gestisce invio di messaggi"""
def send(event=None):
    #eventi vengono passati dai binders
    msg = my_msg.get()
    #libera la casella di input
    my_msg.set("")
    #invia il messaggio sul socket
    client_socket.send(bytes(msg, "utf8"))
    if msg == "quit":
        client_socket.close()
        finestra.destroy()

"""funzione che viene invocata quando viene chiusa la finstra della chat"""
def on_closing(event=None):
    my_msg.set("quit")
    send()
    
"""def finestra"""
finestra = tkt.Tk()
finestra.title("Traccia_Chat")


#CREAZIONE GUI
#definizione widget livello superiore
#creo Frame che contenga i messaggi
messages_frame = tkt.Frame(finestra)
#creiamo una variabile di tipo stringa per i messaggi da inviare.
my_msg = tkt.StringVar()
#indichiamo all'utente dove deve scrivere i suoi messaggi
my_msg.set("Scrivi qui i tuoi messaggi.")
#creiamo una scrollbar per navigare tra i messaggi precedenti.
scrollbar = tkt.Scrollbar(messages_frame)

#parte seguente contiene i messaggi
msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

#creazione campo input e associazione a funzione send
entry_field = tkt.Entry(finestra, textvariable=my_msg)
#lego funzione send a tasto Return
entry_field.bind("<Return>", send)

entry_field.pack()
#creazione tasto invio e associazione a funzione send
send_button = tkt.Button(finestra, text="Invio", command=send)
#integrazione tasto nel pacchetto
send_button.pack()
#utilizzo funzione on_closing
finestra.protocol("WM_DELETE_WINDOW", on_closing)


#CONNESSIONE AL SERVER

HOST = input('Inserire il Server host: ')
PORT = input('Inserire la porta del server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
# Avvia l'esecuzione della Finestra Chat.
tkt.mainloop()
