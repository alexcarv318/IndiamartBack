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
            cities = [city[0] for city in cities]
            return cities

    def get_states(self):
        with Session(self.engine) as session:
            states = session.query(self.contractors.state).distinct().limit(100).all()
            states = [state[0] for state in states]
            return states

    def get_categories(self):
        with Session(self.engine) as session:
            categories = session.query(self.contractors.category).distinct().limit(100).all()
            categories = [category[0] for category in categories]
            return categories

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
                    self.contractors.category.contains(category)
                )

            return stmt.limit(50).all()