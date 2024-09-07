from fastapi import FastAPI
from starlette.responses import RedirectResponse

#Base de datos
from routes.user import user_route


from contextlib import asynccontextmanager
from database import database as connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    #conectar a la base de datos si la conexion esta cerrada
    if connection.is_closed():
        connection.connect()
    try:
        yield  # Aqui es donde se ejecutara la aplicacion
    finally:
        # Cerrar la conexion cuando la aplicacion se detenga
        if not connection.is_closed():
            connection.close()


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

#Rutas
app.include_router(user_route, prefix="/users", tags=["Users"])