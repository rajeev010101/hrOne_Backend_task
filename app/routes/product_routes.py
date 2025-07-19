from fastapi import APIRouter, Query
from typing import Optional
from app.database import products_collection
from app.models.product import Product

router = APIRouter()

# Create Product

@router.post("/products", status_code=201)
async def create_product(product: Product):
    result = await products_collection.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

# List Products with filters & pagination

@router.get("/products")
async def list_products(
    name: Optional[str] = Query(None, description="Search by product name (regex/partial)"),
    size: Optional[str] = Query(None, description="Filter products by size"),
    limit: int = Query(10, description="Number of products to return"),
    offset: int = Query(0, description="Number of products to skip (pagination)")
):
    filter_query = {}
    if name:
        filter_query["name"] = {"$regex": name, "$options": "i"}
    if size:
        filter_query["sizes.size"] = {"$regex": f"^{size}$", "$options": "i"}

    # Async cursor
    products_cursor = products_collection.find(filter_query).sort("_id", 1).skip(offset).limit(limit)

    products = []
    async for product in products_cursor:
        products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "sizes": product.get("sizes", [])
        })

    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": len(products),
            "previous": max(offset - limit, 0)
        }
    }
