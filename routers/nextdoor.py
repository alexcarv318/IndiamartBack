from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_nextdoor_repo
from repositories.nextdoor_repo import NextDoorRepository

router = APIRouter(prefix="/nextdoor", tags=["nextdoor"])

@router.get("/contractors/cities")
def get_cities(
    nextdoor_repo: NextDoorRepository = Depends(get_nextdoor_repo)
):
    cities = nextdoor_repo.get_cities()
    return {"contractors_cities": cities}

@router.get("/contractors/states")
def get_states(
    nextdoor_repo: NextDoorRepository = Depends(get_nextdoor_repo)
):
    states = nextdoor_repo.get_states()
    return {"contractors_states": states}

@router.get("/contractors/categories")
def get_categories(
    nextdoor_repo: NextDoorRepository = Depends(get_nextdoor_repo)
):
    categories = nextdoor_repo.get_categories()
    return {"contractors_categories": categories}

@router.get("/contractors/filter")
def filter_contractors(
    nextdoor_repo: NextDoorRepository = Depends(get_nextdoor_repo),
    name: str | None = None,
    phone: str | None = None,
    city: str | None = None,
    state: str | None = None,
    zip_code: str | None = None,
    category: str | None = None,
):
    try:
        result = nextdoor_repo.filter_contractors(
            name=name,
            phone=phone,
            city=city,
            state=state,
            zip_code=zip_code,
            category=category
        )

        return {"rows_affected": result.get("rows_affected"), "contractors": result.get("contractors")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





