from fastapi import Response, Request


class CookieService:
    @staticmethod
    def set_cookie(response: Response, access_token: str) -> dict:
        response.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True)  #set HttpOnly cookie in response
        return {"access_token": access_token, "token_type": "Bearer"}
    
    @staticmethod
    def get_cookie(request: Request) -> str | None:
        return request.cookies.get('access_token', None)