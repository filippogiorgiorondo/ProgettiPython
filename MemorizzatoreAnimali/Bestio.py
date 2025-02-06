def Bestio(quantiAnimaliVuoiMemorizzare):
    print("\nQual è il nome del tuo animaletto?")
    dizionarioAnimale = input().lower()
    nomeAnimale = dizionarioAnimale
    dizionarioAnimale = {}
    listaAnimali = []
    listaAnimali.append(dizionarioAnimale)
    while True:
        print("\nQuanti parametri (es: peso, altezza, colore del pelo) vuoi memorizzare per", nomeAnimale, "?")
        quantiParametriMemorizzare = int(input())
        if quantiParametriMemorizzare == 0:
            print("\nMi dispiace. Questo programma funziona inserendo almeno un parametro.\nRiavvio del programma...")
        else:           
            n = 1
            conteggio = str(n) + "°"
            for n in range(1,quantiParametriMemorizzare + 1):
                print("\nInserisci il nome del", conteggio, " parametro da memorizzare")
                nomeParametro = input()
                print("\nInserisci il nome del", conteggio, " dato da memorizzare\nEs: se il parametro scelto è 'altezza', il dato potrebbe essere '20 cm'")
                nomeDato = input()
                dizionarioAnimale[nomeParametro] = nomeDato
                n = n + 1
                conteggio = str(n) + "°"
                print("\nPerfetto! Le tue informazioni sono state salvate con successo.\n")
            break
    print(nomeAnimale, ":")
    for i in listaAnimali:
        print(i)
        break

while True:
    print("Hai una pessima memoria...lo so.\nNon preoccuparti perchè sono qui per memorizzare tutte le informazioni riguardanti i tuoi animali")
    print("E' un piacere averti qui. Il mio nome è Bestio\nTu come ti chiami?")
    nomeUtente = input()
    print("\nForza", nomeUtente, "! Iniziamo !")
    print("\nQuanti animali vuoi memorizzare?")
    quantiAnimaliVuoiMemorizzare = int(input())
    if quantiAnimaliVuoiMemorizzare == 0:
        print("\nMi dispiace. Questo programma funziona inserendo almeno un animale.\nRiavvio del programma...\n\n")
    elif quantiAnimaliVuoiMemorizzare == 1:
        print(Bestio(quantiAnimaliVuoiMemorizzare))
        break
    else:
        for k in range(1,quantiAnimaliVuoiMemorizzare + 1):
            print(Bestio(quantiAnimaliVuoiMemorizzare))
            print("Questi sono i tutti i dati")
        break
        