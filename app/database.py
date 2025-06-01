from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email
from models import Base, User, Password
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError

engine = create_engine("sqlite:///slurppass.db", echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

class HashArgon:
    ph = PasswordHasher(
        time_cost=3,
        memory_cost=131072,  # 128 MB
        parallelism=4,
        hash_len=32,
        salt_len=16,
    )

    @staticmethod
    def generate_hash(password: str) -> str:
        return HashArgon.ph.hash(password)

    @staticmethod
    def verify_hash(hashed_password: str, input_password: str) -> bool:
        try:
            return HashArgon.ph.verify(hashed_password, input_password)
        except InvalidHashError:
            return False
        except VerifyMismatchError:
            return False

#utility functions
def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()


def confirm_action(prompt: str) -> bool:
    return input(f"{prompt} (yes/no): ").strip().lower() == "yes"


def is_validEmail(email):
    try:
        valid = validate_email(email, check_deliverability=True)
        return valid.normalized
    except:
        return None

#crud
def register():
    name, email, password = (
        input("enter name: "),
        input("enter email: "),
        input("enter password: "),
    )
    emailInfo = is_validEmail(email)
    if emailInfo:
        if get_user_by_email(emailInfo):
            print(f"user already exists: {email}")
            return
        hashed_password = HashArgon.generate_hash(password)
        print(hashed_password)
        try:
            session.add(User(name=name, email=email, password=hashed_password))
            session.commit()
            print("user added")

        except IntegrityError:
            session.rollback()
            print("Error")

    else:
        print("email is not valid")


def login():
    email = input("Enter email: ")
    password = input("Enter password: ")

    user = get_user_by_email(email)

    if not user:
        print("No user found with that email!")
        return

    if HashArgon.verify_hash(user.password, password):
        print("Logging in...")
    else:
        print("Invalid password!")
