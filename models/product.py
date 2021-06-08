class Product:
    __slots__ = ("data", "name", "number", "active_ingredients")

    def __init__(self, data):
        self.data = data
        self.number = data["product_number"]
        self.name = data["brand_name"]
        self.active_ingredients = [x["name"] for x in self.data["active_ingredients"]]
