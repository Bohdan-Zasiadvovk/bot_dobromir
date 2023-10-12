class Order:
    user = {}
    order_details = {}

    def __init__(self, user=False, order_details=None, db_object=None):
        self.user = user
        if order_details:
            self.order_details = order_details
        else:
            self.order_details = self.get_order()
            if not self.order_details:
                self.create_order()

    def create_order(self):
        self.order_details ={}

    def get_order(self):
        return self.order_details

    def update_product(self, product_slug, count):
        if product_slug in self.order_details:
            self.order_details[product_slug] = count
            return True
        else:
            return False

    def add_product(self, product_slug):
        if product_slug not in self.order_details:
            self.order_details[product_slug] = 0
            return True
        else:
            return False

    def set_count(self, product_slug, count):
        if product_slug in self.order_details:
            self.order_details[product_slug] = count
            return True
        else:
            return False

    def delete_product(self, product_slug):
        if product_slug in self.order_details:
            del self.order_details[product_slug]
            return True
        else:
            return False

    def confirmed_order(self):
        self.status = "confirmed"
        return True