import socket


from src.storage.db import insert_into_table, fetch_data
from src.storage.models import TABLES

def get_hostname(ip_adrr):
    """Essaie de récupérer le hostname via une requête DNS inverse"""
    try:
        hostname = socket.gethostbyaddr(ip_adrr)[0]
        return hostname
    except socket.herror:
        return "UNKNOWN"

def insert_packet(data):
    """Insère un packet réseau dans la table realtime_traffic"""
    insert_into_table(TABLES["realtime_traffic"], data)

def insert_known_device(mac_address, ip_address):
    """Ajoute un appareil détecté dans known_devices uniquement s'il n'existe pas déjà."""

    existing_device = fetch_data(TABLES["known_devices"], conditions={"mac_address": mac_address})
    
    if existing_device :
        print(f"⚠️ L'appareil {mac_address} existe déjà dans la base.")
        return
    
    hostname = get_hostname(ip_address)
    data = {
        "mac_address": mac_address,
        "ip_address": ip_address,
        "hostname": hostname
    }
    insert_into_table(TABLES["known_devices"], data)


def insert_visited_site(src_ip, domain):
    """Ajoute un site vsité dasn visited_sites"""
    data = {
        "src_ip": src_ip,
        "domain": domain
    }
    insert_into_table(TABLES["visited_sites"], data)