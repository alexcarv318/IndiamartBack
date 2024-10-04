from sqlalchemy.orm import Session

from databases.buildzoom_db import buildzoom_engine, buildzoom_base


class BuildZoomRepository:

    def __init__(self):
        self.engine = buildzoom_engine
        self.contractors = buildzoom_base.classes.contractors
        self.cities = buildzoom_base.classes.cities
        self.states = buildzoom_base.classes.states

    def get_cities(self):
        with Session(self.engine) as session:
            cities = session.query(self.cities.value).distinct.limit(100).all()
            cities = [city[0] for city in cities]
            return cities

    def get_states(self):
        with Session(self.engine) as session:
            states = session.query(self.states.value).distinct.limit(100).all()
            states = [state[0] for state in states]
            return states

    def filter_contractors(
        self,
        company_name: str | None = None,
        phone: str | None = None,
        city: str | None = None,
        state: str | None = None,
        postal_code: str | None = None,
    ):
        with Session(self.engine) as session:
            stmt = (
                session.query(self.contractors)
                .join(self.cities, self.cities.id == self.contractors.city)
                .join(self.states, self.states.id == self.contractors.state)
            )

            if company_name:
                stmt = stmt.filter(
                    self.contractors.company_name.contains(company_name)
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
            if postal_code:
                stmt = stmt.filter(
                    self.contractors.postal_code.contains(postal_code)
                )

            return stmt.limit(50).all()

