# Script de capture avec Scapy

# Il sagit ici d'un code juste pour creer la mabranche celle de sniffing ( pour la générations des donnés )

from scapy.all import sniff, IP, TCP, UDP, DNS
from datetime import datetime
import socket

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Inconnu"

def analyse_packet(packet):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if packet.haslayer(IP):
        src = packet[IP].src
        dst = packet[IP].dst
        proto = "UNKNOWN"
        if packet.haslayer(TCP):
            proto = "TCP"
        elif packet.haslayer(UDP):
            proto = "UDP"
        elif packet.haslayer(DNS):
            proto = "DNS"
        
        log = f"🔹 [{proto}] {timestamp} | {src} → {dst}"
        
        if packet.haslayer(TCP) or packet.haslayer(UDP):
            sport = packet[TCP].sport if packet.haslayer(TCP) else packet[UDP].sport
            dport = packet[TCP].dport if packet.haslayer(TCP) else packet[UDP].dport
            log += f" | Port: {sport} → {dport}"
        
        if packet.haslayer(DNS) and packet[DNS].qr == 0:
            try:
                log += f' | Requête: "{packet[DNS].qd.qname.decode()}"'
            except:
                pass
        
        log += f" | {len(packet)} octets"
        print(log)

print("Démarrage de la capture...")
sniff(prn=analyse_packet, store=0)
