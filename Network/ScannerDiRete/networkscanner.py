import os
import time
import nmap
import scapy.all as scapy

# Funzione per eseguire una scansione SYN sulle porte specificate (80 e 443)
def scan_ports(ip, ports):
    nm = nmap.PortScanner()
    print(f"Scanning IP: {ip} on ports: {ports}")
    nm.scan(ip, ports, arguments='-sS')  # -sS per SYN scan
    return nm[ip]

# Funzione per monitorare la rete e rilevare nuovi dispositivi (ARP requests)
def discover_devices():
    print("Starting ARP scan to discover devices...")
    devices = []
    arp_request = scapy.ARP(pdst="192.168.1.0/24")
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    # Funzione che restituisce la lista dei dispositivi con indirizzo IP e MAC
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    for element in answered_list:
        device = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        devices.append(device)

    return devices

# Funzione per la scansione di tutte le porte note su un dispositivo
def scan_all_ports(ip):
    nm = nmap.PortScanner()
    print(f"Scanning all known ports on {ip}")
    nm.scan(ip, '1-65535', arguments='-sS')  # -sS per SYN scan, tutte le porte
    return nm[ip]

# Funzione per monitorare i pacchetti ARP sulla rete
def monitor_arp():
    # Funzione per monitorare pacchetti ARP
    def arp_callback(packet):
        if packet.haslayer(scapy.ARP):
            # Se il pacchetto ARP proviene da un dispositivo conosciuto, esegui la scansione completa
            ip = packet.psrc
            print(f"ARP Request/Reply detected for IP: {ip}")
            print(f"Starting full port scan for {ip}")
            scan_all_ports(ip)

    # Iniziare il monitoraggio dei pacchetti ARP sulla rete
    scapy.sniff(prn=arp_callback, filter="arp", store=0)

# Funzione principale che avvia il monitoraggio della rete
def monitor_network():
    print("Monitoring the network for new devices...")

    # Rileva inizialmente i dispositivi presenti
    previous_devices = discover_devices()
    previous_ips = [device["ip"] for device in previous_devices]

    while True:
        # Rileva i nuovi dispositivi
        devices = discover_devices()
        new_ips = [device["ip"] for device in devices]
        new_devices = [device for device in devices if device["ip"] not in previous_ips]

        # Se ci sono nuovi dispositivi, esegui la scansione sulle porte 80 e 443
        for device in new_devices:
            ip = device["ip"]
            print(f"New device detected: {ip}")

            # Esegui una scansione iniziale su HTTP (porta 80) e HTTPS (porta 443)
            print("Starting initial scan on ports 80 and 443 (HTTP/HTTPS)...")
            scan_result = scan_ports(ip, '80,443')

            # Se la scansione ha trovato delle porte aperte (anche se vuote), stampa
            open_ports = [port for port in scan_result['tcp'] if scan_result['tcp'][port]['state'] == 'open']
            print(f"Open ports found on {ip}: {open_ports}")

        # Attendi un po' prima di ripetere il ciclo (per evitare un sovraccarico continuo)
        print("Waiting for new devices or changes in the network...")
        time.sleep(10)

if __name__ == "__main__":
    # Avviare il monitoraggio della rete in un thread separato per monitorare i pacchetti ARP
    import threading
    arp_thread = threading.Thread(target=monitor_arp)
    arp_thread.daemon = True
    arp_thread.start()

    # Avviare il monitoraggio della rete per nuovi dispositivi
    monitor_network()