from fastapi import FastAPI
import database

app = FastAPI()

@app.get("/products")
async def get_products():
    async with database.pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, name, price FROM products WHERE active=TRUE"
        )

    return [
        {"id": r["id"], "name": r["name"], "price": r["price"]}
        for r in rows
    ]