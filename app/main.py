from fastapi import FastAPI
from app.routes import product_routes, order_routes

app = FastAPI(title="hrOne API")

# Include routers
app.include_router(product_routes.router)
app.include_router(order_routes.router)

# For Render or local testing
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
