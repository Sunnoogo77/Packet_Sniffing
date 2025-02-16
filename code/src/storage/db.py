# Connexion PostgreSQL
import os
import datetime
from dotenv import load_dotenv
from supabase import create_client
from src.storage.models import TABLES

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_into_table(table_name, data):
    """Insérer les données dans la base PostgreSQL Supabase"""
    
    try:
        supabase.table(table_name).insert(data).execute()    
        print("\n\t✅ Données insérées avec succès -------><-------- ")    
    except Exception as e:
        print(f"\n\t❌ Erreur d'insertion des données: {e}")

# def fetch_data(table_name, limit=10, conditions=None):
#     """Récupère des données d'une table avec des conditions facultatives."""
#     try:
#         query = supabase.table(table_name).select("*").limit(limit)
        
#         # Appliquer les conditions si elles existent
#         if conditions:
#             for key, value in conditions.items():
#                 query = query.eq(list(conditions.keys())[0], list(conditions.values())[0])

#         response = query.execute()
#         return response
#     except Exception as e:
#         print(f"❌ Erreur lors de la récupération des données de {table_name} : {e}")
#         return None

def update_last_seen(mac_address):
    """Met à jour le champ last_seen pour un appareil existant."""
    try:
        now = datetime.datetime.now()
        now_str = now.isoformat()
        supabase.table(TABLES["known_devices"]).update({"last_seen": now_str}).eq("mac_address", mac_address).execute()
        print(f"⏱️  Dernière vue de l'appareil {mac_address} mise à jour à {now}.")
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de last_seen pour {mac_address} : {e}")
        

def fetch_data(table_name, limit=10, conditions=None):
    """Récupère des données d'une table avec des conditions facultatives."""
    try:
        query = supabase.table(table_name).select("*").limit(limit)

        if conditions:
            for key, value in conditions.items():
                query = query.eq(key, value)

        response = query.execute()

        if response.data is None:  # Vérifier si data est None, ce qui indique une erreur
            print(f"❌ Erreur Supabase lors de la récupération des données de {table_name} : {response.error}")
            return None

        return response.data

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des données de {table_name} : {e}")
        return None