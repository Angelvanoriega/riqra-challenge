from src.catalog.dao import ProductSearch, ProductList


class Product(object):
    name = ''
    price = ''
    term = ''
    supplier = ''

    def __init__(self, name=None, price=None):
        self.name = name
        self.price = price

    def search(self):
        store = ProductSearch()
        store.term = self.term
        return store.execute()

    def list(self):
        store = ProductList()
        store.supplier = self.supplier
        return store.execute()
