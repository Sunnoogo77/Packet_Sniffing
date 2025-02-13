# Connexion PostgreSQL
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DB_URL = os.getenv("postgresql://postgres:yQWPHF4oacRHwdfW@db.fhnutlzhixbwszpftpqb.supabase.co:5432/postgres")

def connect_db():
    try:
        conn = psycopg2.connect(DB_URL)
        # conn = psycopg2.connect(
        #     user=USER,
        #     password=PASSWORD,
        #     host=HOST,
        #     port=PORT,
        #     dbname=DBNAME
        #     )
        print("-------------> Connexion à la base de données établie <-------------")
        return conn
    except Exception as e:
        print(f"\n\t❌ Erreur de connexion à la base de données: {e}")
        return None


def insert_into_db(data):
    """Insérer les données dans la base PostgreSQL Supabase"""
    
    conn = connect_db()
    if conn is None :
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("""""
            INSERT INTO captures (timestamp, src_ip, dst_ip, src_mac, dst_mac, protocol, src_port, dst_port, site_visited,data_size)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["timestamp"], data["src_ip"], data["dst_ip"], data["src_mac"], data["dst_mac"], 
            data["protocol"], data["src_port"], data["dst_port"], data["site_visited"], data["data_size"]
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("\n\t✅ Données insérées avec succès")
        
    except Exception as e:
        print(f"\n\t❌ Erreur d'insertion des données: {e}")