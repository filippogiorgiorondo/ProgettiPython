import http.client

print ("""
 ____   ____  _        ___ __ __   ____  ______   ___   ____     ___      __ __  ______  ______  ____  
|    \ |    || |      /  _]  |  | /    ||      | /   \ |    \   /  _]    |  |  ||      ||      ||    \ 
|  D  ) |  | | |     /  [_|  |  ||  o  ||      ||     ||  D  ) /  [_     |  |  ||      ||      ||  o  )
|    /  |  | | |___ |    _]  |  ||     ||_|  |_||  O  ||    / |    _]    |  _  ||_|  |_||_|  |_||   _/ 
|    \  |  | |     ||   [_|  :  ||  _  |  |  |  |     ||    \ |   [_     |  |  |  |  |    |  |  |  |   
|  .  \ |  | |     ||     |\   / |  |  |  |  |  |     ||  .  \|     |    |  |  |  |  |    |  |  |  |   
|__|\_||____||_____||_____| \_/  |__|__|  |__|   \___/ |__|\_||_____|    |__|__|  |__|    |__|  |__|   

                                                                                                       
""")

host = input("Inserire indirizzo IP bersaglio: \n")
port = int(input("Inserire porta da controllare (default: 80) \n"))

if port == "":

    port = 80

try:

    connection = http.client.HTTPConnection(host, port)
    connection.request('OPTIONS', '/')
    response = connection.getresponse()

    print("I metodi abilitati sono", response.getheader('allow'))
    connection.close()

except ConnectionRefusedError:

    print("Connessione Fallita.")