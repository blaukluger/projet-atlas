# Importation Framworks
from sqlmodel import Session, create_engine , SQLModel

sqlite_file_name ="database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url , connect_args={"check_same_thread": False})
#postgresql_url ="postgresql://postgres:123456@localhost:5432/projet_atlas"
#engine = create_engine(postgresql_url)
# Une fonction qui permet de données une session pour communiquer avec la base de donnée
def get_session():
    with Session(engine) as session:
        yield session
get_db = get_session

# Fonction pour créer les tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)