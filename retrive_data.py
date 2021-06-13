import json
import os


class Retrieve:
    big = {}
    loca = []
    # xxx------ other shop var ---- xxx
    """
        admin_phone:
        image_url:
        product_name:
        product_price:
        product_description
    """
    product_name = ""
    customer_number = ""
    product_url = ""
    product_price = ""
    product_description = ""

    def front_shop(self, stores):
        self.big = stores
        print(self.big)
        for y, x in stores.items():
            print("product id>>", y)
            print("admin_phone:", x["admin_phone"])
            print("img_url:", x["image_url"])
            print("product_name:", x["product_name"])
            print("product_price:", x["product_price"])
            print("product_description", x["product_description"])
            print(" ")
            Retrieve.product_name = x["product_name"]
            Retrieve.customer_number = x["admin_phone"]
            Retrieve.product_url = x["image_url"]
            Retrieve.product_price = x["product_price"]
            Retrieve.product_description = x["product_description"]
            from helped import connection_status as CS
            path = CS.Cache_local.Cache(CS.Cache_local(), Retrieve.product_url, y)
            if not path:
                self.front_shop(self.big)
            else:
                cached = {y: {'admin_phone': self.customer_number,
                              'image_url': path,
                              'product_name': self.product_name,
                              'product_price': self.product_price,
                              'product_description': self.product_description}}
                self.loca.append(cached)
        d = {k: v for x in self.loca for k, v in x.items()}
        print(d)
        with open('helped/admin.json', 'w') as file:
            file.write(json.dumps(d))

    def other_shop(self, stores):
        self.big = stores
        print(self.big)
        for y, x in stores.items():
            print("product id>>", y)
            print("admin_phone:", x["admin_phone"])
            print("img_url:", x["image_url"])
            print("product_name:", x["product_name"])
            print("product_price:", x["product_price"])
            print("product_description", x["product_description"])
            print(" ")
            Retrieve.product_name = x["product_name"]
            Retrieve.customer_number = x["admin_phone"]
            Retrieve.product_url = x["image_url"]
            Retrieve.product_price = x["product_price"]
            Retrieve.product_description = x["product_description"]
            from helped import connection_status as CS
            path = CS.Cache_local.Cache(CS.Cache_local(), Retrieve.product_url, y)
            if not path:
                self.other_shop(self.big)
            else:
                cached = {y: {'admin_phone': self.customer_number,
                              'image_url': path,
                              'product_name': self.product_name,
                              'product_price': self.product_price,
                              'product_description': self.product_description}}
                self.loca.append(cached)
        d = {k: v for x in self.loca for k, v in x.items()}
        print(d)
        with open('helped/other.json', 'w') as file:
            file.write(json.dumps(d))

    def read_lo(self, filename):
        with open(filename) as file:
            line = json.load(file)
            print(len(line))
            for y, x in line.items():
                Retrieve.product_name = x["product_name"]
                Retrieve.customer_number = x["admin_phone"]
                Retrieve.product_url = x["image_url"]
                Retrieve.product_price = x["product_price"]

        return line
