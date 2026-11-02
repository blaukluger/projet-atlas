# Importation des framworks et la base de données
from sqlmodel import SQLModel, Field
from typing import Optional
from database import engine

# Création des classes qui sont les tables de application atlas
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email:str
    password_hash:str
    role:str

class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title:str

# Permettre de créer des tables dans ma base de données
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
# Phase de lancement 
    if __name__ == "__main__":
        create_db_and_tables()
        print('Tables creer avec succes')