from google.auth.transport import requests
from google.oauth2 import id_token

class Google:
    @staticmethod
    def validated(id_token_str):
        try:
            id_info = id_token.verify_oauth2_token(id_token_str, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info  
        except ValueError as e:
            print(f"Ошибка валидации токена: {e}")
            return None  
