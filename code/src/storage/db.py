# Connexion PostgreSQL
import os
from dotenv import load_dotenv
from supabase import create_client
from src.storage.models import TABLES

load_dotenv()

# # Fetch variables
# USER = os.getenv("user")
# PASSWORD = os.getenv("password")
# HOST = os.getenv("host")
# PORT = os.getenv("port")
# DBNAME = os.getenv("dbname")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# def connect_db():
#     try:
#         conn = psycopg2.connect(
#             user=USER,
#             password=PASSWORD,
#             host=HOST,
#             port=PORT,
#             dbname=DBNAME
#             )
#         print("-------------> Connexion à la base de données établie <-------------")
#         return conn
#     except Exception as e:
#         print(f"\n\t❌ Erreur de connexion à la base de données: {e}")
#         return None


def insert_into_table(table_name, data):
    """Insérer les données dans la base PostgreSQL Supabase"""
    
    # conn = connect_db()
    # if conn is None :
    #     return
    
    try:
        # cursor = conn.cursor()
        # cursor.execute("""""
        #     INSERT INTO captures (timestamp, src_ip, dst_ip, src_mac, dst_mac, protocol, src_port, dst_port, site_visited,data_size)
        #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        # """, (
        #     data["timestamp"], data["src_ip"], data["dst_ip"], data["src_mac"], data["dst_mac"], 
        #     data["protocol"], data["src_port"], data["dst_port"], data["site_visited"], data["data_size"]
        # ))
        
        # conn.commit()
        # cursor.close()
        # conn.close()
        
        response = supabase.table(table_name).insert(data).execute()    
        print("\n\t✅ Données insérées avec succès")
        
    except Exception as e:
        print(f"\n\t❌ Erreur d'insertion des données: {e}")

def fetch_data(table_name, limit=10):
    """Recupre les dernières donnés d'une table donnée"""
    try:
        response = supabase.table(table_name).select("*").order("timestamp", desc=True).limit(limit).execute()
        return response
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des données de {table_name} : {e}")
        return None