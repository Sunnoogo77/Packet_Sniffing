# Script de capture avec Scapy

# Il sagit ici d'un code juste pour creer la mabranche celle de sniffing ( pour la générations des donnés )

from scapy.all import  sniff, IP, TCP, UDP, DNS
from datetime import datetime
import sys
import os

# Get the absolute path to the project root (Packet_Sniffing)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) # Adjust the ".." parts based on your directory depth
sys.path.insert(0, project_root)  # Insert at the beginning of the path

from src.storage.db import insert_into_db # Now this should work




def analyse_packet(packet):
    """ ANalyser et envoyer les donnés à Supabase """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_mac = packet.src if hasattr(packet, "src") else None
        dst_mac = packet.dst if hasattr(packet, "dst") else None
        protocol = packet[IP].proto
        data_size = len(packet)
        
        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            site_visited = None
            
            if packet.haslayer(DNS) and packet[DNS].qr == 0:
                try:
                    site_visited = packet[DNS].qd.qname.decode("utf-8")
                except:
                    pass
                
            data = {
                "timestamp": timestamp,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_mac": src_mac,
                "dst_mac": dst_mac,
                "protocol": protocol,
                "src_port": src_port,
                "dst_port": dst_port,
                "site_visited": site_visited,
                "data_size": data_size
            }
            
            insert_into_db(data)    

print("\n\t🚀 Démarrage de la capture des paquets...")
sniff(prn=analyse_packet, store=0, count=1000) # Capturer 1000 paquets
