import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

# Ambil URL dan Key dari environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Periksa apakah URL dan Key tersedia
if not url or not key:
    raise ValueError("Supabase URL and Key must be set in the .env file.")

# Buat instance klien Supabase
# Klien ini akan diimpor dan digunakan di halaman lain
try:
    supabase: Client = create_client(url, key)
    print("Successfully connected to Supabase.")
except Exception as e:
    print(f"Error connecting to Supabase: {e}")
    supabase = None
