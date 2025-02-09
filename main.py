import uvicorn
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from scraper import scrape_mff_players

# 🚀 Secure API Docs
security = HTTPBasic()

# ✅ Load environment variables before defining routes
DOCS_USER = os.getenv("DOCS_USER", "admin")
DOCS_PASS = os.getenv("DOCS_PASS", "securepassword")


# ✅ Disable FastAPI's default Swagger UI to enforce security
app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/docs", include_in_schema=False)
async def get_docs(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != DOCS_USER or credentials.password != DOCS_PASS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Secure API Docs")

@app.get("/players")
def get_players():
    return scrape_mff_players()

@app.get("/")
def read_root():
    return {"message": "MFF Players API is running!"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "testuser" or form_data.password != "password123":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"access_token": form_data.username, "token_type": "bearer"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)