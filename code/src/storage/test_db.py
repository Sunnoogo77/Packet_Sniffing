# import psycopg2
# from dotenv import load_dotenv
# import os
# import urllib.parse
# from supabase import create_client

import os
from supabase import create_client

url = 'https://fhnutlzhixbwszpftpqb.supabase.co'
key ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZobnV0bHpoaXhid3N6cGZ0cHFiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk0NzU4MDIsImV4cCI6MjA1NTA1MTgwMn0.q6WMdluwoEfr3qspZxp8WSPkNoMq0K7tMxRJrgQ11lU'

supabase = create_client(url, key)

response = supabase.execute()
print(response)


# load_dotenv()

# USER = os.getenv("user")
# PASSWORD = os.getenv("password")
# HOST = os.getenv("host")
# PORT = os.getenv("port")
# DBNAME = os.getenv("dbname")

# encoded_password = urllib.parse.quote_plus(PASSWORD)  # URL-encode the password

# try:
#     connection = psycopg2.connect(
#         user=USER,
#         password=encoded_password,
#         host=HOST,
#         port=PORT,
#         dbname=DBNAME
#     )
#     print("Connection successful!")
#     # ... rest of your code
# except UnicodeDecodeError as e:
#     print(f"Decoding error: {e}")
#     print(f"Error at position: {e.start}")