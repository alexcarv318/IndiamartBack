from sqlalchemy.orm import Session

from databases.indiamart_db import indiamart_base, indiamart_engine


class IndiaMartRepository:

    def __init__(self):
        self.engine = indiamart_engine
        self.products_details = indiamart_base.classes.product_details
        self.company_details = indiamart_base.classes.company_details

    def get_products_categories(self):
        with Session(self.engine) as session:
            product_categories = session.query(self.products_details.category).distinct().limit(100).all()
            product_categories = [category[0] for category in product_categories]
            return product_categories

    def filter_products(
        self,
        min_price: float | None = None,
        max_price: float | None = None,
        name: str | None = None,
        category: str | None = None,
        company_name: str | None = None,
        company_city: str | None = None,
        company_state: str | None = None,
        company_country: str | None = None,
    ):
        with Session(self.engine) as session:
            stmt = (
                session.query(self.products_details)
                .join(self.company_details, self.products_details.company_id == self.company_details.id)
            )

            if name:
                stmt = stmt.filter(
                    self.products_details.name.contains(name)
                )
            if category:
                stmt = stmt.filter(
                    self.products_details.category.contains(category)
                )
            if min_price:
                stmt = stmt.filter(
                    self.products_details.price >= min_price,
                )
            if max_price:
                stmt = stmt.filter(
                    self.products_details.price <= max_price,
                )
            if company_name:
                stmt = stmt.filter(
                    self.company_details.name.contains(company_name),
                )
            if company_city:
                stmt = stmt.filter(
                    self.company_details.city.contains(company_city),
                )
            if company_state:
                stmt = stmt.filter(
                    self.company_details.state.contains(company_state),
                )
            if company_country:
                stmt = stmt.filter(
                    self.company_details.country.contains(company_country),
                )

            return stmt.limit(50).all()
