# supabase_config.py
from supabase import create_client, Client

SUPABASE_URL = "https://apjgpjisdzsvxyuimonv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwamdwamlzZHpzdnh5dWltb252Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc0NzMyMzcsImV4cCI6MjA3MzA0OTIzN30.nVqyuM5bmBGaPrZcKGXM4k3-U4eGK2snxVrQ2-GonFs"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
