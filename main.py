from fastapi import FastAPI, Request, HTTPException

app = FastAPI()


@app.get("/api/data")
async def read_data(request: Request):
    # Azure injects the user's token into the request headers
    user_id_token = request.headers.get("X-MS-TOKEN-AAD-ID-TOKEN")
    user_access_token = request.headers.get("X-MS-TOKEN-AAD-ACCESS-TOKEN")
    
    if not user_id_token or not user_access_token:
        raise HTTPException(status_code=401, detail="Missing authentication tokens")

    # You can use these tokens to call other APIs on behalf of the user if needed
    # Or simply use them to identify the user
    return {
        "message": "Hello from FastAPI",
        "id_token": user_id_token,
        "access_token": user_access_token
    }
