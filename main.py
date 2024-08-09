import logging
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.get("/api/data")
async def read_data(request: Request):
    # Log the incoming request headers for debugging purposes
    logging.info("Received request with headers: %s", request.headers)

    # Retrieve the client principal information injected by Azure Easy Auth
    client_principal_name = request.headers.get("X-MS-CLIENT-PRINCIPAL-NAME")
    client_principal_id = request.headers.get("X-MS-CLIENT-PRINCIPAL-ID")

    # Log the client principal information
    logging.info("Client Principal Name: %s", client_principal_name)
    logging.info("Client Principal ID: %s", client_principal_id)

    # If the principal information is missing, return a 401 Unauthorized error with detailed information
    if not client_principal_name or not client_principal_id:
        missing_principal_info = []
        if not client_principal_name:
            missing_principal_info.append("Client Principal Name")
        if not client_principal_id:
            missing_principal_info.append("Client Principal ID")
        error_detail = f"Missing client principal information: {', '.join(missing_principal_info)}"
        logging.error(error_detail)
        raise HTTPException(status_code=401, detail=error_detail)
    
    # Optionally, still log and check tokens if you require them
    user_id_token = request.headers.get("X-MS-TOKEN-AAD-ID-TOKEN")
    user_access_token = request.headers.get("X-MS-TOKEN-AAD-ACCESS-TOKEN")
    
    logging.info("ID Token: %s", user_id_token)
    logging.info("Access Token: %s", user_access_token)

    # Respond with the client principal information
    return {
        "message": "Hello from FastAPI",
        "client_principal_name": client_principal_name,
        "client_principal_id": client_principal_id,
        "id_token": user_id_token,
        "access_token": user_access_token
    }
