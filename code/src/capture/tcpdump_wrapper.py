# # Utilisation de TCPDump
# import os 
# import getpass
# import subprocess
# from src.utils.helpers import detect_os

# def start_tcpdump_linux(interface, duration, sudoPas, output_file):
#     """Lance TCPDump sous Linux (Necessite Sudo)."""
    
#     sudo_password = sudoPas
#     command = f"echo {sudo_password} | sudo -S tcpdump -i {interface} -G {duration} -w {output_file}"
#     print(f"🚀 Démarrage de TCPDump (Linux) : {command}")
    
#     try:
#         subprocess.run(command, shell=True, check=True)
#         print("Capture terminée (Linux)")
#     except subprocess.CalledProcessError as e:
#         print(f"❌ Erreur lors de la capture: {e}")

# def start_tcpdump_windows(interface, duration, output_file):
#     """Lance TCPDump sous Windows."""
    
#     command = f"tcpdump -i {interface} -G {duration} -w {output_file}"
#     print(f"🚀 Démarrage de TCPDump (Windows) : {command}")
    
#     try:
#         subprocess.run(command, shell=True, check=True)
#         print("Capture terminée (Windows)")
#     except subprocess.CalledProcessError as e:
#         print(f"❌ Erreur lors de la capture: {e}")

# Utilisation de TCPDump
import os 
import sys
import getpass
import subprocess

# Get the absolute path to the project root (Packet_Sniffing)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) # Adjust the ".." parts based on your directory depth
sys.path.insert(0, project_root) 

from src.utils.helpers import detect_os

# Définition du répertoire où stocker les fichiers .pcap
PCAP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pcap_files"))

# S'assurer que le dossier existe
os.makedirs(PCAP_DIR, exist_ok=True)

def start_tcpdump_linux(interface, duration, sudoPas, filename):
    """Lance TCPDump sous Linux (Nécessite Sudo)."""
    
    sudo_password = sudoPas
    output_file = os.path.join(PCAP_DIR, filename)  # Stocker le fichier dans pcap_files
    command = f"echo {sudo_password} | sudo -S tcpdump -i {interface} -G {duration} -w {output_file}"
    
    print(f"🚀 Démarrage de TCPDump (Linux) : {command}")
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ Capture terminée (fichier enregistré : {output_file})")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la capture: {e}")

def start_tcpdump_windows(interface, duration, filename):
    """Lance TCPDump sous Windows."""
    
    output_file = os.path.join(PCAP_DIR, filename)  # Stocker le fichier dans pcap_files
    command = f"tcpdump -i {interface} -G {duration} -w {output_file}"
    
    print(f"🚀 Démarrage de TCPDump (Windows) : {command}")
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ Capture terminée (fichier enregistré : {output_file})")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la capture: {e}")
