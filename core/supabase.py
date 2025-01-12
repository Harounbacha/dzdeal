from supabase import create_client, Client
from django.conf import settings

supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)

def get_supabase_client() -> Client:
    """
    Returns a configured Supabase client instance.
    """
    return supabase
