import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Inventory Service")

# Mock database
INVENTORY_DB: Dict[int, dict] = {
    1: {"name": "Laptop", "price": 999.99, "stock": 10},
    2: {"name": "Smartphone", "price": 499.99, "stock": 25}
}

class Product(BaseModel):
    name: str
    price: float
    stock: int

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    product = INVENTORY_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product_id": product_id, **product}

if __name__ == "__main__":
    uvicorn.run("inventory_service:app", host="0.0.0.0", port=8001, reload=True)
