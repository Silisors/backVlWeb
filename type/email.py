from datetime import datetime
from typing import List
import strawberry
from conn.cliente import records
from strawberry.types import Info
from bson import ObjectId
import re
import pytz
from zoneinfo import ZoneInfo

@strawberry.type
class Email:
    _id: strawberry.ID
    name: str
    email: str
    phone: str
    zipcode: str
    state: str
    dated: str
@strawberry.type
class Query:
    @strawberry.field
    async def get_email(self) -> List[Email]:
        email_documents = await records.find().to_list(length=None)
        emails = []
        for email_document in email_documents:
            email = Email(
                _id=str(email_document["_id"]),
                name=email_document["name"],
                email=email_document["email"],
                phone=email_document["phone"],
                zipcode=email_document["zipcode"],
                state=email_document["state"],
                dated=email_document["dated"]
            )
            emails.append(email)
        return emails
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_email(self, name: str, email: str, phone: str, zipcode: str, state: str) -> str:
        if len(phone)<8 or len(phone)>11:
            raise ValueError("Enter a valid phone number.")
        if len(zipcode)>5 or len(zipcode)<5:
            raise ValueError("Enter a valid zip code.")
        if not name or not email or not phone or not zipcode or not state:
            raise ValueError("Required fields cannot be empty.")
        if not re.match(r"^[A-Za-z\s]+$", name):
            raise ValueError("Name must only contain letters and spaces.")
        if not re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+.[(a-z)]+$', email):
            raise ValueError("It must be a valid email")
        if not re.match(r"^\d+$", zipcode):
            raise ValueError("Zipcode must only contain numbers.")
        if not re.match(r"^\d+$", phone):
            raise ValueError("Phone number must only contain numbers.")
        existing_email = await records.find_one({"email": email})
        existing_phone = await records.find_one({"phone": phone})
        if existing_email:
            raise ValueError("The email is already registered.")
        if existing_phone:
            raise ValueError("The phone number is already registered.")
        
        # Obtener la fecha y hora actual en la zona horaria de Sacramento
        tiempo_utc = datetime.utcnow()
        huso_horario_sacramento = pytz.timezone('America/Los_Angeles')
        tiempo_sacramento = tiempo_utc.astimezone(huso_horario_sacramento)

        # Formatear la fecha y hora en el formato deseado
        tiempo_formateado = tiempo_sacramento.strftime('Fecha: %d-%m-%Y, Hora: %H:%M:%S')


        email_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "zipcode": zipcode,
            "state": state,
            "dated": tiempo_formateado
        }
        result = await records.insert_one(email_data)
        inserted_id = str(result.inserted_id)
        return strawberry.ID(inserted_id)
    @strawberry.mutation
    async def update_email(self, _id: strawberry.ID, name: str, email: str, phone: str, zipcode: str, state: str) -> str:
        result = await records.update_one(
            {"_id": ObjectId(_id)},
            {"$set": {"name": name, "email": email, "phone": phone, "zipcode": zipcode, "state": state}}
        )
        if result.modified_count == 1:
            updated_email_document = await records.find_one({"_id": ObjectId(_id)})
            return Email(
                _id=str(updated_email_document["_id"]),
                name=updated_email_document["name"],
                email=updated_email_document["email"],
                phone=updated_email_document["phone"],
                zipcode=updated_email_document["zipcode"],
                state=updated_email_document["state"]
            )
    @strawberry.mutation
    async def delete_email(self, _id: strawberry.ID) -> str:
        result = await records.delete_one({"_id": ObjectId(_id)})
        if result.deleted_count == 1:
           return f"Email with ID {ObjectId(_id)} deleted successfully."
        else:
            return f"Email with ID {ObjectId(_id)} not found."