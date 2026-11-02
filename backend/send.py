from database import engine , create_db_and_tables
from models import User
from sqlmodel import Session , select

# Appelation de la fonction pour créer la base et les tables
create_db_and_tables()

# Ouverture d'une session  avec ma base de données
with Session(engine) as session:

    # Véréfication si utilisateur exite
    email_test ="brian.chin2005@gmail.com"
    statement = select(User).where(User.email == email_test)
    existing_user =session.exec(statement).first()

    if not existing_user:
        # Si utilisateur n'existe pas on creer un nouveau
        new_User =User(
            email= email_test,
            password_hash="123456",
            role ="admin"
        )
        session.add(new_User)
        session.commit()
        print(f" Utilisateur {email_test} à été créer avec succès !")
    else:
        print(f" Utilisateur {email_test} existe déja dans la base de données .")