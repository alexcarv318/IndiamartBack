from unicodedata import category

from sqlalchemy.orm import Session

from databases.nextdoor_db import nextdoor_engine, nextdoor_base


class NextDoorRepository:

    def __init__(self):
        self.engine = nextdoor_engine
        self.contractors = nextdoor_base.classes.contractors

    def get_cities(self):
        with Session(self.engine) as session:
            cities = session.query(self.contractors.city).distinct().limit(100).all()
            cities = [city[0] for city in cities if city[0]]
            return cities

    def get_states(self):
        with Session(self.engine) as session:
            states = session.query(self.contractors.state).distinct().limit(100).all()
            states = [state[0] for state in states if state[0]]
            return states

    def get_categories(self):
        with Session(self.engine) as session:
            categories = session.query(self.contractors.categories).distinct().limit(50).all()
            categories_lists = [category[0] for category in categories if category[0]]

            flat_categories = []
            for category_list in categories_lists:
                for category in category_list:
                    flat_categories.append(category)
            return flat_categories

    def filter_contractors(
        self,
        name: str | None = None,
        phone: str | None = None,
        city: str | None = None,
        state: str | None = None,
        zip_code: str | None = None,
        category: str | None = None,
    ):
        with Session(self.engine) as session:
            stmt = session.query(self.contractors)

            if name:
                stmt = stmt.filter(
                    self.contractors.name.contains(name)
                )
            if phone:
                stmt = stmt.filter(
                    self.contractors.phone.contains(phone)
                )
            if city:
                stmt = stmt.filter(
                    self.contractors.city.contains(city)
                )
            if state:
                stmt = stmt.filter(
                    self.contractors.state.contains(state)
                )
            if zip_code:
                stmt = stmt.filter(
                    self.contractors.zip_code.contains(zip_code)
                )
            if category:
                stmt = stmt.filter(
                    self.contractors.categories.any(category)
                )

            rows_affected = stmt.count()

            return {"rows_affected": rows_affected, "contractors": stmt.limit(50).all()}
