# Connexion PostgreSQL
import os
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
        print("\n\t✅ Données insérées avec succès")
    except Exception as e:
        print(f"\n\t❌ Erreur d'insertion des données: {e}")

def fetch_data(table_name, limit=10, conditions=None):
    """Récupère des données d'une table avec des conditions facultatives."""
    try:
        query = supabase.table(table_name).select("*").limit(limit)
        
        # Appliquer les conditions si elles existent
        if conditions:
            for key, value in conditions.items():
                query = query.eq(list(conditions.keys())[0], list(conditions.values())[0])

        response = query.execute()
        return response
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des données de {table_name} : {e}")
        return None