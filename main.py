from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.openapi.docs import get_swagger_ui_html
from Auth.auth import authenticate_user, create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES
from routes.user_route import router as usuarios_router
from routes.products_route import router as productos_router
from connection.connection import get_connection
from mysql.connector import MySQLConnection

app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: MySQLConnection = Depends(get_connection)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.correo}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")

# Endpoint para servir el archivo openapi.json
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_json():
    return app.openapi()

app.include_router(usuarios_router, prefix="/api")
app.include_router(productos_router, prefix="/api")
