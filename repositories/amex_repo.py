from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session

from databases.amex_db import amex_engine, amex_base


class AmexRepository:

    def __init__(self):
        self.engine = amex_engine
        metadata = MetaData()
        self.contractors = Table(
            'contractors',
            metadata,
            autoload_with=self.engine
        )

    def get_cities(self):
        with Session(self.engine) as session:
            cities = session.query(self.contractors.c.city).distinct().limit(100).all()
            cities = [city[0] for city in cities if city[0]]
            return cities

    def get_states(self):
        with Session(self.engine) as session:
            states = session.query(self.contractors.c.state).distinct().limit(100).all()
            states = [state[0] for state in states if state[0]]
            return states

    def get_categories(self):
        with Session(self.engine) as session:
            categories = session.query(self.contractors.c.category).distinct().limit(100).all()
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
            stmt = session.query(
                self.contractors.c.name.label("name"),
                self.contractors.c.phone.label("phone"),
                self.contractors.c.address.label("address"),
                self.contractors.c.city.label("city"),
                self.contractors.c.state.label("state"),
                self.contractors.c.category.label("category"),
                self.contractors.c.zip_code.label("zip_code"),
            )

            if name:
                stmt = stmt.filter(
                    self.contractors.c.name.contains(name)
                )
            if phone:
                stmt = stmt.filter(
                    self.contractors.c.phone.contains(phone)
                )
            if city:
                stmt = stmt.filter(
                    self.contractors.c.city.contains(city)
                )
            if state:
                stmt = stmt.filter(
                    self.contractors.c.state.contains(state)
                )
            if category:
                stmt = stmt.filter(
                    self.contractors.c.category.contains(category)
                )
            if zip_code:
                stmt = stmt.filter(
                    self.contractors.c.zip_code.contains(zip_code)
                )

            rows_affected = stmt.count()
            result = stmt.limit(50).all()

            contractors_list = []
            for row in result:
                contractor = {
                    'name': row.name,
                    'phone': row.phone,
                    'address': row.address,
                    'city': row.city,
                    'state': row.state,
                    'category': row.category,
                    'zip_code': row.zip_code,
                }
                contractors_list.append(contractor)

            return {"rows_affected": rows_affected, "contractors": contractors_list}

