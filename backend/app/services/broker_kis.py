
from sqlalchemy.orm import Session
class KISBroker:
    def __init__(self, db: Session):
        self.db = db
    def place_order(self, sym, side: str, qty: float, price: float|None):
        return False, {}
