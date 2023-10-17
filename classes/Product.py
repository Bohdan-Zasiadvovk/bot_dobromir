from classes.Database import Database
import json


class Product:
    DBcursor = None

    def __init__(self, slug: str, db_cursor: Database):
        self.slug = slug
        self.DBcursor = db_cursor

        product_dict = self.db_to_dict()

        self.id = product_dict['id']
        self.slug = product_dict['slug']
        self.name = product_dict['name']

    def db_to_dict(self):
        product_tuple = self.DBcursor.get_product(self.slug)
        product_list = list(product_tuple)
        product = {
            'id': product_list[0],
            'slug': product_list[1],
            'name': product_list[2],
        }
        return product

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, value):
        self._slug = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __str__(self):
        product_dict = {
            "id": self.id,
            "slug": self.slug,
            "name": self.name
        }
        return json.dumps(product_dict, indent=4)
