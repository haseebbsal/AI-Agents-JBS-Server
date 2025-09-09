from pymongo import MongoClient
import pymongo
import jwt
from dotenv import load_dotenv
from datetime import datetime,timedelta,timezone
import os
import bcrypt
import requests
from langchain_community.document_loaders import PyMuPDFLoader
from docx import Document
from langchain_community.document_loaders import CSVLoader
import mailtrap as mt
from PyPDF2 import PdfMerger
from agents.virtual_assistant_agent.crew import ChatCrew
from pathlib import Path


load_dotenv()

uri = os.getenv('MONGO_URI')
secret_key=os.getenv('JWT_SECRET')
client = MongoClient(uri, server_api=pymongo.server_api.ServerApi(
        version="1", strict=True, deprecation_errors=True))
database=client['ai-agents']
userCollection=database['users']


def create_token(data,type:str):
    accessTokenExpiry= datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    refreshTokenExpiry= datetime.now(tz=timezone.utc) + timedelta(days=7)
    if(type=='accessToken'):
        data['exp']=int(accessTokenExpiry.timestamp())
    else:
        data['exp']=int(refreshTokenExpiry.timestamp())
    token=jwt.encode(data,secret_key)
    return token

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password)
    
def get_password_hash(password):
    hashedPassword=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashedPassword

def create_user(user,refreshToken):
    

    # mail = mt.Mail(
    #     sender=mt.Address(email="dev@demomailtrap.com", name="Mailtrap Test"),
    #     to=[mt.Address(email=user['email'])],
    #     subject="You are awesome!",
    #     text="Congrats for sending test email with Mailtrap!",
    # )

    # client = mt.MailtrapClient(token=os.getenv("MAIL_TOKEN"))
    # client.send(mail)

    userCollection.insert_one({"email":user['email'],"password":user['password'],"refresh_token":refreshToken})
    return user

def decode_token(token):
   decodedToken=jwt.decode(token, secret_key, algorithms=["HS256"])
   return decodedToken

def get_user(user):
    foundUser=userCollection.find_one({"email":user['email']})
    return foundUser

def change_password(user,newPass):
    password=get_password_hash(newPass)
    foundUser=userCollection.update_one({"email":user['email']},{"$set":{"password":password}})
    return foundUser

def updateRefreshToken(email,refreshToken):
    userCollection.update_one({"email":email},{"$set":{"refresh_token":refreshToken}})
    return 'updated'

def verifyRefreshMatchToken(email,refreshToken):
    return userCollection.find_one({"email":email,"refresh_token":refreshToken})

def load_document(file_path: str):
    """
    Dynamically load a document using the appropriate loader based on the file type.
    Handles PDFs, DOCX, and TXT files.
    """
    if file_path.endswith(".pdf"):
        # Use PyMuPDFLoader for PDFs
        loader = PyMuPDFLoader(file_path)
        try:
            docs = loader.load()
            return "\n\n".join([doc.page_content for doc in docs if doc.page_content])
        except Exception as e:
            raise ValueError(f"Failed to load PDF document: {e}")

    elif file_path.endswith(".docx"):
        # Use python-docx for DOCX files
        try:
            doc = Document(file_path)
            return "\n\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
        except Exception as e:
            raise ValueError(f"Failed to load DOCX document: {e}")

    elif file_path.endswith(".txt"):
        # Handle TXT files directly
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Failed to load TXT document: {e}")

    else:
        raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")


    
def retreiveUsers():
    listOfUsers=[]
    usersFind=userCollection.find()
    for i in usersFind:
        listOfUsers.append(i['email'])
    return listOfUsers