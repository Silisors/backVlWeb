from fastapi import FastAPI
from controllers.email import email

app = FastAPI()
app.include_router(email)