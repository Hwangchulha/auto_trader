import time, random
def place(symbol:str, side:str, qty:float, price:float|None):
    px = price if price not in (None,0,0.0) else round(random.uniform(100, 200), 2)
    return {"client_id": f"{symbol}-{int(time.time()*1000)}", "status":"filled", "filled_qty": float(qty), "price": float(px)}
