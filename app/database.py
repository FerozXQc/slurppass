from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email
from models import Base, User, Password
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from schemas import RegisterUserSchema, LoginUserSchema
from fastapi import Response
engine = create_engine("sqlite:///slurppass.db", echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

class HashArgon:     #deals with the encryption and decryption
    ph = PasswordHasher(
        time_cost=3,
        memory_cost=131072,  # 128 MiB
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

class UtilityFunctions:    #handy utility functions...

    @staticmethod
    def get_user_by_email(email): 
        return session.query(User).filter_by(email=email).first()

    @staticmethod
    def confirm_action(prompt: str) -> bool:
        return input(f"{prompt} (yes/no): ").strip().lower() == "yes"

    @staticmethod
    def is_validEmail(email):
        try:
            valid = validate_email(email, check_deliverability=True)
            return valid.normalized
        except:
            return None
    

#crud


def db_createUser(name:str,email:str,hashed_password:str):
    try:
        session.add(User(name=name, email=email, password=hashed_password))
        session.commit()
        return f'User:{name} added successfully.'

    except IntegrityError as e:
        session.rollback()
        return f'error: {e}'

def db_addPass(user_id:str,title:str,desc:str,passwd:str):
    try:
        session.add(Password(user_id=user_id,title=title,desc=desc,passwd=passwd))
        session.commit()
        return f'Password saved successfully.'

    except IntegrityError as e:
        session.rollback()
        return f'error: {e}'

def db_listPassLogs(user_id:str):
    list = session.query(Password).filter_by(user_id=user_id).all()
    return list

def db_getPassLog(user_id:str,task_id:int):
    passLog = session.query(Password).filter_by(task_id=task_id, user_id=user_id).first()
    if type(passLog) is not Password:
        return f'no passLog found with the id: #{task_id}'
    return passLog

def db_deletePassLog(user_id:str,task_id:int):
    passLog = db_getPassLog(user_id,task_id)
    session.delete(passLog)
    session.commit()
    return f'passLog with the the id: #{task_id} has been removed'

