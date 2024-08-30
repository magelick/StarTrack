from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    role = Column(String(20), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    terms_accepted = Column(Boolean, default=False)

    children = relationship('ChildProfile', back_populates='parent')

class ChildProfile(Base):
    __tablename__ = 'child_profile'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)
    parent_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    parent = relationship('User', back_populates='children')
    avatar_url = Column(String(200), nullable=True)
    access_list = Column(JSON, nullable=True)
    current_owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    current_owner = relationship('User', backref='owned_children', foreign_keys=[current_owner_id])
    ownership_transfer_history = Column(JSON, nullable=True)
