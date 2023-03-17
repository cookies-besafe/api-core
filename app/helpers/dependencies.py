from fastapi import Header, HTTPException


async def get_token_header(authorization: str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No Authorization header is provided")
    print(authorization)
