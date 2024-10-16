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
            cities = session.query(self.cities.value).distinct().limit(100).all()
            cities = [city[0] for city in cities if city[0]]
            return cities

    def get_states(self):
        with Session(self.engine) as session:
            states = session.query(self.states.value).distinct().limit(100).all()
            states = [state[0] for state in states if state[0]]
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
                session.query(
                    self.contractors.company_name.label('company_name'),
                    self.contractors.phone.label('phone'),
                    self.contractors.postal_code.label('postal_code'),
                    self.cities.value.label('city'),
                    self.states.value.label('state'),
                    self.contractors.address.label('address'),
                    self.contractors.has_verified_license.label('has_verified_license'),
                    self.contractors.bz_score.label('bz_score'),
                    self.contractors.url.label('url'),
                )
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
                    self.cities.value.contains(city)
                )
            if state:
                stmt = stmt.filter(
                    self.states.value.contains(state)
                )
            if postal_code:
                stmt = stmt.filter(
                    self.contractors.postal_code.contains(postal_code)
                )

            rows_affected = stmt.count()
            results = stmt.limit(50).all()
            contractor_list = []
            for row in results:
                contractor = {
                    'company_name': row.company_name,
                    'phone': row.phone,
                    'postal_code': row.postal_code,
                    'city': row.city,
                    'state': row.state,
                    'address': row.address,
                    'has_verified_license': row.has_verified_license,
                    'bz_score': row.bz_score,
                    'url': row.url,
                }
                contractor_list.append(contractor)

            return {"rows_affected": rows_affected, "contractors": contractor_list}


