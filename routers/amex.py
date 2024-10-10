from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_amex_repo
from repositories.amex_repo import AmexRepository

router = APIRouter(prefix="/amex", tags=["amex"])

@router.get("/contractors/cities")
def get_cities(
    amex_repo: AmexRepository = Depends(get_amex_repo)
):
    cities = amex_repo.get_cities()
    return {"contactor_cities": cities}

@router.get("/contractors/states")
def get_states(
    amex_repo: AmexRepository = Depends(get_amex_repo)
):
    states = amex_repo.get_states()
    return {"contactor_states": states}

@router.get("/contractors/categories")
def get_categories(
    amex_repo: AmexRepository = Depends(get_amex_repo)
):
    categories = amex_repo.get_categories()
    return {"contactor_categories": categories}

@router.get("/contractors/filter")
def filter_contractors(
    amex_repo: AmexRepository = Depends(get_amex_repo),
    name: str | None = None,
    phone: str | None = None,
    city: str | None = None,
    state: str | None = None,
    category: str | None = None,
    zip_code: str | None = None,
):
    try:
        result = amex_repo.filter_contractors(
            name=name,
            phone=phone,
            city=city,
            state=state,
            category=category,
            zip_code=zip_code,
        )

        return {"rows_affected": result.get("rows_affected"), "contractors": result.get("contractors")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
