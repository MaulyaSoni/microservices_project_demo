import uvicorn
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Order Service")

# URL of the internal inventory microservice
INVENTORY_SERVICE_URL = "http://localhost:8001/products"
 
class OrderRequest(BaseModel):
    product_id: int
    quantity: int

@app.post("/orders/")
async def create_order(order: OrderRequest):
    # 1. Inter-service Communication: Query the Inventory Service using an async HTTP client
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{INVENTORY_SERVICE_URL}/{order.product_id}")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Product does not exist in inventory")
            response.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Inventory service unavailable")
    
    product_data = response.json()
    
    # 2. Check if enough stock is available
    if product_data["stock"] < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock available")
        
    # 3. Calculate order total and return order confirmation
    total_price = product_data["price"] * order.quantity
    return {
        "status": "Order Placed Successfully",
        "product_name": product_data["name"],
        "quantity": order.quantity,
        "total_cost": round(total_price, 2)
    }

if __name__ == "__main__":
    uvicorn.run("order_service:app", host="0.0.0.0", port=8002, reload=True)
