from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email
from models import User, Password

engine = create_engine("sqlite:///slurppass.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

def confirm_action(prompt:str) -> bool:
    return input(f"{prompt} (yes/no): ").strip().lower()  == 'yes'

def is_validEmail(email):
    try:
        valid = validate_email(email, check_deliverability=True)
        return valid.normalized
    except:
        return None

def add_user():
    name, email,password = input('enter name: '), input('enter email: '), input('enter password: ')
    emailInfo =  is_validEmail(email)
    if emailInfo:
        if get_user_by_email(emailInfo):
            print(f'user already exists: {email}')
            return
        try:
            session.add(User(name=name, email=email, password=password))
            session.commit()
            print('user added')

        except IntegrityError:
            session.rollback()         
            print('Error')

    else:
        print('email is not valid')

def hashPW(password):
    return 'new password'