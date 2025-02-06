
print("-----------------------------------")
print("| Rilevatore Pacchetti tra Socket |")
print("-----------------------------------")

import socket
import struct
import binascii

def crea_sniffer_socket():

    try:

        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        sniffer.bind(("0.0.0.0", 0))

        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        return sniffer

    except socket.error as e: 

        print(f" !!! - Errore durante la creazione del socket: {e}")
        return None
    
def sniff_packets():

    sniffer = crea_sniffer_socket()
    
    if not sniffer:
        return
    
    try:

        while True:

            raw_data, addr = sniffer.recvfrom(65565)

            print(f"Pacchetto da {addr}: {binascii.hexlify(raw_data)}")

            ip_header = raw_data[:28]
            unpacked_header = struct.unpack("!BBHHHBBH4s4s", ip_header)

            print(f"Versione IP: {unpacked_header[0] >> 4}")
            print(f"Indirizzo sorgente: {socket.inet_ntoa(unpacked_header[8])}")
            print(f"Indirizzo destinazione: {socket.inet_ntoa(unpacked_header[9])}")
    
    except KeyboardInterrupt:

        print("\n Sniffing Terminato")

        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sniffer.close

if __name__ == "__main__":

    sniff_packets()