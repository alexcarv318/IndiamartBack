from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_buildzoom_repo
from repositories.buildzoom_repo import BuildZoomRepository

router = APIRouter(prefix="/buildzoom", tags=["buildzoom"])

@router.get("/contractors/cities")
def get_cities(
    buildzoom_repo: BuildZoomRepository = Depends(get_buildzoom_repo)
):
    cities = buildzoom_repo.get_cities()
    return {"contractor_cities": cities}

@router.get("/contractors/states")
def get_states(
    buildzoom_repo: BuildZoomRepository = Depends(get_buildzoom_repo)
):
    states = buildzoom_repo.get_states()
    return {"contractor_states": states}

@router.get("/contractors/filter")
def filter_contractors(
    buildzoom_repo: BuildZoomRepository = Depends(get_buildzoom_repo),
    company_name: str | None = None,
    phone: str | None = None,
    city: str | None = None,
    state: str | None = None,
    postal_code: str | None = None,
):
    try:
        result = buildzoom_repo.filter_contractors(
            company_name=company_name,
            phone=phone,
            city=city,
            state=state,
            postal_code=postal_code,
        )

        return {"contractors": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
