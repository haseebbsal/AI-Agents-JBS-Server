from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import APIRouter, FastAPI,HTTPException,Header,Depends,Request
from utils.index import decode_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Unauthorized")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Unauthorized")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_token(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid