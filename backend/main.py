# Importation 
from fastapi import FastAPI , Depends,HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import User , Ticket
# Initialisation de application FastAPI
app = FastAPI()

# Autorisation que React parle à FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    
)


# Route principale qui envoie un message d'accueil
@app.get("/")
def home():
    return{"message": "Voici le projet Atlas"}

class LoginRequest(BaseModel):
    email: str
    password: str
@app.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or user.password_hash != payload.password:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Identifiants incorectes",
        )
    
    return{
        "message":"Connection réussie",
        "user_id": user.id,
        "email": user.email,
        "role" : user.role
    }
class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str ="user"
    
@app.post("/auth/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Cet Email a dejà été utilisé. "
        )
    new_user= User(
        email=payload.email,
        password_hash=payload.password,
        role=payload.role
     )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message":"Un Utilisateur a été crée avec succès",
        "user_id": new_user.id,
        "email": new_user.email,
        "role" : new_user.role
     }

class TicketCreate(BaseModel):
    title: str
    description: str
    category: str ="Réseau"
    priority : str ="Normale"
    created_by: int

@app.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
        tickets = db.query(Ticket).all()
        return tickets

@app.post("/tickets")
def create_tickets(payload: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(
            title=payload.title,
            description=payload.description,
            category=payload.category,
            priority=payload.priority,
            created_by=payload.created_by,
            status="En cours"
        )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket