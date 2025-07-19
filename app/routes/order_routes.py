from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from app.database import orders_collection, products_collection
from app.models.order import Order

router = APIRouter()

# Create Order


@router.post("/orders", status_code=201)
async def create_order(order: Order):
    """
    Creates a new order.
    """
    try:
        # Validate each productId in the order
        for item in order.items:
            product = await products_collection.find_one({"_id": ObjectId(item.productId)})
            if not product:
                raise HTTPException(status_code=404, detail=f"Product ID {item.productId} not found")

        result = await orders_collection.insert_one(order.dict())
        return {"id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get Orders by User ID

@router.get("/orders/{user_id}")
async def get_orders(
    user_id: str,
    limit: int = Query(10, description="Number of orders to return"),
    offset: int = Query(0, description="Number of orders to skip (pagination)")
):
    """
    Fetch all orders for a user with product details and total price.
    """
    try:
        orders_cursor = orders_collection.find({"userId": user_id}).sort("_id", 1).skip(offset).limit(limit)

        orders = []
        async for order in orders_cursor:
            order_items = []
            total_price = 0.0

            for item in order["items"]:
                product = await products_collection.find_one({"_id": ObjectId(item["productId"])})
                if product:
                    product_details = {
                        "id": str(product["_id"]),
                        "name": product["name"]
                    }
                    total_price += product["price"] * item["qty"]
                else:
                    product_details = {"id": item["productId"], "name": "Unknown"}

                order_items.append({
                    "productDetails": product_details,
                    "qty": item["qty"]
                })

            orders.append({
                "id": str(order["_id"]),
                "items": order_items,
                "total": total_price
            })

        return {
            "data": orders,
            "page": {
                "next": offset + limit,
                "limit": len(orders),
                "previous": max(offset - limit, 0)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
