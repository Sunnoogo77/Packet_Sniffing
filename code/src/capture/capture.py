# Script de capture avec Scapy

from scapy.all import  sniff, IP, TCP, UDP, DNS
from datetime import datetime
import sys
import os

#Définition du repertoire où stocker les fichiers .pcap
PCAP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pcap_files"))  # ✅ Correct


#S'assurer que le dossiers existe
os.makedirs(PCAP_DIR, exist_ok=True)

# Get the absolute path to the project root (Packet_Sniffing)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) 
sys.path.insert(0, project_root)

from src.storage.insert_data import insert_packet, insert_known_device, insert_visited_site 



def analyse_packet(packet):
    """ Analyser et envoyer les donnés à Supabase """
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
                    insert_visited_site(src_ip, site_visited)
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
            
            insert_packet(data)   
            
            if src_mac:
                insert_known_device(src_mac, src_ip)
                if dst_mac:
                    insert_known_device(dst_mac, dst_ip)

def main():
    """Configuration de l'utilisateur et démarrage du sniffing."""
    print("🔹 Configuration de la capture réseau")

    interface = input("📡 Entrez l'interface réseau (ex: wlan0, eth0) : ")
    packet_count = int(input("🔍 Entrez le nombre de paquets à analyser avec Scapy : "))

    print("\n\t🚀 Démarrage du sniffing Scapy...")
    sniff(iface=interface, prn=analyse_packet, count=packet_count, store=10)

if __name__ == "__main__":
    print("-----------------"*5 +"\n")
    print("-----------------"*5 +"\n")
    main()