from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import AuctionItem, Bid
from pydantic import BaseModel
from typing import List

# start calling api

app = FastAPI()     

# make table in database if not yet
Base.metadata.create_all(bind=engine)
 
# Dependency get session database
def get_db() : 
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

# Schema data for api
class AuctionItemCreate (BaseModel) :
    name : str
    description: str
    starting_price: float
    
class BidCreate(BaseModel) :
    auction_id: int
    Description: str
    starting_price : float
    
# API get bid list

@app.get("/auctions", response_models = List[AuctionItemCreate])
def get_auctions(db: Session = Depend(get_db)):
    return db.query(AuctionItem.all())
# API : generate new bid
@app.post("/auctions")
def create_auction(item: AuctionItemCreate, db : Session= depends(get_db)):
    new_item = AuctionItem(
        name = item.name,
        description = item.description,
        starting_price = item.starting_price
    )
    db.add(new_item)
    db.commit ()
    db.refresh(new_item)
    return{"message": "Auction created","id": new_item.id}
# API dat gia thau
@app.post("bids")
def place_bid(bid: BidCreate, db: Session = Depends(get_db)):
    auction_item = db.query(AuctionItem).filter(AuctionItem.id == bid.auction_id).first()
    
    if not auction_item:
        raise HTTPException(status_code = 404, detail = "Auction item not found")
    
    if bid.bid_amount <= auction_item.stating_price:
        raise HTTPException(status_code = 400, detail = "Bid amount must be higher than starting price")
     
    new_bid = bid(
        auction_id = bid.auction.id,
        bidder_name = bid.bidder_name,
        bid_amount = bid.bid_amount
    ) 
    db.add(new_bid)
    db.commit()
    return {"message" : "Bid place successfully"}

