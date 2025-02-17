import socket
# from supabase import create_client
# from src.storage.models import TABLES
import datetime

from src.storage.db import insert_into_table, fetch_data, update_last_seen, update_table
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

# def insert_known_device(mac_address, ip_address):
#     """Ajoute un appareil détecté dans known_devices uniquement s'il n'existe pas déjà."""

#     existing_device = fetch_data(TABLES["known_devices"], conditions={"mac_address": ip_address})
#     print(existing_device)
    
#     if existing_device == []:
#         print(f"⚠️ L'appareil {mac_address} existe déjà dans la base.")
#         return
    
#     hostname = get_hostname(ip_address)
#     data = {
#         "mac_address": mac_address,
#         "ip_address": ip_address,
#         "hostname": hostname
#     }
#     insert_into_table(TABLES["known_devices"], data)
#     print(f"📡 Nouvel appareil ajouté à la base de données : {data}")

def insert_known_device(mac_address, ip_address):
    """Ajoute un appareil détecté dans known_devices uniquement s'il n'existe pas déjà."""

    existing_device = fetch_data(TABLES["known_devices"], conditions={"mac_address": mac_address})

    if existing_device is None:  # Vérifier si fetch_data a retourné une erreur
        print(f"❌ Erreur lors de la vérification de l'appareil {mac_address}.")
        return

    if existing_device:  # Vérifier si existing_device contient des résultats
        # print(f"⚠️ L'appareil {mac_address} existe déjà dans la base.")
        # if existing_device[0]["ip_address"] != ip_address:
        # L'adresse IP a changé, mettre à jour last_ip
        try:
            # supabase.table(TABLES["known_devices"]).update({"last_ip": ip_address}).eq("mac_address", mac_address).execute()
            update_table(TABLES["known_devices"], {"last_ip": ip_address}, {"mac_address": mac_address})
            print(f" L'adresse IP de l'appareil {mac_address} a été mise à jour à {ip_address}.")
        except Exception as e:
            print(f" Erreur lors de la mise à jour de last_ip pour {mac_address} : {e}")
        
        update_last_seen(mac_address)
        print("📡 Appareil déjà existant, mise à jour de last_seen.")
        return

    hostname = get_hostname(ip_address)
    data = {
        "mac_address": mac_address,
        "ip_address": ip_address,
        "hostname": hostname
    }
    insert_into_table(TABLES["known_devices"], data)
    print(f" Nouvel appareil ajouté à la base de données : {data}")


def insert_visited_site(src_ip, domain):
    """Ajoute un site vsité dasn visited_sites"""
    try:
        existing_site = fetch_data(TABLES["visited_sites"], conditions={"domain": domain})
        
        if existing_site:
            now = datetime.now().isoformat()
            # supabase.table(TABLES["visited_sites"]).update({"last_seen": now, "visit_count": existing_site[0]["visit_count"] + 1}).eq("domain", domain).execute()
            update_table(TABLES["visited_sites"], {"last_seen": now, "visit_count": existing_site[0]["visit_count"] + 1}, {"domain": domain})
            print(f"🔍 Mise à jour du site visité : {domain}\n")
        else:
            now = datetime.now().isoformat()
            data = {
                "src_ip": src_ip,
                "domain": domain,
                "last_seen": now
            }
            insert_into_table(TABLES["visited_sites"], data)
            print(f"🔍 Nouveau site visité ajouté : {domain}\n")
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion du site visité : {e}")
    # insert_into_table(TABLES["visited_sites"], data)
    
    
#  avant tout, la structure du de mon code est un peu special, moi j'ai separer les fonction dans deux fichiers different de sorte à ce que les fonction s'appelle et tout.....
# et maintenant, j'ai cette erreur la qui se produit, quand je lance le programe :  
# ❌ Erreur lors de la mise à jour de known_devices : BaseFilterRequestBuilder.eq() missing 1 required positional argument: 'value'
# L'adresse IP de l'appareil c6:52:4f:8d:27:64 a été mise à jour à 35.186.224.26.
# # Or voici les code associer : 
# def insert_known_device(mac_address, ip_address):
#     """Ajoute un appareil détecté dans known_devices uniquement s'il n'existe pas déjà."""

#     existing_device = fetch_data(TABLES["known_devices"], conditions={"mac_address": mac_address})

#     if existing_device is None:  # Vérifier si fetch_data a retourné une erreur
#         print(f"❌ Erreur lors de la vérification de l'appareil {mac_address}.")
#         return

#     if existing_device:  # Vérifier si existing_device contient des résultats
#         # print(f"⚠️ L'appareil {mac_address} existe déjà dans la base.")
#         if existing_device[0]["ip_address"] != ip_address:
#             # L'adresse IP a changé, mettre à jour last_ip
#             try:
#                 # supabase.table(TABLES["known_devices"]).update({"last_ip": ip_address}).eq("mac_address", mac_address).execute()
#                 update_table(TABLES["known_devices"], {"last_ip": ip_address}, {"mac_address", mac_address})
#                 print(f" L'adresse IP de l'appareil {mac_address} a été mise à jour à {ip_address}.")
#             except Exception as e:
#                 print(f" Erreur lors de la mise à jour de last_ip pour {mac_address} : {e}")
        
#         update_last_seen(mac_address)
#         print("📡 Appareil déjà existant, mise à jour de last_seen.")
#         return

#     hostname = get_hostname(ip_address)
#     data = {
#         "mac_address": mac_address,
#         "ip_address": ip_address,
#         "hostname": hostname
#     }
#     insert_into_table(TABLES["known_devices"], data)
#     print(f" Nouvel appareil ajouté à la base de données : {data}")

# et voici la fonction qui est appeler : 
# def update_table(table_name, data, conditions):
#     """Met à jour les données d'une table avec des conditions."""

#     try:
#         query = supabase.table(table_name).update(data)

#         if conditions:
#             for key, value in conditions.items():
#                 query = query.eq(key, value)

#         query.execute()
#         print(f"✅ Mise à jour de {table_name} réussie.")
#     except Exception as e:
#         print(f"❌ Erreur lors de la mise à jour de {table_name} : {e}")
#         return None

