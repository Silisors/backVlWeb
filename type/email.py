from typing import List
import strawberry
from conn.cliente import records
from strawberry.types import Info
from bson import ObjectId


@strawberry.type
class Email:
    _id: strawberry.ID
    name: str
    email: str
    phone: str


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
            )
            emails.append(email)
        return emails


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_email(self, name: str, email: str, phone: str) -> str:
        email = {
            "name": name,
            "email": email,
            "phone": phone
        }
        result = await records.insert_one(email)
        inserted_id = str(result.inserted_id)
        return strawberry.ID(inserted_id)

    @strawberry.mutation
    async def update_email(self, _id: strawberry.ID, name: str, email: str, phone: str) -> str:
        result = await records.update_one(
            {"_id": ObjectId(_id)},
            {"$set": {"name": name, "email": email, "phone": phone}}
        )

        if result.modified_count == 1:
            updated_email_document = await records.find_one({"_id": ObjectId(_id)})
            return Email(
                _id=str(updated_email_document["_id"]),
                name=updated_email_document["name"],
                email=updated_email_document["email"],
                phone=updated_email_document["phone"],
            )

    @strawberry.mutation
    async def delete_email(self, _id: strawberry.ID) -> str:
        result = await records.delete_one({"_id": ObjectId(_id)})

        if result.deleted_count == 1:
           return f"Email with ID {ObjectId(_id)} deleted successfully."
        else:
            return f"Email with ID {ObjectId(_id)} not found."