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
    category1: Annotated[str | None, Query(max_length=255)] = None,
    category2: Annotated[str | None, Query(max_length=255)] = None,
    category3: Annotated[str | None, Query(max_length=255)] = None,
    category4: Annotated[str | None, Query(max_length=255)] = None,
    company_name: Annotated[str | None, Query(max_length=255)] = None,
    company_city: Annotated[str | None, Query(max_length=255)] = None,
    company_state: Annotated[str | None, Query(max_length=255)] = None,
):
    # try:
    result = indiamart_repo.filter_products(
        name=name,
        category1=category1,
        category2=category2,
        category3=category3,
        category4=category4,
        min_price=min_price,
        max_price=max_price,
        company_name=company_name,
        company_city=company_city,
        company_state=company_state,
    )

    return {"rows_affected": result.get("rows_affected"), "products": result.get("products")}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


@router.get("/initial/products")
def get_initial_products(
    indiamart_repo: IndiaMartRepository = Depends(get_indiamart_repo),
):
    products = indiamart_repo.get_first_fifty_rows()
    return {"products": products}

@router.get("/initial/rows")
def get_initial_rows(
    indiamart_repo: IndiaMartRepository = Depends(get_indiamart_repo),
):
    rows_affected = indiamart_repo.get_total_count_of_rows()
    return {"rows_affected": rows_affected}


@router.get("/categories")
def get_categories(
    indiamart_repo: IndiaMartRepository = Depends(get_indiamart_repo),
    category4: str = None,
    category3: str = None,
    category2: str = None
):
    categories = indiamart_repo.get_categories(
        category4=category4,
        category3=category3,
        category2=category2
    )
    return categories