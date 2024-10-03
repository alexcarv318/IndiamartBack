from typing import Annotated

import uvicorn
from fastapi import FastAPI
from fastapi.params import Query
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from db import engine, Base

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/api/products/categories")
def get_products_categories():
    products_table = Base.classes.product_details

    with Session(engine) as session:
        product_categories = session.query(products_table.category).distinct().limit(20).all()
        product_categories = [category[0] for category in product_categories]
        print(product_categories)
        return {
            "product_categories": product_categories
        }

@app.get("/api/products/filter")
def filter_products(
    min_price: float | None = None,
    max_price: float | None = None,
    name: Annotated[str | None, Query(max_length=255)] = None,
    category: Annotated[str | None, Query(max_length=255)] = None,
    company_name: Annotated[str | None, Query(max_length=255)] = None,
    company_city: Annotated[str | None, Query(max_length=255)] = None,
    company_state: Annotated[str | None, Query(max_length=255)] = None,
    company_country: Annotated[str | None, Query(max_length=255)] = None,
):
    products_table = Base.classes.product_details
    company_table = Base.classes.company_details

    with Session(engine) as session:
        stmt = session.query(products_table).join(company_table, products_table.company_id == company_table.id)
        if name:
            stmt = stmt.filter(
                products_table.name.contains(name)
            )
        if category:
            stmt = stmt.filter(
                products_table.category.contains(category)
            )
        if min_price:
            stmt = stmt.filter(
                products_table.price >= min_price,
            )
        if max_price:
            stmt = stmt.filter(
                products_table.price <= max_price,
            )
        if company_name:
            stmt = stmt.filter(
                products_table.name.contains(company_name),
            )
        if company_city:
            stmt = stmt.filter(
                products_table.city.contains(company_city),
            )
        if company_state:
            stmt = stmt.filter(
                products_table.state.contains(company_state),
            )
        if company_country:
            stmt = stmt.filter(
                products_table.country.contains(company_country),
            )

        result = stmt.limit(50).all()

        return {"products": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    engine.connect()
