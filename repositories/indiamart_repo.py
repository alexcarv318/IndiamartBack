from unicodedata import category

from sqlalchemy import Table, MetaData
from sqlalchemy.orm import Session

from databases.indiamart_db import indiamart_base, indiamart_engine


class IndiaMartRepository:

    def __init__(self):
        self.engine = indiamart_engine
        metadata = MetaData()
        self.products_details = indiamart_base.classes.product_details
        self.company_details = indiamart_base.classes.company_details
        self.category_mapping = Table(
            'category_mapping',
            metadata,
            autoload_with=self.engine
        )

    def get_total_count_of_rows(self):
        with Session(self.engine) as session:
            return session.query(self.products_details).count()

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
            category1: str | None = None,
            category2: str | None = None,
            category3: str | None = None,
            category4: str | None = None,
            company_name: str | None = None,
            company_city: str | None = None,
            company_state: str | None = None,
    ):
        with Session(self.engine) as session:
            stmt = (
                session.query(
                    self.products_details.id.label('product_id'),
                    self.products_details.name.label('product_name'),
                    self.products_details.price.label('product_price'),
                    self.category_mapping.c.caregory1.label('product_category'),
                    self.category_mapping.c.category2.label('product_category2'),
                    self.category_mapping.c.category3.label('product_category3'),
                    self.category_mapping.c.category4.label('product_category4'),
                    self.products_details.url.label('product_url'),
                    self.products_details.pdfLink.label('product_pdf_link'),
                    self.products_details.productDescription.label('product_description'),
                    self.products_details.specs.label('product_specs'),
                    self.company_details.id.label('company_id'),
                    self.company_details.name.label('company_name'),
                    self.company_details.city.label('company_city'),
                    self.company_details.state.label('company_state'),
                )
                .join(self.company_details, self.products_details.company_id == self.company_details.id)
                .join(self.category_mapping, self.products_details.category == self.category_mapping.c.caregory1)
            )

            if name:
                stmt = stmt.filter(self.products_details.name.contains(name))
            if category1:
                stmt = stmt.filter(self.category_mapping.c.caregory1 == category1)
            if category2:
                stmt = stmt.filter(self.category_mapping.c.category2 == category2)
            if category3:
                stmt = stmt.filter(self.category_mapping.c.category3 == category3)
            if category4:
                stmt = stmt.filter(self.category_mapping.c.category4 == category4)
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

            rows_affected = stmt.count()
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
                }
                product_list.append(product)

            return {"rows_affected": rows_affected, "products": product_list}

    def get_first_fifty_rows(self):
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
                )
                .join(self.company_details, self.products_details.company_id == self.company_details.id)
            )

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
                }
                product_list.append(product)

            return product_list


    def get_distinct_categories_4(self):
        with Session(self.engine) as session:
            distinct_categories = session.query(self.category_mapping.c.category4).distinct().all()
            categories_list = [category[0] for category in distinct_categories if category[0]]
            return categories_list

    def get_distinct_categories_3(self, category4):
        with Session(self.engine) as session:
            distinct_categories = session.query(self.category_mapping.c.category3)
            distinct_categories = distinct_categories.filter(self.category_mapping.c.category4 == category4)
            distinct_categories = distinct_categories.distinct().all()
            categories_list = [category[0] for category in distinct_categories if category[0]]
            return categories_list

    def get_distinct_categories_2(self, category3):
        with Session(self.engine) as session:
            distinct_categories = session.query(self.category_mapping.c.category2)
            distinct_categories = distinct_categories.filter(self.category_mapping.c.category3 == category3)
            distinct_categories = distinct_categories.distinct().all()
            categories_list = [category[0] for category in distinct_categories if category[0]]
            return categories_list

    def get_distinct_categories_1(self, category2):
        with Session(self.engine) as session:
            distinct_categories = session.query(self.category_mapping.c.caregory1)
            distinct_categories = distinct_categories.filter(self.category_mapping.c.category2 == category2)
            distinct_categories = distinct_categories.distinct().all()
            categories_list = [category[0] for category in distinct_categories if category[0]]
            return categories_list
