from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from database import SessionLocal, engine, Base
from models import AuctionItem, Bid
from pydantic import BaseModel, constr, confloat, validator
from typing import List, Optional, Union
from datetime import datetime, timezone

app = FastAPI()

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AuctionItemCreate(BaseModel):
    name: str
    description: str 
    starting_price: float

class BidCreate(BaseModel):
    auction_id: int
    bidder_name: str  # Fixed field name
    bid_amount: float # Fixed field name

@app.get("/auctions", response_model=List[AuctionItemCreate])
def get_auctions(db: Session = Depends(get_db)):
    """Get all auction items"""
    return db.query(AuctionItem).all()

@app.post("/auctions")
def create_auction(item: AuctionItemCreate, db: Session = Depends(get_db)):
    """Create new auction item"""
    new_item = AuctionItem(
        name=item.name,
        description=item.description,
        starting_price=item.starting_price
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Auction created", "id": new_item.id}

@app.post("/bids")  # Fixed route path
def place_bid(bid: BidCreate, db: Session = Depends(get_db)):
    """Place a bid on an auction item"""
    auction_item = db.query(AuctionItem).filter(AuctionItem.id == bid.auction_id).first()
    
    if not auction_item:
        raise HTTPException(status_code=404, detail="Auction item not found")
    
    if bid.bid_amount <= auction_item.starting_price:  # Fixed field name
        raise HTTPException(status_code=400, detail="Bid amount must be higher than starting price")
     
    new_bid = Bid(  # Fixed model name
        auction_id=bid.auction_id,
        bidder_name=bid.bidder_name,
        bid_amount=bid.bid_amount
    )
    db.add(new_bid)
    db.commit()
    return {"message": "Bid placed successfully"}

