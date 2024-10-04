def get_indiamart_repo():
    from repositories.indiamart_repo import IndiaMartRepository
    return IndiaMartRepository()

def get_nextdoor_repo():
    from repositories.nextdoor_repo import NextDoorRepository
    return NextDoorRepository()

def get_buildzoom_repo():
    from repositories.buildzoom_repo import BuildZoomRepository
    return BuildZoomRepository()

def get_amex_repo():
    from repositories.amex_repo import AmexRepository
    return AmexRepository()