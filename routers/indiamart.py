from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Query, Depends

from dependencies import get_indiamart_repo
from repositories.indiamart_repo import IndiaMartRepository

router = APIRouter(prefix="/indiamart", tags=["indiamart"])


@router.get("/products/categories")
def get_products_categories(
    indiamart_repo: IndiaMartRepository = Depends(get_indiamart_repo),
):
    product_categories = indiamart_repo.get_products_categories()
    return {"product_categories": product_categories}


@router.get("/products/filter")
def filter_products(
    indiamart_repo: IndiaMartRepository = Depends(get_indiamart_repo),
    min_price: float | None = None,
    max_price: float | None = None,
    name: Annotated[str | None, Query(max_length=255)] = None,
    category: Annotated[str | None, Query(max_length=255)] = None,
    company_name: Annotated[str | None, Query(max_length=255)] = None,
    company_city: Annotated[str | None, Query(max_length=255)] = None,
    company_state: Annotated[str | None, Query(max_length=255)] = None,
    company_country: Annotated[str | None, Query(max_length=255)] = None,
):
    try:
        result = indiamart_repo.filter_products(
            name=name,
            category=category,
            min_price=min_price,
            max_price=max_price,
            company_name=company_name,
            company_city=company_city,
            company_state=company_state,
            company_country=company_country,
        )

        return {"rows_affected": result.get("rows_affected"), "products": result.get("products")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))