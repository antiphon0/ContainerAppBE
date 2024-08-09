import logging
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.get("/api/data")
async def read_data(request: Request):
    # Log the incoming request headers for debugging purposes
    logging.info("Received request with headers: %s", request.headers)

    # Retrieve the tokens injected by Azure Easy Auth
    user_id_token = request.headers.get("X-MS-TOKEN-AAD-ID-TOKEN")
    user_access_token = request.headers.get("X-MS-TOKEN-AAD-ACCESS-TOKEN")

    # Log the tokens received
    logging.info("ID Token: %s", user_id_token)
    logging.info("Access Token: %s", user_access_token)

    # If the tokens are missing, return a 401 Unauthorized error with detailed information
    if not user_id_token or not user_access_token:
        missing_tokens = []
        if not user_id_token:
            missing_tokens.append("ID Token")
        if not user_access_token:
            missing_tokens.append("Access Token")
        error_detail = f"Missing authentication tokens: {', '.join(missing_tokens)}"
        logging.error(error_detail)
        raise HTTPException(status_code=401, detail=error_detail)
    
    # Perform actions with the tokens if necessary, such as calling other APIs or verifying claims
    
    return {
        "message": "Hello from FastAPI",
        "id_token": user_id_token,
        "access_token": user_access_token
    }
