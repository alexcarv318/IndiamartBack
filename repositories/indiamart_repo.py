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
            product_categories = [category[0] for category in product_categories if category[0]]
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
                session.query(
                    self.products_details.id.label('product_id'),
                    self.products_details.name.label('product_name'),
                    self.products_details.price.label('product_price'),
                    self.products_details.category.label('product_category'),
                    self.products_details.url.label('product_url'),
                    self.products_details.pdfLink.label('product_pdf_link'),
                    self.products_details.productDescription.label('product_description'),
                    self.products_details.specs.label('product_specs'),
                    self.company_details.id.label('company_id'),
                    self.company_details.name.label('company_name'),
                    self.company_details.city.label('company_city'),
                    self.company_details.state.label('company_state'),
                    self.company_details.country.label('company_country')
                )
                .join(self.company_details, self.products_details.company_id == self.company_details.id)
            )

            if name:
                stmt = stmt.filter(self.products_details.name.contains(name))
            if category:
                stmt = stmt.filter(self.products_details.category.contains(category))
            if min_price:
                stmt = stmt.filter(self.products_details.price >= min_price)
            if max_price:
                stmt = stmt.filter(self.products_details.price <= max_price)
            if company_name:
                stmt = stmt.filter(self.company_details.name.contains(company_name))
            if company_city:
                stmt = stmt.filter(self.company_details.city.contains(company_city))
            if company_state:
                stmt = stmt.filter(self.company_details.state.contains(company_state))
            if company_country:
                stmt = stmt.filter(self.company_details.country.contains(company_country))

            results = stmt.limit(50).all()

            product_list = []
            for row in results:
                product = {
                    'product_id': row.product_id,
                    'product_name': row.product_name,
                    'product_price': row.product_price,
                    'product_category': row.product_category,
                    'product_url': row.product_url,
                    'product_pdf_link': row.product_pdf_link,
                    'product_description': row.product_description,
                    'product_specs': row.product_specs,
                    'company_id': row.company_id,
                    'company_name': row.company_name,
                    'company_city': row.company_city,
                    'company_state': row.company_state,
                    'company_country': row.company_country,
                }
                product_list.append(product)

            return product_list
