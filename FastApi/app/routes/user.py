from fastapi import APIRouter, Body, HTTPException
from models.user import User

from database import UserModel, database

user_route = APIRouter()


@user_route.get("/")
def get_all_users():
    try:
        users = UserModel.select()  # Obtén todos los usuarios
        # Convierte los usuarios a un formato serializable
        user_list = [{
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "email": user.email,
            "adress": user.adress,  # Asegúrate de que el nombre del campo es correcto
            "document": user.document
        } for user in users]
        return user_list
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@user_route.get("/{userId}")
def get_user(userId: int):
    try:
        user = UserModel.get(UserModel.id == userId)
        return user
    except Exception as e:
        print(e)
        return {"error": str(e)}


@user_route.post("/users")
def create_user(user: User = Body(...)):
    try:
        database.connect()
        UserModel.create(
            name=user.name, 
            age=user.age, 
            email=user.email, 
            adress=user.adress, 
            document=user.document
        )
        return user
    except Exception as e:
        print(e)
        return {"error": str(e)}
    finally:
        database.close()  # Asegúrate de cerrar la conexión


@user_route.put("/{userId}")
def update_user(userId: int,user: User = Body(...)):
    try:
        existing_user = UserModel.get(UserModel.id == userId)  # Busca el usuario por ID
        
        # Actualiza los campos del usuario con los valores del cuerpo de la solicitud
        existing_user.name = user.name
        existing_user.age = user.age
        existing_user.email = user.email
        existing_user.adress = user.adress
        existing_user.document = user.document
        
        existing_user.save()  # Guarda los cambios en la base de datos
        return {"message": "User updated successfully"}
    except UserModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@user_route.delete("/{userId}")
def delete_user(userId: int):
    try:
        user = UserModel.get(UserModel.id == userId)
        user.delete_instance()
        return "Ususario, borrado"
    except Exception as e:
        print(e)
        return {"error":str(e)}