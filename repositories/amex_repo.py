from sqlalchemy.orm import Session

from databases.amex_db import amex_engine, amex_base


class AmexRepository:

    def __init__(self):
        self.engine = amex_engine
        self.contractors = amex_base.classes.contractors

    def get_cities(self):
        with Session(self.engine) as session:
            cities = session.query(self.contractors.cities).limit(100).all()
            cities = [city[0] for city in cities if city[0]]
            return cities

    def get_states(self):
        with Session(self.engine) as session:
            states = session.query(self.contractors.state).limit(100).all()
            states = [state[0] for state in states if state[0]]
            return states

    def get_categories(self):
        with Session(self.engine) as session:
            categories = session.query(self.contractors.category).limit(100).all()
            categories = [category[0] for category in categories if category[0]]
            return categories

    def filter_contractors(
        self,
        name: str | None = None,
        phone: str | None = None,
        city: str | None = None,
        state: str | None = None,
        category: str | None = None,
        zip_code: str | None = None,
    ):
        with Session(self.engine) as session:
            stmt = session.query(self.contractors)

            if name:
                stmt = stmt.filter(
                    self.contractors.contains(name)
                )
            if phone:
                stmt = stmt.filter(
                    self.contractors.contains(phone)
                )
            if city:
                stmt = stmt.filter(
                    self.contractors.contains(city)
                )
            if state:
                stmt = stmt.filter(
                    self.contractors.contains(state)
                )
            if category:
                stmt = stmt.filter(
                    self.contractors.contains(category)
                )
            if zip_code:
                stmt = stmt.filter(
                    self.contractors.contains(zip_code)
                )

            return stmt.limit(50).all()

