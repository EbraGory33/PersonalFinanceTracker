from app.core.config import settings
import plaid
from plaid.api import plaid_api
import base64

# Available environments are
# 'Production'
# 'Sandbox'
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': settings.PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

def encrypt_id(id: str) -> str:
    """Encodes a string ID to base64 format (like JavaScript's btoa)"""
    encoded_bytes = base64.b64encode(id.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decrypt_id(encoded_id: str) -> str:
    """Decodes a base64-encoded string back to original"""
    decoded_bytes = base64.b64decode(encoded_id.encode('utf-8'))
    return decoded_bytes.decode('utf-8')
