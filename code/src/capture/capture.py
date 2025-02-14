# Script de capture avec Scapy

# Il sagit ici d'un code juste pour creer la mabranche celle de sniffing ( pour la générations des donnés )

from scapy.all import  sniff, IP, TCP, UDP, DNS
from datetime import datetime
import sys
import os

#Définition du repertoire où stocker les fichiers .pcap
PCAP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pcap_files"))  # ✅ Correct


#S'assurer que le dossiers existe
os.makedirs(PCAP_DIR, exist_ok=True)

# Get the absolute path to the project root (Packet_Sniffing)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) # Adjust the ".." parts based on your directory depth
sys.path.insert(0, project_root)  # Insert at the beginning of the path

from src.storage.insert_data import insert_packet, insert_known_device, insert_visited_site # Now this should work
from src.capture.tcpdump_wrapper import start_tcpdump_linux, start_tcpdump_windows
from src.utils.helpers import detect_os 



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

def analyse_pcap(filename):
    """Analyser un fichier pcap"""
    file_path = os.path.join(PCAP_DIR, filename)
    
    if not os.path.exists(file_path):
        print(f"❌ Le fichier {file_path} n'existe pas.")
        return
    
    packets = sniff(offline=file_path)
    for packet in packets:
        analyse_packet(packet)
        

# print("\n\t🚀 Démarrage de la capture des paquets...")
# sniff(prn=analyse_packet, store=0, count=1000) # Capturer 1000 paquets


def main():
    """Configuration de l'utilisateur et démarrage du sniffing."""
    print("🔹 Configuration de la capture réseau")

    interface = input("📡 Entrez l'interface réseau (ex: wlan0, eth0) : ")
    duration = int(input("⏳ Entrez la durée de capture TCPDump (en secondes) : "))
    packet_count = int(input("🔍 Entrez le nombre de paquets à analyser avec Scapy : "))
    output_file = "capture.pcap"

    os_type = detect_os()

    if os_type == "linux":
        start_tcpdump_linux(interface, duration, output_file)
    elif os_type == "windows":
        start_tcpdump_windows(interface, duration, output_file)
    else:
        print("❌ Système non reconnu, arrêt de la capture.")
        return

    print("🚀 Démarrage du sniffing Scapy...")
    sniff(iface=interface, prn=analyse_packet, count=packet_count, store=10)

    print("📂 Analyse du fichier PCAP généré...")
    analyse_pcap(output_file)

if __name__ == "__main__":
    print("-----------------")
    main()