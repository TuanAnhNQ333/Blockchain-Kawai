from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    
    bids = relationship("Bid", back_populates="user")

class AuctionItem(Base):
    __tablename__ = "auction_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    starting_price = Column(Float)
    current_price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User")
    bids = relationship("Bid", back_populates="item")

class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("auction_items.id"))
    
    user = relationship("User", back_populates="bids")
    item = relationship("AuctionItem", back_populates="bids")
