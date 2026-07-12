import os
import requests

from dotenv import load_dotenv
from jose import jwt
from jose.exceptions import JWTError

load_dotenv()

class AuthService:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.audience = os.getenv("AUTH0_AUDIENCE")

    def verify_token(self, token: str):
     try:
        print("Domain:", self.domain)
        print("Audience:", self.audience)

        jwks_url = f"https://{self.domain}/.well-known/jwks.json"
        jwks = requests.get(jwks_url).json()
        print("\n========== JWKS ==========")
        print(jwks)
        print("===============================\n")
        unverified_header = jwt.get_unverified_header(token)
        print("\n========== JWT HEADER ==========")
        print(unverified_header)
        print("===============================\n")


        rsa_key = next(
    (
        {
            "kty": key["kty"],
            "kid": key["kid"],
            "use": key["use"],
            "n": key["n"],
            "e": key["e"],
        }
        for key in jwks["keys"]
        if key.get("kid") == unverified_header.get("kid")
    ),
    None,
)

        if not rsa_key:
            raise Exception("Unable to find matching Auth0 public key.")

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=self.audience,
            issuer=f"https://{self.domain}/",
        )

        print("JWT verified successfully.")
        return payload

     except Exception as e:
        print("JWT Verification Error:", type(e).__name__, str(e))
        raise